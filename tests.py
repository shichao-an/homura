# -*- coding: utf-8 -*-
import shutil
import os
from unittest import TestCase
from homura import download, get_resource_name

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(PROJECT_PATH, 'test_data')
TEST_DATA_SUBDIR = os.path.join(TEST_DATA_DIR, 'sub')
SUBDIR_RELPATH = os.path.basename(TEST_DATA_SUBDIR)
FILE_SMALL = 'http://download.thinkbroadband.com/MD5SUMS'
FILE_1MB = 'http://download.thinkbroadband.com/1MB.zip'
FILE_5MB = 'http://download.thinkbroadband.com/5MB.zip'
FILE_301_SMALL = 'http://dev.moleculea.com/homura/301/SMD5SUMS'
FILE_301_1MB = 'http://dev.moleculea.com/homura/301/S1MB.zip'
FILE_301_5MB = 'http://dev.moleculea.com/homura/301/S5MB.zip'


def cleanup_data():
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)


class TestDownload(TestCase):
    """Test homura.download"""
    def setUp(self):
        cleanup_data()
        os.mkdir(TEST_DATA_DIR)
        os.mkdir(TEST_DATA_SUBDIR)
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

    def tearDown(self):
        cleanup_data()
