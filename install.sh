#!/bin/bash
# Canonical Pure SSZ Metric - Installation Script
# © 2025 Carmen Wrede & Lino Casu
# Licensed under the Anti-Capitalist Software License v1.4

set -euo pipefail

# Print header
echo "================================================================"
echo "Canonical Pure SSZ Metric Installer"
echo "v1.1.0-canonical-pure - Research Framework"
echo "================================================================"

# Initialize flags
DEV_MODE=false
TEST_MODE=false

for arg in "$@"; do
    case "$arg" in
        --dev)
            DEV_MODE=true
            ;;
        --test)
            TEST_MODE=true
            ;;
    esac
done

# Detect Python interpreter
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python not found."
    echo "INSTALL: FAILED"
    exit 1
fi

# Check Python version >= 3.9
PYTHON_VERSION_OK=$($PYTHON_CMD -c "import sys; print(1 if sys.version_info >= (3, 9) else 0)")
if [ "$PYTHON_VERSION_OK" != "1" ]; then
    echo "ERROR: Python >= 3.9 is required."
    echo "INSTALL: FAILED"
    exit 1
fi

echo "Using Python: $($PYTHON_CMD --version)"

# Upgrade pip and install package
echo "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip --quiet

if [ "$DEV_MODE" = true ]; then
    echo "Installing package in editable developer mode with dev/viz dependencies..."
    $PYTHON_CMD -m pip install -e ".[dev,viz]"
else
    echo "Installing package in editable production mode..."
    $PYTHON_CMD -m pip install -e .
fi

if [ "$TEST_MODE" = true ]; then
    echo "Running pytest..."
    if $PYTHON_CMD -m pytest -q; then
        echo "Tests passed!"
    else
        echo "ERROR: Tests failed."
        echo "INSTALL: FAILED"
        exit 1
    fi
fi

echo "================================================================"
echo "INSTALL: PASS"
echo "================================================================"
