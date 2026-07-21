"""
Dataset loader, schema detector, validator, and image downloader for the VLM Benchmarking Pipeline.
Supports schema-agnostic parsing, validation checking, and automated image downloading/caching.
"""

import json
import logging
import os
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
import torch
from PIL import Image, ImageOps

logger = logging.getLogger("vlm_benchmark")


class DatasetSchema:
    """Represents the auto-detected schema of the JSONL dataset."""

    def __init__(self):
        self.id_field: Optional[str] = None
        self.url_field: Optional[str] = None
        self.filename_field: Optional[str] = None
        self.caption_field: Optional[str] = None
        self.ocr_field: Optional[str] = None
        self.category_field: Optional[str] = None
        self.labels_field: Optional[str] = None
        self.metadata_fields: List[str] = []

    def __repr__(self) -> str:
        return (
            f"Schema(id_field={self.id_field}, url_field={self.url_field}, "
            f"filename_field={self.filename_field}, caption={self.caption_field}, "
            f"ocr={self.ocr_field}, category={self.category_field}, labels={self.labels_field})"
        )


class DatasetLoader:
    """Manages dataset inspection, downloading, validation, and loading."""

    def __init__(self, jsonl_path: str, images_dir: str, download_missing: bool = True):
        self.jsonl_path = Path(jsonl_path).resolve()
        self.images_dir = Path(images_dir).resolve()
        self.download_missing = download_missing
        self.schema = DatasetSchema()

        # Internal state
        self.records: List[Dict[str, Any]] = []
        self.validation_report: Dict[str, Any] = {}

        # Load and Inspect
        self.inspect_schema()
        self.load_records()

    def _detect_field(self, sample_keys: set, exact_candidates: List[str], partial_keywords: Optional[List[str]] = None) -> Optional[str]:
        """Helper to find a matching field from sample keys based on exact matches or partial keywords."""
        for cand in exact_candidates:
            if cand in sample_keys:
                return cand
        if partial_keywords:
            for k in sample_keys:
                if any(kw in k.lower() for kw in partial_keywords):
                    return k
        return None

    def inspect_schema(self) -> None:
        """Inspects the JSONL file to dynamically detect fields without assuming a schema."""
        if not self.jsonl_path.exists():
            raise FileNotFoundError(f"Dataset JSONL file not found at {self.jsonl_path}")

        # Look at the first 100 entries to determine the schema
        sample_keys = set()
        samples: List[Dict[str, Any]] = []

        with open(self.jsonl_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                try:
                    data = json.loads(line)
                    sample_keys.update(data.keys())
                    samples.append(data)
                except Exception:
                    pass
                if i >= 100:
                    break

        if not samples:
            raise ValueError(f"No valid JSON records found in {self.jsonl_path}")

        # Auto-detect fields using helper
        self.schema.id_field = self._detect_field(sample_keys, ["id", "image_id", "img_id", "key", "name"], ["id"])
        if not self.schema.id_field and sample_keys:
            self.schema.id_field = list(sample_keys)[0]

        self.schema.url_field = self._detect_field(sample_keys, ["image_url", "url", "src", "img_url", "image"], ["url", "uri"])
        self.schema.filename_field = self._detect_field(sample_keys, ["filename", "file_name", "image_path", "image", "filepath"])
        self.schema.caption_field = self._detect_field(sample_keys, ["caption", "description", "alt_text", "alt", "text"], ["caption", "desc", "alt"])
        self.schema.ocr_field = self._detect_field(sample_keys, ["ocr", "ocr_text", "text", "words", "transcription"], ["ocr", "text", "trans"])
        self.schema.category_field = self._detect_field(sample_keys, ["category", "type", "class", "genre"], ["category", "type", "class"])
        self.schema.labels_field = self._detect_field(sample_keys, ["labels", "tags", "annotations"], ["label", "tag"])

        # Determine metadata fields (all other fields)
        recognized = {
            self.schema.id_field,
            self.schema.url_field,
            self.schema.filename_field,
            self.schema.caption_field,
            self.schema.ocr_field,
            self.schema.category_field,
            self.schema.labels_field,
        }
        self.schema.metadata_fields = [
            k for k in sample_keys if k not in recognized and k is not None
        ]

        # Print Schema Info
        print(f"\n====================================")
        print(f"AUTO-DETECTED DATASET SCHEMA")
        print(f"====================================")
        print(f"Image ID Field      : {self.schema.id_field}")
        print(f"Image URL Field     : {self.schema.url_field}")
        print(f"Filename Field      : {self.schema.filename_field}")
        print(f"Caption Field       : {self.schema.caption_field}")
        print(f"OCR Field           : {self.schema.ocr_field}")
        print(f"Category Field      : {self.schema.category_field}")
        print(f"Labels Field        : {self.schema.labels_field}")
        print(f"Metadata Fields     : {self.schema.metadata_fields}")
        print(f"====================================\n")
        logger.info(f"Auto-detected schema: {self.schema}")

    def load_records(self) -> None:
        """Loads all records from the JSONL file."""
        self.records = []
        with open(self.jsonl_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                try:
                    data = json.loads(line)
                    self.records.append(data)
                except Exception as e:
                    logger.warning(
                        f"Skipping line {i} in JSONL due to parsing error: {e}"
                    )

    def validate_dataset(self) -> Dict[str, Any]:
        """Validates the dataset records, checks local files, and builds a validation report."""
        invalid_json_count = 0
        missing_metadata_count = 0
        broken_urls_count = 0
        duplicate_ids = set()
        seen_ids = set()

        # Check invalid JSON rows
        with open(self.jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    json.loads(line)
                except Exception:
                    invalid_json_count += 1

        # Iterate records for content-level validation
        for rec in self.records:
            rec_id = rec.get(self.schema.id_field) if self.schema.id_field else None
            if rec_id:
                if rec_id in seen_ids:
                    duplicate_ids.add(rec_id)
                seen_ids.add(rec_id)

            # Missing metadata check
            has_missing_meta = False
            for fld in self.schema.metadata_fields:
                if rec.get(fld) is None:
                    has_missing_meta = True
            if has_missing_meta:
                missing_metadata_count += 1

            # Check if URL looks broken (empty or doesn't start with http)
            if self.schema.url_field:
                url = rec.get(self.schema.url_field)
                if not url or not str(url).startswith(("http://", "https://")):
                    broken_urls_count += 1

        # Check local files
        self.images_dir.mkdir(parents=True, exist_ok=True)
        local_files = os.listdir(self.images_dir)
        set(local_files)

        missing_images = []
        corrupted_images = []
        valid_local_count = 0

        for rec in self.records:
            img_path = self.get_local_image_path(rec)
            if not img_path:
                missing_images.append(rec.get(self.schema.id_field, "unknown"))
                continue

            if not img_path.exists():
                missing_images.append(rec.get(self.schema.id_field, "unknown"))
            else:
                # Check if image is corrupted by opening it
                try:
                    with Image.open(img_path) as img:
                        img.verify()
                    valid_local_count += 1
                except Exception as e:
                    corrupted_images.append(img_path.name)
                    logger.error(f"Image corrupted at {img_path}: {e}")

        self.validation_report = {
            "total_records": len(self.records),
            "invalid_json_lines": invalid_json_count,
            "duplicate_ids_count": len(duplicate_ids),
            "duplicate_ids": list(duplicate_ids)[:10],
            "missing_metadata_records": missing_metadata_count,
            "broken_urls_count": broken_urls_count,
            "missing_images_count": len(missing_images),
            "missing_images": missing_images[:10],
            "corrupted_images_count": len(corrupted_images),
            "corrupted_images": corrupted_images[:10],
            "valid_local_images_count": valid_local_count,
        }

        # Save validation report
        report_path = self.jsonl_path.parent / "outputs/archive/validation_report.json"
        try:
            with open(report_path, "w", encoding="utf-8") as rf:
                json.dump(self.validation_report, rf, indent=2)
            logger.info(f"Dataset validation report saved to {report_path}")
        except Exception as e:
            logger.error(f"Failed to save validation report: {e}")

        return self.validation_report

    def get_local_image_path(self, record: Dict[str, Any]) -> Optional[Path]:
        """Determines the local path for an image in the record."""
        rec_id = record.get(self.schema.id_field)
        if not rec_id:
            return None

        # 1. Check if filename field specifies it
        if self.schema.filename_field:
            fn = record.get(self.schema.filename_field)
            if fn:
                # If absolute or relative path, check if exists
                p = Path(fn)
                if p.exists():
                    return p
                # Check in images_dir
                p = self.images_dir / p.name
                if p.exists():
                    return p

        # 2. Check by ID naming convention in images_dir: {id}.jpg, {id}.png
        extensions = [".jpg", ".png", ".jpeg", ".webp"]
        for ext in extensions:
            p = self.images_dir / f"{rec_id}{ext}"
            if p.exists():
                return p

        # 3. Check by url-decoded filename from URL in images_dir
        if self.schema.url_field:
            url = record.get(self.schema.url_field)
            if url:
                parsed_url = urllib.parse.urlparse(url)
                url_filename = os.path.basename(parsed_url.path)
                decoded_fn = urllib.parse.unquote(url_filename)

                # Check decoded filename directly
                p = self.images_dir / decoded_fn
                if p.exists():
                    return p

                # Check standard extensions
                p_id = self.images_dir / f"{rec_id}.jpg"
                return p_id

        # Default path fallback
        return self.images_dir / f"{rec_id}.jpg"

    def download_and_cache_images(self, limit: Optional[int] = None) -> None:
        """Downloads missing images from URLs and caches them locally."""
        if not self.download_missing or not self.schema.url_field:
            logger.info("Image downloading is disabled or URL field is missing.")
            return

        self.images_dir.mkdir(parents=True, exist_ok=True)
        downloaded = 0
        skipped = 0
        failed = 0

        # Determine subset to download
        records_to_process = self.records
        if limit is not None:
            records_to_process = self.records[:limit]

        print(f"Checking images for {len(records_to_process)} records...")

        for rec in records_to_process:
            rec_id = rec.get(self.schema.id_field)
            url = rec.get(self.schema.url_field)

            if not rec_id or not url:
                continue

            target_path = self.get_local_image_path(rec)
            if not target_path:
                target_path = self.images_dir / f"{rec_id}.jpg"

            # If image already exists and is not corrupted, skip download
            if target_path.exists():
                try:
                    with Image.open(target_path) as img:
                        img.verify()
                    skipped += 1
                    continue
                except Exception:
                    logger.warning(
                        f"Cached image {target_path} is corrupted. Re-downloading..."
                    )

            # Download the image
            try:
                logger.info(f"Downloading {url} -> {target_path}")
                response = requests.get(
                    url, timeout=15, headers={"User-Agent": "VLM-Benchmark/1.0"}
                )
                if response.status_code == 200:
                    with open(target_path, "wb") as f:
                        f.write(response.content)
                    # Verify download integrity
                    with Image.open(target_path) as img:
                        img.verify()
                    downloaded += 1
                else:
                    failed += 1
                    logger.error(
                        f"Failed downloading {url}: Status {response.status_code}"
                    )
            except Exception as e:
                failed += 1
                logger.error(f"Exception downloading {url}: {e}")

        print(
            f"Download complete: {downloaded} downloaded, {skipped} skipped (already cached), {failed} failed."
        )
        logger.info(
            f"Download summary: {downloaded} downloaded, {skipped} skipped, {failed} failed."
        )


class VLMDataset(torch.utils.data.Dataset):
    """Custom lazy-loading dataset for VLM Benchmarking."""

    def __init__(self, loader: DatasetLoader, max_records: Optional[int] = None):
        self.loader = loader
        self.records = loader.records
        if max_records is not None:
            self.records = self.records[:max_records]

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(
        self, idx: int
    ) -> Tuple[Image.Image, str, Dict[str, Any], Dict[str, Any]]:
        """Returns (image, image_id, metadata, original_json_row)."""
        rec = self.records[idx]
        rec_id = rec.get(self.loader.schema.id_field, f"unknown_{idx}")

        # Load image
        img_path = self.loader.get_local_image_path(rec)
        if not img_path or not img_path.exists():
            raise FileNotFoundError(f"Image for ID {rec_id} not found at {img_path}")

        try:
            image = Image.open(img_path).convert("RGB")
            # Apply EXIF rotation if present
            image = ImageOps.exif_transpose(image)
        except Exception as e:
            raise IOError(f"Failed to open image {img_path} for ID {rec_id}: {e}")

        # Construct metadata
        metadata = {}
        for fld in self.loader.schema.metadata_fields:
            metadata[fld] = rec.get(fld)
        if self.loader.schema.category_field:
            metadata["category"] = rec.get(self.loader.schema.category_field)
        if self.loader.schema.caption_field:
            metadata["ground_truth_caption"] = rec.get(self.loader.schema.caption_field)
        if self.loader.schema.ocr_field:
            metadata["ground_truth_ocr"] = rec.get(self.loader.schema.ocr_field)

        return image, str(rec_id), metadata, rec


def get_dataloader(
    loader: DatasetLoader, batch_size: int = 1, max_records: Optional[int] = None
) -> List[Tuple[Image.Image, str, Dict[str, Any], Dict[str, Any]]]:
    """
    Returns a simple iterable list for VLM loading.
    Since batching raw images of varying sizes is complex and VLMs are processed sequentially,
    we yield data items individually (batch_size=1 equivalent).
    """
    dataset = VLMDataset(loader, max_records)
    return dataset
