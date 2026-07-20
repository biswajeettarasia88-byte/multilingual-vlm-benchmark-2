def compute_readiness(source_scores, candidate_scores, coverage):
    # Dummy logic for M12 simulation
    avg_source = sum(s["score"] for s in source_scores) / len(source_scores) if source_scores else 0
    avg_cand = sum(c["quality_score"] for c in candidate_scores) / len(candidate_scores) if candidate_scores else 0
    
    readiness = (avg_source * 0.4) + (avg_cand * 0.4) + (min(len(coverage["languages"]), 10) * 2)
    return min(100, max(0, readiness))
