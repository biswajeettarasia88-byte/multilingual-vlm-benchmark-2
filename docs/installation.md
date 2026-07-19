# Installation Guide

## Project Overview
The Multilingual VLM Benchmark is a research-grade framework designed to evaluate how well Vision Language Models (VLMs) comprehend visible text inside images (Task 2 - Text in Image). The pipeline extracts OCR text, classifies scripts, identifies languages, transliterates and translates regional texts, and generates Text-Aware Question Answering (QA) pairs.

## System Requirements
- **Operating Systems**: Windows 10/11, Ubuntu 20.04+, macOS 12+
- **Python Version**: Python 3.10, 3.11, or 3.12
- **Memory**: Minimum 16GB RAM (32GB recommended for large local models)
- **CUDA Requirements**: CUDA 11.8 or newer if running models locally on GPU.
- **GPU Recommendations**: 
  - Minimum: 8GB VRAM (for 4-bit quantization models like Qwen or InternVL)
  - Recommended: 24GB VRAM (RTX 3090 / 4090) for full precision inference

## Clone the Repository
Begin by cloning the benchmark repository from GitHub:
```bash
git clone https://github.com/organization/multilingual-vlm-benchmark.git
cd multilingual-vlm-benchmark
```

## Virtual Environment Setup
It is highly recommended to isolate dependencies using a virtual environment.

### Using Python `venv`
**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### Using Conda
```bash
conda env create -f environment.yml
conda activate vlm-benchmark
```

## Dependency Installation
Once activated, install the required PyPI packages:
```bash
pip install -r requirements.txt
```
If you intend to run local VLMs using HuggingFace Transformers on GPU, ensure you install the CUDA-optimized version of PyTorch according to the [official PyTorch instructions](https://pytorch.org/get-started/locally/).

## Verify Installation
You can verify the setup is functioning correctly by running the help command:
```bash
python -m project.main --help
```

### First Successful Run
To execute your first benchmarking pipeline on the sample configuration:
```bash
python -m project.main --config project/configs/config.yaml --max-images 2
```

## Expected Directory Structure
Upon cloning, your repository should match the following structure:
```
multilingual-vlm-benchmark/
├── .github/
├── docs/
├── examples/
├── project/
│   ├── configs/
│   ├── datasets/
│   ├── logs/
│   ├── models/
│   ├── outputs/
│   ├── prompts/
│   └── reports/
├── tests/
├── README.md
├── requirements.txt
└── environment.yml
```

## Common Installation Errors
- **`grpcio` hang during pip install**: The Pip dependency resolver can sometimes hang on Windows. Upgrading pip (`python -m pip install --upgrade pip`) or running `pip install grpcio --no-binary=grpcio` usually resolves this.
- **CUDA Out of Memory**: If installation succeeds but inference fails, edit `config.yaml` to enforce 4-bit quantization or reduce the batch size.

---
## Related Documentation
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Datasets](datasets.md)
- [Models](models.md)
- [Pipeline](pipeline.md)
- [Examples](examples.md)
- [Troubleshooting](troubleshooting.md)
