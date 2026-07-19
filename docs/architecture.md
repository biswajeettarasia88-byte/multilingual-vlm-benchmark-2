# Architecture Overview

**Version:** 1.0.0  
**Last Updated:** 2026-07-19

**Purpose:** Explain the repository and system architecture.  
**Scope:** Repository layout, execution flow, data flow, pipeline, adapters.

---

## Table of Contents
1. [Repository Layout](#repository-layout)
2. [Directory Responsibilities](#directory-responsibilities)
3. [Execution Flow](#execution-flow)
4. [Data Flow](#data-flow)
5. [Evaluation Pipeline](#evaluation-pipeline)
6. [Model Adapters](#model-adapters)
7. [Future Scalability](#future-scalability)

## Repository Layout
The repository cleanly separates datasets, framework code, and documentation.
- `configs/`
- `docs/`
- `evaluation/`
- `examples/`
- `images/`
- `models/`
- `project/`
- `scripts/`
- `tests/`
- `utilities/`

## Directory Responsibilities
- `project/`: Core orchestrator.
- `evaluation/`: Scoring engine.
- `models/`: Adapters to VLMs.

## Execution Flow
Main execution starts via `project/main.py`, invoking data loaders and forwarding to the model adapters.

## Data Flow
Image & JSON -> Preprocessing -> Model Inference -> Raw Prediction -> Evaluation Engine -> Score.

## Evaluation Pipeline
See [Benchmark Pipeline details](#data-flow) or refer to `benchmark_design.md`.

## Model Adapters
Abstracted classes integrating local weights and remote APIs.

## Future Scalability
Designed to scale from 20 to 50,000+ benchmark images.

**Related:** [Dataset Schema](dataset_schema.md), [Model Integration](model_integration.md)
