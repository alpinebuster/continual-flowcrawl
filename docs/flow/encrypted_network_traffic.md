# Traditional network access methods

Plaintext DNS + TCP/HTTP (TLS) transport + partially observable metadata in the network

```txt
┌────────────────────────────┐
│     Browser enters URL     │
│     https://example.com    │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│        1. DNS Query        │
│    example.com → IP address│
│    e.g.: 93.184.216.34     │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│      2. TCP Connection     │
│     Three-way handshake    │
│     (SYN / ACK)            │
│     Establishes reliable   │
│     communication channel  │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│   3. TLS Handshake (HTTPS) │
│      - Negotiate keys      │
│      - Verify certificate  │
│    ⚠️ SNI (domain) may be  │
│       plaintext            │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│     4. HTTP Request/Resp   │
│   Browser → GET /index.html│
│   Server → HTML / CSS / JS │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│      🌍 Webpage returned   │
│      Page fully rendered   │
└────────────────────────────┘
```
