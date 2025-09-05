#!/bin/bash
# Installation script for Simple Grapher

set -e

echo "Installing Simple Grapher..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIMPLE_GRAPHER_SCRIPT="$SCRIPT_DIR/simple-grapher"

# Check if the script exists
if [ ! -f "$SIMPLE_GRAPHER_SCRIPT" ]; then
    echo "Error: simple-grapher script not found in $SCRIPT_DIR"
    exit 1
fi

# Make sure the script is executable
chmod +x "$SIMPLE_GRAPHER_SCRIPT"

# Create a symlink in /usr/local/bin (requires sudo)
echo "Creating symlink in /usr/local/bin..."
if sudo ln -sf "$SIMPLE_GRAPHER_SCRIPT" /usr/local/bin/simple-grapher; then
    echo "Simple Grapher installed successfully!"
    echo "You can now run 'simple-grapher' from anywhere in your terminal."
    echo ""
    echo "Try it out:"
    echo "  simple-grapher --help"
    echo "  simple-grapher --version"
else
    echo "Failed to create symlink. You may need to run with sudo or install manually."
    echo ""
    echo "Manual installation:"
    echo "1. Add this directory to your PATH:"
    echo "   export PATH=\"$SCRIPT_DIR:\$PATH\""
    echo "2. Add the above line to your ~/.zshrc or ~/.bash_profile"
    echo "3. Restart your terminal or run: source ~/.zshrc"
fi
