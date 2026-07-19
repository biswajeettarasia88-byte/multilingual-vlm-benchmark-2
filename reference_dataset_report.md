# Reference Dataset Ingestion Report (Milestone 10)

## Dataset Selected
- **Dataset**: PaddleOCR Public Test Images
- **Reason for selection**: Represents official, stable, and highly relevant multilingual VLM evaluation data distributed transparently via GitHub infrastructure. Contains both dense document OCR and natural scene text.
- **Access method**: Raw HTTP Fetch (`HTTPRawDownloader`) via `raw.githubusercontent.com`.
- **License summary**: APACHE-2.0 (Permissive, open research and commercial use).

## Pipeline Performance
- **Images Attempted**: 2
- **Images Downloaded**: 2
- **Images Accepted**: 2

## Validation Results
- Checksum/Size Verification: **PASSED**
- License Normalization: **PASSED** (Mapped to APACHE-2.0)
- Duplicate Detection: **PASSED**
- Benchmark Manifest Insertion: **PASSED**

## Remaining Limitations
- Scaling HTTP downloads across thousands of URLs still requires careful rate-limit monitoring to avoid IP bans.
- GitHub Raw endpoints are stable for public repositories, but rely on the upstream repository not changing its branch structure.