# Ethics and Privacy Guidelines

The `benchmark-v1` dataset strictly adheres to global privacy laws (e.g., GDPR, CCPA) and ethical AI dataset construction principles.

## 1. Privacy Considerations & PII Scrubbing
All images ingested into the benchmark must be reviewed for Personally Identifiable Information (PII) and processed through a scrubbing workflow before entering the dataset.
- **Faces**: Any recognizable human faces must be blurred or obfuscated. Crowds without identifiable individuals are exempt.
- **Vehicle License Plates**: All readable vehicle license plates must be blurred.
- **Personal Documents**: Personal IDs, passports, or medical records containing names, DOBs, or SSNs are strictly banned unless they are officially released synthetic open-data examples.
- **Children**: Images explicitly depicting children (even blurred) are excluded from the dataset entirely out of an abundance of caution.
- **Medical Information**: Patient charts or prescription labels containing sensitive health information must be entirely redacted.

## 2. Sensitive Locations
Images of sensitive military, intelligence, or heavily restricted government installations are strictly prohibited unless officially released under a government open-data license.

## 3. Copyright & License Governance
- **Approved Licenses**: CC-BY-4.0, CC-BY-SA-4.0, CC0-1.0, MIT, Apache-2.0, Public Domain.
- **Attribution**: The `photographer` and `source` fields in the metadata JSON are mandatory for all CC-BY records.

## 4. Data Removal Requests
A public email channel is provided in the repository `README.md` to allow individuals or copyright holders to request the immediate removal of any image. Upon verification, the image and all associated metadata will be permanently deleted from all active repositories and subsequent releases.
