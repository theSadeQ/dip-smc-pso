# Research Batch Master Index

**Total Claims:** 508
**Total Batches:** 17 (7 CRITICAL + 10 HIGH)
**Generated:** 2025-10-02
**Status:** Ready for research!

---

## Quick Start

1. **Start here:** `01_CRITICAL_sliding_mode_classical/`
2. **Read workflow:** Open any batch folder → `BATCH_INFO.md` → `INSTRUCTIONS.md`
3. **Copy prompt:** `PROMPT.md` → ChatGPT
4. **Fill CSV:** Follow `INSTRUCTIONS.md` step-by-step
5. **Track progress:** `python .dev_tools/claim_extraction/citation_tracker.py`

---

## Research Strategy

### Phase 1: CRITICAL Batches (Priority 1) → ~4 hours total
**Do these FIRST! Small batches, high impact.**

- [x] **Batch 01** - Sliding Mode Classical (4 claims, ~1.0h) ✅ **COMPLETED**
- [ ] **Batch 02** - PSO Optimization (3 claims, ~0.8h)
- [ ] **Batch 03** - Control Theory General (3 claims, ~0.8h)
- [ ] **Batch 04** - Lyapunov Stability (2 claims, ~0.5h)
- [ ] **Batch 05** - Inverted Pendulum (2 claims, ~0.5h)
- [ ] **Batch 06** - Super-Twisting (2 claims, ~0.5h)
- [ ] **Batch 07** - Fault Detection (1 claim, ~0.2h)

**CRITICAL Total:** 17 claims, ~4.3 hours
**CRITICAL Progress:** 4/17 claims completed (23.5%)

---

### Phase 2: HIGH Priority Batches (Priority 2) → ~90 hours total
**Do these SECOND. Larger batches, systematic approach.**

#### Week 1: Focused Topics (~20 hours)

- [ ] **Batch 09** - Fault Detection (27 claims, ~5.4h)
- [ ] **Batch 10** - Numerical Methods (20 claims, ~4.0h)
- [ ] **Batch 11** - Sliding Mode Classical (18 claims, ~3.6h)
- [ ] **Batch 12** - Benchmarking & Performance (17 claims, ~3.4h)
- [ ] **Batch 13** - PSO Optimization (16 claims, ~3.2h)

**Week 1 Total:** 98 claims, ~19.6 hours

#### Week 2: Algorithm-Specific (~10 hours)

- [ ] **Batch 14** - Super-Twisting (13 claims, ~2.6h)
- [ ] **Batch 15** - Inverted Pendulum (11 claims, ~2.2h)
- [ ] **Batch 16** - Adaptive Control (11 claims, ~2.2h)
- [ ] **Batch 17** - Control Theory General (7 claims, ~1.4h)

**Week 2 Total:** 42 claims, ~8.4 hours

#### Special: Implementation General (Do in sub-batches)

- [ ] **Batch 08** - Implementation General (314 claims, ~63h)
  - **Strategy:** Subdivide into 6-8 smaller batches by file/module
  - **Approach:** Many claims share same citations → High reuse rate!
  - **Recommendation:** Research 10-15 unique citations, copy-paste across similar claims
  - **Estimated actual time:** ~15-20 hours with smart batching

**HIGH Priority Total:** 444 claims, ~90 hours (optimized to ~35-40 hours with batching)

---

## Batch Details

| # | Batch ID | Priority | Topic | Claims | Time | Status |
|---|----------|----------|-------|--------|------|--------|
| 1 | `01_CRITICAL_sliding_mode_classical` | CRITICAL | Sliding Mode Classical | 4 | 1.0h | ✅ **Completed** |
| 2 | `02_CRITICAL_pso_optimization` | CRITICAL | PSO Optimization | 3 | 0.8h | ⬜ Not Started |
| 3 | `03_CRITICAL_control_theory_general` | CRITICAL | Control Theory General | 3 | 0.8h | ⬜ Not Started |
| 4 | `04_CRITICAL_lyapunov_stability` | CRITICAL | Lyapunov Stability | 2 | 0.5h | ⬜ Not Started |
| 5 | `05_CRITICAL_inverted_pendulum` | CRITICAL | Inverted Pendulum | 2 | 0.5h | ⬜ Not Started |
| 6 | `06_CRITICAL_sliding_mode_super_twisting` | CRITICAL | Super-Twisting | 2 | 0.5h | ⬜ Not Started |
| 7 | `07_CRITICAL_fault_detection` | CRITICAL | Fault Detection | 1 | 0.2h | ⬜ Not Started |
| 8 | `08_HIGH_implementation_general` | HIGH | Implementation General | 314 | 62.8h | ⬜ Special (see strategy) |
| 9 | `09_HIGH_fault_detection` | HIGH | Fault Detection | 27 | 5.4h | ⬜ Not Started |
| 10 | `10_HIGH_numerical_methods` | HIGH | Numerical Methods | 20 | 4.0h | ⬜ Not Started |
| 11 | `11_HIGH_sliding_mode_classical` | HIGH | Sliding Mode Classical | 18 | 3.6h | ⬜ Not Started |
| 12 | `12_HIGH_benchmarking_performance` | HIGH | Benchmarking & Performance | 17 | 3.4h | ⬜ Not Started |
| 13 | `13_HIGH_pso_optimization` | HIGH | PSO Optimization | 16 | 3.2h | ⬜ Not Started |
| 14 | `14_HIGH_sliding_mode_super_twisting` | HIGH | Super-Twisting | 13 | 2.6h | ⬜ Not Started |
| 15 | `15_HIGH_inverted_pendulum` | HIGH | Inverted Pendulum | 11 | 2.2h | ⬜ Not Started |
| 16 | `16_HIGH_sliding_mode_adaptive` | HIGH | Adaptive Control | 11 | 2.2h | ⬜ Not Started |
| 17 | `17_HIGH_control_theory_general` | HIGH | Control Theory General | 7 | 1.4h | ⬜ Not Started |

---

## Progress Tracking

### Overall Statistics

- **Total Claims:** 461 claims (excluding Batch 08 special handling)
- **Completed:** 4 claims (0.9%)
- **In Progress:** 0 claims
- **Not Started:** 457 claims
- **Estimated Time:** ~40-50 hours (with smart citation reuse)
- **Time Spent:** ~1.0 hours (Batch 01)

### Update Progress

**To check current progress:**
```bash
cd D:\Projects\main
python .dev_tools/claim_extraction/citation_tracker.py
```

**To mark batch complete:**
1. Complete all claims in batch (fill CSV)
2. Update this file: Change ⬜ to ✅
3. Update "Completed" count above

### Citation Reuse Database

**See:** `artifacts/common_citations.md` for complete database

**Recent Additions (Batch 01):**
- **slotine1991applied** - Used 2 times in Batch 01
- **shtessel2013sliding** - Used 2 times in Batch 01

**Common citations you'll find repeatedly:**

#### Sliding Mode Control
- Slotine & Li (1991) - "Applied Nonlinear Control"
- Utkin (1992) - "Sliding Modes in Control and Optimization"
- Edwards & Spurgeon (1998) - "Sliding Mode Control: Theory and Applications"

#### Super-Twisting Algorithm
- Levant (2003) - "Higher-order sliding modes, differentiation and output-feedback control"
- Moreno & Osorio (2008) - "A Lyapunov approach to second-order sliding mode controllers"

#### PSO Optimization
- Kennedy & Eberhart (1995) - "Particle swarm optimization"
- Shi & Eberhart (1998) - "A modified particle swarm optimizer"
- Clerc & Kennedy (2002) - "The particle swarm - explosion, stability, and convergence"

#### Adaptive Control
- Ioannou & Sun (1996) - "Robust Adaptive Control"
- Åström & Wittenmark (2013) - "Adaptive Control" (2nd ed.)

#### Lyapunov Stability
- Khalil (2002) - "Nonlinear Systems" (3rd ed.)
- Slotine & Li (1991) - "Applied Nonlinear Control" (Chapter 3)

#### Inverted Pendulum
- Åström & Furuta (2000) - "Swinging up a pendulum by energy control"
- Fantoni & Lozano (2001) - "Non-linear Control for Underactuated Mechanical Systems"

**Pro Tip:** Create a "my_citations.txt" file with BibTeX entries for these common references. Copy-paste as needed!

---

## Files in Each Batch Folder

Every batch folder contains:
1. **BATCH_INFO.md** - Overview, metadata, completion checklist
2. **INSTRUCTIONS.md** - Step-by-step workflow (detailed!)
3. **PROMPT.md** - Exact ChatGPT prompt (copy-paste ready)
4. **EXPECTED_OUTPUT.md** - What ChatGPT will return (format verification)
5. **claims.json** - Technical claim data (for automation)

---

## Workflow Summary

### Daily Research Session (2-3 hours)

**Morning (5 min):**
1. Check progress: `python .dev_tools/claim_extraction/citation_tracker.py`
2. Pick next uncompleted batch from index above
3. Open batch folder

**Research Loop (2-3 hours):**
1. Read `BATCH_INFO.md` (2 min)
2. Read `INSTRUCTIONS.md` (5 min)
3. Copy `PROMPT.md` → ChatGPT (30 sec)
4. Wait for response (2-5 min)
5. Verify against `EXPECTED_OUTPUT.md` (1 min)
6. Fill CSV following `INSTRUCTIONS.md` (10-15 min)
7. Save and verify (2 min)
8. Repeat for next claim/batch!

**Evening (5 min):**
1. Save CSV (Ctrl+S)
2. Run progress tracker
3. Update this index (mark completed batches)
4. Note any reusable citations for tomorrow

---

## Tips for Efficient Research

### 1. Batch Similar Claims
- Research all "boundary layer" claims together
- Copy-paste same citation across similar techniques
- **Time savings:** 50-70%!

### 2. Use Citation Database
- Keep a running list of citations you've found
- Format: "Topic → Citation → BibTeX Key"
- Reuse instead of re-researching

### 3. ChatGPT Pro Tips
- Ask for specific sources: "Cite the ORIGINAL paper, not surveys"
- Request alternatives: "Suggest 2-3 options and explain which is best"
- Format enforcement: "Please match the exact output format requested"

### 4. Quality Checks
- Verify DOIs with CrossRef.org
- Check author names and years
- Ensure BibTeX keys are valid format

### 5. Progress Motivation
- Celebrate small wins (each batch completed!)
- Track your citation coverage increasing
- Watch the progress bar grow in tracker script

---

## Next Steps

1. **Right now:** Open `01_CRITICAL_sliding_mode_classical/`
2. **Read:** `BATCH_INFO.md` in that folder
3. **Follow:** Step-by-step instructions
4. **Complete:** First batch (~1 hour)
5. **Celebrate:** You've cited 4 claims! 🎉
6. **Continue:** Move to next batch

---

## Questions?

- **Workflow details:** See `artifacts/RESEARCH_WORKFLOW_GUIDE.md`
- **Quick start:** See `artifacts/RESEARCH_QUICKSTART.md`
- **ChatGPT prompts:** See `artifacts/chatgpt_research_prompts.md`
- **Progress tracking:** Run `python .dev_tools/claim_extraction/citation_tracker.py`

---

**Let's get started! Open batch 01 and begin researching! 🚀📚**
