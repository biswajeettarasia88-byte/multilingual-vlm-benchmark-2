# Sampling Protocol & Dataset Balance

This document defines the strict inclusion, exclusion, and distribution rules for `benchmark-v1`.

## Inclusion Criteria
- High-resolution real-world photographs or officially released digital documents.
- Readable text (for humans).
- Explicit open-redistribution licenses (e.g., CC-BY-4.0).

## Exclusion Criteria
- Severe motion blur or out-of-focus imagery preventing text extraction.
- AI-generated imagery or synthesized OCR targets.
- Copyrighted imagery preventing redistribution (e.g., Pinterest, private social media).
- Near-duplicates of existing images.

## Target Dataset Balances
To prevent benchmark bias, the following hard caps are enforced for `benchmark-v1` (and all subsequent releases):
- **Language**: No single language may exceed 25% of the total dataset.
- **Country**: No single country origin may exceed 20%.
- **Category**: No single scene category (e.g., Transit, Receipts) may exceed 20%.
- **Difficulty**: Uniformly balanced across Easy, Medium, Hard, and Expert.
- **Environment**: 50/50 balance between Indoor and Outdoor scenes.
- **Format**: 60% Scene Text, 30% Documents, 10% Charts/Tables.
- **OCR Density**: Balanced representation of sparse (1-5 words) and dense (>50 words) text images.

## Split Generation Rules
- **Leakage Prevention**: No near-duplicates (pHash) allowed across train, validation, and test splits.
- **Burst Sequence Protection**: Images captured in the same chronological burst sequence or video frame extraction must be assigned to the identical split.
- **Hidden Test Set**: The test split will remain physically hidden for the official leaderboard and will not be published publicly.
