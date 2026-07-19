# Configuration Guide

The `project/configs/config.yaml` file acts as the central control plane for the benchmark pipeline. It dictates which models run, how datasets are loaded, and hardware settings.

## Hardware & Runtime Configuration (`runtime`)

### `device`
- **Default Value:** `"cuda"`
- **Accepted Values:** `"cuda"`, `"cpu"`, `"mps"`
- **Purpose:** Specifies the hardware backend for model inference.
- **Example:** `device: "cuda"` executes the model on the Nvidia GPU. Use `"cpu"` if no GPU is available.

### `default_precision`
- **Default Value:** `"bf16"`
- **Accepted Values:** `"bf16"`, `"fp16"`, `"float32"`
- **Purpose:** Controls the base floating-point precision for loading weights. `bf16` is highly recommended for Ampere+ GPUs to save memory without losing precision.

### `quantization`
- **Default Value:** `"4bit"`
- **Accepted Values:** `"4bit"`, `"8bit"`, `"none"`
- **Purpose:** Compresses model weights. 
- **Effect:** Setting to `"4bit"` enables `bitsandbytes` quantization, drastically reducing VRAM usage at a slight cost to inference speed.

### `resume`
- **Default Value:** `true`
- **Accepted Values:** `true`, `false`
- **Purpose:** Enables smart checkpointing. If `true`, the pipeline will skip images that already have a `.json` output file in the `outputs/` directory.

## Dataset Configuration (`dataset`)

### `download_missing`
- **Default Value:** `true`
- **Accepted Values:** `true`, `false`
- **Purpose:** Controls automatic remote fetching of images.
- **When to enable:** When cloning fresh from GitHub and the `datasets/images/` folder is empty. The loader will parse `image_url` and download files to disk.
- **When to disable:** If you are operating in an offline/airgapped environment and have already mounted pre-downloaded images.

## Model Configuration (`models`)
This block controls which models are actively benchmarked.

### `[model_name].enabled`
- **Default Value:** `false` (for heavy models)
- **Accepted Values:** `true`, `false`
- **Purpose:** Determines if the engine will initialize and benchmark this model.

### `[model_name].model_id`
- **Purpose:** The precise HuggingFace Hub repository string or local path (e.g. `Qwen/Qwen2.5-VL-7B-Instruct`).

### `[model_name].api_key_env`
- **Purpose:** If using an API-based model (e.g. Gemini), this field dictates which environment variable the wrapper should search for to authorize requests (e.g. `GEMINI_API_KEY`).

## Example Complete config.yaml
```yaml
runtime:
  device: "cuda"
  default_precision: "bf16"
  quantization: "4bit"
  resume: true

dataset:
  path: "project/datasets/signs.jsonl"
  download_missing: true

models:
  Qwen:
    enabled: true
    model_id: "Qwen/Qwen2.5-VL-7B-Instruct"
  Gemini:
    enabled: false
    model_id: "gemini-2.5-flash"
    api_key_env: "GEMINI_API_KEY"
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
