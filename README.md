# Multilingual VLM Benchmark

## Project Overview
This repository provides a comprehensive pipeline for evaluating Vision-Language Models (VLMs) on multilingual OCR and visual understanding tasks. It acts as an orchestrator to retrieve images, run model inference across various endpoints (GPT-4V, Gemini, InternVL, Pixtral, Qwen, etc.), and rigorously evaluate text extraction and reasoning capabilities.

## Repository Structure
- `docs/`: Core documentation (`ARCHITECTURE.md`, `CONFIGURATION.md`, `DATASETS.md`, `EVALUATION.md`, `EXAMPLES.md`, `INSTALLATION.md`, `MODELS.md`, `PIPELINE.md`, `PROJECT_STRUCTURE.md`, `TROUBLESHOOTING.md`)
- `project/`: Core orchestration, configuration, and data loader implementations.
- `tools/`: Utility scripts for data ingestion, downloading, duplicate checking, and candidate validation.
- `models/`: Interface adapters connecting to external model APIs and local weights.
- `evaluation/`: The automated scoring and metric computation engines.
- `tests/`: Automated unit tests covering pipeline execution and integrations.
- `examples/`: Showcase scenarios featuring real-world images and expected output pairs.
- `outputs/`: Prediction artifacts and scoring summaries generated during evaluation runs.

## Installation
Detailed installation instructions can be found in [docs/INSTALLATION.md](docs/installation.md).

## Usage
The main entry point for the benchmark is `project/main.py`. Ensure your environment variables (like `OPENAI_API_KEY`) are set according to [docs/CONFIGURATION.md](docs/configuration.md).

## Benchmark Scope
For an in-depth look at our datasets, supported models, and pipeline architecture, please review:
- [Datasets Guide](docs/datasets.md)
- [Models Guide](docs/models.md)
- [Pipeline Architecture](docs/pipeline.md)
- [Evaluation Metrics](docs/evaluation.md)

## Reproducibility & Citation
All benchmark configurations are deterministic. To reproduce findings, simply run the pipeline on the specified dataset subsets. Please see [CITATION.cff](CITATION.cff) when referencing this repository in academic work.
