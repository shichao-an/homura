# -*- coding: utf-8 -*-
from homura import utf8_encode
import shutil
import os
from unittest import TestCase
from homura import download, get_resource_name

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(PROJECT_PATH, 'test_data')
TEST_DATA_SUBDIR = os.path.join(TEST_DATA_DIR, 'sub')
TEST_DATA_ASCII = TEST_DATA_SUBDIR
TEST_DATA_UNICODE = os.path.join(TEST_DATA_DIR, u'下载')
TEST_DATA_UTF8 = utf8_encode(os.path.join(TEST_DATA_DIR, u'离线'))
SUBDIR_RELPATH = os.path.basename(TEST_DATA_SUBDIR)
FILE_SMALL = 'http://download.thinkbroadband.com/MD5SUMS'
FILE_1MB = 'http://download.thinkbroadband.com/1MB.zip'
FILE_5MB = 'http://download.thinkbroadband.com/5MB.zip'
FILE_301_SMALL = 'http://dev.moleculea.com/homura/301/SMD5SUMS'
FILE_301_1MB = 'http://dev.moleculea.com/homura/301/S1MB.zip'
FILE_301_5MB = 'http://dev.moleculea.com/homura/301/S5MB.zip'
FILE_UNICODE = u'http://dev.moleculea.com/离线下载.txt'
FILE_UTF8 = 'http://dev.moleculea.com/离线下载.txt'


def cleanup_data():
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)


class TestDownload(TestCase):
    """Test homura.download"""
    def setUp(self):
        cleanup_data()
        os.mkdir(TEST_DATA_DIR)
        os.mkdir(TEST_DATA_SUBDIR)
        os.mkdir(TEST_DATA_UNICODE)
        os.mkdir(TEST_DATA_UTF8)
        os.chdir(TEST_DATA_DIR)

    def test_simple(self):
        download(FILE_1MB)
        f = os.path.join(TEST_DATA_DIR, get_resource_name(FILE_1MB))
        assert os.path.exists(f)
        os.remove(f)

    def test_path(self):
        url = FILE_SMALL

        # path=''
        download(url=url, path='')
        f = os.path.join(TEST_DATA_DIR, get_resource_name(url))
        assert os.path.exists(f)
        os.remove(f)

        # path='.'
        download(url=url, path='.')
        f = os.path.join(TEST_DATA_DIR, get_resource_name(url))
        assert os.path.exists(f)
        os.remove(f)

        # path=TEST_DATA_SUBDIR
        download(url=url, path=TEST_DATA_SUBDIR)
        f = os.path.join(TEST_DATA_SUBDIR, get_resource_name(url))
        assert os.path.exists(f)
        os.remove(f)

        # path='foobar'
        download(url=url, path='foobar')
        f = os.path.join(TEST_DATA_DIR, 'foobar')
        assert os.path.exists(f)
        os.remove(f)

        # path='foo/bar'
        with self.assertRaises(IOError):
            download(url=url, path='foo/bar')
        f = os.path.join(TEST_DATA_DIR, 'foo', 'bar')
        assert not os.path.exists(f)

    def test_redirect(self):
        url = FILE_301_SMALL
        eurl = FILE_SMALL

        # No path
        download(url=url)
        f = os.path.join(TEST_DATA_DIR, get_resource_name(url))
        ef = os.path.join(TEST_DATA_DIR, get_resource_name(eurl))
        assert not os.path.exists(f)
        assert os.path.exists(ef)
        os.remove(ef)

        # path='foobar'
        download(url=url, path='foobar')
        f = os.path.join(TEST_DATA_DIR, 'foobar')
        assert os.path.exists(f)
        os.remove(f)

    def test_unicode(self):
        url = FILE_UNICODE
        path_ascii = TEST_DATA_ASCII
        path_unicode = TEST_DATA_UNICODE
        path_utf8 = TEST_DATA_UTF8

        # No path
        download(url=url)
        f = os.path.join(TEST_DATA_DIR, get_resource_name(url))
        assert os.path.exists(f)
        os.remove(f)

        # ASCII path
        download(url=url, path=path_ascii)
        f = os.path.join(TEST_DATA_DIR, path_ascii, get_resource_name(url))
        assert os.path.exists(f)
        os.remove(f)

        # Unicode path
        download(url=url, path=path_unicode)
        f = os.path.join(TEST_DATA_DIR, path_unicode, get_resource_name(url))
        assert os.path.exists(f)
        os.remove(f)

        # UTF-8 path
        download(url=url, path=path_utf8)
        f = os.path.join(utf8_encode(TEST_DATA_DIR), path_utf8,
                         utf8_encode(get_resource_name(url)))
        assert os.path.exists(f)
        os.remove(f)

    def test_utf8(self):
        url = FILE_UTF8
        path_ascii = TEST_DATA_ASCII
        path_unicode = TEST_DATA_UNICODE
        path_utf8 = TEST_DATA_UTF8

        # No path
        download(url=url)
        f = os.path.join(TEST_DATA_DIR, get_resource_name(url))
        assert os.path.exists(f)
        os.remove(f)

        # ASCII path
        download(url=url, path=path_ascii)
        f = os.path.join(TEST_DATA_DIR, path_ascii, get_resource_name(url))
        assert os.path.exists(f)
        os.remove(f)

        # Unicode path
        download(url=url, path=path_unicode)
        f = os.path.join(TEST_DATA_DIR, path_unicode, get_resource_name(url))
        assert os.path.exists(f)
        os.remove(f)

        # UTF-8 path
        download(url=url, path=path_utf8)
        f = os.path.join(utf8_encode(TEST_DATA_DIR), path_utf8,
                         utf8_encode(get_resource_name(url)))
        assert os.path.exists(f)
        os.remove(f)

    def tearDown(self):
        cleanup_data()
