# tcpdump with netns
在 Linux 中通过 **Network Namespace (netns)**，你可以为浏览器创建一个完全虚拟化的网络栈，这个环境里**没有回环地址以外的任何流量**。当你在这个隔离的命名空间内启动抓包时，捕获到的 `pcap` 将会是百分百的纯净。

### 核心步骤

#### 1. 创建独立的网络命名空间
首先，创建一个名为 `clean_web` 的空间，并建立一对虚拟网卡（veth pair）用于与物理网络通信。

```bash
# 创建命名空间
sudo ip netns add clean_web

# 创建虚拟网卡对
sudo ip link add veth_inner type veth peer name veth_outer

# 将一端放入命名空间
sudo ip link set veth_inner netns clean_web

# 设置 IP 地址（这里假设你的主网段是 192.168.1.x）
sudo ip addr add 192.168.88.1/24 dev veth_outer
sudo ip link set veth_outer up

sudo ip netns exec clean_web ip addr add 192.168.88.2/24 dev veth_inner
sudo ip netns exec clean_web ip link set veth_inner up
sudo ip netns exec clean_web ip link set lo up
```

#### 2. 配置路由与 NAT (联通互联网)
为了让这个隔离的空间能访问外网，你需要配置转发。

```bash
# 设置默认网关
sudo ip netns exec clean_web ip route add default via 192.168.88.1

# 开启 IP 转发（假设 eth0 是你联网的网卡）
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -s 192.168.88.0/24 -o eth0 -j MASQUERADE
```

#### 3. 执行抓包并启动浏览器
这是最关键的一步。由于所有浏览器产生的流量都必须经过 `veth_inner` 这个接口，你只需要盯着它看。

1.  **在命名空间内启动抓包：**
    ```bash
    sudo ip netns exec clean_web tcpdump -i veth_inner -w target_site.pcap
    ```
2.  **在命名空间内启动浏览器（以隔离模式）：**
    打开另一个终端执行：
    ```bash
    sudo ip netns exec clean_web sudo -u $USER google-chrome --user-data-dir=/tmp/pure_browser --no-first-run
    ```

### 为什么这个方法对“请求很多资源”最有效？

*   **进程级隔离：** 这个 Namespace 里只有 Chrome 一个进程。即便网站请求了 1000 个不同域名的资源（图片、脚本、广告），它们全部都要通过 `veth_inner` 这个虚拟网口。
*   **物理级过滤：** 你不需要关心目标 IP 是什么。你抓取的是这个“虚拟网卡”的全部进出流量。系统层面的 NTP 同步、其他软件的后台更新、系统通知等，都在 Namespace 之外，**绝对不会**进入这个 `pcap` 文件。
*   **完整性：** 它抓取的是最原始的以太网帧，包含了所有的 TCP 三次握手、TLS 协商和多域名并发连接。

### 导出与清理
完成访问后，直接 `Ctrl+C` 停止 `tcpdump`。你会得到一个极其完美的 `target_site.pcap`。

**清理环境：**
```bash
sudo ip netns del clean_web
rm -rf /tmp/pure_browser
```

如果你是在 macOS 或 Windows 上，建议通过 **Docker** 运行一个 Linux 容器并使用 `--net` 参数来模拟类似的隔离效果，因为这二者原生不支持 Linux 的 Namespace 机制。
```

### DNS
在 `ip netns exec` 环境下，浏览器经常会因为找不到 DNS 服务器而无法打开网页。
**解决方案：** 手动指定命名空间的 DNS。
```bash
# 创建并配置命名空间的 DNS 配置文件
sudo mkdir -p /etc/netns/clean_web
echo "nameserver 8.8.8.8" | sudo tee /etc/netns/clean_web/resolv.conf
echo "nameserver 1.1.1.1" | sudo tee /etc/netns/clean_web/resolv.conf
```
*注：Linux 当执行 `ip netns exec <name>` 时，会自动优先查找 `/etc/netns/<name>/resolv.conf`。*
