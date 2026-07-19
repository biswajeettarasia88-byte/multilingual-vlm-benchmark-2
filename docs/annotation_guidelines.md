# Annotation Guidelines

**Version:** 1.0.0  
**Last Updated:** 2026-07-19

**Purpose:** Guide for dataset annotators.  
**Scope:** Rules for bounding boxes, translations, grounding.

---

## Table of Contents
1. [Bounding Boxes & Polygons](#bounding-boxes--polygons)
2. [Language & Script Labeling](#language--script-labeling)
3. [Translation & Romanization](#translation--romanization)
4. [Named Entities](#named-entities)
5. [Grounding & Reasoning](#grounding--reasoning)
6. [Reading Order](#reading-order)
7. [Quality Checks](#quality-checks)

## Bounding Boxes & Polygons
Use tight boxes. For curved/distorted text, use polygons or rotated boxes.

## Language & Script Labeling
Strict adherence to ISO codes. Handle mixed scripts accurately.

## Translation & Romanization
Context-aware English translation. Standard romanization schemes.

## Named Entities
Tag standard NER categories (LOC, ORG, PER).

## Grounding & Reasoning
Explicit mappings between entities in text and their coordinates. Multi-hop logic defined in reasoning chains.

## Reading Order
Left-to-right, top-to-bottom unless script dictates otherwise.

## Quality Checks
All annotations must pass blind peer-review and automated format checks.

**Related:** [Dataset Schema](dataset_schema.md)
