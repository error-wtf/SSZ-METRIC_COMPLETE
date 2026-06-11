#!/bin/bash
# SSZ Metric Complete - Test Runner Script
# Version: 2.2.0-canonical

set -e

echo "=========================================="
echo "SSZ Metric Complete - Running All Tests"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run install.sh first."
    exit 1
fi

# Activate virtual environment
echo "[1/3] Activating virtual environment..."
source .venv/bin/activate

# Run tests with coverage
echo "[2/3] Running tests with coverage..."
pytest tests/ -v --cov=src --cov-report=html --cov-report=term

# Generate test report
echo "[3/3] Generating test report..."
python -m pytest tests/ -v --tb=short > test_report.txt 2>&1 || true

echo ""
echo "=========================================="
echo "Test Run Complete!"
echo "=========================================="
echo ""
echo "Coverage report: htmlcov/index.html"
echo "Test report: test_report.txt"
echo ""
