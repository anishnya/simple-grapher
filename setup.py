"""
Setup script for Simple Grapher.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simple-grapher",
    version="0.1.0",
    author="anishnya",
    author_email="anishnya@example.com",
    description="A simple command line tool for creating graphs and visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anishnya/simple-grapher",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        "console_scripts": [
            "simple-grapher=simple_grapher.cli:main",
        ],
    },
)
