def generate_campaigns(ranked_gaps):
    campaigns = []
    for i, gap in enumerate(ranked_gaps):
        name = f"Campaign_{chr(65+i)}"
        target = f"{gap['key']} ({gap['type']})"
        campaigns.append({
            "name": name,
            "target": target,
            "priority": gap["priority_score"],
            "suggested_datasets": ["PaddleOCR-Public", "MLT-2019"] if gap['type'] == 'language' else ["FUNSD", "CORD"],
            "expected_diversity_gain": gap["deficit"]
        })
    return campaigns
