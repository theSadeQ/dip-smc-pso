# Research Batches - Organized Citation Research System

**Your Question:** Create folder init for each group with exact prompts, expected outputs, and detailed instructions

**Your Answer:** ✅ Complete! 17 batch folders ready with 5 files each!

---

## What You Got

### 📁 Folder Structure

```
research_batches/
├── _BATCH_INDEX.md              ← START HERE! Master index with progress tracking
├── _AUTOMATION/
│   └── generate_batch_folders.py  ← Script that created all this
│
├── 01_CRITICAL_sliding_mode_classical/
│   ├── BATCH_INFO.md            ← Read first: overview & metadata
│   ├── INSTRUCTIONS.md          ← Step-by-step workflow
│   ├── PROMPT.md                ← Exact ChatGPT prompt (copy-paste!)
│   ├── EXPECTED_OUTPUT.md       ← What ChatGPT returns
│   └── claims.json              ← Claim data (technical)
│
├── 02_CRITICAL_pso_optimization/
│   └── [same 5 files]
│
├── 03-07_CRITICAL_*/            ← 5 more CRITICAL batches
│   └── [same 5 files each]
│
└── 08-17_HIGH_*/                ← 10 HIGH priority batches
    └── [same 5 files each]
```

**Total:** 17 batch folders × 5 files = 85 files ready for research!

---

## Quick Start (5 Minutes to First Citation!)

### Step 1: Open Master Index (1 minute)
```bash
# Open this file:
start artifacts/research_batches/_BATCH_INDEX.md
```

### Step 2: Choose First Batch (30 seconds)
Start with: `01_CRITICAL_sliding_mode_classical/`
(Only 4 claims, ~1 hour total)

### Step 3: Read Batch Files (2 minutes)
1. Open `01_CRITICAL_sliding_mode_classical/BATCH_INFO.md` → Overview
2. Open `INSTRUCTIONS.md` → Follow step-by-step

### Step 4: Copy Prompt to ChatGPT (30 seconds)
1. Open `PROMPT.md`
2. Copy everything after "COPY EVERYTHING BELOW THIS LINE"
3. Paste to ChatGPT

### Step 5: Fill CSV (10-15 minutes)
Follow `INSTRUCTIONS.md` exactly:
- Get ChatGPT response
- Verify format against `EXPECTED_OUTPUT.md`
- Fill 6 columns in CSV for each claim
- Save

**🎉 Done! First 4 claims cited!**

---

## What's in Each Batch Folder?

Every folder has EXACTLY 5 files:

### 1. BATCH_INFO.md (Overview)
- Claim count and time estimate
- Claims summary table
- Suggested citations (pre-research)
- Completion checklist
- **Read this FIRST!**

### 2. INSTRUCTIONS.md (Step-by-Step)
- Prerequisites (what to open)
- Step 1-7 detailed workflow
- Excel tips for CSV filling
- Success criteria
- Troubleshooting guide
- **Your main guide!**

### 3. PROMPT.md (ChatGPT Prompt)
- Exact copy-paste ready prompt
- All claims pre-filled
- Suggested starting references
- Output format requirements
- **Copy to ChatGPT!**

### 4. EXPECTED_OUTPUT.md (Format Verification)
- Example of what ChatGPT returns
- Format checklist
- What to do if format is wrong
- **Verify response!**

### 5. claims.json (Technical Data)
- Machine-readable claim data
- For automation/scripting
- **Optional reading**

---

## Research Strategy

### Phase 1: CRITICAL Batches (Week 1, ~4 hours)

Do these FIRST! Small, high-impact batches:

| Batch | Topic | Claims | Time |
|-------|-------|--------|------|
| 01 | Sliding Mode Classical | 4 | 1.0h |
| 02 | PSO Optimization | 3 | 0.8h |
| 03 | Control Theory General | 3 | 0.8h |
| 04 | Lyapunov Stability | 2 | 0.5h |
| 05 | Inverted Pendulum | 2 | 0.5h |
| 06 | Super-Twisting | 2 | 0.5h |
| 07 | Fault Detection | 1 | 0.2h |

**Total:** 17 claims, ~4 hours → 80% coverage for critical theorems!

### Phase 2: HIGH Batches (Weeks 2-4, ~35-40 hours)

Systematic research with citation reuse:

**Week 2: Focused Topics** (~20 hours)
- Batches 09-13: Fault detection, numerical methods, SMC, benchmarking, PSO

**Week 3: Algorithm-Specific** (~10 hours)
- Batches 14-17: Super-twisting, pendulum, adaptive, control theory

**Week 4: Implementation General** (~15-20 hours optimized)
- Batch 08: 314 claims → Subdivide + high citation reuse!

**Total:** 444 claims, ~35-40 hours with batching → 90%+ overall coverage!

---

## Key Features

### ✅ Zero Ambiguity
- **Exact prompts:** Copy-paste ready, no guessing
- **Exact outputs:** Know what ChatGPT will return
- **Exact columns:** 6 tracking columns clearly specified
- **Exact workflow:** Step-by-step instructions (7 steps)

### ✅ Self-Contained
- Each folder = complete research package
- No hunting for instructions across files
- No context switching
- All info in one place

### ✅ Progress Tracking
- Master index with checkboxes
- Automated tracker script
- Time estimates vs actual
- Citation reuse metrics

### ✅ Efficiency Boosters
- Pre-suggested citations per topic
- Citation reuse database in master index
- Batch similar claims together
- Smart ChatGPT prompts for alternatives

---

## Workflow Example

### Daily Research Session (2-3 hours)

**Morning (5 min):**
```bash
# 1. Check progress
python .dev_tools/claim_extraction/citation_tracker.py

# 2. Open master index
start artifacts/research_batches/_BATCH_INDEX.md

# 3. Pick next batch (use checkboxes)
cd artifacts/research_batches/01_CRITICAL_sliding_mode_classical/
```

**Research Loop (2-3 hours):**
1. Read `BATCH_INFO.md` (2 min)
2. Read `INSTRUCTIONS.md` (5 min)
3. Copy `PROMPT.md` → ChatGPT (30 sec)
4. Get response (2-5 min)
5. Verify against `EXPECTED_OUTPUT.md` (1 min)
6. Fill CSV (10-15 min per batch)
7. Save and verify (2 min)

**Evening (5 min):**
```bash
# 1. Save CSV
# 2. Run tracker
python .dev_tools/claim_extraction/citation_tracker.py

# 3. Update master index (check off completed batch)
# 4. Note reusable citations for tomorrow
```

---

## Time Estimates vs Reality

### Estimated (Conservative)
- CRITICAL: 4 hours
- HIGH: 90 hours
- **Total:** ~94 hours

### Optimized (With Citation Reuse)
- CRITICAL: 3-4 hours
- HIGH: 25-30 hours
- **Total:** ~30-35 hours

**Efficiency gain:** 60-65% time savings!

**How?**
1. **Citation reuse:** Same citation used 10-20 times
2. **Batching:** Research similar claims together
3. **Smart prompts:** ChatGPT suggests multiple claims at once
4. **Learning curve:** Get faster after first few batches

---

## Common Citations (Save These!)

You'll use these REPEATEDLY across batches:

### Sliding Mode Control
- Slotine & Li (1991) - `slotine1991applied`
- Utkin (1992) - `utkin1992sliding`
- Edwards & Spurgeon (1998) - `edwards1998sliding`

### Super-Twisting
- Levant (2003) - `levant2003higher`
- Moreno & Osorio (2008) - `moreno2008lyapunov`

### PSO
- Kennedy & Eberhart (1995) - `kennedy1995particle`
- Shi & Eberhart (1998) - `shi1998modified`

### Adaptive Control
- Ioannou & Sun (1996) - `ioannou1996robust`
- Åström & Wittenmark (2013) - `astrom2013adaptive`

### Lyapunov
- Khalil (2002) - `khalil2002nonlinear`

**Pro Tip:** Create `my_citations.txt` with full BibTeX entries for quick lookup!

---

## Success Metrics

Track your progress with these metrics:

### Citation Coverage
- **Current:** 5.3% (27/508 claims)
- **After CRITICAL:** ~15% (75/508 claims)
- **After HIGH:** ~90% (460/508 claims)
- **Target:** 80%+ for publication!

### Citation Reuse Rate
- **Target:** 50%+ reuse rate
- **Meaning:** Find 100 unique citations → Cite 200+ claims
- **Benefit:** 2× efficiency!

### Time Efficiency
- **Individual research:** 20-30 min/claim × 508 = 170-250 hours
- **Batched research:** 5-10 min/claim × 508 = 40-85 hours
- **Your savings:** ~130-165 hours!

---

## Troubleshooting

### Q: ChatGPT response doesn't match EXPECTED_OUTPUT.md format?
**A:** Ask ChatGPT: *"Please reformat to match the exact structure requested in the prompt"*

### Q: Can't find claim in CSV?
**A:** Use Ctrl+F to search for Claim_ID (case-sensitive)

### Q: Citations seem generic or irrelevant?
**A:** Ask ChatGPT: *"Can you suggest more specific citations for [technique] and explain why?"*

### Q: Excel crashed before saving?
**A:** You saved ChatGPT response to .txt file, right? Resume from there!

### Q: How do I know when batch is complete?
**A:** Run `python .dev_tools/claim_extraction/citation_tracker.py` → Should show 100% for that batch

---

## Next Steps

### Right Now (5 minutes)
1. Open `_BATCH_INDEX.md`
2. Read the research strategy
3. Open `01_CRITICAL_sliding_mode_classical/`
4. Read `BATCH_INFO.md` → `INSTRUCTIONS.md`

### This Week (4 hours)
1. Complete all 7 CRITICAL batches
2. Track progress with citation tracker
3. Build your citation database

### Next 2-3 Weeks (30-40 hours)
1. Complete HIGH priority batches
2. Subdivide Batch 08 into manageable chunks
3. Celebrate reaching 80%+ coverage! 🎉

---

## Additional Resources

- **Master Index:** `_BATCH_INDEX.md` (progress tracking)
- **Workflow Guide:** `../RESEARCH_WORKFLOW_GUIDE.md` (comprehensive)
- **Quick Start:** `../RESEARCH_QUICKSTART.md` (5-minute intro)
- **ChatGPT Prompts:** `../chatgpt_research_prompts.md` (templates)
- **Progress Tracker:** `.dev_tools/claim_extraction/citation_tracker.py`
- **CSV File:** `../claims_research_tracker.csv` (your work file)

---

## Questions?

- **How does this work?** Read `RESEARCH_WORKFLOW_GUIDE.md`
- **Where do I start?** Open `_BATCH_INDEX.md` → Batch 01
- **What's my progress?** Run `citation_tracker.py`
- **How to use ChatGPT?** See `chatgpt_research_prompts.md`

---

**Everything is ready! Open _BATCH_INDEX.md and start researching! 🚀📚**

**Generated:** 2025-10-02
**System Version:** Citation Research Batch System v1.0
**Total Files Created:** 85 files (17 batches × 5 files)
**Total Claims:** 461 claims (ready for systematic research)
