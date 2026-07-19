# Evaluation Metrics

**Version:** 1.0.0  
**Last Updated:** 2026-07-19

**Purpose:** Define scoring calculations mathematically.  
**Scope:** OCR, Translation, Grounding, Reasoning metrics.

---

## Table of Contents
1. [OCR Metrics](#ocr-metrics)
2. [Translation Metrics](#translation-metrics)
3. [Grounding Metrics](#grounding-metrics)
4. [Reasoning Metrics](#reasoning-metrics)
5. [Score Aggregation](#score-aggregation)

## OCR Metrics
- **CER (Character Error Rate)**
- **WER (Word Error Rate)**
- **NED (Normalized Edit Distance)**: Character-level Levenshtein distance normalized by string length.

## Translation Metrics
- **BLEU, ROUGE**: N-gram overlaps.
- **COMET**: Semantic similarity.
- **ChrF**: Character n-gram overlap.

## Grounding Metrics
- **IoU (Intersection over Union)**
- **mAP (Mean Average Precision)**

## Reasoning Metrics
- **Exact Match & F1**
- **Semantic Similarity**
- **Hallucination Rate**

## Score Aggregation
Weighted scoring and overall benchmark averages across tasks.

**Related:** [Benchmark Design](benchmark_design.md)
