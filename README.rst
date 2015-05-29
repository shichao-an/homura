Homura
======

|Build| |PyPI version|

Homura (ほむら) is a Python downloader with progress, which can be used to download large files.

It is named after `Homura Akemi <http://ja.wikipedia.org/wiki/%E6%9A%81%E7%BE%8E%E3%81%BB%E3%82%80%E3%82%89>`_.

Features
========

* PycURL based
* Resume downloads (if server supports `byte ranges <http://en.wikipedia.org/wiki/Byte_serving>`_ on the resource)
* Support for requests.Session


Installation
------------
Homura depends on `PycURL <http://pycurl.sourceforge.net/>`_. Install dependencies before installing the python package:

Ubuntu

.. code-block:: bash

    $ sudo apt-get install build-essential libcurl4-openssl-dev python-dev

Fedora

.. code-block:: bash

    $ sudo yum groupinstall "Development Tools"
    $ sudo yum install libcurl libcurl-devel python-devel

Then, install homura

.. code-block:: bash

    $ pip install homura

Usage
-----

The simplest usage is to import the utility function ``download``:

.. code-block:: python

    >>> from homura import download
    >>> download('http://download.thinkbroadband.com/200MB.zip')
        3%      6.2 MiB     739.5 KiB/s            0:04:28 ETA

To specify path for downloaded file:

.. code-block:: python

    >>> download(url='http://download.thinkbroadband.com/200MB.zip',
                 path='/path/to/big.zip')

You can specify extra headers as a dictionary:

.. code-block:: python

    >>> download(url='http://example.com', headers={'API-Key': '123456'})

Or you can work with ``Session`` objects of the `requests <http://docs.python-requests.org/en/latest/>`_ library:

.. code-block:: python

    >>> import requests
    >>> s = requests.Session()
    # Do some work with `s` and send requests
    >>> download(url='http://example.com', session=s)

.. |Build| image:: https://api.travis-ci.org/shichao-an/homura.png?branch=master
   :target: http://travis-ci.org/shichao-an/homura
.. |PyPI version| image:: https://img.shields.io/pypi/v/homura.png
   :target: https://pypi.python.org/pypi/homura/
