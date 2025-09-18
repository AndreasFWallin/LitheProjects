#!/usr/bin/env python3
"""
Setup script for PDF to DOCX Converter CLI Tool
"""

from setuptools import setup, find_packages

# Read README if exists, else use docstring
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A simple CLI tool for converting PDF files to DOCX format by extracting text."

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pdf2docx-cli",
    version="1.0.0",
    author="CLI Tool",
    author_email="cli@example.com",
    description="A simple CLI tool for converting PDF to DOCX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/pdf2docx-cli",
    py_modules=["pdf2docx"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pdf2docx=pdf2docx:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
)