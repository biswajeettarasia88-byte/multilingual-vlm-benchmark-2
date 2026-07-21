# Multilingual VLM Benchmark

A rigorous, massive-scale evaluation framework designed to test Vision-Language Models (VLMs) on multi-hop reasoning, strict OCR accuracy, and spatial grounding across diverse global languages and scripts.

---

## 📖 Project Overview

### Problem Statement
Modern foundation models can read English text effortlessly, but often hallucinate or fail when confronted with densely packed, multi-script environments like a crowded Asian street market, a complex Indian railway schedule, or a mixed-language Arabic/French highway sign. 

### Objectives
The Multilingual VLM Benchmark bridges the gap between simple text extraction (OCR) and complex multimodal logic. It evaluates VLMs against top-tier academic standards by focusing on linguistic diversity (22+ languages), complex visual grounding, and hierarchical reading orders.

### Features
- **Core OCR**: Text Detection, Character/Word Accuracy, Romanization.
- **Linguistic Analysis**: Language Identification, Script Identification, Translation.
- **Entity Extraction**: Named Entity Recognition (NER).
- **Spatial Logic**: Visual Grounding, Layout Analysis, Bounding Box / Polygon Localization.
- **Advanced Reasoning**: Multi-hop Visual Question Answering (VQA), Scene Understanding, Instruction Following.

---

## 🗂️ Directory Structure
For a deep dive into the architecture, read the [Project Structure](docs/PROJECT_STRUCTURE.md) document.

```text
.
├── configs/          # YAML configurations driving the benchmark and models
├── data/             # Persistent data storage for datasets and benchmark splits
├── docs/             # Granular markdown documentation
├── evaluation/       # Scoring engine, metric calculations, report generation
├── examples/         # Example assets for demonstration
├── models/           # VLM API adapters and wrapper scripts
├── project/          # Core orchestrator logic and data loaders
├── scripts/          # Independent utilities and visualization generators
├── tests/            # Unit tests for pipeline integrity
├── tools/            # Orchestration pipelines, downloaders, validators, planners
└── utilities/        # Shared helper functions
```

---

## ⚙️ Installation & Quick Start

Refer to [Installation Guide](docs/installation.md) for full instructions.

```bash
git clone https://github.com/biswajeettarasia88-byte/multilingual-vlm-benchmark.git
cd multilingual-vlm-benchmark
conda create -n mvlm python=3.10 -y
conda activate mvlm
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"
```

## 🔄 Pipeline
Our benchmark follows a rigorous ingestion, annotation, and validation pipeline. 
See the comprehensive [Pipeline Documentation](docs/pipeline.md) for Mermaid flowcharts and step-by-step descriptions.

## 🖼️ Example Images
To understand the annotation and expected output structures, view the [Examples](docs/examples.md) page.

## 📊 Datasets & Models
- Read about our dataset generation and structure in [Datasets](docs/datasets.md)
- Learn how to integrate new models in [Models](docs/models.md)
- Explore the evaluation metrics and logic in [Evaluation](docs/EVALUATION.md)

## 🛠️ Configuration & Troubleshooting
- [Configuration](docs/configuration.md): How to adjust YAML properties.
- [Troubleshooting](docs/troubleshooting.md): Fix common issues in pipeline execution.

---

## 🤝 Contributing
Please review our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

## 📄 License & Citation
This project is licensed under the terms described in the [LICENSE](LICENSE) file. 
For citation details, see the [CITATION.cff](CITATION.cff) file.

## 📬 Contact
For questions, issues, or contributions, please open an issue on the GitHub repository.
