#!/bin/zsh

if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed. Please install Python and pip before running this script."
    exit 1
fi

echo "Installing Python packages..."
pip install -r requirements.txt

echo "All Python packages have been installed successfully."

