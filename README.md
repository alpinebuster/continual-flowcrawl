<!--
  Title: Continual Flow Crawl
  Description: Crawl, capture PCAP, and extract webpages through ECH/TOR/VPN.
  Author: alpinebuster
  -->

<div align="center">
  <img width="50%" alt="Logo" src=".github/continual-flowcrawl.svg">
  <a href="https://spec.torproject.org/"><img src="https://raw.githubusercontent.com/alpinebuster/continual-flowcrawl/main/.github/tor_logo.png" title="Tor Logo" style="max-width:100%;" width="256" /></a>

  # Continual Flow Crawl
  <p>It combines ease of use with the robust privacy features of ECH/Tor/VPN, allowing for secure and untraceable data collection.</p>

  [![Release][release-version-shield]][releases-link]
  [![Last Commit][last-commit-shield]][commit-link]
  ![Python][python-version-shield]
  [![license][license-shield]][license-link]
</div>

## BrowserTime
See more configurations in `https://www.sitespeed.io/documentation/browsertime/configuration/`

```sh
# Aliyun: https://dns.alidns.com/dns-query
# Google: https://dns.google/dns-query
# Tencent: https://doh.pub/dns-query
curl -H "accept: application/dns-json" "https://cloudflare-dns.com/dns-query?name=https://tls-ech.dev/"

docker build -t sitespeedio/browsertime .

# Avoid broadcasting/ARP/communication with other containers on default bridge `docker0`
docker network create flowcrawl-net
#
# --browser firefox \
# --firefox.preference "network.trr.mode:3" \
# --firefox.preference "network.trr.uri:https://cloudflare-dns.com/dns-query" \
# --firefox.preference "network.dns.echconfig.enabled:true" \
# --firefox.preference "network.dns.use_https_rr_as_altsvc:true" \
# --firefox.preference "network.trr.confirmation_telemetry:false" \
# --firefox.collectMozLog true --firefox.geckoProfiler true \
#
# --firefox.preference browser.safebrowsing.malware.enabled:false \
# --firefox.preference browser.safebrowsing.phishing.enabled:false \
# --firefox.preference browser.safebrowsing.downloads.enabled:false \
# --firefox.preference browser.ping-centre.telemetry:false \
# --firefox.preference toolkit.telemetry.enabled:false \
# --firefox.preference datareporting.healthreport.uploadEnabled:false \
#
# --firefox.preference app.update.enabled:false \
# --firefox.preference extensions.update.enabled:false \
# --firefox.preference browser.search.update:false \
#
# --firefox.preference identity.fxaccounts.enabled:false \
# --firefox.preference services.sync.engine.addons:false \
# --firefox.preference services.sync.engine.passwords:false \
#
# --firefox.preference extensions.enabledScopes:0 \
# --firefox.preference extensions.autoDisableScopes:0 \
# --firefox.preference beacon.enabled:false \
#
docker run --rm \
    --network flowcrawl-net \
    -v "$(pwd)":/browsertime \
    sitespeedio/browsertime:26.3.2 \
    -n 5 \
    --video --tcpdump --visualMetrics \
    --browser chrome \
    --chrome.args "enable-features=EncryptedClientHello" \
    --chrome.args "use-dns-https-alpn" \
    --chrome.args "force-dns-over-https=https://cloudflare-dns.com/dns-query" \
    --chrome.args "disable-async-dns" \
    --chrome.collectNetLog \
    --chrome.args "disable-background-networking" \
    --chrome.args "disable-component-update" \
    --chrome.args "disable-sync" \
    --chrome.args "disable-default-apps" \
    --chrome.args "disable-domain-reliability" \
    --chrome.args "disable-extensions" \
    https://tls-ech.dev/

# or
nohup python -u ./flowcrawl/run_browsertime.py data/links-for-request/ech/links-CF.txt > run_browsertime.log 2>&1 &
```

Check `encrypted_client_hello` filed in the `chromeNetlog-*.json`, you will see something like this:
```json
{"params":{"cipher_suite":4865,"encrypted_client_hello":true,"is_resumed":false,"key_exchange_group":4588,"next_proto":"h2","peer_signature_algorithm":1027,"version":"TLS 1.3"},"phase":2,"source":{"id":90,"start_time":"332374709","type":9},"time":"332374921","type":61},
```

<hr>

## FlowCrawl
> Requests → Tor(9050) → (tun0, Virtual Network Card, if enabled) → VPN Client(27890) → VPN Server → Internet

This is the most common approach, typically used to hide Tor usage from your Internet Service Provider (ISP).

- **Principle:** VPN client acts as a front proxy, and Tor’s traffic is sent through the encrypted tunnel established by VPN client.
- **Effect:** Your ISP can only see that you are connected to a VPN and cannot detect Tor usage; Tor nodes only see the VPN server’s IP, not your real IP.
- **Configuration:** Set `HTTPSProxy` or `Socks5Proxy` in Tor’s configuration to point to Clash’s local port.

1. **Install dependencies**:<br>
`pip install -r requirements.txt` or:
```sh
poetry install
source $(poetry env info -p)/bin/activate
# or
. $(poetry env info -p)/bin/activate

# (Optional)
pip install -e .
```

2. **Install and Start TOR Service**:
Start the clash first by running `docker compose --profile clash up -d`.

For advanced usage with bridges, start with the following configuration:

"""txt
#Use socks5h # Use SOCKS5 proxy and let DNS resolution also be carried out through the proxy (remote resolution)
#HTTPSProxy 127.0.0.1:27890
#HTTPSProxyAuthenticator user:password
Socks5Proxy 127.0.0.1:27890


UseBridges 1

ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy managed
Bridge obfs4 51.79.30.226:35077 6D0268328156594C41B50BF94EBD7CDCFAF985E2 cert=wQ35o1bPKT8CFmg/5C4eKmRMt4O+q6pBuflVe3vscbGS12bb4vwC5BnYepnNf0vgdDrnYQ iat-mode=0
Bridge obfs4 146.59.116.226:50845 DA91DE63966E03676A9994BDB7A18D1DCE2FAF10 cert=IAur+EwfAIbdC8jy+Mi9xlmh5ouL577Ya6ygJBEChWS8lNiEfy3hU/IAvDZ5Ntw/w2Oidg iat-mode=0

ClientTransportPlugin webtunnel exec /usr/bin/webtunnel
Bridge webtunnel [2001:db8:f765:be98:4d81:b8cb:fadc:2bc6]:443 58A23BB757C3FDDBAA0E3CA5E631B7225A87F852 url=https://redlib.005184.xyz/wlDwrKzwL3J43jiDCjT0Mb0z ver=0.0.3
Bridge webtunnel [2001:db8:ce90:3593:272e:4975:a031:55b]:443 12382A2F3912AD1983A97C8709CBAE47ADB60BE3 url=https://miranda.today/LWwxIXDHCyyScn7oDauPMTmX ver=0.0.3

ClientTransportPlugin snowflake exec /usr/bin/snowflake-client
Bridge snowflake
Bridge snowflake
"""

then start tor with this configuration:
1) Debian/Ubuntu: <br>
    `apt update && apt upgrade`
    `apt-get install tor wget`<br>
    `service tor start`
2) Windows: Download [`tor.exe`][tor-download], and:<br>
    `tor.exe --service install`<br>
    `tor.exe --service start`
3) MacOS: <br>
    `brew install tor`<br>
    `brew services start tor`

More detailed script on linux:

```sh
sudo apt install tor obfs4proxy
sudo apt install snowflake-client -y

sudo vi /etc/tor/torrc

sudo systemctl enable tor
sudo systemctl restart tor

sudo systemctl status tor
sudo netstat -lntp | grep tor
sudo journalctl -e -f -u tor@default

curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org
# >>> "Congratulations. This browser is configured to use Tor."

wget -e use_proxy=yes \
     -e https_proxy=socks5h://127.0.0.1:9050 \
     https://example.com

# The output IP should be the Tor exit node, not the real IP of your server
curl --socks5-hostname 127.0.0.1:9050 https://api.ipify.org
```

### Arguments
| **arg**      | **Long**            | **Description**                                                                        |
|--------------|---------------------|----------------------------------------------------------------------------------------|
| **General**: |                     |                                                                                        |
| -h           | --help              | Help message                                                                           |
| -v           | --verbose           | Show more information about the progress                                               |
| -u           | --url *.onion       | URL of Webpage to crawl or extract                                                     |
| -w           | --without           | Without using TOR Network                                                              |
| -rua         | --random-ua         | Enable random user-agent rotation for requests     |
| -rpr         | --random-proxy      | Enable random proxy rotation from res/proxies.txt (requires -w flag, one proxy per line, format: host:port) |
| -px          | --proxy             | IP address for SOCKS5 proxy (Default: 127.0.0.1 for using TOR)                         |
| -pr          | --proxyport         | Port for SOCKS5 proxy (Default: 9050)                                                  |
| -f           | --folder            | The directory which will contain the generated files                                   |
| -V           | --version           | Show version and exit                                                                  |
| **Extract**: |                     |                                                                                        |
| -e           | --extract           | Extract page's code to terminal or file (Default: Terminal)                            |
| -i           | --input filename    | Input file with URL(s) (separated by line)                                             |
| -o           | --output [filename] | Output page(s) to file(s) (for one page)                                               |
| -y           | --yara              | Perform yara keyword search:<br>h = search entire html object,<br>t = search only text |
| **Crawl**:   |                     |                                                                                        |
| -c           | --crawl             | Crawl website (Default output on website/links.txt)                                    |
| -d           | --depth             | Set depth of crawler's travel (Default: 1)                                             |
| -p           | --pause             | Seconds of pause between requests (Default: 0)                                         |
| -j           | --json              | Export crawl findings to JSON in addition to txt outputs                               |
| -x           | --xml               | Export crawl findings to XML in addition to txt outputs                                |
| -DB          | --database          | Export crawl findings and link graph to SQLite database                                |
| -vis         | --visualization     | Generate HTML visualization from SQLite database (requires -DB)                        |
| -l           | --log               | Log file with visited URLs and their response code                                     |

### Usage & Examples

#### As Extractor:
To just extract a single webpage to terminal:

```shell
$ python flowcrawl/main.py -u http://www.github.com
<!DOCTYPE html>
...
</html>
```

Extract into a file (github.htm) without the use of TOR:

```shell
$ python flowcrawl/main.py -w -u http://www.github.com -o github.htm
## File created on /script/path/github.htm
```

Extract to terminal and find only the line with google-analytics:

```shell
$ python flowcrawl/main.py -u http://www.github.com | grep 'google-analytics'
    <meta name="google-analytics" content="UA-*******-*">
```

Extract to file and find only the line with google-analytics using yara:
```shell
$ python flowcrawl/main.py -v -w -u https://github.com -e -y 0
...
```

**_Note:_** update res/keyword.yar to search for other keywords.
Use ```-y 0``` for raw html searching and ```-y 1``` for text search only.

Extract a set of webpages (imported from file) to terminal:

```shell
$ python flowcrawl/main.py -i links.txt
...
```

#### As Crawler:
Crawl the links of the webpage without the use of TOR, also show verbose output (really helpful):

```shell
$ python flowcrawl/main.py -v -w -u http://www.github.com/ -c
## URL: http://www.github.com/
## Your IP: *.*.*.*
## Crawler Started from http://www.github.com/ with step 1 and wait 0
## Step 1 completed with: 11 results
## File created on /script/path/links.txt
```

Crawl the webpage with depth 2 (2 clicks) and 5 seconds waiting before crawl the next page:

```shell
$ python flowcrawl/main.py -v -u http://www.github.com/ -c -d 2 -p 5
## TOR is ready!
## URL: http://www.github.com/
## Your IP: *.*.*.*
## Crawler Started from http://www.github.com with step 2 and wait 5
## Step 1 completed with: 11 results
## Step 2 completed with: 112 results
## File created on /script/path/links.txt
```

#### As Both:
You can crawl a page and also extract the webpages into a folder with a single command:

```shell
$ python flowcrawl/main.py -v -u http://www.github.com/ -c -d 2 -p 5 -e
## TOR is ready!
## URL: http://www.github.com/
## Your IP: *.*.*.*
## Crawler Started from http://www.github.com with step 1 and wait 5
## Step 1 completed with: 11 results
## File created on /script/path/FolderName/index.htm
## File created on /script/path/FolderName/projects.html
## ...
```
***Note:*** *The default (and only for now) file for crawler's links is the `links.txt` document. Also, to extract right after the crawl you have to give `-e` argument*

Following the same logic; you can parse all these pages to grep (for example) and search for specific text:

```shell
$ python flowcrawl/main.py -u http://www.github.com/ -c -e | grep '</html>'
</html>
</html>
...
```

#### As Both + Keyword Search:
You can crawl a page, perform a keyword search and extract the webpages that match the findings into a folder with a single command:

```shell
$ python flowcrawl/main.py -v -u http://www.github.com/ -c -d 2 -p 5 -e -y h
## TOR is ready!
## URL: http://www.github.com/
## Your IP: *.*.*.*
## Crawler Started from http://www.github.com with step 1 and wait 5
## Step 1 completed with: 11 results
## File created on /script/path/FolderName/index.htm
## File created on /script/path/FolderName/projects.html
## ...
```

***Note:*** *Update res/keyword.yar to search for other keywords.
Use ```-y h``` for raw html searching and ```-y t``` for text search only.*

## License
“GPL” stands for “General Public License”. Using the GNU GPL will require that all the released improved versions be free software ([More info][gpl-faq]).

<!-- Links -->
[last-commit-shield]: https://img.shields.io/github/last-commit/alpinebuster/continual-flowcrawl?logo=github&label=Last%20Commit&style=plastic
[release-version-shield]: https://img.shields.io/github/v/release/alpinebuster/continual-flowcrawl?logo=github&label=Release&style=plastic
[python-version-shield]: https://img.shields.io/badge/Python-v3-green.svg?style=plastic&logo=python&label=Python
[commit-link]: https://github.com/alpinebuster/continual-flowcrawl/commits/main
[releases-link]: https://github.com/alpinebuster/continual-flowcrawl/releases
[license-link]: https://github.com/alpinebuster/continual-flowcrawl/blob/master/LICENSE
[pypi-package]: https://pypi.org/project/flowcrawl/
[tor-whyslow]: https://www.torproject.org/docs/faq.html.en#WhySlow
[tor-download]: https://www.torproject.org/download/tor/
[tor-docs]: https://www.torproject.org/docs/
[gpl-faq]: https://www.gnu.org/licenses/gpl-faq.html
