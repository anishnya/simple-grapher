"""
Data processing module for Simple Grapher.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd


class DataProcessor:
    """Handles data loading and processing for graph creation."""

    def __init__(self) -> None:
        """Initialize the data processor."""
        pass

    def load_csv(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        Load a CSV file and return a pandas DataFrame with x,y pairs.
        Uses the first two columns as x,y pairs regardless of column names.

        Args:
            file_path: Path to the CSV file

        Returns:
            pandas DataFrame with x,y columns (renamed to 'x' and 'y') or None if loading fails
        """
        try:
            # Load the CSV file
            df = pd.read_csv(file_path)

            # Check if we have at least 2 columns
            if len(df.columns) < 2:
                raise ValueError(
                    f"CSV file must have at least 2 columns, found {len(df.columns)}"
                )

            # Use the first two columns as x,y pairs
            x_column = df.columns[0]
            y_column = df.columns[1]

            # Create a new DataFrame with just the first two columns, renamed to 'x' and 'y'
            result_df = pd.DataFrame({"x": df[x_column], "y": df[y_column]})

            return result_df

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            return None
        except pd.errors.EmptyDataError:
            print(f"Error: File '{file_path}' is empty")
            return None
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file '{file_path}': {e}")
            return None
        except Exception as e:
            print(f"Error loading CSV file '{file_path}': {e}")
            return None

    def load_multiple_csvs(
        self, sources: List[Dict[str, Any]]
    ) -> Dict[str, pd.DataFrame]:
        """
        Load multiple CSV files and return a dictionary of DataFrames.
        Uses the first two columns of each CSV as x,y pairs.

        Args:
            sources: List of source dictionaries with 'file' and 'label'

        Returns:
            Dictionary mapping labels to DataFrames
        """
        dataframes: Dict[str, pd.DataFrame] = {}

        for source in sources:
            file_path = source.get("file")
            label = source.get("label", file_path)

            if file_path:
                df = self.load_csv(file_path)
                if df is not None:
                    dataframes[label] = df
                else:
                    print(f"Warning: Failed to load {file_path}")

        return dataframes

    def process_data(
        self, data_source: Union[str, Dict[str, Any], List[Dict[str, Any]]]
    ) -> Optional[Union[pd.DataFrame, Dict[str, pd.DataFrame]]]:
        """
        Process data from various sources.
        Uses the first two columns of CSV files as x,y pairs.

        Args:
            data_source: Data source as string path, dictionary, or list of source dictionaries

        Returns:
            pandas DataFrame (single source) or dict of DataFrames (multiple sources) or None if processing fails
        """
        if isinstance(data_source, str):
            # Single file path
            return self.load_csv(data_source)
        elif isinstance(data_source, dict):
            if "file" in data_source:
                # Single source dictionary
                file_path = data_source.get("file")
                if file_path is not None:
                    return self.load_csv(file_path)
                else:
                    return None
            else:
                # Legacy format - return None for now
                return None
        elif isinstance(data_source, list):
            # List of sources
            return self.load_multiple_csvs(data_source)
        else:
            return None

    def validate_sources(self, sources: List[Dict[str, Any]]) -> List[str]:
        """
        Validate a list of data sources.

        Args:
            sources: List of source dictionaries to validate

        Returns:
            List of validation error messages (empty if all valid)
        """
        errors = []

        for i, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"Source {i} is not a dictionary")
                continue

            if "file" not in source:
                errors.append(f"Source {i} missing required 'file' field")
                continue

            if "label" not in source:
                errors.append(f"Source {i} missing required 'label' field")

            # Check if file exists
            file_path = Path(source["file"])
            if not file_path.exists():
                errors.append(f"Source {i} file '{source['file']}' not found")

        return errors
