# DoH (Domain over HTTPS)

Encrypt DNS queries using HTTPS to prevent others from seeing which domains you’re resolving.

## How it works?

When you visit a website, for example: example.com, your browser first needs to ask DNS: “Which IP address corresponds to this domain?” The traditional process is:

```txt
You → DNS server: What is the IP for example.com?
(plaintext)
DNS → You: 93.184.216.34
```

Problem: Any intermediary on the network can see which domains you are querying.

---

DoH wraps DNS requests inside HTTPS:

```txt
Browser
  ↓
HTTPS request (encrypted)
  ↓
DNS over HTTPS server
  ↓
Returns IP (still encrypted)
```

Outsiders can only see that you connected to an HTTPS server, but cannot see which domain you queried.
