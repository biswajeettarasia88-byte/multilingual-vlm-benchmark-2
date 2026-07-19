# Benchmark Protocol

**Version:** 1.0.0  
**Last Updated:** 2026-07-19

**Purpose:** Define rules for evaluation and submission.  
**Scope:** Integrity, hidden sets, leaderboards.

---

## Table of Contents
1. [Hidden Test Policy](#hidden-test-policy)
2. [Evaluation Process](#evaluation-process)
3. [Submission Format](#submission-format)
4. [Leaderboard Policy](#leaderboard-policy)
5. [Versioning](#versioning)
6. [Reproducibility](#reproducibility)

## Hidden Test Policy
The test set annotations are never published.

## Evaluation Process
Predictions are submitted as JSON and scored via standard scripts.

## Submission Format
Raw model outputs mapping exactly to `expected_output.json`.

## Leaderboard Policy
Open to all models, with specific tracks for Open vs. Closed weights.

## Versioning
SemVer for code; Major.Minor for dataset milestones.

## Reproducibility
Submissions must document seeds, hyperparameters, and environment.

**Related:** [Leaderboard](leaderboard.md), [Reproducibility](reproducibility.md)
