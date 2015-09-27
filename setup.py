from setuptools import setup
from codecs import open as codecs_open

with codecs_open('README.rst', encoding='utf-8') as f:
    lng_desc = f.read()

setup(
    name='homura',
    version='0.1.3',
    description="Python downloader with progress",
    long_description=lng_desc,
    keywords='download progress',
    author='Shichao An',
    author_email='shichao.an@nyu.edu',
    url='https://github.com/shichao-an/homura',
    license='BSD',
    install_requires=open('requirements.txt').read().splitlines(),
    py_modules=['homura'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
