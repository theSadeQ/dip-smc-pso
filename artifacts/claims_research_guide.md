# Claims Research Tracker - Usage Guide

**File:** `artifacts/claims_research_tracker.csv`
**Total Claims:** 508
**Format:** UTF-8 CSV (Excel/Google Sheets compatible)

---

## Quick Start (5 Minutes to First Citation!)

### 1. Open the CSV
- **Excel:** Double-click `claims_research_tracker.csv`
- **Google Sheets:** File → Import → Upload file

### 2. Filter for CRITICAL Claims
1. Click on "Priority" column header
2. Filter → Show only "CRITICAL"
3. You'll see 11 uncited theorems/lemmas (highest priority!)

### 3. Research Your First Claim
**Example: FORMAL-THEOREM-001**
- **Description:** "Hysteresis with deadband δ prevents oscillation..."
- **File:** `docs/fdi_threshold_calibration_methodology.md:261`

**Research Steps:**
1. Google Scholar search: `"hysteresis deadband oscillation" control systems`
2. Find relevant paper (e.g., "Hysteresis-based switching algorithms for supervisory control")
3. Fill in CSV:
   - `Research_Status`: "in_progress"
   - `Suggested_Citation`: "Hespanha et al. (2003)"
   - `BibTeX_Key`: "hespanha2003hysteresis"
   - `DOI_or_URL`: "10.1109/TAC.2003.812777"
   - `Reference_Type`: "journal"
   - `Research_Notes`: "IEEE TAC, proves oscillation prevention"
4. Update `Research_Status` to "completed"

---

## CSV Structure

### Column Groups

#### **Filter/Sort Columns (Left Side)**
| Column | Purpose | Your Action |
|--------|---------|-------------|
| `Priority` | CRITICAL/HIGH/MEDIUM | Sort by this first |
| `Research_Status` | Track progress | Fill: empty → in_progress → completed |
| `Category` | theoretical/implementation | Filter to group similar claims |
| `Type` | theorem/lemma/implementation | Helps identify claim nature |
| `Has_Citation` | YES/NO | Shows if citation exists |

#### **Identification**
| Column | Purpose |
|--------|---------|
| `Claim_ID` | Unique identifier (e.g., FORMAL-THEOREM-001) |

#### **Research Content**
| Column | Purpose |
|--------|---------|
| `Research_Description` | Short summary for quick scanning |
| `Full_Claim_Text` | Full claim text (truncated at 300 chars) |

#### **Research Tracking (YOU FILL THESE!)**
| Column | What to Enter | Example |
|--------|---------------|---------|
| `Research_Status` | empty/in_progress/completed | "completed" |
| `Suggested_Citation` | Author (Year) format | "Levant (2003)" |
| `BibTeX_Key` | Citation key for .bib file | "levant2003higher" |
| `DOI_or_URL` | Digital Object Identifier or URL | "10.1109/TAC.2003.812777" |
| `Reference_Type` | journal/conference/book/arxiv/website | "journal" |
| `Research_Notes` | Any notes | "Proves finite-time convergence" |

#### **Location Info (Reference)**
| Column | Purpose |
|--------|---------|
| `File_Path` | Where the claim appears |
| `Line_Number` | Exact line in file |
| `Scope` | Code scope (for implementation claims) |

#### **Metadata**
| Column | Purpose |
|--------|---------|
| `Existing_Citation_Format` | If already cited, what format |
| `Confidence` | Extraction confidence (0.0-1.0) |

---

## Research Workflow

### Phase 1: CRITICAL Claims (11 claims, ~2-3 hours)
**Priority:** Uncited theorems and lemmas (scientific validity risk)

1. **Filter:** `Priority = CRITICAL`
2. **Focus:** Mathematical proofs, convergence theorems, stability claims
3. **Keywords to search:**
   - "sliding mode control theorem"
   - "Lyapunov stability finite-time"
   - "super-twisting convergence proof"
   - "PSO global optimization"

4. **Good Sources:**
   - IEEE Transactions on Automatic Control
   - Automatica
   - International Journal of Control
   - Conference: CDC, ACC, IFAC

### Phase 2: HIGH Claims (459 claims, ~20-30 hours)
**Priority:** Uncited implementation claims (reproducibility risk)

**Strategy: Batch Similar Claims**

1. **Filter by algorithm type:**
   - `Research_Description` contains "sliding mode" → Research SMC literature
   - `Research_Description` contains "PSO" → Research PSO optimization
   - `Research_Description` contains "adaptive" → Research adaptive control

2. **Reuse Citations:**
   - Many claims reference same papers!
   - Example: All super-twisting claims likely cite Levant (2003)
   - Example: All PSO claims likely cite Kennedy & Eberhart (1995)

3. **Common References:**
   - **Classical SMC:** Slotine & Li (1991), Utkin (1992)
   - **Super-Twisting:** Levant (2003, 2005), Moreno & Osorio (2012)
   - **Adaptive SMC:** Slotine & Li (1987), Plestan et al. (2010)
   - **PSO:** Kennedy & Eberhart (1995), Shi & Eberhart (1998)
   - **Inverted Pendulum:** Åström & Furuta (2000), Graichen et al. (2007)

### Phase 3: MEDIUM Claims (38 claims, ~1-2 hours)
**Priority:** Validate existing citations (quality check)

1. **Filter:** `Priority = MEDIUM`
2. **Action:** Verify existing citations are correct
3. **Check:** BibTeX entries exist, DOI is valid, citation format matches

---

## Research Tips

### Finding Papers Efficiently

1. **Google Scholar** (https://scholar.google.com)
   - Search: `"exact phrase" author:levant year:2003`
   - Click "Cite" → Get BibTeX

2. **arXiv** (https://arxiv.org)
   - Great for preprints
   - Search: `ti:sliding mode control`

3. **IEEE Xplore** (https://ieeexplore.ieee.org)
   - Best for control theory
   - Filter by journal: Transactions on Automatic Control

4. **DOI Lookup** (https://doi.org)
   - If you have DOI, get full citation

### BibTeX Key Naming Convention

**Format:** `firstauthor_year_keyword`

**Examples:**
- `levant2003higher` → Levant (2003) "Higher-order sliding modes..."
- `slotine1991applied` → Slotine & Li (1991) "Applied Nonlinear Control"
- `kennedy1995pso` → Kennedy & Eberhart (1995) "Particle swarm optimization"
- `moreno2012strict` → Moreno & Osorio (2012) "Strict Lyapunov..."

### Common Pitfalls

❌ **Don't do this:**
- Leaving `Research_Status` empty when done (you'll forget what's complete!)
- Using inconsistent citation formats (use Author (Year) always)
- Forgetting to note DOI (you'll need it for BibTeX)
- Not reusing citations (waste of time!)

✅ **Do this:**
- Update `Research_Status` immediately: empty → in_progress → completed
- Copy-paste BibTeX directly from Google Scholar
- Note reference type (helps organize .bib file later)
- Search similar claims before researching (reuse citations!)

---

## Excel Tips & Tricks

### Filtering for Efficiency

**Filter by Priority (recommended order):**
```
1. CRITICAL → Research all 11 first
2. HIGH + Filter "sliding mode" → Batch research SMC
3. HIGH + Filter "PSO" → Batch research optimization
4. MEDIUM → Validate existing
```

**Filter by Research Status:**
```
- Empty → Not started
- "in_progress" → Continue where you left off
- "completed" → Skip these
```

### Conditional Formatting (Visual Progress)

1. Select `Research_Status` column
2. Home → Conditional Formatting → Highlight Cell Rules
3. Set colors:
   - "completed" → Green
   - "in_progress" → Yellow
   - Empty → Red

### Formulas for Progress Tracking

**Add a progress summary at top:**
```
=COUNTIF(B:B,"completed") & " / " & COUNTA(B:B)-1 & " completed"
```

---

## Example Research Session (15 Minutes)

### Claim: FORMAL-THEOREM-004
**Description:** "PSO-optimized gains ensure global asymptotic stability..."
**File:** `docs/pso_gain_bounds_mathematical_foundations.md:733`

**Research Steps:**

1. **Google Scholar Search:**
   ```
   "PSO optimization" "global stability" "inverted pendulum"
   ```

2. **Found Paper:**
   - Title: "Stability analysis of PSO-based adaptive control"
   - Author: Li et al. (2015)
   - Journal: IEEE Transactions on Cybernetics

3. **Fill CSV:**
   ```
   Research_Status: completed
   Suggested_Citation: Li et al. (2015)
   BibTeX_Key: li2015stability
   DOI_or_URL: 10.1109/TCYB.2014.2354911
   Reference_Type: journal
   Research_Notes: Proves global stability for PSO-tuned controllers
   ```

4. **Save BibTeX to notes:**
   ```bibtex
   @article{li2015stability,
     title={Stability analysis of PSO-based adaptive control},
     author={Li, Yun and Ang, Keng Hwee and Chong, Gregory CY},
     journal={IEEE Transactions on Cybernetics},
     year={2015},
     doi={10.1109/TCYB.2014.2354911}
   }
   ```

**Time:** ~3 minutes per claim (once you get the hang of it!)

---

## Output for Phase 2 (AI Citation Integration)

Once you complete the CSV research, the data will be used to:

1. **Generate BibTeX entries** automatically
2. **Update documentation** with proper citations
3. **Validate** citation coverage
4. **Create** unified references.bib file

**Your CSV research** → **Automated citation insertion** → **80%+ coverage!**

---

## Progress Tracking

### Daily Goals (Suggested)

**Day 1:** CRITICAL claims (11 claims) → ~3 hours
**Day 2-4:** HIGH claims - SMC related (~150 claims) → ~3 hours/day
**Day 5-7:** HIGH claims - PSO/optimization (~150 claims) → ~3 hours/day
**Day 8-10:** HIGH claims - remaining (~159 claims) → ~3 hours/day
**Day 11:** MEDIUM validation (38 claims) → ~2 hours

**Total Time:** ~25-30 hours over 2 weeks

### Milestones

- ✅ **Milestone 1:** CRITICAL claims complete (11/11)
- ✅ **Milestone 2:** 100 HIGH claims researched
- ✅ **Milestone 3:** 250 HIGH claims researched
- ✅ **Milestone 4:** All HIGH claims complete (459/459)
- ✅ **Milestone 5:** MEDIUM validation complete (38/38)
- ✅ **Phase 2 Ready:** CSV complete, ready for automated citation insertion

---

## Support & Questions

**Common Questions:**

**Q: Can't find a citation for a claim?**
A: Mark `Research_Status: in_progress`, add `Research_Notes: "No direct citation found"`, move on. We'll consolidate later.

**Q: Found multiple possible citations?**
A: Choose the most authoritative (IEEE/Automatica preferred), note others in `Research_Notes`.

**Q: Claim seems wrong/invalid?**
A: Note in `Research_Notes: "Claim validation needed"` - we'll review in Phase 2.

**Q: How detailed should Research_Notes be?**
A: Brief! Just key info: "Main theorem paper" or "Survey article, page 45" or "arXiv preprint only".

---

## Next Steps After CSV Completion

1. **Save your completed CSV** (keep original as backup)
2. **Submit for Phase 2** (AI-assisted citation insertion)
3. **Review generated BibTeX** entries
4. **Validate documentation** updates
5. **Final quality check** → 80%+ citation coverage achieved!

---

**Happy Researching! You've got this! 🔬📚**

**Quick Stats:**
- Start: 5.3% citation coverage (27/508)
- Target: 80%+ citation coverage (~400/508)
- Your Impact: +373 new citations for scientific rigor!
