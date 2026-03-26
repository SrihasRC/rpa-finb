#!/bin/bash

# Quick Start Script for Financial Compliance Monitoring System

echo "======================================================================"
echo "RPA-Based Financial Compliance Monitoring System - Quick Start"
echo "======================================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "Found: $python_version"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Run the complete pipeline
echo "======================================================================"
echo "Running Complete Pipeline"
echo "======================================================================"
echo ""

python3 run_pipeline.py

echo ""
echo "======================================================================"
echo "Setup Complete!"
echo "======================================================================"
echo ""
echo "Generated Files:"
echo "  ✓ data/transactions.csv"
echo "  ✓ models/model.pkl"
echo "  ✓ outputs/compliance_report.csv"
echo "  ✓ outputs/flagged_transactions.csv"
echo ""
echo "Next Steps:"
echo "  1. Start API server: python3 api/main.py"
echo "  2. Open browser: http://localhost:8000/docs"
echo "  3. Review README.md for UiPath integration"
echo ""
echo "======================================================================"
