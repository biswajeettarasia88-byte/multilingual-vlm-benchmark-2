# Ethics and Privacy Guidelines

The `benchmark-v1` dataset strictly adheres to global privacy laws (e.g., GDPR, CCPA) and ethical AI dataset construction principles.

## 1. Privacy Considerations
All images ingested into the benchmark must be reviewed for Personally Identifiable Information (PII).
- **Faces**: Any recognizable human faces must be blurred or obfuscated during the preprocessing phase. Images with crowds where individuals cannot be identified do not require blurring.
- **Vehicle License Plates**: All readable vehicle license plates must be blurred.
- **Government Documents**: Sample documents (passports, IDs) must be synthetic, officially released open-data examples, or have all PII (names, exact DOBs, ID numbers) securely redacted.

## 2. Sensitive Locations
Images of sensitive military, intelligence, or heavily restricted government installations are strictly prohibited unless the image is released under an official government open-data license.

## 3. Copyright Compliance
- **Logos & Trademarks**: Images containing commercial logos are permitted strictly under fair use for academic research, provided the image itself is distributed under a compatible license (e.g., CC-BY-4.0).
- **Books & Art**: Scans of copyrighted books, paintings, or art where the copyright holder has not granted redistribution rights are prohibited.

## 4. Data Removal Requests
A public email channel must be provided in the repository `README.md` to allow individuals or copyright holders to request the immediate removal of any image from the dataset. Upon verification, the image and all associated metadata/annotations will be permanently deleted from the active repository and all subsequent releases.
