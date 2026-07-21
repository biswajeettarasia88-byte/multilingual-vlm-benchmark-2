# Datasets Guide

## Purpose
Explains how datasets are managed, parsed, and orchestrated via the `project/datasets/` implementation.

## Usage
Datasets are managed using the loader in `project/loader.py`. The `tools/connectors/plugins/` directory allows for parsing from known schemas like CORD and FUNSD.

## Supported Formats
- Currently supports JSON manifests detailing image path, bounding boxes, text, and language.
- Managed by `tools/ingestion/metadata_builder.py`.

## Related Files
- `project/loader.py`
- `tools/connectors/plugins/`
