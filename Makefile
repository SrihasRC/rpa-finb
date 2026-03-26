.PHONY: help install test dataset model reports pipeline api clean all

help:
	@echo "RPA-Based Financial Compliance Monitoring System"
	@echo ""
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make test      - Run installation tests"
	@echo "  make dataset   - Generate synthetic dataset"
	@echo "  make model     - Train ML model"
	@echo "  make reports   - Generate compliance reports"
	@echo "  make pipeline  - Run complete pipeline"
	@echo "  make api       - Start API server"
	@echo "  make clean     - Remove generated files"
	@echo "  make all       - Run everything (pipeline + api)"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

test:
	@echo "Running installation tests..."
	python test_installation.py

dataset:
	@echo "Generating synthetic dataset..."
	python data/generate_dataset.py

model:
	@echo "Training ML model..."
	python models/train_model.py

reports:
	@echo "Generating compliance reports..."
	python outputs/generate_reports.py

pipeline:
	@echo "Running complete pipeline..."
	python run_pipeline.py

api:
	@echo "Starting API server..."
	@echo "Server will run at http://localhost:8000"
	@echo "API docs at http://localhost:8000/docs"
	python api/main.py

clean:
	@echo "Cleaning generated files..."
	rm -f data/transactions.csv
	rm -f models/model.pkl
	rm -f outputs/compliance_report.csv
	rm -f outputs/flagged_transactions.csv
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete"

all: pipeline
	@echo ""
	@echo "Pipeline complete! Starting API server..."
	@echo ""
	python api/main.py
