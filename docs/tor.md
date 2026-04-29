# Tor (The Onion Router)

Uses layered encryption and relay forwarding to make it difficult for others to know who you are and what websites you are accessing.

## How it works?

In normal web access:

```txt
You → Website
```

The problems are:

* Your ISP can see which websites you visit
* The website can see your IP address
* Network intermediaries can analyze your traffic

---

The core of Tor is **Onion Routing**

This means data is encrypted in layers, like an onion.

Its workflow:

```txt
You
 ↓
Entry Node (Guard Node)
 ↓
Relay Node
 ↓
Exit Node
 ↓
Target Website
```

Each hop only knows the “previous hop” and the “next hop,” but not the full path. This helps hide:

* Your real IP
* Your geographic location
* The origin of the request

---

## Difference between Tor and VPN

VPN:

```txt
You → VPN → Website
```

The VPN provider knows who you are.

Tor:

```txt
Multiple distributed nodes
No single point knows the full path
```
