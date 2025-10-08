# Example from: docs\plans\citation_system\00_master_roadmap.md
# Index: 2
# Runnable: True
# Hash: 8a23f5e4

# Mitigation: Adjust confidence thresholds
CRITICAL_THRESHOLD = 0.9  # Increase from 0.8
manual_review_queue = [c for c in claims if c['confidence'] < CRITICAL_THRESHOLD]
# Expected: Reduce false positives from 15% to <10%