# Model Integration

**Version:** 1.0.0  
**Last Updated:** 2026-07-19

**Purpose:** Guide to adding new VLMs.  
**Scope:** Adapter interfaces and inputs/outputs.

---

## Table of Contents
1. [Supported APIs](#supported-apis)
2. [Supported Local Models](#supported-local-models)
3. [Adapter Interface](#adapter-interface)

## Supported APIs
GPT-4o, Gemini 2.5 Pro, Claude Opus 4.

## Supported Local Models
Qwen2.5-VL, InternVL3, MiniCPM-V, Molmo, Pixtral, Phi-4 Multimodal, Llama 4 Vision.

## Adapter Interface
Must accept standard image tensors / paths and output strict JSON.
Expected Inputs: Image file, Question String.
Expected Outputs: JSON conforming to `prediction.json`.

**Related:** [Architecture](architecture.md)
