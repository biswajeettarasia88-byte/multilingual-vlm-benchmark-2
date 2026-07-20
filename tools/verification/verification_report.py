import json
import os
from collections import Counter

def generate_reports(candidates, out_dir):
    stats = {
        "processed": len(candidates),
        "verified": sum(1 for c in candidates if c.get("verification_status") == "VERIFIED"),
        "partially_verified": sum(1 for c in candidates if c.get("verification_status") == "PARTIALLY_VERIFIED"),
        "review_required": sum(1 for c in candidates if c.get("verification_status") == "REVIEW_REQUIRED"),
        "failed": sum(1 for c in candidates if c.get("verification_status") == "FAILED"),
        "http_statuses": dict(Counter([c.get("http_status") for c in candidates if c.get("http_status")])),
        "content_types": dict(Counter([c.get("content_type") for c in candidates if c.get("content_type")])),
        "redirect_stats": dict(Counter([c.get("redirect_count", 0) for c in candidates])),
        "failure_reasons": dict(Counter([note for c in candidates for note in c.get("verification_notes", [])])),
        "dataset_breakdown": dict(Counter([c.get("dataset_name") for c in candidates]))
    }
    
    times = [c.get("response_time_ms", 0) for c in candidates if c.get("response_time_ms")]
    sizes = [c.get("content_length", 0) for c in candidates if c.get("content_length")]
    stats["avg_response_time_ms"] = sum(times) / len(times) if times else 0
    stats["avg_content_length"] = sum(sizes) / len(sizes) if sizes else 0
    
    with open(os.path.join(out_dir, "verification_statistics.json"), "w") as f:
        json.dump(stats, f, indent=2)
        
    failures = [c for c in candidates if c.get("verification_status") == "FAILED"]
    with open(os.path.join(out_dir, "verification_failures.json"), "w") as f:
        json.dump(failures, f, indent=2)
        
    with open(os.path.join(out_dir, "candidate_verification_report.json"), "w") as f:
        json.dump(candidates, f, indent=2)
        
    md = [
        "# Verification Summary",
        f"- **Processed**: {stats['processed']}",
        f"- **Verified**: {stats['verified']}",
        f"- **Partially Verified**: {stats['partially_verified']} (Routed to REVIEW_REQUIRED)",
        f"- **Failed**: {stats['failed']}",
        "",
        "## HTTP Statuses"
    ]
    for k, v in stats["http_statuses"].items(): md.append(f"- {k}: {v}")
    md.extend(["", "## Failure Reasons"])
    for k, v in stats["failure_reasons"].items(): md.append(f"- {k}: {v}")
    
    with open(os.path.join(out_dir, "verification_summary.md"), "w") as f:
        f.write("\n".join(md))
        
    pipeline = [
        "# Verification Pipeline Report",
        "## Architecture Overview",
        "The Candidate Verification Pipeline introduces a fast pre-flight check prior to human review and ingestion. "
        "It uses a modular `VerifierRegistry` to dispatch requests to specialized verifiers (e.g. `HttpVerifier`).",
        "",
        "## Workflow Diagram",
        "```mermaid",
        "graph TD",
        "A[Discovery] --> B[Candidate Verification]",
        "B --> C[Human Review]",
        "C --> D[Controlled Ingestion]",
        "D --> E[Validation]",
        "E --> F[Manifest Update]",
        "```",
        "",
        "## Verification Policy",
        "- Prefer `HEAD` requests for speed. Fall back to lightweight `GET`.",
        "- Restrict MIME types to `image/*`.",
        "- A candidate receives `READY` if and only if its status is `VERIFIED`.",
        "- `PARTIALLY_VERIFIED` candidates are routed to `REVIEW_REQUIRED`.",
        "",
        "## Performance Metrics",
        f"- **Average Response Time**: {stats['avg_response_time_ms']:.1f} ms",
        f"- **Average Content Length**: {stats['avg_content_length']:.0f} bytes",
        "",
        "## Recommendations for Milestone 12",
        "Deploy this hardened verification logic on the next scale-out discovery campaign to drastically reduce the 404/Connection Error rejection rates seen during ingestion."
    ]
    with open(os.path.join(out_dir, "verification_pipeline_report.md"), "w") as f:
        f.write("\n".join(pipeline))
