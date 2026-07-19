# Versioning Policy

## Benchmark Updates
- **Minor Versions** (e.g., v1.1): Additions of new images or minor corrections to annotations.
- **Major Versions** (e.g., v2.0): Breaking changes to the JSON schema or evaluation methodology.

## Deprecation & Correction Tracking
- If an image is flagged for removal (e.g., privacy request), its JSON metadata is retained but marked `"status": "deprecated"`. The image file is securely deleted.
- Corrections to OCR or bounding boxes are tracked via an internal Git changelog and released during minor version bumps.

## ID Stability
- `image_id` is universally stable. Once an ID (e.g., `BENCHMARK_0001`) is minted, it is never reused or reassigned, even if the image is deprecated.
