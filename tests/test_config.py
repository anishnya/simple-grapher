"""
Tests for the Config module.
"""

import tempfile
from pathlib import Path

import pytest

from simple_grapher.core import Config


class TestConfig:
    """Test cases for the Config class."""

    def test_config_creation(self):
        """Test creating a config object with default values."""
        config = Config()

        assert config.graph.title == ""
        assert config.graph.x_axis.label == ""
        assert config.graph.y_axis.label == ""
        assert config.graph.style.width == 10
        assert config.graph.style.height == 10
        assert config.graph.style.fonts.title_size == 16
        assert config.graph.style.grid.show is True
        assert len(config.data.sources) == 0
        assert config.output.format == "png"
        assert config.output.dpi == 300

    def test_config_from_yaml_string(self):
        """Test creating a config from a YAML string."""
        yaml_content = """
graph:
  title: "Test Graph"
  x_axis:
    label: "X Label"
    min: 0
    max: 100
  y_axis:
    label: "Y Label"
    min: 0
    max: 50
  style:
    width: 12
    height: 8
    fonts:
      title_size: 18
      label_size: 14
      legend_size: 12
    grid:
      show: false

data:
  sources:
    - file: "test1.csv"
      label: "Test 1"
    - file: "test2.csv"
      label: "Test 2"

output:
  format: "svg"
  dpi: 150
  save_path: "./test_output.svg"
"""

        config = Config.from_yaml_string(yaml_content)

        assert config.graph.title == "Test Graph"
        assert config.graph.x_axis.label == "X Label"
        assert config.graph.x_axis.min == 0
        assert config.graph.x_axis.max == 100
        assert config.graph.y_axis.label == "Y Label"
        assert config.graph.y_axis.min == 0
        assert config.graph.y_axis.max == 50
        assert config.graph.style.width == 12
        assert config.graph.style.height == 8
        assert config.graph.style.fonts.title_size == 18
        assert config.graph.style.fonts.label_size == 14
        assert config.graph.style.fonts.legend_size == 12
        assert config.graph.style.grid.show is False
        assert len(config.data.sources) == 2
        assert config.data.sources[0].file == "test1.csv"
        assert config.data.sources[0].label == "Test 1"
        assert config.data.sources[1].file == "test2.csv"
        assert config.data.sources[1].label == "Test 2"
        assert config.output.format == "svg"
        assert config.output.dpi == 150
        assert config.output.save_path == "./test_output.svg"

    def test_config_from_yaml_file(self):
        """Test creating a config from a YAML file."""
        yaml_content = """
graph:
  title: "File Test Graph"
  x_axis:
    label: "Time"
  y_axis:
    label: "Value"

data:
  sources:
    - file: "data.csv"
      label: "Data"

output:
  format: "png"
  save_path: "./output.png"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            temp_file = f.name

        try:
            config = Config.from_yaml_file(temp_file)

            assert config.graph.title == "File Test Graph"
            assert config.graph.x_axis.label == "Time"
            assert config.graph.y_axis.label == "Value"
            assert len(config.data.sources) == 1
            assert config.data.sources[0].file == "data.csv"
            assert config.data.sources[0].label == "Data"
            assert config.output.format == "png"
            assert config.output.save_path == "./output.png"
        finally:
            Path(temp_file).unlink()

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = Config()
        config.graph.title = "Test Title"
        config.graph.x_axis.label = "X Axis"
        config.graph.x_axis.min = 0
        config.graph.x_axis.max = 100
        config.data.add_source("test.csv", "Test Data")
        config.output.format = "svg"
        config.output.save_path = "./test.svg"

        config_dict = config.to_dict()

        assert config_dict["graph"]["title"] == "Test Title"
        assert config_dict["graph"]["x_axis"]["label"] == "X Axis"
        assert config_dict["graph"]["x_axis"]["min"] == 0
        assert config_dict["graph"]["x_axis"]["max"] == 100
        assert len(config_dict["data"]["sources"]) == 1
        assert config_dict["data"]["sources"][0]["file"] == "test.csv"
        assert config_dict["data"]["sources"][0]["label"] == "Test Data"
        assert config_dict["output"]["format"] == "svg"
        assert config_dict["output"]["save_path"] == "./test.svg"

    def test_config_validation(self):
        """Test config validation."""
        config = Config()

        # Empty config should have validation errors
        errors = config.validate()
        assert len(errors) > 0
        assert "Graph title is required" in errors
        assert "At least one data source is required" in errors

        # Add required fields
        config.graph.title = "Test Graph"
        config.data.add_source("nonexistent.csv", "Test")

        errors = config.validate()
        assert "Graph title is required" not in errors
        assert "At least one data source is required" not in errors
        assert any("File 'nonexistent.csv' does not exist" in error for error in errors)

    def test_data_source_validation(self):
        """Test data source validation."""
        from simple_grapher.core import DataSource

        # Valid data source
        source = DataSource(file="test.csv", label="Test")
        assert source.file == "test.csv"
        assert source.label == "Test"

        # Data source with empty file should raise error
        with pytest.raises(ValueError, match="Data source 'file' is required"):
            DataSource(file="", label="Test")

        # Data source without label should use filename
        source = DataSource(file="test.csv")
        assert source.file == "test.csv"
        assert source.label == "test"  # filename without extension

    def test_output_config_validation(self):
        """Test output config validation."""
        from simple_grapher.core import OutputConfig

        # Valid output config
        output = OutputConfig(format="png")
        assert output.format == "png"
        assert output.dpi == 300
        assert output.save_path == "./output/graph.png"

        # Invalid format should raise error
        with pytest.raises(ValueError, match="Invalid format"):
            OutputConfig(format="invalid")

    def test_add_data_source(self):
        """Test adding data sources."""
        config = Config()

        # Add source with label
        config.data.add_source("file1.csv", "Label 1")
        assert len(config.data.sources) == 1
        assert config.data.sources[0].file == "file1.csv"
        assert config.data.sources[0].label == "Label 1"

        # Add source without label (should use filename)
        config.data.add_source("file2.csv")
        assert len(config.data.sources) == 2
        assert config.data.sources[1].file == "file2.csv"
        assert config.data.sources[1].label == "file2"

    def test_line_style_config_validation(self):
        """Test line style configuration validation."""
        from simple_grapher.core import LineStyleConfig

        # Valid line style config
        line_style = LineStyleConfig(
            markers=["o", "s", "^"],
            line_styles=["-", "--"],
            auto_cycle=True,
            line_width=2.5,
            marker_size=8.0,
        )
        assert line_style.markers == ["o", "s", "^"]
        assert line_style.line_styles == ["-", "--"]
        assert line_style.auto_cycle is True
        assert line_style.line_width == 2.5
        assert line_style.marker_size == 8.0

        # Invalid marker should raise error
        with pytest.raises(ValueError, match="Invalid marker"):
            LineStyleConfig(markers=["invalid_marker"])

        # Invalid line style should raise error
        with pytest.raises(ValueError, match="Invalid line style"):
            LineStyleConfig(line_styles=["invalid_style"])

        # Invalid line width should raise error
        with pytest.raises(ValueError, match="Line width must be positive"):
            LineStyleConfig(line_width=0)

        # Invalid marker size should raise error
        with pytest.raises(ValueError, match="Marker size must be positive"):
            LineStyleConfig(marker_size=-1)

    def test_config_with_line_styles(self):
        """Test config with line style options."""
        yaml_content = """
graph:
  title: "Test Graph with Line Styles"
  x_axis:
    label: "X Label"
  y_axis:
    label: "Y Label"
  style:
    line_style:
      markers: ['o', 's', '^']
      line_styles: ['-', '--', '-.']
      auto_cycle: false
      line_width: 3.0
      marker_size: 10.0

data:
  sources:
    - file: "test.csv"
      label: "Test"

output:
  format: "png"
  save_path: "./test.png"
"""

        config = Config.from_yaml_string(yaml_content)

        assert config.graph.style.line_style.markers == ["o", "s", "^"]
        assert config.graph.style.line_style.line_styles == ["-", "--", "-."]
        assert config.graph.style.line_style.auto_cycle is False
        assert config.graph.style.line_style.line_width == 3.0
        assert config.graph.style.line_style.marker_size == 10.0

    def test_config_to_dict_with_line_styles(self):
        """Test converting config with line styles to dictionary."""
        config = Config()
        config.graph.title = "Test Title"
        config.graph.style.line_style.markers = ["D", "h", "p"]
        config.graph.style.line_style.line_styles = ["--", "-.", ":"]
        config.graph.style.line_style.auto_cycle = False
        config.graph.style.line_style.line_width = 2.5
        config.graph.style.line_style.marker_size = 8.0

        config_dict = config.to_dict()

        assert config_dict["graph"]["style"]["line_style"]["markers"] == ["D", "h", "p"]
        assert config_dict["graph"]["style"]["line_style"]["line_styles"] == [
            "--",
            "-.",
            ":",
        ]
        assert config_dict["graph"]["style"]["line_style"]["auto_cycle"] is False
        assert config_dict["graph"]["style"]["line_style"]["line_width"] == 2.5
        assert config_dict["graph"]["style"]["line_style"]["marker_size"] == 8.0
