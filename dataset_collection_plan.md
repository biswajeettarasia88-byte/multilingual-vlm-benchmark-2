# Dataset Collection Plan (v0.2.0 Pilot)

## Objective
This plan outlines the acquisition strategy for the **first 100 real multilingual images** to populate `benchmark-v1`. No data has been downloaded, and no synthetic data has been generated.

## Selected Candidate Datasets
After surveying public datasets, the following combination has been selected to maximize diversity while strictly adhering to open redistribution licenses (CC-BY-4.0 / MIT / Public Domain):
1. **MLT-2019**: 40 images (Scene Text, Transportation, Commercial)
2. **XFUND**: 20 images (Government Forms, Public Services)
3. **ChartQA**: 5 images (Charts/Tables)
4. **M4-Receipt**: 5 images (Receipts/Commercial)
5. **Wikimedia Commons / OpenStreetMap**: 30 images (Healthcare, Education, under-represented languages)

## Expected Coverage Metrics (100 Images)
- **Category Coverage**: 
  - Scene Text: ~20
  - Transportation: ~20
  - Gov/Public Services: ~15
  - Healthcare: ~10
  - Education: ~10
  - Commercial: ~10
  - Documents: ~10
  - Receipts: ~5
  - Charts/Tables: ~5
- **Language Coverage**: Hindi, Arabic, Korean, Japanese, Spanish, Italian, Chinese, Thai, Swahili, Tamil, Nepali, English.
- **Script Coverage**: Devanagari, Arabic, Hangul, Han, Hiragana/Katakana, Latin, Thai, Tamil.

## Human Review & Quality Rules
Before any image enters the benchmark, it will pass through a strict human review pipeline detailed in `candidate_images_manifest.json` ensuring:
- **No PII**: Faces and license plates blurred (per `docs/ethics.md`).
- **License Integrity**: Verified CC-BY/MIT/PD status.
- **Visual Quality**: No severe blur or unreadable occlusions.

## Known Risks
- **Redistribution Rights**: Ensuring images from Wikimedia Commons explicitly allow commercial redistribution without "ShareAlike" traps that might infect the benchmark license.
- **PII Scrubbing Overhead**: Finding natural scene text often inadvertently captures faces. A strict pre-processing blurring pipeline must be maintained.

## Remaining Work Before Annotation
1. **Download Candidates**: Execute `tools/download_images.py` against the selected sources to download the 100 raw images.
2. **Human Filtering**: Manually filter the 100 candidates to drop any that fail the PII or blur checks.
3. **Finalize Manifest**: Update `candidate_images_manifest.json` into the official `benchmark_manifest.json`.

> [!IMPORTANT]
> The strategic planning for the 100-image pilot is complete. Please review the dataset selections and the ethics guidelines. I await your explicit approval before triggering the Python download scripts to ingest real data!
