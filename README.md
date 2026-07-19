# Multilingual VLM Benchmark

A rigorous, massive-scale evaluation framework designed to test Vision-Language Models (VLMs) on multi-hop reasoning, strict OCR accuracy, and spatial grounding across diverse global languages and scripts.

---

## 📖 Project Overview

The Multilingual VLM Benchmark is engineered to bridge the gap between simple text extraction (OCR) and complex multimodal logic. Modern foundation models can read English text effortlessly, but often hallucinate or fail when confronted with densely packed, multi-script environments like a crowded Asian street market, a complex Indian railway schedule, or a mixed-language Arabic/French highway sign.

This repository provides the core **evaluation framework**, the mathematical **scoring engine**, and the exhaustive **dataset schemas** needed to evaluate VLMs against top-tier academic standards.

## 🎯 Motivation & Benchmark Philosophy

Currently, many benchmarks evaluate VLMs on contrived examples or clean, scanned documents. However, true AI autonomy requires models to interact with the messy, physical world. Our philosophy mandates that a benchmark must:
1. **Reflect Reality**: Use unedited, real-world photographs with glare, occlusion, and noise.
2. **Prevent Contamination**: Strictly partition the dataset to maintain hidden evaluation splits.
3. **Punish Hallucinations**: Utilize strict metric systems that heavily penalize invented text.
4. **Demand Reasoning**: Test the model's ability to combine localized text extraction with multi-hop logic (e.g., *“If I am at Gate 2, what time does the next train to Tokyo depart?”*).

## 🚀 Why Another Benchmark?

While exceptional benchmarks like OCRBench, DocVQA, and MMMU exist, they often under-represent low-resource languages and scripts. The Multilingual VLM Benchmark focuses aggressively on **linguistic diversity** (22+ languages), **complex visual grounding**, and **hierarchical reading orders**—challenges that routinely break contemporary multimodal models.

---

## 🛠️ Supported Benchmark Tasks

Our framework rigorously evaluates VLMs across a spectrum of multimodal tasks:

- **Core OCR**: Text Detection, Character/Word Accuracy, Romanization.
- **Linguistic Analysis**: Language Identification, Script Identification, Translation.
- **Entity Extraction**: Named Entity Recognition (NER).
- **Spatial Logic**: Visual Grounding, Layout Analysis, Bounding Box / Polygon Localization.
- **Advanced Reasoning**: Multi-hop Visual Question Answering (VQA), Scene Understanding, Instruction Following.

---

## 🗂️ Repository Architecture & Directory Tree

This repository enforces strict separation of concerns between the evaluation framework and the benchmark dataset:

```text
.
├── configs/          # YAML configurations driving the benchmark and models
├── docs/             # Granular markdown documentation
├── evaluation/       # Scoring engine, metric calculations, report generation
├── examples/         # Public demo showcase (NOT the official benchmark split)
├── images/           # Global repository assets
├── models/           # VLM API adapters and wrapper scripts
├── project/          # Core orchestrator logic (data loaders, main loop)
│   └── datasets/     # Train/Validation/Test data splits
├── scripts/          # Independent utilities and visualization generators
├── tests/            # Unit tests for pipeline integrity
└── utilities/        # Shared helper functions (logging, file I/O)
```

---

## ⚙️ Installation & Quick Start

1. Clone the repository:
```bash
git clone https://github.com/biswajeettarasia88-byte/multilingual-vlm-benchmark.git
cd multilingual-vlm-benchmark
```

2. Create a virtual environment and install dependencies:
```bash
conda create -n mvlm python=3.10 -y
conda activate mvlm
pip install -r requirements.txt
```

3. Configure your API keys (for closed-source models):
```bash
export OPENAI_API_KEY="your-key-here"
```

---

## 🤖 Supported Models

The evaluation pipeline is modular and supports the following architectures (both local execution and API access):

- **Closed Source (API)**: GPT-4o, Gemini 2.5 Pro, Claude Opus 4
- **Open Source (Local/API)**: Qwen2.5-VL, InternVL3, MiniCPM-V, Molmo, Pixtral, Phi-4 Multimodal, Llama 4 Vision

---

## 📊 Evaluation Overview

The benchmark employs mathematical, industry-standard metrics to eliminate subjective grading:
- **OCR Accuracy**: Normalized Edit Distance (NED), CER, WER.
- **Translation Quality**: BLEU, COMET, ChrF.
- **Visual Grounding**: Intersection over Union (IoU), Mean Average Precision (mAP).
- **Reasoning**: Exact Match, Semantic Similarity, F1, Hallucination Penalty.

---

## 🖼️ Example Visualizations & JSON Schemas

*This section will be expanded after the reference example is implemented.*

## 🏆 Leaderboard & Benchmark Results

*This section will be expanded after the reference example is implemented.*

---

## 🗺️ Repository Roadmap

The benchmark is designed for massive long-term scalability:
- **Phase A (Current)**: Architecture stabilization and pipeline scaffolding.
- **Phase B (Upcoming)**: Construction of a 20-image showcase gallery demonstrating complex multi-script OCR.
- **Version 1.0**: 100 benchmark images (Baseline Evaluation).
- **Version 2.0**: 500 images (Rigorous Multilingual Evaluation).
- **Version 3.0**: 5,000 images (Automated large-scale text-in-wild ingestion).
- **Version 4.0**: 50,000+ multilingual images.

---

## 🤝 Contributing

We welcome contributions! Please follow our standard workflow: fork the repository, create a feature branch, and submit a PR. 
*Note: Any changes to the core `annotation.json` schema require a major version bump.*

## ❓ FAQ

**Q: Are the images in the `examples/` folder part of the official test set?**
No, the `examples/` folder contains a public showcase demonstrating the annotation schema. True benchmark evaluations run against a hidden `test/` split to prevent model contamination.

**Q: Can I submit a new VLM for evaluation?**
Yes. You can write a new model adapter in the `models/` directory and run the evaluation script locally.

## 📄 License & Citation

The evaluation framework is provided under standard open-source licensing. 
Detailed licensing information for the dataset, including strict copyright and Fair Use adherence, will be documented in `metadata.json` for all evaluated images.

If you use this benchmark in your research, please cite:
*(Citation details will be added upon final release).*
