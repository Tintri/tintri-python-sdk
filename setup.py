#!/usr/bin/python
import os

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='Tintri PySDK',
    version='1.0',
    include_package_data=True,
    description='A Python SDK for Tintri management APIs.',
    author='Tintri',
    author_email='pysdk@tintri.com',
    license='BSD',
    keywords='tintri python sdk',
    url='http://hub.tintricity.com/discussions/automation',
    packages=find_packages(exclude=["test", "tintri.test", "tintri.test.*", "tintri.v310.internal"]),
    long_description=read('README'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License'
    ],
    install_requires=[
        'requests'
    ]
)
