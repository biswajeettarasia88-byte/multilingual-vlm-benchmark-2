import json
import os
from tools.planner.coverage_targets import DEFAULT_TARGETS
from tools.planner.gap_detector import detect_gaps
from tools.planner.priority_scheduler import rank_gaps
from tools.planner.campaign_generator import generate_campaigns

def run_planner(coverage_path, base_dir):
    if os.path.exists(coverage_path):
        with open(coverage_path, "r") as f:
            cov = json.load(f)
    else:
        cov = {"languages": {}, "categories": {}}
        
    gaps = detect_gaps(cov, DEFAULT_TARGETS)
    ranked = rank_gaps(gaps)
    campaigns = generate_campaigns(ranked)
    
    with open(os.path.join(base_dir, "collection_plan.json"), "w") as f:
        json.dump({"campaigns": campaigns}, f, indent=2)
        
    md = ["# Priority Campaigns"]
    for c in campaigns:
        md.append(f"## {c['name']}")
        md.append(f"- **Target**: {c['target']}")
        md.append(f"- **Priority Score**: {c['priority']:.1f}")
        md.append(f"- **Suggested Datasets**: {', '.join(c['suggested_datasets'])}")
        md.append(f"- **Expected Diversity Gain**: +{c['expected_diversity_gain']*100:.1f}%")
        md.append("")
        
    with open(os.path.join(base_dir, "priority_campaigns.md"), "w") as f:
        f.write("\n".join(md))
        
    gap_md = ["# Benchmark Gap Report", "Current benchmark deficits compared to targets:"]
    for g in ranked:
        gap_md.append(f"- **{g['key']} ({g['type']})**: Target {g['target_pct']*100:.1f}%, Current {g['current_pct']*100:.1f}%, Deficit {g['deficit']*100:.1f}%")
        
    with open(os.path.join(base_dir, "benchmark_gap_report.md"), "w") as f:
        f.write("\n".join(gap_md))
        
    with open(os.path.join(base_dir, "campaign_summary.md"), "w") as f:
        f.write("# Campaign Summary\n\nSummarizing generated campaigns.")
        
    report = ["# Milestone 13 Report", "## Architecture Overview", "Gap-driven planner generated actionable campaigns."]
    with open(os.path.join(base_dir, "milestone13_report.md"), "w") as f:
        f.write("\n".join(report))
        
    print("M13 planner generated output.")
