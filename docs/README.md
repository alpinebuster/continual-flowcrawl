# Continual FlowCrawl Documentation

> SNI (Server Name Indication) only appears in the TLS ClientHello phase

DoH and ECH do just one thing: **prevent the real SNI in ClientHello from being visible to network intermediaries**.

```txt
[User enters domain]
  ↓
DNS query (protected by DoH here)
  ↓
Resolve IP
  ↓
TLS connection
  ↓
Handshake (protected by ECH here)
  ↓
Fully encrypted HTTP communication
```

```txt
You can think of ECH + CDN like this:

You go to a hotel (origin server), but must first pass through the front desk (edge)

Outer TLS = you talking to the front desk
Inner TLS = the front desk relaying your request to the actual room

So:

Outer cipher suite = languages the front desk understands
Inner cipher suite = language used inside the room
```

## Objective

* Classify invisible SNI
* Target App Testset (*200+* ECH & *200+* VPN websites) -> Acc. 95+%
* Non-Target App Testset (*600+* normal websites) -> FPR < 2%
* Half-year cycle ECH dataset -> Acc. 90+%
* Model parameters (< 10M)

## Difficulties

* A: DoH hides the domain during the **query stage**
* B: ECH hides the real domain during the **access stage**, and both IP and domain point to edge servers, making TLS fingerprints (JA4 & JA4S) based on server-side features ineffective (cipher suites, extensions, etc.)
* C: Different ECH websites may have very similar and diverse resource types (e.g., two sites both being chat applications)

## Roadmap

> This depends on how Huawei’s generalization test set is constructed. Our data is collected at the **client side**, where a full ECH access event can be observed. Huawei’s may be collected at the **network gateway**, where only single-session traffic is visible.

Under ECH, in `Client → Network Gateway → CDN`, the following is visible:

* Destination IP (usually CDN anycast IP)
* ASN (Cloudflare / Akamai / AWS)
* Port (443 / QUIC 443)
* TLS ClientHello outer information (outer CH)
* QUIC Initial packet (for HTTP/3)

Not visible:

* Real SNI (inner ClientHello)
* Real domain
* HTTP Host
* URL

Preliminary approaches:

* Coarse-grained detection of ECH (ASN (Autonomous System Number) → IP belongs to CDN such as Cloudflare / Fastly / Akamai)

* For difficulty A, reuse classic DoH features and methods

* For difficulty B, use multimodal data. Not all traffic of ECH-enabled websites is fully encrypted; a significant portion remains non-ECH. If multimodal data can be constructed, traditional traffic behavior features can be incorporated.

* For difficulty B, if Huawei’s dataset is collected at the **network gateway** with only single-session data, use client-side classification to obtain multimodal data. Even with ECH, the handshake still exposes: TLS ClientHello fingerprint + QUIC fingerprint (JA3 / JA4)

* For difficulty B, use client-side classification to supplement DNS-side information (if DoH is not used)

* For difficulty C, use IP intelligence + CDN service mapping (semi-inference). For example:
  `Cloudflare IP → large set of websites`
  `Google IP → YouTube / Search / Gmail`
  However, this is **service-type inference**, not **website identification**, so it can be used as mash information (similar to etbert’s method)

* For difficulty C, directly use raw PCAP bytes (netmamba)

### How can HAR “indirectly help” PCAP?

The value of HAR is to serve as a **reference for feature design**. HAR reveals what typically happens during a website visit:

* Number of requests (page load complexity)
* Resource type ratio (JS / CSS / image)
* Request order structure
* Domain distribution (CDN / API / main domain)
* Request timing distribution (burst / lazy load)

👉 Then map these to features extractable from PCAP:

1. Traffic timing patterns (from HAR request timeline)

PCAP can extract:

* Packet inter-arrival time
* Flow burst patterns
* TLS record timing
* Packet size sequence
* Flow duration
* Upstream/downstream ratio and sequence
* TLS features (limited, JA4 fingerprint)

2. Traffic size structure (size signature)

HAR insight:

* Image-heavy → large responses
* API-heavy → small JSON responses

PCAP can extract:

* Packet size distribution
* Flow byte histogram
* Upstream/downstream ratio

3. Connection structure (flow graph)

HAR insight:

* How many domains a page requests

PCAP can extract:

* Destination IP count
* TLS session count

4. CDN / service fingerprint (weakened version)

HAR shows:

* api.xxx.com
* cdn.xxx.net

PCAP only sees:

* IP ASN (Autonomous System Number)

  * ASN / IP range
  * Connection fan-out
    Connections to Cloudflare / AWS / Google

5. Real challenges under ECH

When ECH is enabled:

❌ SNI cannot be used for classification
❌ Domain names disappear
❌ HAR’s “site structure information” becomes invisible

Therefore:

👉 Classification must rely on **traffic behavior fingerprinting**

```txt
Step 1: PCAP → Flow conversion
  Five-tuple flow (src/dst IP, src/dst port, protocol)

Step 2: Feature extraction (core)
  - Traffic behavior features
  - TLS features (limited)
  - Network topology

Step 3: Where is HAR used?
  HAR is only used for:

  ✔ Training label understanding → know what a site's access pattern looks like
  ✔ Feature inspiration → help design flow pattern features
  ✔ Data alignment (very important)
      HAR → ground truth labeling
      PCAP → feature extraction
```
