# Multilingual Dataset Survey (Candidate Sources)

This document surveys publicly available datasets suitable for inclusion in `benchmark-v1` while strictly adhering to open redistribution licenses (e.g., CC-BY-4.0).

## 1. MLT-2019 (Multi-Lingual Text)
- **URL**: [ICDAR 2019 MLT](https://rrc.cvc.uab.es/?ch=15)
- **License**: CC-BY-4.0 (for research/academic)
- **Redistribution**: Allowed with attribution
- **Image Count**: 20,000
- **Languages**: 10 (Arabic, Bangla, Chinese, English, French, German, Hindi, Italian, Japanese, Korean)
- **Scripts**: 7 (Arabic, Bengali, Han, Latin, Devanagari, Japanese, Hangul)
- **Categories**: Scene Text, Urban Environments, Commercial Signs
- **OCR Suitability**: High (Designed specifically for scene text)
- **Document/Chart Suitability**: Low
- **Geographic Diversity**: High (Global urban centers)

## 2. DocVQA (Document Visual Question Answering)
- **URL**: [DocVQA](https://www.docvqa.org/)
- **License**: UCSF Industry Documents Library Terms (Public Domain / CC0 equivalent)
- **Redistribution**: Allowed for non-commercial research
- **Image Count**: 12,000+
- **Languages**: Primarily English
- **Scripts**: Latin
- **Categories**: Invoices, Letters, Government Forms, Reports
- **OCR Suitability**: High
- **Document/Chart Suitability**: High
- **Geographic Diversity**: Low (US-centric)

## 3. XFUND (Multilingual Form Understanding)
- **URL**: [XFUND GitHub](https://github.com/doc-analysis/XFUND)
- **License**: MIT / Open Access
- **Redistribution**: Allowed
- **Image Count**: 1,393 fully annotated forms
- **Languages**: 7 (Chinese, Japanese, Spanish, French, Italian, German, Portuguese)
- **Scripts**: Latin, Han, Japanese
- **Categories**: Government Forms, Receipts, Medical Records
- **OCR Suitability**: High
- **Document/Chart Suitability**: High
- **Geographic Diversity**: Medium

## 4. ChartQA
- **URL**: [ChartQA GitHub](https://github.com/vis-nlp/ChartQA)
- **License**: MIT
- **Redistribution**: Allowed
- **Image Count**: 21,000+
- **Languages**: Primarily English
- **Scripts**: Latin
- **Categories**: Bar charts, line charts, pie charts
- **OCR Suitability**: Medium
- **Document/Chart Suitability**: Very High
- **Geographic Diversity**: Low (Data visualization centric)

## 5. M4-Receipt
- **URL**: (Academic Release)
- **License**: CC-BY-NC 4.0
- **Redistribution**: Allowed non-commercially
- **Image Count**: ~10,000
- **Languages**: Thai, Chinese, Japanese, English
- **Scripts**: Thai, Han, Japanese, Latin
- **Categories**: Commercial, Receipts
- **OCR Suitability**: High
- **Document/Chart Suitability**: High
- **Geographic Diversity**: High (Asia focus)

## 6. OpenStreetMap (OSM) Mapillary / Wikimedia Commons
- **URL**: [Wikimedia Commons](https://commons.wikimedia.org/)
- **License**: CC-BY-SA 4.0 / Public Domain
- **Redistribution**: Fully Allowed
- **Image Count**: Millions
- **Languages**: Global
- **Scripts**: Global
- **Categories**: Transportation, Geography, Street Scenes, Public Services
- **OCR Suitability**: Variable (Requires manual filtering)
- **Document/Chart Suitability**: Low
- **Geographic Diversity**: Extreme

---

## Recommended Selection Strategy
To achieve the 100-image pilot goal with maximum diversity:
1. **MLT-2019**: Source 40 images (Scene Text, Transportation, Commercial) targeting Hindi, Arabic, Korean, and Japanese.
2. **XFUND**: Source 20 images (Documents, Government) targeting Spanish, Italian, and Chinese.
3. **ChartQA**: Source 5 images (Charts/Tables).
4. **M4-Receipt**: Source 5 images (Receipts) targeting Thai.
5. **Wikimedia Commons**: Source 30 images manually for under-represented languages (Swahili, Tamil, Nepali) in Healthcare, Education, and Airport environments.
