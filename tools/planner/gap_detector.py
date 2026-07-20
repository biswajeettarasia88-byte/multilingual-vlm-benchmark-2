def detect_gaps(coverage_report, targets):
    total = sum(coverage_report.get("languages", {}).values())
    if total == 0:
        total = 1 # avoid zero div for empty benchmark
        
    gaps = []
    
    for lang, target_pct in targets["languages"].items():
        current_count = coverage_report.get("languages", {}).get(lang, 0)
        current_pct = current_count / total
        if current_pct < target_pct:
            gaps.append({
                "type": "language",
                "key": lang,
                "current_pct": current_pct,
                "target_pct": target_pct,
                "deficit": target_pct - current_pct
            })
            
    for cat, target_pct in targets["categories"].items():
        current_count = coverage_report.get("categories", {}).get(cat, 0)
        current_pct = current_count / total
        if current_pct < target_pct:
            gaps.append({
                "type": "category",
                "key": cat,
                "current_pct": current_pct,
                "target_pct": target_pct,
                "deficit": target_pct - current_pct
            })
            
    return gaps
