# ECH (Encrypted Client Hello)
> Ech checker: https://tls-ech.dev/.

把“你要访问哪个网站”这件事也加密起来。

## How it works?
在没有 ECH 的 HTTPS 里，即使是加密连接，网络设备仍然能看到：你访问的是哪个域名（比如 example.com），因为在 TLS 握手阶段，有个字段叫：SNI（Server Name Indication），它是明文的。

---

ECH 的作用就是把 TLS 握手里的 ClientHello 进行加密，重点加密：SNI（最重要）+ 一些辅助信息。

这样中间设备只能看到连接了一台服务器（但不知道具体域名）--> 真实访问的网站被隐藏了

```txt
浏览器：
  先拿到“加密用的公钥”（从 DNS 或 HTTPS DNS）

然后：

ClientHello（里面的 SNI 被加密）
  ├── Outer SNI（明文，可见）
  │     通常是 CDN / 边缘服务器域名
  └── Inner SNI（被 ECH 加密）
        真实访问的网站（example.com）
        ↓
client-facing server（入口服务器）
        ↓
解密 SNI → 转发到正确网站
```

## Websites that have already enabled ECH
ECH enabled sites: https://divested.dev/misc/ech.txt

e.g.
```txt
https://123moviesfree.net
https://1377x.to
https://bereal.com
https://arnebrachhold.de
https://aryion.com
https://blogchaat.com
https://mp3juice.blog
https://mp4moviez.sc
https://rutracker.org
https://sarkariexam.com
https://suksesbogil.com
```

## What is Client-Facing Server?
> Edge server（边缘服务器）, Front-end proxy（前置代理）, Gateway（网关）, Reverse proxy（反向代理）, CDN edge node

ECH is usually decrypted on the client-facing server.

```txt
Browser
  ↓
Cloudflare / Nginx / Edge Server  <-- (client-facing)
  ↓
Web Server（API）
  ↓
Target Data
```
