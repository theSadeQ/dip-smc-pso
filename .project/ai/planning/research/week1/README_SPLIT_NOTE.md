# Week 1 Split Note

**Date**: October 18, 2025
**Action**: Week 1 folder split into existing vs future work

---

## What Changed?

**Week 1 originally contained 5 tasks**:
1. QW-2: Run existing benchmarks ✅ **EXISTING** (stays here)
2. QW-1: Document SMC theory ✅ **EXISTING** (stays here)
3. QW-4: Chattering metrics ✅ **EXISTING** (stays here)
4. **MT-3: Adaptive inertia PSO** ❌ **FUTURE** (moved to `.ai/planning/futurework/week1/`)
5. QW-3: Visualize PSO convergence ✅ **EXISTING** (stays here)

---

## Files Moved to Futurework

**Moved to** `.ai/planning/futurework/week1/`:
- `tasks/MT-3.md`
- `results/adaptive_pso_log.txt`
- `results/pso_adaptive_inertia_comparison.md`
- `results/run_adaptive_pso.py`

**Reason**: MT-3 implements a **new PSO algorithm** (adaptive inertia), which should be deferred until existing work complete per ROADMAP_EXISTING_PROJECT.md.

---

## Week 1 Now Contains (4 Tasks)

**EXISTING WORK ONLY**:
1. **QW-2**: Run benchmarks for existing 7 controllers
2. **QW-1**: Document existing SMC theory
3. **QW-4**: Add chattering metrics for existing controllers
4. **QW-3**: Visualize current PSO convergence

**Total**: 7 hours (reduced from 10 hours)

---

## Historical Documents Note

**IMPORTANT**: The following documents still reference MT-3 in their content:
- `PLAN.md` (lines reference 5 tasks including MT-3)
- `DAILY_LOG.md` (logs MT-3 progress)
- `COMPLETION_SUMMARY.md` (tracks MT-3 completion)
- `WEEK1_FINAL_SUMMARY.md` (may reference MT-3)

These are **historical planning documents** from the original ROADMAP.md (before split). References to MT-3 should be understood as **deferred to futurework**.

**For current work**, use:
- `.ai/planning/research/ROADMAP_EXISTING_PROJECT.md` (authoritative for existing work)
- `.ai/planning/futurework/ROADMAP_FUTURE_RESEARCH.md` (authoritative for future work)

---

## Next Steps

**Complete existing Week 1 tasks first** (QW-1, QW-2, QW-3, QW-4):
- These are foundational for all subsequent work
- See ROADMAP_EXISTING_PROJECT.md for updated plan

**MT-3 deferred until**:
- Existing 7 controllers validated
- PSO baseline established
- Research paper on existing work complete

**See**: `.ai/planning/futurework/week1/README.md` for MT-3 integration path
