def rank_gaps(gaps):
    scored = []
    for g in gaps:
        score = g["deficit"] * 100
        # Hardcode arbitrary priorities for demo
        if g["type"] == "language" and g["key"] == "ar": score += 20
        if g["type"] == "language" and g["key"] == "hi": score += 15
        
        g["priority_score"] = score
        scored.append(g)
        
    scored.sort(key=lambda x: x["priority_score"], reverse=True)
    return scored
