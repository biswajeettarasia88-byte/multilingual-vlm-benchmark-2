def score_candidate(candidate, verification_status, source_tier):
    score = 0
    if verification_status == "VERIFIED": score += 40
    if source_tier == "A": score += 20
    elif source_tier == "B": score += 10
    if candidate.get("license"): score += 10
    if candidate.get("language"): score += 15
    if candidate.get("category"): score += 15
    
    # Negative weights
    if candidate.get("privacy_risk"): score -= 50
    
    status = "READY" if score >= 80 and verification_status == "VERIFIED" and source_tier == "A" else "REVIEW_REQUIRED"
    return {"quality_score": max(0, score), "status": status}
