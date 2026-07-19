# Dataset Schema

**Version:** 1.0.0  
**Last Updated:** 2026-07-19

**Purpose:** Fully document JSON schemas.  
**Scope:** All benchmark JSON formats.

---

## Table of Contents
1. [metadata.json](#metadatajson)
2. [annotation.json](#annotationjson)
3. [qa.json](#qajson)
4. [prediction.json](#predictionjson)
5. [score.json](#scorejson)
6. [report.json](#reportjson)
7. [failure_cases.json](#failure_casesjson)
8. [expected_output.json](#expected_outputjson)

## metadata.json
Fields: `dataset_name`, `dataset_version`, `sample_version`, `image_id`, `sample_id`, `annotation_version`, `annotation_timestamp`, `annotation_tool`, `review_status`, `reviewer`, `license`, `license_url`, `source`, `source_url`, `copyright`, `checksum`, `image_sha256`, `image_width`, `image_height`, `original_resolution`, `orientation`, `rotation`, `capture_device`, `camera_model`, `capture_type`, `lighting`, `weather`, `blur`, `noise`, `occlusion`, `perspective`, `scene_type`, `country`, `city`, `gps`, `text_density`, `language_distribution`, `script_distribution`.

## annotation.json
Fields: `region_id`, `bbox`, `polygon`, `rotated_bbox`, `reading_order`, `parent_region`, `child_regions`, `text`, `normalized_text`, `language`, `script`, `romanization`, `translation`, `font_style`, `font_color`, `background_color`, `vertical_text`, `handwritten`, `curved`, `occluded`, `confidence`, `entity`, `entity_type`, `entity_bbox`, `entity_region`, `region_connections`, `layout_graph`, `text_flow`, `scene_description`, `reasoning_chain`, `visual_grounding`, `qa_pairs`, `difficulty`, `benchmark_tasks`, `evaluation_targets`, `metadata`.

*(Sections for qa.json, prediction.json, score.json, report.json, failure_cases.json, expected_output.json will be expanded with snippets after the reference example is implemented).*

**Related:** [Annotation Guidelines](annotation_guidelines.md)
