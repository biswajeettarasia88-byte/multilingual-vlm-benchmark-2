# Output Examples

## Sample Input JSON
```json
{
  "image_id": "MCD_NOTICE_01",
  "image_url": "https://example.com/parking.jpg",
  "image_path": "images/parking.jpg"
}
```

## Sample Target Image (Conceptual)
*A photo of a yellow signboard on a street that reads:*
**नगर निगम दिल्ली**
**पार्किंग निषेध**
**यहाँ गाड़ियाँ खड़ी करना मना है।**

## Example Extracted Final JSON Output
After execution, the VLM produces a unified checkpoint tracking the precise inference parameters and the strict Text-in-Image schema.

```json
{
  "image_id": "MCD_NOTICE_01",
  "model_id": "Qwen/Qwen2.5-VL-7B-Instruct",
  "gpu_used": "NVIDIA GeForce RTX 4090",
  "processing_time_sec": 4.12,
  "ocr_text": "नगर निगम दिल्ली\nपार्किंग निषेध\nयहाँ गाड़ियाँ खड़ी करना मना है।",
  "scripts": [
    "Devanagari"
  ],
  "languages": [
    "Hindi"
  ],
  "multilingual_extraction": {
    "original": "नगर निगम दिल्ली\nपार्किंग निषेध\nयहाँ गाड़ियाँ खड़ी करना मना है।",
    "romanized": "Nagar Nigam Delhi\nParking Nishedh\nYahan gaadiyan khadi karna mana hai.",
    "english_translation": "Municipal Corporation Delhi\nNo Parking\nParking vehicles here is prohibited."
  },
  "text_qa": {
    "question": "Which department issued this notice?",
    "answer": "The Municipal Corporation Delhi issued this notice."
  }
}
```

## Understanding the Fields
- **ocr_text:** Notice how newline characters `\n` are preserved, and exact punctuation is maintained. No summaries are generated.
- **multilingual_extraction:** The transliteration accurately reflects spoken phonetic Romanization without awkwardly translating words into English during the transliteration phase.
- **text_qa:** Generates a question that strictly evaluates text comprehension.

---
## Related Documentation
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Datasets](datasets.md)
- [Models](models.md)
- [Pipeline](pipeline.md)
- [Examples](examples.md)
- [Troubleshooting](troubleshooting.md)
