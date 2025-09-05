"""
Tests for CLI functionality.
"""

import argparse
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple_grapher.cli import (  # noqa: E402
    create_graph_config,
    create_parser,
    main,
    process_input,
)


class TestCLI(unittest.TestCase):
    """Test cases for CLI functionality."""

    def test_parser_creation(self):
        """Test argument parser creation."""
        parser = create_parser()
        self.assertIsInstance(parser, argparse.ArgumentParser)

    def test_parser_arguments(self):
        """Test that parser has required arguments."""
        parser = create_parser()
        args = parser.parse_args(["--input", "test.yaml"])
        self.assertEqual(args.input, "test.yaml")

    def test_process_input_with_basic_config(self):
        """Test processing input with basic config structure."""
        basic_config_yaml = """
graph:
  title: "Sample Data Visualization"
  x_axis:
    label: "Time (seconds)"
    min: 0
    max: 100
  y_axis:
    label: "Value"
    min: 0
    max: 50
  style:
    width: 10
    height: 10
    fonts:
      title_size: 16
      label_size: 12
      legend_size: 10
    grid:
      show: true

data:
  sources:
    - file: "ex1.csv"
      label: "ex1"
    - file: "ex2.csv"
      label: "ex2"
    - file: "ex3.csv"
      label: "ex3"

output:
  format: "png"
  dpi: 300
  quality: "high"
  save_path: "./output/graph.png"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(basic_config_yaml)
            tmp_path = tmp.name

        try:
            config = process_input(tmp_path)

            # Test that config is loaded correctly
            self.assertIsInstance(config, dict)
            self.assertIn("graph", config)
            self.assertIn("data", config)
            self.assertIn("output", config)

            # Test data sources structure
            self.assertIn("sources", config["data"])
            sources = config["data"]["sources"]
            self.assertIsInstance(sources, list)
            self.assertEqual(len(sources), 3)

            # Test individual source structure
            for i, source in enumerate(sources, 1):
                self.assertIn("file", source)
                self.assertIn("label", source)
                self.assertEqual(source["file"], f"ex{i}.csv")
                self.assertEqual(source["label"], f"ex{i}")

        finally:
            os.unlink(tmp_path)

    def test_create_graph_config(self):
        """Test graph configuration creation."""
        test_data = {
            "graph": {"title": "Test Graph"},
            "data": {"sources": [{"file": "test.csv", "label": "test"}]},
            "output": {"format": "png"},
        }

        config = create_graph_config(test_data)
        self.assertEqual(config, test_data)

    @patch("simple_grapher.cli.process_input")
    @patch("simple_grapher.core.graph_builder.GraphBuilder.create_graph_from_config")
    @patch("simple_grapher.core.graph_builder.GraphBuilder.save_graph")
    def test_main_function(
        self, mock_save_graph, mock_create_graph, mock_process_input
    ):
        """Test main function execution."""
        # Mock configuration with data sources
        mock_config = {
            "data": {
                "sources": [
                    {"file": "test1.csv", "label": "test1"},
                    {"file": "test2.csv", "label": "test2"},
                ]
            },
            "output": {"save_path": "./test_output.png", "dpi": 300},
        }
        mock_process_input.return_value = mock_config
        mock_create_graph.return_value = "mock_figure"
        mock_save_graph.return_value = True

        # Test with valid arguments
        with patch("sys.argv", ["simple-grapher", "--input", "test.yaml"]):
            result = main()
            self.assertEqual(result, 0)
            mock_process_input.assert_called_once_with("test.yaml")
            mock_create_graph.assert_called_once()
            mock_save_graph.assert_called_once()

    def test_main_with_missing_input(self):
        """Test main function with missing required input."""
        with patch("sys.argv", ["simple-grapher"]):
            with self.assertRaises(SystemExit):
                main()


if __name__ == "__main__":
    unittest.main()
