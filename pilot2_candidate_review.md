# Pilot 2 Candidate Review (Revised)

## Summary
- **Total Candidates Discovered**: 12
- **Download-ready candidates**: 8
- **Pending candidates**: 4
- **Review-required candidates**: 4

## Source Distribution
- Wikimedia Commons: 8
- Hugging Face: 2
- Kaggle: 0 (Skipped due to Auth)
- Zenodo: 2

## Diversity Metrics
- **Language Distribution**: Unknown, Spanish, English, Thai, Hindi, Nepali
- **Script Distribution**: Unknown, Devanagari, Thai, Latin
- **Category Distribution**: Documents/OCR, Street signs, Receipts/Commercial, Transportation signage, Tourist information, Government/Public Services

## Missing Metadata & Known Risks
- **Hugging Face**: Official datasets typically require downloading massive Parquet/Arrow archives. A direct image URL is rarely exposed without using the dataset viewer API. Status marked as `PENDING`.
- **Zenodo**: Returns ZIP archives containing hundreds of images. Requires manual review to select a specific file path inside the archive.
- **Kaggle**: Explicitly skipped to avoid bypass mechanisms.

## Candidate Breakdown
| ID | Source | License | Category | Language | Status | Action |
|---|---|---|---|---|---|---|
| WIKI_000 | Wikimedia Commo... | CC-BY-SA-3.0 | Street signs | Hindi | READY | PENDING |
| WIKI_001 | Wikimedia Commo... | CC-BY-SA-4.0 | Street signs | Hindi | READY | PENDING |
| WIKI_002 | Wikimedia Commo... | CC0-1.0 | Transportation signage | Thai | READY | PENDING |
| WIKI_003 | Wikimedia Commo... | CC0-1.0 | Transportation signage | Thai | READY | PENDING |
| WIKI_004 | Wikimedia Commo... | CC-BY-SA-4.0 | Government/Public Services | Nepali | READY | PENDING |
| WIKI_005 | Wikimedia Commo... | CC-BY-SA-4.0 | Government/Public Services | Nepali | READY | PENDING |
| WIKI_006 | Wikimedia Commo... | CC-BY-SA-4.0 | Tourist information | Spanish | READY | PENDING |
| WIKI_007 | Wikimedia Commo... | CC-BY-SA-3.0 | Tourist information | Spanish | READY | PENDING |
| HF_000 | uv-scripts/ocr... | UNKNOWN | Documents/OCR | Unknown | PENDING | REVIEW_REQUIRED |
| HF_001 | unsloth/LaTeX_O... | UNKNOWN | Documents/OCR | Unknown | PENDING | REVIEW_REQUIRED |
| ZEN_000 | A labeled datas... | CC-BY-4.0 | Receipts/Commercial | Unknown | PENDING | REVIEW_REQUIRED |
| ZEN_001 | Food items matc... | CC-BY-4.0 | Receipts/Commercial | Unknown | PENDING | REVIEW_REQUIRED |