"""
Tests for core functionality.
"""

import os
import tempfile
import unittest

import matplotlib.pyplot as plt
import pandas as pd

from simple_grapher.core.data_processor import DataProcessor
from simple_grapher.core.graph_builder import GraphBuilder
from simple_grapher.utils.yaml_parser import parse_config_file


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = DataProcessor()
        self.sample_config = {
            "data": {
                "sources": [
                    {"file": "ex1.csv", "label": "ex1"},
                    {"file": "ex2.csv", "label": "ex2"},
                    {"file": "ex3.csv", "label": "ex3"},
                ]
            }
        }

    def test_load_csv_with_valid_file(self):
        """Test loading CSV with valid file."""
        # Create a temporary CSV file
        csv_content = "x,y\n1,2\n3,4\n5,6\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            df = self.processor.load_csv(tmp_path)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(len(df), 3)
            self.assertListEqual(list(df.columns), ["x", "y"])
            self.assertListEqual(list(df["x"]), [1, 3, 5])
            self.assertListEqual(list(df["y"]), [2, 4, 6])
        finally:
            os.unlink(tmp_path)

    def test_load_csv_with_custom_columns(self):
        """Test loading CSV with custom column names - should use first two columns."""
        csv_content = "time,value\n1,2\n3,4\n5,6\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            df = self.processor.load_csv(tmp_path)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(len(df), 3)
            self.assertListEqual(list(df.columns), ["x", "y"])
            self.assertListEqual(list(df["x"]), [1, 3, 5])
            self.assertListEqual(list(df["y"]), [2, 4, 6])
        finally:
            os.unlink(tmp_path)

    def test_load_csv_with_missing_file(self):
        """Test loading CSV with missing file."""
        df = self.processor.load_csv("nonexistent.csv")
        self.assertIsNone(df)

    def test_load_csv_with_insufficient_columns(self):
        """Test loading CSV with insufficient columns (less than 2)."""
        csv_content = "a\n1\n3\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            df = self.processor.load_csv(tmp_path)
            self.assertIsNone(df)
        finally:
            os.unlink(tmp_path)

    def test_load_multiple_csvs(self):
        """Test loading multiple CSV files."""
        # Create two temporary CSV files
        csv1_content = "x,y\n1,2\n3,4\n"
        csv2_content = "x,y\n5,6\n7,8\n"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp1:
            tmp1.write(csv1_content)
            tmp1_path = tmp1.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp2:
            tmp2.write(csv2_content)
            tmp2_path = tmp2.name

        try:
            sources = [
                {"file": tmp1_path, "label": "data1"},
                {"file": tmp2_path, "label": "data2"},
            ]

            dataframes = self.processor.load_multiple_csvs(sources)
            self.assertIsInstance(dataframes, dict)
            self.assertEqual(len(dataframes), 2)
            self.assertIn("data1", dataframes)
            self.assertIn("data2", dataframes)
            self.assertIsInstance(dataframes["data1"], pd.DataFrame)
            self.assertIsInstance(dataframes["data2"], pd.DataFrame)
        finally:
            os.unlink(tmp1_path)
            os.unlink(tmp2_path)

    def test_process_data_with_sources_list(self):
        """Test data processing with sources list."""
        # Create a temporary CSV file
        csv_content = "x,y\n1,2\n3,4\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            sources = [{"file": tmp_path, "label": "test_data"}]
            result = self.processor.process_data(sources)
            self.assertIsInstance(result, dict)
            self.assertIn("test_data", result)
            self.assertIsInstance(result["test_data"], pd.DataFrame)
        finally:
            os.unlink(tmp_path)

    def test_process_data_with_single_source(self):
        """Test data processing with single source."""
        csv_content = "x,y\n1,2\n3,4\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            single_source = {"file": tmp_path, "label": "test_data"}
            result = self.processor.process_data(single_source)
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 2)
        finally:
            os.unlink(tmp_path)

    def test_process_data_with_string_path(self):
        """Test data processing with string path."""
        csv_content = "x,y\n1,2\n3,4\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            result = self.processor.process_data(tmp_path)
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 2)
        finally:
            os.unlink(tmp_path)


class TestGraphBuilder(unittest.TestCase):
    """Test cases for GraphBuilder class."""

    def setUp(self):
        """Set up test fixtures."""
        self.builder = GraphBuilder()
        self.sample_data = {
            "sources": [
                {"file": "ex1.csv", "label": "ex1"},
                {"file": "ex2.csv", "label": "ex2"},
            ]
        }

    def test_create_graph_with_data_sources(self):
        """Test graph creation with data sources list."""
        # Create sample DataFrames
        df1 = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        df2 = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})

        data_sources = [
            {"dataframe": df1, "label": "Dataset 1"},
            {"dataframe": df2, "label": "Dataset 2"},
        ]

        result = self.builder.create_graph(data_sources, "line", "Test Graph", "X", "Y")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, plt.Figure)

    def test_create_graph_with_different_types(self):
        """Test graph creation with different graph types."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        data_sources = [{"dataframe": df, "label": "Test Data"}]

        graph_types = ["line", "bar", "scatter"]
        for graph_type in graph_types:
            result = self.builder.create_graph(data_sources, graph_type)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, plt.Figure)

    def test_create_graph_from_dataframes(self):
        """Test graph creation from dictionary of DataFrames."""
        df1 = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        df2 = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})

        dataframes = {"Dataset 1": df1, "Dataset 2": df2}

        result = self.builder.create_graph_from_dataframes(
            dataframes, "line", "Test Graph"
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, plt.Figure)

    def test_create_graph_with_invalid_type(self):
        """Test graph creation with invalid graph type."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        data_sources = [{"dataframe": df, "label": "Test Data"}]

        result = self.builder.create_graph(data_sources, "invalid_type")
        self.assertIsNone(result)

    def test_create_graph_with_empty_sources(self):
        """Test graph creation with empty data sources."""
        result = self.builder.create_graph([], "line")
        self.assertIsNone(result)

    def test_save_graph(self):
        """Test graph saving functionality."""
        # Create a sample graph
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        data_sources = [{"dataframe": df, "label": "Test Data"}]
        figure = self.builder.create_graph(data_sources, "line")

        self.assertIsNotNone(figure)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            result = self.builder.save_graph(figure, tmp_path)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(tmp_path))
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestIntegrationWithBasicConfig(unittest.TestCase):
    """Test integration with basic_config.yaml structure."""

    def setUp(self):
        """Set up test fixtures."""
        self.basic_config_yaml = """
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

    def test_parse_basic_config_structure(self):
        """Test parsing the basic config structure."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tmp:
            tmp.write(self.basic_config_yaml)
            tmp_path = tmp.name

        try:
            config = parse_config_file(tmp_path)

            # Test graph configuration
            self.assertEqual(config["graph"]["title"], "Sample Data Visualization")
            self.assertEqual(config["graph"]["x_axis"]["label"], "Time (seconds)")
            self.assertEqual(config["graph"]["y_axis"]["label"], "Value")

            # Test data sources
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

            # Test output configuration
            self.assertEqual(config["output"]["format"], "png")
            self.assertEqual(config["output"]["dpi"], 300)
            self.assertEqual(config["output"]["save_path"], "./output/graph.png")

        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
