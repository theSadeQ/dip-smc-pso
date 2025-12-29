# QW-2: Run Existing Benchmarks

**Effort**: 1 hour | **Priority**: START HERE | **ROI**: Highest visibility

## Quick Summary
Run existing pytest benchmarks for 7 controllers, generate performance matrix CSV.

## Commands
```bash
# Run all benchmarks
pytest tests/test_benchmarks/ --benchmark-only --benchmark-autosave

# Generate JSON
pytest tests/test_benchmarks/ --benchmark-only --benchmark-json=week1/results/benchmarks.json
```

## Deliverables
- week1/results/baseline_performance.csv (7 controllers × 4 metrics)
- week1/results/benchmarks.json (optional)

## Success Criteria
- [ ] Benchmarks run without errors
- [ ] Performance CSV generated
- [ ] Results saved to week1/results/

See PLAN.md Task 1 for full details.
