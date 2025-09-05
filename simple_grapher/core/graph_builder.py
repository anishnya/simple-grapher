"""
Graph building module for Simple Grapher.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure


class GraphBuilder:
    """Handles graph creation and customization."""

    def __init__(self) -> None:
        """Initialize the graph builder."""
        self.supported_types = ["line", "bar", "scatter"]
        self.fig: Optional[Figure] = None
        self.ax: Optional[Axes] = None

    def create_graph(
        self,
        data_sources: List[Dict[str, Any]],
        graph_type: str = "line",
        title: str = "Graph",
        x_label: str = "X",
        y_label: str = "Y",
        style_config: Optional[Any] = None,
    ) -> Optional[plt.Figure]:
        """
        Create a graph from a list of data sources.

        Args:
            data_sources: List of data source dictionaries with 'dataframe' and 'label' keys
            graph_type: Type of graph to create (line, bar, scatter)
            title: Graph title
            x_label: X-axis label
            y_label: Y-axis label
            style_config: StyleConfig object for styling options

        Returns:
            matplotlib Figure object or None if creation fails
        """
        if graph_type not in self.supported_types:
            print(
                f"Error: Unsupported graph type '{graph_type}'. Supported types: {self.supported_types}"
            )
            return None

        if not data_sources:
            print("Error: No data sources provided")
            return None

        try:
            # Create figure and axis
            figsize = (10, 6)
            if style_config:
                figsize = (style_config.width, style_config.height)
            self.fig, self.ax = plt.subplots(figsize=figsize)

            # Set up line style cycling if auto_cycle is enabled
            if (
                style_config
                and style_config.line_style.auto_cycle
                and graph_type == "line"
            ):
                from cycler import cycler

                markers = style_config.line_style.markers
                line_styles = style_config.line_style.line_styles

                # If no markers specified, just cycle through line styles
                if not markers:
                    # Just cycle through line styles with no markers
                    custom_cycler = cycler(linestyle=line_styles)
                else:
                    # Create all combinations of markers and line styles
                    combined_styles = []
                    for marker in markers:
                        for line_style in line_styles:
                            combined_styles.append((marker, line_style))

                    # Create cycler with combined styles
                    custom_cycler = cycler(
                        marker=[style[0] for style in combined_styles],
                        linestyle=[style[1] for style in combined_styles],
                    )

                if self.ax is not None:
                    self.ax.set_prop_cycle(custom_cycler)

            # Plot each data source
            if self.ax is None:
                print("Error: No axis available for plotting")
                return

            for i, source in enumerate(data_sources):
                if "dataframe" not in source or "label" not in source:
                    print(
                        f"Warning: Skipping source missing 'dataframe' or 'label': {source}"
                    )
                    continue

                df = source["dataframe"]
                label = source["label"]

                if not isinstance(df, pd.DataFrame):
                    print(f"Warning: Skipping source with invalid dataframe: {label}")
                    continue

                if df.empty:
                    print(f"Warning: Skipping empty dataframe: {label}")
                    continue

                # Get x and y columns (assume first two columns are x,y)
                x_col = df.columns[0]
                y_col = df.columns[1]

                # Plot based on graph type
                if graph_type == "line":
                    # Use style configuration if available
                    if style_config and style_config.line_style.auto_cycle:
                        # Let cycler handle marker and line style
                        self.ax.plot(
                            df[x_col],
                            df[y_col],
                            label=label,
                            linewidth=style_config.line_style.line_width,
                            markersize=style_config.line_style.marker_size,
                        )
                    else:
                        # Manual selection of marker and line style
                        marker = None  # Default to no marker
                        linestyle = "-"
                        if style_config and style_config.line_style.markers:
                            marker = style_config.line_style.markers[
                                i % len(style_config.line_style.markers)
                            ]
                        if style_config and style_config.line_style.line_styles:
                            linestyle = style_config.line_style.line_styles[
                                i % len(style_config.line_style.line_styles)
                            ]

                        # Only add marker parameter if we have markers
                        plot_kwargs = {
                            "label": label,
                            "linestyle": linestyle,
                            "linewidth": (
                                style_config.line_style.line_width
                                if style_config
                                else 2
                            ),
                        }
                        if marker is not None:
                            plot_kwargs["marker"] = marker
                            plot_kwargs["markersize"] = (
                                style_config.line_style.marker_size
                                if style_config
                                else 6
                            )

                        self.ax.plot(df[x_col], df[y_col], **plot_kwargs)
                elif graph_type == "bar":
                    self.ax.bar(df[x_col], df[y_col], label=label, alpha=0.7)
                elif graph_type == "scatter":
                    # Use marker from style config if available
                    marker = "o"  # Default marker for scatter plots
                    if style_config and style_config.line_style.markers:
                        marker = style_config.line_style.markers[
                            i % len(style_config.line_style.markers)
                        ]
                    elif style_config and not style_config.line_style.markers:
                        # If no markers specified, use default circle
                        marker = "o"
                    self.ax.scatter(
                        df[x_col],
                        df[y_col],
                        label=label,
                        alpha=0.7,
                        marker=marker,
                        s=(
                            style_config.line_style.marker_size**2
                            if style_config
                            else 36
                        ),
                    )

            # Customize the plot
            self.ax.set_title(title, fontsize=16, fontweight="bold")
            self.ax.set_xlabel(x_label, fontsize=12)
            self.ax.set_ylabel(y_label, fontsize=12)
            self.ax.legend()
            self.ax.grid(True, alpha=0.3)

            # Adjust layout
            plt.tight_layout()

            return self.fig

        except Exception as e:
            print(f"Error creating graph: {e}")
            return None

    def create_graph_from_dataframes(
        self,
        dataframes: Dict[str, pd.DataFrame],
        graph_type: str = "line",
        title: str = "Graph",
        x_label: str = "X",
        y_label: str = "Y",
        style_config: Optional[Any] = None,
    ) -> Optional[plt.Figure]:
        """
        Create a graph from a dictionary of DataFrames.

        Args:
            dataframes: Dictionary mapping labels to DataFrames
            graph_type: Type of graph to create
            title: Graph title
            x_label: X-axis label
            y_label: Y-axis label
            style_config: StyleConfig object for styling options

        Returns:
            matplotlib Figure object or None if creation fails
        """
        # Convert dictionary to list format
        data_sources = []
        for label, df in dataframes.items():
            data_sources.append({"dataframe": df, "label": label})

        return self.create_graph(
            data_sources, graph_type, title, x_label, y_label, style_config
        )

    def create_graph_from_config(
        self, config: Dict[str, Any], data_processor: Any
    ) -> Optional[plt.Figure]:
        """
        Create a graph from a complete configuration dictionary.

        Args:
            config: Complete configuration including graph, data, and output settings
            data_processor: DataProcessor instance to load data

        Returns:
            matplotlib Figure object or None if creation fails
        """
        if not isinstance(config, dict):
            return None

        # Extract graph configuration
        graph_config = config.get("graph", {})
        graph_type = graph_config.get("type", "line")
        title = graph_config.get("title", "Graph")

        # Extract axis labels
        x_axis = graph_config.get("x_axis", {})
        y_axis = graph_config.get("y_axis", {})
        x_label = x_axis.get("label", "X")
        y_label = y_axis.get("label", "Y")

        # Extract style configuration
        style_config = graph_config.get("style", {})

        # Extract data sources
        data_config = config.get("data", {})
        sources = data_config.get("sources", [])

        if not sources:
            print("Error: No data sources found in configuration")
            return None

        # Load data from sources
        dataframes = data_processor.load_multiple_csvs(sources)

        if not dataframes:
            print("Error: Failed to load any data from sources")
            return None

        # Create the graph
        return self.create_graph_from_dataframes(
            dataframes, graph_type, title, x_label, y_label, style_config
        )

    def save_graph(
        self,
        figure: plt.Figure,
        output_path: Union[str, Path],
        dpi: int = 300,
        format: Optional[str] = None,
    ) -> bool:
        """
        Save the graph to a file.

        Args:
            figure: matplotlib Figure object to save
            output_path: Path where to save the graph
            dpi: DPI for the output image
            format: Output format (png, pdf, svg, etc.). If None, inferred from file extension

        Returns:
            True if successful, False otherwise
        """
        if figure is None:
            print("Error: No figure to save")
            return False

        output_path = Path(output_path)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Determine format from file extension if not specified
            if format is None:
                format = output_path.suffix[1:].lower()  # Remove the dot
                if not format:
                    format = "png"  # Default to PNG

            # Save the figure
            figure.savefig(output_path, dpi=dpi, format=format, bbox_inches="tight")
            print(f"Graph saved to: {output_path}")
            return True

        except Exception as e:
            print(f"Error saving graph: {e}")
            return False

    def get_supported_types(self) -> List[str]:
        """
        Get list of supported graph types.

        Returns:
            List of supported graph type strings
        """
        return self.supported_types.copy()

    def validate_graph_type(self, graph_type: str) -> bool:
        """
        Validate if a graph type is supported.

        Args:
            graph_type: Graph type to validate

        Returns:
            True if supported, False otherwise
        """
        return graph_type in self.supported_types
