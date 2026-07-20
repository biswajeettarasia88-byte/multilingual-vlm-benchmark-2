import json
import os

def select_campaign(collection_plan):
    campaigns = collection_plan.get("campaigns", [])
    if not campaigns:
        return None
    return sorted(campaigns, key=lambda x: x["priority"], reverse=True)[0]

def resolve_datasets(campaign):
    return campaign.get("suggested_datasets", [])

def discover_candidates(datasets):
    # Mocking candidate discovery based on datasets
    cands = []
    for i, ds in enumerate(datasets):
        cands.append({
            "candidate_id": f"cand_{ds}_{i}",
            "dataset": ds,
            "verification_status": "PENDING"
        })
    return cands

def verify_and_score(cands):
    # Mock verification and scoring
    scored = []
    for c in cands:
        c["verification_status"] = "VERIFIED"
        c["quality_score"] = 85
        c["priority"] = 100
        c["download_status"] = "READY"
        c["license"] = "CC-BY-4.0"
        c["languages"] = ["ar"] if c["dataset"] in ["PaddleOCR-Public", "MLT-2019"] else ["en"]
        c["scripts"] = ["Arabic"] if "ar" in c["languages"] else ["Latin"]
        c["category"] = "scene_text"
        c["estimated_coverage_gain"] = 0.05
        scored.append(c)
    return scored

def filter_candidates(cands):
    return [c for c in cands if c.get("quality_score", 0) >= 80 and c.get("verification_status") == "VERIFIED"]

def build_queue(filtered_cands):
    return sorted(filtered_cands, key=lambda x: x["priority"], reverse=True)

def execute_campaign(plan_path):
    if not os.path.exists(plan_path):
        return []
    with open(plan_path, "r") as f:
        plan = json.load(f)
        
    campaign = select_campaign(plan)
    if not campaign:
        return []
        
    datasets = resolve_datasets(campaign)
    raw_cands = discover_candidates(datasets)
    scored_cands = verify_and_score(raw_cands)
    filtered = filter_candidates(scored_cands)
    queue = build_queue(filtered)
    
    return queue
