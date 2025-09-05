"""
YAML parsing utilities for Simple Grapher.

This module provides utilities for parsing YAML configuration files
and data files for graph creation.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml


class YAMLParser:
    """Handles YAML file parsing and validation."""

    def __init__(self) -> None:
        """Initialize the YAML parser."""
        self.data: Optional[Dict[str, Any]] = None

    def load_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load and parse a YAML file.

        Args:
            file_path: Path to the YAML file

        Returns:
            Parsed YAML data as a dictionary

        Raises:
            FileNotFoundError: If the file doesn't exist
            yaml.YAMLError: If the YAML is malformed
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                if not isinstance(data, dict):
                    raise yaml.YAMLError(
                        f"YAML file {file_path} does not contain a dictionary"
                    )
                self.data = data
                return self.data
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file {file_path}: {e}")

    def load_string(self, yaml_string: str) -> Dict[str, Any]:
        """
        Load and parse a YAML string.

        Args:
            yaml_string: YAML content as a string

        Returns:
            Parsed YAML data as a dictionary

        Raises:
            yaml.YAMLError: If the YAML is malformed
        """
        try:
            data = yaml.safe_load(yaml_string)
            if not isinstance(data, dict):
                raise yaml.YAMLError("YAML string does not contain a dictionary")
            self.data = data
            return self.data
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML string: {e}")

    def save_file(self, data: Dict[str, Any], file_path: Union[str, Path]) -> None:
        """
        Save data to a YAML file.

        Args:
            data: Data to save
            file_path: Path where to save the YAML file
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False, indent=2)

    def get_value(self, key_path: str, default: Any = None) -> Any:
        """
        Get a value from the loaded data using dot notation.

        Args:
            key_path: Dot-separated path to the value (e.g., 'config.graph.title')
            default: Default value if key not found

        Returns:
            The value at the specified path or default
        """
        if self.data is None:
            return default

        keys = key_path.split(".")
        value = self.data

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def validate_schema(self, required_keys: List[str]) -> bool:
        """
        Validate that the loaded data contains required keys.

        Args:
            required_keys: List of required key paths

        Returns:
            True if all required keys are present, False otherwise
        """
        if self.data is None:
            return False

        for key_path in required_keys:
            if self.get_value(key_path) is None:
                return False

        return True


def parse_config_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Convenience function to parse a YAML config file.

    Args:
        file_path: Path to the YAML config file

    Returns:
        Parsed configuration data
    """
    parser = YAMLParser()
    return parser.load_file(file_path)


def parse_data_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Convenience function to parse a YAML data file.

    Args:
        file_path: Path to the YAML data file

    Returns:
        Parsed data
    """
    parser = YAMLParser()
    return parser.load_file(file_path)
