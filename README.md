<div align="center">
  <h1>🌍 Benchmark Task 2 (Text in Image)</h1>
  <p>
    <b>A production-ready pipeline for multilingual Vision-Language Model benchmarking and automated dataset generation.</b>
  </p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![Code Style: PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
</div>

---

## 📑 Table of Contents
1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Repository Structure](#-repository-structure)
4. [Pipeline Architecture](#-pipeline-architecture)
5. [Installation](#-installation)
6. [Quick Start](#-quick-start)
7. [Configuration](#-configuration)
8. [Example Images](#-example-images)
9. [Example Output](#-example-output)
10. [Documentation](#-documentation)
11. [License](#-license)

---

## 📖 Project Overview

Vision-Language Models (VLMs) have demonstrated incredible capabilities in zero-shot image understanding, but evaluating their ability to process complex multilingual text directly from images remains a significant challenge.

**This repository provides a fully automated framework to benchmark VLMs strictly on Benchmark Task 2 (Text in Image).** 

The primary objective of this pipeline is to ingest raw image metadata and rigorously evaluate how well state-of-the-art models (like GPT-4o, Gemini, Qwen, and InternVL) can perform Optical Character Recognition (OCR), detect native scripts, identify languages, generate transliterations and translations, and formulate text-aware comprehension questions. By removing generic scene-understanding, this repository provides a highly specialized diagnostic tool for multilingual text-in-image performance.

---

## ✨ Features

- **Task 2 Enforcement**: Generates questions *only* about extracted text (e.g., "Which department issued the notice?") and strictly rejects generic visual queries.
- **Extensive Model Support**: Benchmark both lightweight local Hugging Face VLMs and high-performance cloud APIs natively.
- **Automated Dataset Caching**: Missing image URLs are automatically downloaded, verified, and cached locally.
- **Resilient Orchestration**: Features stateful checkpointing, Out-Of-Memory (OOM) recovery, and PyTorch CUDA garbage collection.
- **End-to-End Evaluation**: Automatically tracks OCR extraction success, script detection, language detection, translation quality, and JSON validity.

---

## 📂 Repository Structure

```text
.
├── docs/                 # Extended documentation and API references
├── examples/             # Sample inputs, prompts, and outputs
├── images/               # Sample images and dataset snapshots
├── logs/                 # Execution logs
├── project/
│   ├── configs/          # YAML settings driving model/dataset configurations
│   ├── datasets/         # Source JSONL files and cached image downloads
│   ├── models/           # Individual wrappers for local and API VLMs
│   ├── prompts/          # Standardized instructional text templates
│   ├── outputs/          # Output JSONL checkpoints representing raw model generation
│   ├── reports/          # Evaluation summaries, CSV leaderboards, and plotted graphs
│   ├── main.py           # Core orchestrator and pipeline entry point
│   ├── loader.py         # Dynamic schema auto-detection and image caching logic
│   ├── benchmark.py      # Core inference loop tracking latency and success
│   └── evaluation.py     # Evaluation engine parsing and scoring structural accuracy
├── tests/                # Unittests and integration tests
├── .github/              # CI workflows
├── README.md             # Primary execution guide
├── requirements.txt      # PyPI dependencies
└── LICENSE               # MIT License
```

---

## 🔄 Pipeline Architecture

The execution flow processes images sequentially through the following standardized stages:

```
project/main.py (Orchestrator)
      ↓
Dataset Loader (project/loader.py)
      ↓
Prompt Generator (project/benchmark.py)
      ↓
Vision Language Model (project/models/*)
      ↓
OCR Extraction
      ↓
Script Detection
      ↓
Language Detection
      ↓
Translation
      ↓
QA Generation
      ↓
Evaluation (project/evaluation.py)
      ↓
Leaderboard (project/report.py)
      ↓
PDF Report (project/plots.py)
```

---

## 📦 Installation

We strongly recommend using a virtual environment (Python 3.10+ required).

```bash
git clone https://github.com/example/text-in-image-benchmark.git
cd text-in-image-benchmark

python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🚀 Quick Start

Ensure your keys are configured if you are using Cloud API models like GPT-4o or Gemini:
```bash
# On Windows (PowerShell)
$env:OPENAI_API_KEY="your_openai_key"

# On macOS/Linux
export OPENAI_API_KEY="your_openai_key"
```

Execute the orchestration pipeline on the sample configuration:
```bash
python -m project.main --config project/configs/config.yaml --max-images 5
```

Once the pipeline finishes, the results are stored directly in your workspace:
- **Checkpoints (Raw JSON):** `project/outputs/`
- **PDF Report & Leaderboard:** `project/reports/Reports/`

---

## ⚙️ Configuration

The entire pipeline is driven by a single `config.yaml` file located at `project/configs/config.yaml`. 

You do not need to modify Python code to switch models or datasets. The dataset auto-detector automatically detects fields in any standard `.jsonl` format.

See [Configuration Documentation](docs/configuration.md) for a comprehensive list of all supported properties.

---

## 🖼 Example Images

![Example](images/example_signboard.jpg)

*(A sample image from the dataset, evaluated for text extraction and multilingual comprehension).*

---

## 📝 Example Output

Below is a realistic, complete example of what the pipeline ingests and successfully generates based on the benchmark schema.

### Input

**Image:** [Signboard image]  
**Caption Context:** "A speed limit sign in Hindi."

↓

### Generated Output

```json
{
  "ocr_text": "नगर निगम दिल्ली\nपार्किंग निषेध\nयहाँ गाड़ियाँ खड़ी करना मना है।",
  "scripts": [
    "Devanagari"
  ],
  "languages": [
    "Hindi"
  ],
  "multilingual_extraction": {
    "original": "नगर निगम दिल्ली\nपार्किंग निषेध\nयहाँ गाड़ियाँ खड़ी करना मना है।",
    "romanized": "Nagar Nigam Delhi\nParking Nishedh\nYahan gaadiyan khadi karna mana hai.",
    "english_translation": "Municipal Corporation Delhi\nNo Parking\nParking vehicles here is prohibited."
  },
  "text_qa": {
    "question": "Which department issued this notice?",
    "answer": "The Municipal Corporation Delhi issued this notice."
  }
}
```

---

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:
- [Installation](docs/installation.md)
- [Configuration](docs/configuration.md)
- [Datasets](docs/datasets.md)
- [Models](docs/models.md)
- [Pipeline](docs/pipeline.md)
- [Examples](docs/examples.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
