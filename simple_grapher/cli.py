"""
Command line interface for Simple Grapher.
"""

import argparse
import sys
from typing import Any, Dict

from simple_grapher.core.data_processor import DataProcessor
from simple_grapher.core.graph_builder import GraphBuilder
from simple_grapher.utils.yaml_parser import YAMLParser


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="simple-grapher",
        description="A simple command line tool for creating graphs and visualizations",
    )

    # Arguments
    parser.add_argument("--input", action="store", required=True)

    return parser


def process_input(input: str) -> Dict[str, Any]:
    """Open the YAML file and parse the data."""
    yaml_parser = YAMLParser()
    return yaml_parser.load_file(input)


def create_graph_config(data: Any) -> Any:
    """Create the graph configuration."""
    return data


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args: argparse.Namespace = parser.parse_args()

    try:
        # Process the input configuration
        config = process_input(args.input)

        print(f"Simple Grapher CLI - Processing configuration from {args.input}")
        print(f"Found {len(config.get('data', {}).get('sources', []))} data sources")

        # Create data processor and graph builder
        data_processor = DataProcessor()
        graph_builder = GraphBuilder()

        # Create the graph from configuration
        figure = graph_builder.create_graph_from_config(config, data_processor)

        if figure is None:
            print("Error: Failed to create graph")
            return 1

        # Save the graph
        output_config = config.get("output", {})
        output_path = output_config.get("save_path", "./output/graph.png")
        dpi = output_config.get("dpi", 300)

        success = graph_builder.save_graph(figure, output_path, dpi=dpi)

        if success:
            print(f"Graph successfully created and saved to {output_path}")
        else:
            print("Error: Failed to save graph")
            return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
