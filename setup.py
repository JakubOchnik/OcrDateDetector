#!/usr/bin/env python
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ocr-date-detector",
    version = "0.0.1",
    author = "Jakub Ochnik",
    description = ("Automatic detection of picture date based on OCR."),
    license = "MIT",
    packages = ['ocr_date_detector'],
    entry_points={"console_scripts": ["ocr-date-detector = ocr_date_detector.cli:main"]},
    long_description=read('README.md'),
)
