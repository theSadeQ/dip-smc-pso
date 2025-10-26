# MT-3: Adaptive Inertia PSO

**Effort**: 3 hours | **Priority**: HIGHEST ROI | **Impact**: 30% faster convergence

## Quick Summary
Implement time-varying inertia w(t) = w_max - (w_max - w_min) * t/T for PSO.

## Discovery
✅ Adaptive inertia ALREADY IMPLEMENTED via `pso_cfg.w_schedule` (lines 862-894)!

## Task
1. Check if `w_schedule` in config.yaml
2. If missing, add: `w_schedule: [0.9, 0.4]`
3. Run comparison tests (fixed vs adaptive)
4. Document 30% speedup

## Tests
```bash
# Fixed inertia baseline
python simulate.py --ctrl classical_smc --run-pso --save week1/results/gains_fixed_inertia.json

# Adaptive inertia (add w_schedule to config first)
python simulate.py --ctrl classical_smc --run-pso --save week1/results/gains_adaptive_inertia.json
```

## Expected Results
- Fixed: 50 generations, cost ~0.0245
- Adaptive: 35 generations, cost ~0.0243
- **Speedup: 30%** (15 fewer generations)

## Success Criteria
- [ ] w_schedule configured
- [ ] ≥20% speedup achieved
- [ ] Solution quality maintained
- [ ] Results documented

See PLAN.md Task 4 for full details.
