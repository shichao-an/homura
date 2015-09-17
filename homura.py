# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
import datetime
import os
import six
import sys
import time
import pycurl
import shutil
from requests.utils import unquote as _unquote
from humanize import naturalsize

PY3 = sys.version_info[0] == 3
STREAM = sys.stderr
DEFAULT_RESOURCE = 'index.html'

if PY3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


def eval_path(path):
    return os.path.abspath(os.path.expanduser(path))


def utf8_encode(s):
    res = s
    if isinstance(res, six.text_type):
        res = s.encode('utf-8')
    return res


def utf8_decode(s):
    res = s
    if isinstance(res, six.binary_type):
        res = s.decode('utf-8')
    return res


def unquote(s):
    res = s
    if not PY3:
        if isinstance(res, six.text_type):
            res = s.encode('utf-8')
    return _unquote(res)


def dict_to_list(d):
    return ['%s: %s' % (k, v) for k, v in d.items()]


def is_temp_path(path):
    if path is None:
        return True
    else:
        path = eval_path(path)
        if os.path.isdir(path):
            return True
    return False


def get_resource_name(url):
    url = utf8_decode(url)  # decode to unicode so PY3's urlparse won't break
    o = urlparse(url)
    resource = os.path.basename(o.path)
    if not resource:
        res = DEFAULT_RESOURCE
    else:
        res = resource
    return utf8_decode(unquote(res))


class Homura(object):
    progress_template = \
        '%(percent)6d%% %(downloaded)12s %(speed)15s %(eta)18s ETA' + ' ' * 4
    eta_limit = 2592000  # 30 days

    def __init__(self, url, path=None, headers=None, session=None,
                 show_progress=True, resume=True, auto_retry=True,
                 max_rst_retries=5, pass_through_opts=None):
        """
        :param str url: URL of the file to be downloaded
        :param str path: local path for the downloaded file; if None, it will
            be the URL base name
        :param dict headers: extra headers
        :param session: session used to download (if you want to work with
            requests library)
        :type session: `class:requests.Session`
        :param bool show_progress: whether to show download progress
        :param bool resume: whether to resume download (by
            filename)
        :param bool auto_retry: whether to retry automatically upon closed
            transfer until the file's download is finished
        :param int max_rst_retries: number of retries upon connection reset by
            peer (effective only when `auto_retry` is True)
        :param dict pass_through_opts: a dictinary of options passed to cURL
        """
        self.url = url  # url is in unicode
        self.path = self._get_path(path, url)
        self.headers = headers
        self.session = session
        self.show_progress = show_progress
        self.resume = resume
        self.auto_retry = auto_retry
        self.max_rst_retries = max_rst_retries
        self.start_time = None
        self.content_length = 0
        self.downloaded = 0
        self._path = path  # Save given path
        self._pycurl = pycurl.Curl()
        self._cookie_header = self._get_cookie_header()
        self._last_time = 0.0
        self._rst_retries = 0
        self._pass_through_opts = pass_through_opts

    def _get_cookie_header(self):
        if self.session is not None:
            cookie = dict(self.session.cookies)
            res = []
            for k, v in cookie.items():
                s = '%s=%s' % (k, v)
                res.append(s)
            if not res:
                return None
            return '; '.join(res)

    def _get_path(self, path, url):
        if path is None:
            res = get_resource_name(url)
        else:
            # decode path to unicode so that os.path.join won't break
            res = eval_path(utf8_decode(path))
            if os.path.isdir(res):
                resource = get_resource_name(url)
                res = os.path.join(res, resource)
        return res

    def _get_pycurl_headers(self):
        headers = self.headers or {}
        if self._cookie_header is not None:
            headers['Cookie'] = self._cookie_header
        return dict_to_list(headers) or None

    def curl(self):
        """Sending a single cURL request to download"""
        c = self._pycurl
        # Resume download
        if os.path.exists(self.path) and self.resume:
            mode = 'ab'
            self.downloaded = os.path.getsize(self.path)
            c.setopt(pycurl.RESUME_FROM, self.downloaded)
        else:
            mode = 'wb'
        with open(self.path, mode) as f:
            c.setopt(c.URL, utf8_encode(self.url))
            c.setopt(c.WRITEDATA, f)
            h = self._get_pycurl_headers()
            if h is not None:
                c.setopt(pycurl.HTTPHEADER, h)
            c.setopt(c.NOPROGRESS, 0)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(c.PROGRESSFUNCTION, self.progress)
            if self._pass_through_opts:
                for key, value in self._pass_through_opts.items():
                    c.setopt(key, value)
            c.perform()

    def start(self):
        """
        Start downloading, handling auto retry, download resume and path
        moving
        """
        if not self.auto_retry:
            self.curl()
            return
        while not self.is_finished:
            try:
                self.curl()
            except pycurl.error as e:
                # transfer closed with n bytes remaining to read
                if e.args[0] == 18:
                    pass
                # HTTP server doesn't seem to support byte ranges.
                # Cannot resume.
                elif e.args[0] == 33:
                    break
                # Recv failure: Connection reset by peer
                elif e.args[0] == 56:
                    if self._rst_retries < self.max_rst_retries:
                        pass
                    else:
                        raise e
                    self._rst_retries += 1
                else:
                    raise e
        self._move_path()
        self._done()

    def progress(self, download_t, download_d, upload_t, upload_d):
        self.content_length = self.downloaded + int(download_t)
        if int(download_t) == 0:
            return
        if not self.show_progress:
            return
        if self.start_time is None:
            self.start_time = time.time()
        duration = time.time() - self.start_time + 1
        speed = download_d / duration
        speed_s = naturalsize(speed, binary=True)
        speed_s += '/s'
        if speed == 0.0:
            eta = self.eta_limit
        else:
            eta = int((download_t - download_d) / speed)
        if eta < self.eta_limit:
            eta_s = str(datetime.timedelta(seconds=eta))
        else:
            eta_s = 'n/a'
        downloaded = self.downloaded + download_d
        downloaded_s = naturalsize(downloaded, binary=True)
        percent = int(downloaded / self.content_length * 100)
        params = {
            'downloaded': downloaded_s,
            'percent': percent,
            'speed': speed_s,
            'eta': eta_s,
        }
        if STREAM.isatty():
            p = (self.progress_template + '\r') % params
        else:
            current_time = time.time()
            if self._last_time == 0.0:
                self._last_time = current_time
            else:
                interval = current_time - self._last_time
                if interval < 0.5:
                    return
                self._last_time = current_time
            p = (self.progress_template + '\n') % params
        STREAM.write(p)
        STREAM.flush()

    @property
    def is_finished(self):
        if os.path.exists(self.path):
            return self.content_length == os.path.getsize(self.path)

    def _done(self):
        STREAM.write('\n')
        STREAM.flush()

    def _move_path(self):
        """
        Move the downloaded file to the authentic path (identified by
        effective URL)
        """
        if is_temp_path(self._path) and self._pycurl is not None:
            eurl = self._pycurl.getinfo(pycurl.EFFECTIVE_URL)
            er = get_resource_name(eurl)
            r = get_resource_name(self.url)
            if er != r and os.path.exists(self.path):
                new_path = self._get_path(self._path, eurl)
                shutil.move(self.path, new_path)
                self.path = new_path


def download(url, path=None, headers=None, session=None, show_progress=True,
             resume=True, auto_retry=True, max_rst_retries=5,
             pass_through_opts=None):
    """Main download function"""
    hm = Homura(url, path, headers, session, show_progress, resume,
                auto_retry, max_rst_retries, pass_through_opts)
    hm.start()
