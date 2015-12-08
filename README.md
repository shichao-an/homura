## Homura

[![Build Status][travis-image]][travis-link]
[![PyPI Version][pypi-image]][pypi-link]

Homura (ほむら) is a Python downloader with progress, which can be used to download large files.

It is named after [Homura Akemi](http://ja.wikipedia.org/wiki/%E6%9A%81%E7%BE%8E%E3%81%BB%E3%82%80%E3%82%89>).

### Features

* PycURL based
* Resume downloads (if server supports [byte ranges](http://en.wikipedia.org/wiki/Byte_serving) on the resource)
* Support for `requests.Session`

### Installation

Homura depends on [PycURL](http://pycurl.sourceforge.net/). Install dependencies before installing the python package:

#### Ubuntu

```bash
sudo apt-get install build-essential libcurl4-openssl-dev python-dev
```

#### Fedora

Yum:

```bash
sudo yum groupinstall "Development Tools"
sudo yum install libcurl libcurl-devel python-devel
```

DNF:

```bash
sudo dnf groupinstall "Development Tools"
sudo dnf install libcurl libcurl-devel python-devel
```

#### Install Homura

```bash
pip install homura
```

### Usage

The simplest usage is to import the utility function `download`:

```python
from homura import download
download('http://download.thinkbroadband.com/200MB.zip')
    3%      6.2 MiB     739.5 KiB/s            0:04:28 ETA
```

To specify path for downloaded file:

```python
download(url='http://download.thinkbroadband.com/200MB.zip',
         path='/path/to/big.zip')
```

You can specify extra headers as a dictionary:

```python
download(url='http://example.com', headers={'API-Key': '123456'})
```

You can work with `Session` objects of the [requests](http://docs.python-requests.org/en/latest/) library:

```python
import requests
s = requests.Session()
# Do some work with `s` and send requests
download(url='http://example.com', session=s)
```

Pass options to `setopt` of the `pycurl.Curl` object via the `pass_through_opts` argument:

```python
import pycurl
download(url=url, pass_through_opts={pycurl.FOLLOWLOCATION: True})
```

[travis-image]: https://api.travis-ci.org/shichao-an/homura.png?branch=master
[travis-link]: https://travis-ci.org/shichao-an/homura
[pypi-image]: https://img.shields.io/pypi/v/homura.png
[pypi-link]: https://pypi.python.org/pypi/homura/
