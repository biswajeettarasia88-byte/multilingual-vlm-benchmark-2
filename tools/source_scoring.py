def score_source(source_meta):
    score = 0
    if source_meta.get('download_stability'): score += 20
    if source_meta.get('license_clarity'): score += 20
    if source_meta.get('research_relevance'): score += 15
    if source_meta.get('metadata_quality'): score += 15
    if source_meta.get('reproducibility'): score += 15
    if source_meta.get('multilingual'): score += 15
    
    tier = "C"
    if score >= 90: tier = "A"
    elif score >= 75: tier = "B"
    return {"score": score, "tier": tier}
