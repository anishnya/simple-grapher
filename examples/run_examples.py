#!/usr/bin/env python3
"""
Script to run all example configurations.

This script demonstrates how to use the various YAML configuration files
to create different types of graphs with different styling approaches.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Add the parent directory to the path so we can import simple_grapher
sys.path.insert(0, str(Path(__file__).parent.parent))

from simple_grapher import Config, DataProcessor, GraphBuilder


def create_sample_data():
    """Create sample data for demonstration."""
    x = np.linspace(0, 10, 50)

    data = {
        "x": x,
        "y1": np.sin(x),
        "y2": np.cos(x),
        "y3": np.sin(x + np.pi / 4),
        "y4": np.cos(x + np.pi / 4),
        "y5": np.sin(x + np.pi / 2),
        "y6": np.cos(x + np.pi / 2),
    }

    df = pd.DataFrame(data)
    return df


def create_dataframes_from_config(config):
    """Create dataframes directly from configuration without CSV files."""
    df = create_sample_data()
    dataframes = {}

    for source in config.data.sources:
        # Generate random data for each series
        series_num = len(dataframes) + 1
        if series_num <= 6:
            # Use predefined patterns for first 6 series
            y_data = df[f"y{series_num}"].values
        else:
            # Generate random data for additional series
            x = np.linspace(0, 10, 50)
            y_data = np.sin(x + series_num * np.pi / 6) + np.random.normal(
                0, 0.1, len(x)
            )

        # Create dataframe with x, y columns
        series_df = pd.DataFrame({"x": df["x"], "y": y_data})

        dataframes[source.label] = series_df

    return dataframes


def run_config_example(config_file, description):
    """Run a single configuration example."""
    print(f"\n=== {description} ===")
    print(f"Using config: {config_file}")

    try:
        # Load configuration
        config = Config.from_yaml_file(config_file)
        print(f"✓ Loaded config: '{config.graph.title}'")

        # Create graph builder
        graph_builder = GraphBuilder()

        # Generate data directly from config
        dataframes = create_dataframes_from_config(config)

        if not dataframes:
            print("⚠️  No data loaded - skipping graph creation")
            return

        # Create graph
        fig = graph_builder.create_graph_from_dataframes(
            dataframes,
            "line",  # Default to line plot
            config.graph.title,
            config.graph.x_axis.label,
            config.graph.y_axis.label,
            config.graph.style,
        )

        if fig:
            # Save graph
            graph_builder.save_graph(
                fig,
                config.output.save_path,
                dpi=config.output.dpi,
                format=config.output.format,
            )
            print(f"✓ Graph saved to: {config.output.save_path}")
        else:
            print("✗ Failed to create graph")

    except Exception as e:
        print(f"✗ Error: {e}")


def run_scatter_example(config_file, description):
    """Run a scatter plot configuration example."""
    print(f"\n=== {description} ===")
    print(f"Using config: {config_file}")

    try:
        # Load configuration
        config = Config.from_yaml_file(config_file)
        print(f"✓ Loaded config: '{config.graph.title}'")

        # Create graph builder
        graph_builder = GraphBuilder()

        # Generate data directly from config
        dataframes = create_dataframes_from_config(config)

        if not dataframes:
            print("⚠️  No data loaded - skipping graph creation")
            return

        # Create scatter plot
        fig = graph_builder.create_graph_from_dataframes(
            dataframes,
            "scatter",  # Scatter plot
            config.graph.title,
            config.graph.x_axis.label,
            config.graph.y_axis.label,
            config.graph.style,
        )

        if fig:
            # Save graph
            graph_builder.save_graph(
                fig,
                config.output.save_path,
                dpi=config.output.dpi,
                format=config.output.format,
            )
            print(f"✓ Scatter plot saved to: {config.output.save_path}")
        else:
            print("✗ Failed to create scatter plot")

    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Main function to run all examples."""
    print("=== YAML Configuration Examples ===\n")

    # Ensure output directory exists
    Path("output").mkdir(exist_ok=True)

    # Define examples to run
    examples = [
        ("default_styling.yaml", "Default Styling - Clean Solid Lines"),
        ("minimal_yaml.yaml", "Minimal Configuration"),
        ("auto_cycling_demo.yaml", "Auto Cycling Demo"),
        ("manual_styling_demo.yaml", "Manual Styling Demo"),
    ]

    scatter_examples = [
        ("scatter_markers_demo.yaml", "Scatter Plot with Markers"),
        ("scatter_defaults.yaml", "Scatter Plot Defaults"),
    ]

    # Run line plot examples
    for config_file, description in examples:
        run_config_example(config_file, description)

    # Run scatter plot examples
    for config_file, description in scatter_examples:
        run_scatter_example(config_file, description)

    print("\n=== Summary ===")
    print("✓ All configuration examples completed!")
    print("✓ Check the 'output' directory for generated graphs")
    print("✓ Data is generated randomly each time - no CSV files needed")
    print("\nAvailable configuration files:")
    for config_file, description in examples + scatter_examples:
        print(f"  - {config_file}: {description}")


if __name__ == "__main__":
    main()
