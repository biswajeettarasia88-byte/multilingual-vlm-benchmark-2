# Troubleshooting Guide

## Missing API Key
**Error:** `ValueError: API key not found` or 401 Unauthorized from cloud providers.
**Solution:** Ensure you export the correct environment variable dictated in `config.yaml` before running the pipeline.
**Windows:** `set GEMINI_API_KEY=your_key`
**Linux:** `export GEMINI_API_KEY=your_key`

## CUDA Unavailable
**Error:** `AssertionError: Torch not compiled with CUDA enabled` or fallback to incredibly slow CPU execution.
**Solution:** PyTorch was installed from PyPI without CUDA bindings. Uninstall `torch` and reinstall using the custom index URL:
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Out of Memory (CUDA OOM)
**Error:** `torch.cuda.OutOfMemoryError`
**Solution:**
1. Open `config.yaml`.
2. Change `quantization: "none"` to `quantization: "4bit"`.
3. The benchmark engine is designed with smart memory fallbacks and will attempt to retry the load; however, if you have less than 8GB VRAM, you must use smaller models (like MiniCPM) or use API models (Gemini, GPT-4o).

## Dataset Missing / Image Download Failed
**Error:** `Failed to load image index X`
**Solution:** The image URL may be broken, or you may be running in an offline environment with `download_missing: true`. If offline, manually place images in `project/datasets/images/` and set `download_missing: false`.

## JSON Parsing Failed
**Error:** `invalid_outputs: 1` in the final evaluation report.
**Solution:** The LLM failed to adhere to the strict 9-key JSON schema. Open the `_raw.txt` file in the `outputs/` directory to inspect what the model actually hallucinated. Upgrading to a more robust model (like GPT-4o) usually resolves parsing failures.

## Windows Path Issues
**Error:** `FileNotFoundError` related to long paths or slashes.
**Solution:** Python handles forward slashes perfectly on Windows. Ensure your `config.yaml` paths use standard forward slashes (e.g. `project/datasets/signs.jsonl`), avoiding backslash escaping issues.

---
## Related Documentation
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Datasets](datasets.md)
- [Models](models.md)
- [Pipeline](pipeline.md)
- [Examples](examples.md)
- [Troubleshooting](troubleshooting.md)
