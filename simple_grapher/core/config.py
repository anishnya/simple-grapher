"""
Configuration management for Simple Grapher.

This module provides dataclasses and utilities for managing configuration
that matches the structure of YAML configuration files.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..utils.yaml_parser import YAMLParser


@dataclass
class FontsConfig:
    """Configuration for font settings."""

    title_size: int = 16
    label_size: int = 12
    legend_size: int = 10


@dataclass
class GridConfig:
    """Configuration for grid settings."""

    show: bool = True


@dataclass
class LineStyleConfig:
    """Configuration for line and marker styling."""

    # Available markers: 'o', 's', '^', 'v', '<', '>', 'p', '*', '+', 'x', 'D', 'h', 'H', '1', '2', '3', '4', '|', '_', '.', ','
    # Default to no markers (empty list means no markers)
    markers: List[str] = field(default_factory=lambda: [])
    # Available line styles: '-', '--', '-.', ':'
    # Default to solid lines only
    line_styles: List[str] = field(default_factory=lambda: ["-"])
    # Whether to cycle through markers and line styles automatically
    auto_cycle: bool = True
    # Line width
    line_width: float = 2.0
    # Marker size
    marker_size: float = 6.0

    def __post_init__(self) -> None:
        """Validate marker and line style configuration after initialization."""
        # Validate markers
        valid_markers = [
            "o",
            "s",
            "^",
            "v",
            "<",
            ">",
            "p",
            "*",
            "+",
            "x",
            "D",
            "h",
            "H",
            "1",
            "2",
            "3",
            "4",
            "|",
            "_",
            ".",
            ",",
        ]
        for marker in self.markers:
            if marker not in valid_markers:
                raise ValueError(
                    f"Invalid marker '{marker}'. Valid markers: {valid_markers}"
                )

        # Validate line styles
        valid_line_styles = ["-", "--", "-.", ":"]
        for line_style in self.line_styles:
            if line_style not in valid_line_styles:
                raise ValueError(
                    f"Invalid line style '{line_style}'. Valid line styles: {valid_line_styles}"
                )

        # Validate numeric values
        if self.line_width <= 0:
            raise ValueError("Line width must be positive")
        if self.marker_size <= 0:
            raise ValueError("Marker size must be positive")


@dataclass
class StyleConfig:
    """Configuration for graph styling."""

    width: int = 10
    height: int = 10
    fonts: FontsConfig = field(default_factory=FontsConfig)
    grid: GridConfig = field(default_factory=GridConfig)
    line_style: LineStyleConfig = field(default_factory=LineStyleConfig)


@dataclass
class AxisConfig:
    """Configuration for axis settings."""

    label: str = ""
    min: Optional[float] = None
    max: Optional[float] = None


@dataclass
class GraphConfig:
    """Configuration for graph settings."""

    title: str = ""
    x_axis: AxisConfig = field(default_factory=AxisConfig)
    y_axis: AxisConfig = field(default_factory=AxisConfig)
    style: StyleConfig = field(default_factory=StyleConfig)


@dataclass
class DataSource:
    """Configuration for a single data source."""

    file: str = ""
    label: str = ""

    def __post_init__(self) -> None:
        """Validate the data source after initialization."""
        if not self.file:
            raise ValueError("Data source 'file' is required")
        if not self.label:
            self.label = Path(self.file).stem


@dataclass
class DataConfig:
    """Configuration for data sources."""

    sources: List[DataSource] = field(default_factory=list)

    def add_source(self, file: str, label: Optional[str] = None) -> None:
        """Add a new data source."""
        if label is None:
            label = Path(file).stem
        self.sources.append(DataSource(file=file, label=label))


@dataclass
class OutputConfig:
    """Configuration for output settings."""

    format: str = "png"
    dpi: int = 300
    save_path: str = "./output/graph.png"

    def __post_init__(self) -> None:
        """Validate output configuration after initialization."""
        valid_formats = ["png", "jpg", "jpeg", "svg", "pdf"]
        if self.format.lower() not in valid_formats:
            raise ValueError(
                f"Invalid format '{self.format}'. Must be one of: {valid_formats}"
            )


@dataclass
class Config:
    """Main configuration class that matches the YAML structure."""

    graph: GraphConfig = field(default_factory=GraphConfig)
    data: DataConfig = field(default_factory=DataConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    @classmethod
    def from_yaml_file(cls, file_path: Union[str, Path]) -> "Config":
        """
        Create a Config instance from a YAML file.

        Args:
            file_path: Path to the YAML configuration file

        Returns:
            Config instance loaded from the YAML file

        Raises:
            FileNotFoundError: If the file doesn't exist
            yaml.YAMLError: If the YAML is malformed
            ValueError: If the configuration is invalid
        """
        parser = YAMLParser()
        data = parser.load_file(file_path)
        return cls.from_dict(data)

    @classmethod
    def from_yaml_string(cls, yaml_string: str) -> "Config":
        """
        Create a Config instance from a YAML string.

        Args:
            yaml_string: YAML content as a string

        Returns:
            Config instance loaded from the YAML string

        Raises:
            yaml.YAMLError: If the YAML is malformed
            ValueError: If the configuration is invalid
        """
        parser = YAMLParser()
        data = parser.load_string(yaml_string)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """
        Create a Config instance from a dictionary.

        Args:
            data: Dictionary containing configuration data

        Returns:
            Config instance created from the dictionary

        Raises:
            ValueError: If the configuration is invalid
        """
        # Extract graph configuration
        graph_data = data.get("graph", {})
        graph_config = GraphConfig(
            title=graph_data.get("title", ""),
            x_axis=AxisConfig(
                label=graph_data.get("x_axis", {}).get("label", ""),
                min=graph_data.get("x_axis", {}).get("min"),
                max=graph_data.get("x_axis", {}).get("max"),
            ),
            y_axis=AxisConfig(
                label=graph_data.get("y_axis", {}).get("label", ""),
                min=graph_data.get("y_axis", {}).get("min"),
                max=graph_data.get("y_axis", {}).get("max"),
            ),
            style=StyleConfig(
                width=graph_data.get("style", {}).get("width", 10),
                height=graph_data.get("style", {}).get("height", 10),
                fonts=FontsConfig(
                    title_size=graph_data.get("style", {})
                    .get("fonts", {})
                    .get("title_size", 16),
                    label_size=graph_data.get("style", {})
                    .get("fonts", {})
                    .get("label_size", 12),
                    legend_size=graph_data.get("style", {})
                    .get("fonts", {})
                    .get("legend_size", 10),
                ),
                grid=GridConfig(
                    show=graph_data.get("style", {}).get("grid", {}).get("show", True),
                ),
                line_style=LineStyleConfig(
                    markers=graph_data.get("style", {})
                    .get("line_style", {})
                    .get(
                        "markers",
                        ["o", "s", "^", "v", "<", ">", "p", "*", "+", "x", "D", "h"],
                    ),
                    line_styles=graph_data.get("style", {})
                    .get("line_style", {})
                    .get("line_styles", ["-", "--", "-.", ":"]),
                    auto_cycle=graph_data.get("style", {})
                    .get("line_style", {})
                    .get("auto_cycle", True),
                    line_width=graph_data.get("style", {})
                    .get("line_style", {})
                    .get("line_width", 2.0),
                    marker_size=graph_data.get("style", {})
                    .get("line_style", {})
                    .get("marker_size", 6.0),
                ),
            ),
        )

        # Extract data configuration
        data_config = DataConfig()
        data_sources = data.get("data", {}).get("sources", [])
        for source_data in data_sources:
            data_config.add_source(
                file=source_data.get("file", ""),
                label=source_data.get("label"),
            )

        # Extract output configuration
        output_data = data.get("output", {})
        output_config = OutputConfig(
            format=output_data.get("format", "png"),
            dpi=output_data.get("dpi", 300),
            save_path=output_data.get("save_path", "./output/graph.png"),
        )

        return cls(
            graph=graph_config,
            data=data_config,
            output=output_config,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Config instance to a dictionary.

        Returns:
            Dictionary representation of the configuration
        """
        return {
            "graph": {
                "title": self.graph.title,
                "x_axis": {
                    "label": self.graph.x_axis.label,
                    "min": self.graph.x_axis.min,
                    "max": self.graph.x_axis.max,
                },
                "y_axis": {
                    "label": self.graph.y_axis.label,
                    "min": self.graph.y_axis.min,
                    "max": self.graph.y_axis.max,
                },
                "style": {
                    "width": self.graph.style.width,
                    "height": self.graph.style.height,
                    "fonts": {
                        "title_size": self.graph.style.fonts.title_size,
                        "label_size": self.graph.style.fonts.label_size,
                        "legend_size": self.graph.style.fonts.legend_size,
                    },
                    "grid": {
                        "show": self.graph.style.grid.show,
                    },
                    "line_style": {
                        "markers": self.graph.style.line_style.markers,
                        "line_styles": self.graph.style.line_style.line_styles,
                        "auto_cycle": self.graph.style.line_style.auto_cycle,
                        "line_width": self.graph.style.line_style.line_width,
                        "marker_size": self.graph.style.line_style.marker_size,
                    },
                },
            },
            "data": {
                "sources": [
                    {"file": source.file, "label": source.label}
                    for source in self.data.sources
                ]
            },
            "output": {
                "format": self.output.format,
                "dpi": self.output.dpi,
                "save_path": self.output.save_path,
            },
        }

    def validate(self) -> List[str]:
        """
        Validate the configuration and return any errors.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Validate graph configuration
        if not self.graph.title:
            errors.append("Graph title is required")

        # Validate data sources
        if not self.data.sources:
            errors.append("At least one data source is required")

        for i, source in enumerate(self.data.sources):
            if not Path(source.file).exists():
                errors.append(f"Data source {i}: File '{source.file}' does not exist")

        # Validate output path
        output_path = Path(self.output.save_path)
        if not output_path.parent.exists():
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                errors.append(f"Cannot create output directory: {e}")

        return errors

    def is_valid(self) -> bool:
        """
        Check if the configuration is valid.

        Returns:
            True if valid, False otherwise
        """
        return len(self.validate()) == 0
