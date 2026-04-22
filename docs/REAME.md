# Doh + ECH
> SNI（Server Name Indication）只出现在 TLS 的 ClientHello 阶段

DoH 和 ECH 只做一件事：“让 ClientHello 的真实 SNI 不被网络中间人看到”。

```txt
[用户输入域名]
  ↓
DNS 查询（DoH保护这里）
  ↓
找到IP
  ↓
TLS连接
  ↓
握手（ECH保护这里）
  ↓
全加密HTTP通信
```

```txt
可以把 ECH + CDN 理解成：

你去酒店（源站），但要先经过前台（边缘）

外层 TLS = 你和前台说话
内层 TLS = 前台帮你转达你真正要找的房间

所以：

外层 cipher suite = 前台能听懂什么语言
内层 cipher suite = 房间里真正交流的语言
```

## Objective
- 分类看不见的 SNI
- Target App Testset (*200+* ECH & *200+* VPN Website) -> Acc. 95+%
- Non-Target App Testset (*600+* Normal Website) -> FPR <2%
- Half-year Cycle ECH Dataset -> Acc. 90+%
- Model Params (<10M)

## Difficulties
- A: Doh 导致看不到**查询时候**的 domain
- B: ECH 导致看不到**访问时候**真实 domain，**ip 和 domain 都指向边缘服务器**，导致针对服务器的加密套件、Extensions套件等的 TLS 指纹（JA4 & JA4S）失效
- C: 不同 ECH 网站访问的资源类型可能十分相似并且资源类型很多（比如两个网站都是聊天软件）

## Roadmap
> 这个要看华为的泛化测试集是怎么样的，因为我们抓数据是在**客户端**，能拿到一次完整的 ECH 访问事件。而华为的可能是在**网络出口**，这种情况下只能抓到单个 session 的流量

在 ECH 下，`Client → 网络出口 → CDN`, 能看到：

- 目标 IP（通常是 CDN anycast IP）
- ASN（Cloudflare / Akamai / AWS）
- 端口（443 / QUIC 443）
- TLS ClientHello 外层信息（outer CH）
- QUIC Initial packet（如果是 HTTP/3）

看不到：
- 真实 SNI（inner ClientHello）
- 真实域名
- HTTP Host
- URL

初步可以试验的方法：

- 先粗粒度检测是 ECH（ASN（Autonomous System Number，自治系统编号） -> IP 归属 CDN（Cloudflare / Fastly / Akamai））

- 针对难点A，借用经典 Doh 特征 + 方法

- 针对难点B，采用多模态数据，ECH 网站并非全部流量都是全加密，还有大部分流量是非 ECH 的，因此如果能构造多模态数据就可以加上传统流量行为特征。
- 针对难点B，如果华为的泛化测试集是在**网络出口**抓的只有单个 session 的数据，采用通过客户端级分类拿到多模态数据：即使 ECH，握手仍然暴露：TLS ClientHello fingerprint + QUIC 指纹（JA3 / JA4）
- 针对难点B，借用客户端级分类来进行 DNS 侧补充（如果没 DoH）

- 针对难点C，IP 情报 + CDN 业务映射（半推断），可以做 `Cloudflare IP → 大量网站集合` + `Google IP → YouTube / Search / Gmail`，但这是“服务类型推断”，不是“网站识别”。因此可以作为 mash 信息（参考 etbert 的方法）
- 针对难点C，直接原始 pcap 字节（netmamba）

### HAR 能怎么“间接帮助”PCAP？
HAR 的价值在于用来做“特征设计参考”，HAR 能看到一个网站访问时通常会产生的：

- 请求数量（page load complexity）
- 资源类型比例（JS / CSS / image）
- 请求顺序结构
- 域名分布（CDN / API / main domain）
- 请求时间分布（burst / lazy load）

👉 然后映射到 PCAP 可以提取的特征：

1. 流量节奏特征（timing pattern）-> 来自 HAR 的“请求时间线”

PCAP可提：

- packet inter-arrival time
- flow burst pattern
- TLS record timing
- packet size sequence
- flow duration
- upstream/downstream ratio/sequence
- TLS特征（有限, JA4 FP）

2. 流量大小结构（size signature）

HAR启发：

图片多 → 大响应
API多 → 小 JSON

PCAP可提：

- packet size distribution
- flow byte histogram
- upstream/downstream ratio

3. 连接结构（flow graph）

HAR启发：

一个页面会请求多少域名

PCAP可提：

- destination IP count
- TLS session count

4. CDN / 服务指纹（弱化版）

HAR能看到：

api.xxx.com
cdn.xxx.net

PCAP只能看到：

IP ASN（Autonomous System Number (ASN)）
  - ASN / IP range
  - connection fan-out
连接到 Cloudflare / AWS / Google

5. 在 ECH 场景下的现实问题

当 ECH 开启后：

❌ SNI 不能用于分类
❌ 域名消失
❌ HAR 的“网站结构信息”完全不可见

所以：

👉 分类必须依赖 流量行为特征（traffic fingerprinting）

```txt
Step 1：PCAP → Flow 化
  五元组flow（src/dst IP, src/dst port, protocol）

Step 2：提特征（核心）
  - 流量行为特征
  - TLS特征（有限）
  - 网络拓扑

Step 3：HAR 用在哪里？
  HAR只用于：

  ✔ 训练标签理解 -> 知道“某网站访问结构长什么样”
  ✔ 特征启发 -> 帮你设计 flow pattern features
  ✔ 数据对齐（非常重要）
      HAR → 标注 ground truth
      PCAP → feature extraction
```
