# CAPTCHA
“虚拟网卡劫持”抓包的步骤：

### 第一步：环境准备 (NPcap)
1.  **确认安装**：确保安装了 **Wireshark** 并勾选了 **NPcap**。
2.  **开启 Loopback**：在安装 NPcap 时，必须勾选 **"Install NPcap in WinPcap API-compatible Mode"** 和 **"Support loopback traffic"**。
3.  **验证网卡**：打开 Wireshark，你应该能看到一个名为 **"Adapter for loopback traffic capture"** 的网卡。这是我们的目标。

### 第二步：启动“空转发”代理 (转发器)
为了让流量走 Loopback，我们需要一个在本地 `127.0.0.1` 监听的代理。推荐使用 **goproxy** 或 **mitmproxy**，如果你追求极致原始，可以用 **Gost** 开启一个简单的 SOCKS5 转发：

*   **使用 Gost (推荐，轻量且不改包)**：
    ```sh
    git clone https://github.com/go-gost/gost.git
    cd gost/cmd/gost
    go build
    gost -L socks5://:1080
    ```

    *这会在本地 1080 端口开一个“直通”管道。*

### 第三步：配置 Browsertime 走“特制管道”
在 Windows 命令行启动 Browsertime，并强制其流量进入我们的本地管道：

```powershell
npx browsertime https://your-site.com `
  --chrome.args "proxy-server=socks5://127.0.0.1:1080" `
  --chrome.args "host-resolver-rules='MAP * 127.0.0.1, EXCLUDE localhost'" `
  -n 1
```

**关键参数解释：**
*   **`proxy-server`**: 强制所有请求发往本地 1080 端口。
*   **`host-resolver-rules`**: 强制 Chrome 将所有域名的 DNS 解析都指向本地，确保没有任何 DNS 请求溜出物理网卡。

### 第四步：像“侧车”一样抓包
现在，你可以利用 Docker 容器或者 TShark 在本地进行精准捕获。

#### 使用 TShark (Windows 原生)
打开另一个 PowerShell，直接针对环回网卡抓包：
```powershell
# 1. 先找到 Loopback 网卡的序号
tshark -D
# 2. 针对 1080 端口抓包（这对应了 Chrome 到 Gost 的流量）
tshark -i "Adapter for loopback traffic capture" -f "tcp port 1080" -w loopback_clean.pcap
```

### 为什么这个方案能达到“极致干净”？

1.  **物理隔离**：Windows 系统的后台流量（如系统更新、Telemetry）默认直接寻找物理网卡（Ethernet/Wi-Fi）的默认网关，它们不会无缘无故地去访问 `127.0.0.1:1080`。
2.  **逻辑过滤**：你在 Wireshark/TShark 中只监听 `loopback` 网卡。在这个网卡里，**除了你主动塞进去的 Chrome 流量，几乎没有其他东西。**
3.  **原始性保持**：使用 SOCKS5 代理比 HTTP 代理更能保持 TCP 层的原始特征，因为它只是简单的 TCP 转发（Tunneling）。

### 人机验证
因为你是在 Windows 宿主机上运行 Browsertime：
1.  **不要加 `--headless`**：这样 Chrome 窗口会弹出来。
2.  **利用暂停**：在你的 `preScript` 里加一个 `await commands.wait.byTime(30000);`。
3.  **手动操作**：窗口弹出后，你有 30 秒时间去点验证码。点完后，Browsertime 会继续执行，而你的 TShark 会忠实地记录下验证通过后的所有业务流量。

### 流量链路全拆解

当启动了 Gost 并让 Chrome 走这个“管道”时，流量的路径实际上发生了一次**“次元跳跃”**。

简单来说，流量分成了**前半程（虚拟隔离）**和**后半程（真实联网）**。

#### 1. 前半程：Chrome → Loopback → Gost
这是你抓包工具（Wireshark/TShark）盯着看的部分。
*   **指令下达**：你给 Chrome 传了参数 `--proxy-server=socks5://127.0.0.1:1080`。
*   **封包出发现**：Chrome 想要访问 `example.com`。由于它被告知有代理，它不会直接寻找物理网卡，而是直接把数据包发往本地回环地址 `127.0.0.1` 的 `1080` 端口。
*   **进入虚拟通道**：这些数据包会经过 **NPcap Loopback Adapter**。此时，Wireshark 就能抓到这些“干净”的包。这些包的特征是：**源 IP 是 127.0.0.1，目的 IP 也是 127.0.0.1**。

#### 2. 中转站：Gost (转发器)
Gost 就像是一个站在“虚拟次元”和“现实世界”边界的邮差。
*   **接收请求**：Gost 在 `1080` 端口接到了 Chrome 的请求，拆开一看：“哦，你要去访问 `example.com` 啊”。
*   **建立桥梁**：Gost 作为一个独立的 Windows 进程，它开始执行自己的网络请求逻辑。

#### 3. 后半程：Gost → 物理网卡 → 互联网
这是杂讯流量聚集的地方，但你的抓包工具已经不在乎这里了。
*   **发起连接**：Gost 进程通过你的 **物理网卡（以太网/Wi-Fi）** 发起一个真实的 TCP 连接到 `example.com` 的真实 IP。
*   **搬运数据**：Gost 把从 Chrome（Loopback）那里收到的二进制流，原封不动地“搬运”给真实网站；再把网站返回的数据，“搬运”回 Chrome。

### 抓包时的视角切换

在 Wireshark 里，你会看到一个很有趣的现象：
*   如果你监听 **物理网卡**：你会看到大量的 Gost 进程产生的流量，还混杂着 Windows 系统的垃圾包，很难分清谁是谁。
*   如果你监听 **Loopback 网卡**：你会看到一个极其安静的环境，里面**只有** Chrome 和 Gost 之间的对话。每一个包都是为了你的性能测试而存在的。

---

### 总结
流量访问网站的过程是：**Chrome (内部) -> NPcap Loopback -> Gost (中转) -> 物理网卡 -> 互联网**。

### 1. 从 SOCKS5 协议的“握手”机制来看
SOCKS5 协议（RFC 1928）的设计初衷就是做一个**通用的电路级网关（Circuit-Level Gateway）**。它的交互分为两个阶段：

*   **协商阶段**：Chrome 告诉 GOST：“我想用 SOCKS5，不需要密码”。GOST 回复：“好的”。
*   **请求阶段**：Chrome 发送一个 `CONNECT` 请求，包含目标地址（如 `example.com:443`）。GOST 连接目标地址，成功后给 Chrome 回一个“成功”的信号。
*   **透传阶段（关键）**：**一旦连接建立，GOST 就会进入“盲目转发”模式。** 它在本地 TCP 连接（Loopback）和远端 TCP 连接（物理网卡）之间建立一个双向的 `io.Copy` 循环。

**证据：** 在这个阶段，GOST 既不解析 TLS 握手，也不检查 HTTP Header。它只是把从端口 A 收到的 Byte 数组原封不动地写入端口 B。这就是所谓的“透明度”。

### 2. “转发”与“代理”的差异化证明
你提到的文档里区分了代理和转发，但它们对二进制的处理是一致的：

*   **转发 (TCP Forwarding)**：连握手都没有，直接把 1080 端口收到的第一个字节就扔给目标地址。这是 100% 的原始二进制。
*   **代理 (SOCKS5)**：只在**开头**有几个字节的协议协商。一旦协商完成，后续的流量（比如整场 HTTPS 通话）就变成了上述的 TCP 转发模式。

### 3. 实验验证：如何肉眼可见地证明它没动？
你可以做一个简单的实验：
1.  在 Browsertime 跑测试时，用 Wireshark 在 Loopback 抓包。
2.  找到一个 TLS `Client Hello` 包。
3.  查看它的 **JA3 指纹**（TLS 握手的特征哈希）。
4.  你会发现，通过 GOST 转发出来的 JA3 指纹，与 Chrome 直连（不挂代理）时的 **JA3 指纹完全一致**。

**这意味着：** 即使经过了 GOST 搬运，目标服务器看到的依然是那个纯正的、带着 Chrome 原始特征的请求。
