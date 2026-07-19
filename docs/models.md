# Supported Models

The benchmark architecture supports a modular VLM framework where any model can be dynamically attached by subclassing `BaseVLM`.

## 1. Gemini
- **Backend:** Google GenAI SDK (Cloud)
- **API Requirements:** Requires `GEMINI_API_KEY` set in the environment.
- **Advantages:** Extreme speed, zero local VRAM cost, exceptional multilingual capability.
- **Limitations:** Data privacy constraints (sends images to Google servers), rate limiting.

## 2. GPT-4o
- **Backend:** OpenAI SDK (Cloud)
- **API Requirements:** Requires `OPENAI_API_KEY`.
- **Advantages:** Unmatched reasoning and robust JSON-schema adherence natively.
- **Limitations:** Cost per token.

## 3. Qwen (Qwen2.5-VL)
- **Backend:** HuggingFace Transformers (Local)
- **GPU Requirements:** 8GB VRAM (4-bit), 24GB VRAM (BF16).
- **Advantages:** Open-weights, absolute data privacy, massive multilingual training on Asian languages.
- **Limitations:** Slow generation times locally on lower-end GPUs.

## 4. InternVL
- **Backend:** HuggingFace Transformers (Local)
- **GPU Requirements:** Similar to Qwen (highly dependent on chosen parameter scale).
- **Advantages:** Extremely high resolution processing capabilities.

## 5. MiniCPM
- **Backend:** HuggingFace Transformers (Local)
- **Advantages:** Extremely lightweight. Operates smoothly on 4GB-8GB VRAM.

## 6. Molmo, Phi4, Llama
- Fully supported through HuggingFace with analogous VRAM constraints and API interfaces. Llama Vision offers robust performance in open-source tasks.

## The Model Lifecycle (`BaseVLM`)
All models implement a unified wrapper lifecycle:
1. **`__init__`**: Captures configurations.
2. **`load_model()`**: Allocates VRAM or verifies API keys.
3. **`generate(image, prompt)`**: Executes inference.
4. **`cleanup()`**: Triggers garbage collection and flushes CUDA memory when benchmarking ends to prevent OOM bleeding between models.

### How to Switch Models
Simply toggle the boolean in `project/configs/config.yaml`:
```yaml
models:
  Qwen:
    enabled: true
  Gemini:
    enabled: false
```

---
## Related Documentation
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Datasets](datasets.md)
- [Models](models.md)
- [Pipeline](pipeline.md)
- [Examples](examples.md)
- [Troubleshooting](troubleshooting.md)
