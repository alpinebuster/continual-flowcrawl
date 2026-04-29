# JA4+

| Full Name | Short Name | Description |
|---|---|---|
| JA4 | JA4 | TLS Client Fingerprinting |
| JA4Server | JA4S | TLS Server Response / Session Fingerprinting |
| JA4HTTP | JA4H | HTTP Client Fingerprinting |
| JA4Latency | JA4L | Client to Server Latency Measurment / Light Distance |
| JA4LatencyServer | JA4LS | Server to Client Latency Measurement / Light Distance |
| JA4X509 | JA4X | X509 TLS Certificate Fingerprinting |
| JA4SSH | JA4SSH | SSH Traffic Fingerprinting |
| JA4TCP | JA4T | TCP Client Fingerprinting |
| JA4TCPServer | JA4TS | TCP Server Response Fingerprinting |
| [JA4TCPScan](https://github.com/FoxIO-LLC/ja4tscan) | [JA4TScan](https://github.com/FoxIO-LLC/ja4tscan) | [Active TCP Fingerprint Scanner](https://github.com/FoxIO-LLC/ja4tscan) |
| JA4DHCP | JA4D | DHCP Fingerprinting |
| JA4DHCPv6 | JA4D6 | DHCPv6 Fingerprinting |

## JA4: TLS Client Fingerprinting
![JA4](./imgs/JA4.png)

The end result is a fingerprint that looks like:
`t13d1516h2_8daaf6152771_b186095e22b6`

```txt
(QUIC=”q”, DTLS="d", or TLS over TCP=”t”)
(2 character TLS version)
(SNI=”d” or no SNI=”i”)
(2 character count of ciphers)
(2 character count of extensions)
(first and last characters of first ALPN extension value)
_
(sha256 hash of the list of cipher hex codes sorted in hex order, truncated to 12 characters)
_
(sha256 hash of (the list of extension hex codes sorted in hex order)_(the list of signature algorithms), truncated to 12 characters)
```

## JA4S: TLS Server Response / Session Fingerprinting
![JA4S](./imgs/JA4S.png)

## JA4H: HTTP Client Fingerprint
![JA4H](./imgs/JA4H.png)

## JA4T: TCP Client Fingerprinting
![JA4T](./imgs/JA4T.png)

## JA4L: Client to Server Latency Measurment / Light Distance
![JA4L](./imgs/JA4L.png)
