"""
Simple Grapher - A command line tool for creating simple graphs and visualizations.
"""

__version__ = "0.1.0"
__author__ = "anishnya"

from .cli import main
from .core import Config, DataProcessor, GraphBuilder
from .utils import YAMLParser, parse_config_file, parse_data_file

__all__ = [
    "main",
    "Config",
    "GraphBuilder",
    "DataProcessor",
    "YAMLParser",
    "parse_config_file",
    "parse_data_file",
]
