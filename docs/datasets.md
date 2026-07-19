# Datasets Guide

## Dataset Overview
The pipeline consumes image metadata formatted as JSON Lines (`.jsonl`). Each line represents an image to benchmark.

### Supported Datasets
The repository supports two default datasets:
1. `signs.jsonl` (Targeted at street boards and navigation signs)
2. `images_scripts_multilingual.jsonl` (Broad coverage including documents, notices, and handwriting)

### Folder Layout
```
project/datasets/
├── images/                             # Local cache for downloaded JPEGs/PNGs
├── signs.jsonl                         # Manifest file
└── images_scripts_multilingual.jsonl   # Manifest file
```

## JSON Schema Structure
The `DatasetLoader` automatically detects dataset schemas using adaptive mapping.

**Required Fields:**
- `id` or `image_id`: Unique identifier for the record.
- `image_url` or `url`: Remote URL to fetch the image if not found locally.
- `local_path` or `image_path`: Expected filename inside `project/datasets/images/`.

**Optional Fields:**
- `language`: Expected language ground truth.
- `text` or `ocr_text`: Ground truth OCR for evaluation scoring.

### Example Dataset Record
```json
{
  "image_id": "STREET_001",
  "image_url": "https://example.com/images/street_001.jpg",
  "image_path": "images/street_001.jpg",
  "language": "Hindi",
  "task": "Text in Image"
}
```

## How DatasetLoader Works

### Automatic Schema Detection
Because JSONL datasets can vary, `DatasetLoader` reads the first 100 lines and maps incoming keys to internal canonical keys (e.g. mapping `image_id` to `id`).

### Image Downloading and Caching
When `download_missing: true` is configured in `config.yaml`, the loader will verify if `image_path` exists locally. If it does not, it will execute an HTTP request to `image_url`, download the binary, and save it permanently into the `project/datasets/images/` cache. 

### Offline Mode
If you are airgapped, set `download_missing: false`. The loader will strictly enforce local paths, instantly failing records where the image is missing from the disk.

## Adding a Custom Dataset
To add your own images:
1. Create `my_dataset.jsonl` in the datasets folder.
2. Ensure every line has an `image_id` and a valid local path or URL.
3. Point `config.yaml` dataset path to `project/datasets/my_dataset.jsonl`.

---
## Related Documentation
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Datasets](datasets.md)
- [Models](models.md)
- [Pipeline](pipeline.md)
- [Examples](examples.md)
- [Troubleshooting](troubleshooting.md)
