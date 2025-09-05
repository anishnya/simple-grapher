"""
Tests for YAML parser functionality.
"""

import os
import tempfile
import unittest

from simple_grapher.utils.yaml_parser import (
    YAMLParser,
    parse_config_file,
    parse_data_file,
)


class TestYAMLParser(unittest.TestCase):
    """Test cases for YAMLParser class."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = YAMLParser()
        self.sample_yaml = """
graph:
  title: "Test Graph"
  type: "line"
  width: 800
  height: 600
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

    def test_load_string(self):
        """Test loading YAML from string."""
        data = self.parser.load_string(self.sample_yaml)
        self.assertIsInstance(data, dict)
        self.assertIn("graph", data)
        self.assertEqual(data["graph"]["title"], "Test Graph")

    def test_load_file(self):
        """Test loading YAML from file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(self.sample_yaml)
            tmp_path = tmp.name

        try:
            data = self.parser.load_file(tmp_path)
            self.assertIsInstance(data, dict)
            self.assertIn("graph", data)
        finally:
            os.unlink(tmp_path)

    def test_get_value(self):
        """Test getting values using dot notation."""
        self.parser.load_string(self.sample_yaml)

        # Test simple key
        self.assertEqual(self.parser.get_value("graph.title"), "Test Graph")

        # Test nested key
        self.assertEqual(self.parser.get_value("graph.x_axis.label"), "Time (seconds)")

        # Test sources list access
        sources = self.parser.get_value("data.sources")
        self.assertIsInstance(sources, list)
        self.assertEqual(len(sources), 3)
        self.assertEqual(sources[0]["file"], "ex1.csv")
        self.assertEqual(sources[0]["label"], "ex1")

        # Test non-existent key
        self.assertIsNone(self.parser.get_value("nonexistent"))

        # Test default value
        self.assertEqual(self.parser.get_value("nonexistent", "default"), "default")

    def test_validate_schema(self):
        """Test schema validation."""
        self.parser.load_string(self.sample_yaml)

        # Test with valid required keys
        required_keys = ["graph.title", "data.sources"]
        self.assertTrue(self.parser.validate_schema(required_keys))

        # Test with invalid required keys
        invalid_keys = ["nonexistent", "graph.title"]
        self.assertFalse(self.parser.validate_schema(invalid_keys))

    def test_save_file(self):
        """Test saving data to YAML file."""
        test_data = {"test": "value", "nested": {"key": "nested_value"}}

        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            self.parser.save_file(test_data, tmp_path)

            # Verify the file was created and contains correct data
            self.assertTrue(os.path.exists(tmp_path))

            # Load it back and verify
            loaded_data = self.parser.load_file(tmp_path)
            self.assertEqual(loaded_data, test_data)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""

    def test_parse_config_file(self):
        """Test parse_config_file convenience function."""
        sample_config = """
graph:
  title: "My Graph"
  type: "bar"
  x_axis:
    label: "X Axis"
  y_axis:
    label: "Y Axis"
  style:
    width: 10
    height: 10

data:
  sources:
    - file: "data1.csv"
      label: "Data 1"
    - file: "data2.csv"
      label: "Data 2"

output:
  format: "png"
  save_path: "./output.png"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(sample_config)
            tmp_path = tmp.name

        try:
            data = parse_config_file(tmp_path)
            self.assertEqual(data["graph"]["title"], "My Graph")
            self.assertIn("sources", data["data"])
            self.assertEqual(len(data["data"]["sources"]), 2)
        finally:
            os.unlink(tmp_path)

    def test_parse_data_file(self):
        """Test parse_data_file convenience function."""
        sample_data = """
datasets:
  - name: "Dataset 1"
    values: [1, 2, 3, 4, 5]
  - name: "Dataset 2"
    values: [2, 4, 6, 8, 10]
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(sample_data)
            tmp_path = tmp.name

        try:
            data = parse_data_file(tmp_path)
            self.assertIn("datasets", data)
            self.assertEqual(len(data["datasets"]), 2)
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
