from collections import Counter
import json

def analyze_coverage(candidates):
    langs = Counter(c.get("language") for c in candidates if c.get("language"))
    scripts = Counter(c.get("script") for c in candidates if c.get("script"))
    categories = Counter(c.get("category") for c in candidates if c.get("category"))
    datasets = Counter(c.get("dataset_name") for c in candidates if c.get("dataset_name"))
    
    return {
        "languages": dict(langs),
        "scripts": dict(scripts),
        "categories": dict(categories),
        "datasets": dict(datasets)
    }
