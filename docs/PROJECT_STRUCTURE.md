# Project Structure

## Purpose
Provides a detailed explanation of the major components of the Multilingual VLM Benchmark based on actual implementation.

## Directory Tree
```text
.
├── configs/          # YAML configurations driving the benchmark and models
├── data/             # Persistent data storage for datasets and benchmark splits
├── docs/             # Granular markdown documentation
├── evaluation/       # Scoring engine, metric calculations, report generation
├── examples/         # Example assets for demonstration
├── models/           # VLM API adapters and wrapper scripts
├── project/          # Core orchestrator logic and data loaders
│   ├── datasets/
│   ├── logs/
│   └── prompts/
├── scripts/          # Independent utilities and visualization generators
├── tests/            # Unit tests for pipeline integrity
├── tools/            # Orchestration pipelines, downloaders, validators, planners
│   ├── archive/
│   ├── cache/
│   ├── campaign/
│   ├── connectors/
│   ├── downloaders/
│   ├── ingestion/
│   ├── planner/
│   ├── reporting/
│   ├── review/
│   └── verification/
└── utilities/        # Shared helper functions
```

## Related Files
- `README.md`
