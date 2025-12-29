# Session Handoff: Citation Research System

**Status:** 9 background research batches running (41.2% complete, ~1 hour remaining)

## What's Running

```bash
# Check progress anytime:
python .dev_tools/research/check_all_batches.py

# Current: 205/497 claims researched
# Batch 1-3, 5-9: RUNNING | Batch 4: COMPLETE (0 citations - needs AI fix)
```

## When Batches Finish (Auto-detect or user says "done")

**Step 1:** Merge all 9 batch results
```bash
python .dev_tools/research/merge_all_batches.py \
  --output artifacts/research/phase1_complete.json
```

**Step 2:** Analyze quality & run Phase 2 AI enhancement (if weak claims >15%)
```bash
# Analyze
python .dev_tools/research/phase2_ai_enhancement.py \
  --analyze artifacts/research/phase1_complete.json

# Run Phase 2 (uses Claude API to fix weak queries, costs ~$0.50-1.50)
python .dev_tools/research/phase2_ai_enhancement.py \
  --input artifacts/research/phase1_complete.json \
  --output artifacts/research/phase2_final.json
```

**Step 3:** Validate & generate report
```bash
python .dev_tools/research/validate_results.py
python .dev_tools/research/generate_phase2_report.py
```

## Key Files

- **Batches:** `academic/batch_01_*.json` through `batch_09_*.json`
- **Logs:** `logs/batch_01_optimization.log` ... `batch_09_medium.log`
- **Tools:** `.dev_tools/research/` (all scripts)
- **Guide:** `docs/plans/citation_system/phase2_ai_enhancement_guide.md`

## Expected Outcome

- **Phase 1:** ~300-400 citations (60-70% coverage)
- **Phase 2 (AI-enhanced):** 700-800 citations (85%+ coverage)
- **Final:** `bibliography.bib` with 400-800 academic references

## Todo List Context

Currently 9 batches in-progress, then pending: merge → validate → report.

## Quick Commands

```bash
# Progress check
python .dev_tools/research/check_all_batches.py

# Kill all batches (if needed)
pkill -f research_pipeline.py

# Monitor Batch 1 live
tail -f logs/batch_01_optimization.log
```

**Next Action:** Wait for batches to finish (~1 hour) or check progress.
