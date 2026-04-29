# Doh (Domain over https)
用 HTTPS 加密 DNS 查询，防止别人看到你在解析什么域名。

## How it works?
你访问网站时，比如：example.com，浏览器需要先问 DNS：“这个域名对应哪个 IP？”。传统流程是：

```txt
你 → DNS 服务器：example.com 是什么 IP？
（明文）
DNS → 你：93.184.216.34
```

问题：任何网络中间人都能看到你查了什么域名。

---

DoH 把 DNS 请求塞进 HTTPS：

```txt
浏览器
  ↓
HTTPS 请求（加密）
  ↓
DNS over HTTPS 服务器
  ↓
返回 IP（仍然加密）
```

外部只能看到你连了某个 HTTPS 服务器，但看不到你查的域名。
