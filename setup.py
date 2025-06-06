#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="myreze",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="",
    author_email="",
    description="Data processing and visualization toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
