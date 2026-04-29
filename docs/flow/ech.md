# ECH (Encrypted Client Hello)

> ECH checker: `https://tls-ech.dev/`.

Encrypts **which website you’re trying to visit**.

## How it works?

In HTTPS without ECH, even though the connection is encrypted, network devices can still see which domain you’re visiting (for example, example.com). This is because during the TLS handshake there is a field called **SNI (Server Name Indication)**, and it is sent in plaintext.

---

The purpose of ECH is to encrypt the **ClientHello** in the TLS handshake, especially:
SNI (most important) + some auxiliary information.

As a result, intermediaries can only see that you connected to a server (but not the specific domain) → the actual destination website is hidden.

```txt
Browser:
  First obtains the "public key for encryption" (from DNS or HTTPS DNS)

Then:

ClientHello (SNI inside is encrypted)
  ├── Outer SNI (plaintext, visible)
  │     Usually a CDN / edge server domain
  └── Inner SNI (encrypted with ECH)
        The real destination website (example.com)
        ↓
client-facing server (entry server)
        ↓
Decrypts SNI → forwards to the correct website
```

## Websites that have already enabled ECH

ECH enabled sites: [https://divested.dev/misc/ech.txt](https://divested.dev/misc/ech.txt)

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

> Edge server, Front-end proxy, Gateway, Reverse proxy, CDN edge node

ECH is usually decrypted on the client-facing server.

```txt
Browser
  ↓
Cloudflare / Nginx / Edge Server  <-- (client-facing)
  ↓
Web Server (API)
  ↓
Target Data
```
