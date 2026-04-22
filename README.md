<!--
  Title: Continual Flow Crawl
  Description: Crawl, capture PCAP, and extract webpages through ECH/TOR/VPN.
  Author: alpinebuster
  -->

<div align="center">
  <img width="50%" alt="Logo" src=".github/continual-flowcrawl.svg">

  # Continual Flow Crawl
  <p>It combines ease of use with the robust privacy features of ECH/Tor/VPN, allowing for secure and untraceable data collection.</p>

  [![Release][release-version-shield]][releases-link]
  [![Last Commit][last-commit-shield]][commit-link]
  ![Python][python-version-shield]
  [![license][license-shield]][license-link]
</div>

## Getting Started
See more configurations in `https://www.sitespeed.io/documentation/browsertime/configuration/`

```sh
docker build -t sitespeedio/browsertime .
docker run --rm -v "$(pwd)":/browsertime sitespeedio/browsertime:26.3.2 \
    -n 50 \
    --video --tcpdump --visualMetrics \
    --browser chrome \
    https://www.sitespeed.io/
```

### What makes it simple and easy to use?

If you are a terminal maniac you know that things have to be simple and clear. Passing the output into other tools is necessary and accuracy is the key.

With a single argument, you can read an .onion webpage or a regular one, through TOR Network and by using pipes you can pass the output at any other tool you prefer.

```shell
$ flowcrawl -u http://www.github.com/ | grep 'google-analytics'
    <meta-name="google-analytics" content="UA-XXXXXX- ">
```

If you want to crawl the links of a webpage use the `-c` and **BAM** you got on a file all the inside links. You can even use `-d` to crawl them and so on. You can also use the argument `-p` to wait some seconds before the next crawl.

```shell
$ flowcrawl -v -u http://www.github.com/ -c -d 2 -p 2
# TOR is ready!
# URL: http://www.github.com/
# Your IP: XXX.XXX.XXX.XXX
# Crawler started from http://www.github.com/ with 2 depth crawl and 2 second(s) delay:
# Step 1 completed with: 11 results
# Step 2 completed with: 112 results
# File created on /path/to/project/links.txt
```

> [!TIP]
> Crawling is not illegal, but violating copyright *is*. It’s always best to double-check a website’s T&C before start crawling them. Some websites set up what’s called `robots.txt` to tell crawlers not to visit those pages.
> <br>This crawler *will* allow you to go around this, but we always *recommend* respecting robots.txt.

<hr>

## Installation

### Easy Installation:
- from [PyPi][pypi-package]:<br>
`pip install flowcrawl`
- with homebrew:<br>
*Coming soon...*

### Manual Installation:
1. **Clone this repository**:<br>
`git clone https://github.com/alpinebuster/continual-flowcrawl.git`
2. **Install dependencies**:<br>
`pip install -r requirements.txt`
3. **Install and Start TOR Service**:
    1. **Debian/Ubuntu**: <br>
        `apt-get install tor`<br>
        `service tor start`
    2. **Windows**: Download [`tor.exe`][tor-download], and:<br>
        `tor.exe --service install`<br>
        `tor.exe --service start`
    3. **MacOS**: <br>
        `brew install tor`<br>
        `brew services start tor`
    4. For different distros, visit:<br>
       [TOR Setup Documentation][tor-docs]

## Arguments
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

## Usage & Examples

### As Extractor:
To just extract a single webpage to terminal:

```shell
$ python flowcrawl.py -u http://www.github.com
<!DOCTYPE html>
...
</html>
```

Extract into a file (github.htm) without the use of TOR:

```shell
$ python flowcrawl.py -w -u http://www.github.com -o github.htm
## File created on /script/path/github.htm
```

Extract to terminal and find only the line with google-analytics:

```shell
$ python flowcrawl.py -u http://www.github.com | grep 'google-analytics'
    <meta name="google-analytics" content="UA-*******-*">
```

Extract to file and find only the line with google-analytics using yara:
```shell
$ python flowcrawl.py -v -w -u https://github.com -e -y 0
...
```
**_Note:_** update res/keyword.yar to search for other keywords.
Use ```-y 0``` for raw html searching and ```-y 1``` for text search only.

Extract a set of webpages (imported from file) to terminal:

```shell
$ python flowcrawl.py -i links.txt
...
```


### As Crawler:
Crawl the links of the webpage without the use of TOR, also show verbose output (really helpful):

```shell
$ python flowcrawl.py -v -w -u http://www.github.com/ -c
## URL: http://www.github.com/
## Your IP: *.*.*.*
## Crawler Started from http://www.github.com/ with step 1 and wait 0
## Step 1 completed with: 11 results
## File created on /script/path/links.txt
```

Crawl the webpage with depth 2 (2 clicks) and 5 seconds waiting before crawl the next page:

```shell
$ python flowcrawl.py -v -u http://www.github.com/ -c -d 2 -p 5
## TOR is ready!
## URL: http://www.github.com/
## Your IP: *.*.*.*
## Crawler Started from http://www.github.com with step 2 and wait 5
## Step 1 completed with: 11 results
## Step 2 completed with: 112 results
## File created on /script/path/links.txt
```
### As Both:
You can crawl a page and also extract the webpages into a folder with a single command:

```shell
$ python flowcrawl.py -v -u http://www.github.com/ -c -d 2 -p 5 -e
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
$ python flowcrawl.py -u http://www.github.com/ -c -e | grep '</html>'
</html>
</html>
...
```

### As Both + Keyword Search:
You can crawl a page, perform a keyword search and extract the webpages that match the findings into a folder with a single command:

```shell
$ python flowcrawl.py -v -u http://www.github.com/ -c -d 2 -p 5 -e -y h
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

---

## TODO
### Requirements
The following was tested on Ubuntu 22.04.1 LTS.

1) Python 3.7 or higher.
2) wget:
```bash
apt update && apt upgrade
apt install wget
```

3) Google Chrome. The version used to create this dataset is 119.0.6046.159. To download the current version as an example:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# Make sure that Chrome is installed:
google-chrome --version
```

3) tshark 4.0.6 or higher: Note that if you are a non-super user, then you will need to either allow non-super users to capture packets when downloading the package, or add the user to the set of users that can capture packets.
```bash
apt install tshark
```

4) Python packages:
```sh
pip3 install bs4
```

### Creating the dataset

1) Set the following alias for the `chrome` command:
```bashrc
alias chrome="google-chrome"
```

2) Create the traces by issuing requests to webpages. The requests are issued
one at a time:
```sh
python3 create_trace.py --links_folder=<folder_path_containing_links> --output_folder=<path_to_output_folder> --requests_per_webpage=<number_of_requests> --starting_index=<index>
```

The parameters are as follows:
- `--links_folder` is the path to the folder containing the links to the webpages to be used in the experiment. The folder is expected to contain subfolders of servers, and in each subfolder a file named `links.txt` which contains the links for different webpages, each link in a row.
- `--output_folder` is the path to the folder where the traces will be saved. The output folder will contain subfolders for each server, and in each subfolder there will be a folder for each webpage, and in each webpage folder there will be a folder for each request. Each request folder will contain the pcap file, the HTML file, the NetLog file, log, and the key file. The key file is used to decrypt the traffic.
- `--requests_per_webpage` is the number of requests to be sent to each webpage, sequentially.
- `--starting_index` is a number to add as a prefix to the trace number. This is useful when running the script multiple times to create multiple datasets. The default value is 0.

Usage example:
```sh
python3 create_trace.py --links_folder=links-for-request --output_folder=data2 --requests_per_webpage=100 --starting_index=0002
```

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
