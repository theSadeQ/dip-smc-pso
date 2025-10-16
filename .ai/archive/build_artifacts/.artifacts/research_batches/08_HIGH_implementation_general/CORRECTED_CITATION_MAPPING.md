# Batch 08 - Corrected Citation Mapping

**Purpose:** Quick reference guide for correcting the 15 severe/critical citation mismatches
**Status:** Ready for CSV integration
**Verification:** Based on automated source code analysis

---

## Critical Mismatches (2 Claims) - Fix Immediately

| Claim ID | File:Line | Incorrect Citation | Correct Citation | Rationale |
|----------|-----------|-------------------|------------------|-----------|
| CODE-IMPL-086 | trial_runner.py:105 | Utkin (1977) - SMC | **No citation needed** (software pattern) | Factory pattern for simulation trials, not SMC theory |
| CODE-IMPL-109 | threading.py:180 | Levant (2003) - Super-Twisting | **No citation needed** (software pattern) | Deadlock detection code, not control algorithm |

**Alternative:** If citations required for software patterns, use:
- CODE-IMPL-086: Gamma et al. (1995) "Design Patterns" (factory pattern)
- CODE-IMPL-109: Goetz et al. (2006) "Java Concurrency in Practice" (deadlock detection)

---

## Severe Mismatches (13 Claims) - High Priority

### Group 1: Cross-Validation (3 claims)

| Claim ID | File:Line | Incorrect | Correct |
|----------|-----------|-----------|---------|
| CODE-IMPL-063 | cross_validation.py:1 | Shapiro & Wilk (1965) | **Stone (1978)** - Cross-validation |
| CODE-IMPL-064 | cross_validation.py:92 | Shapiro & Wilk (1965) | **Stone (1978)** - Cross-validation |
| CODE-IMPL-066 | cross_validation.py:317 | Shapiro & Wilk (1965) | **Stone (1978)** - Cross-validation |

**Citation:**
```bibtex
@article{stone1978cross,
  title={Cross-validatory choice and assessment of statistical predictions},
  author={Stone, Mervyn},
  journal={Journal of the Royal Statistical Society: Series B (Methodological)},
  volume={36},
  number={2},
  pages={111--147},
  year={1978},
  doi={10.1080/02331887808801414}
}
```

---

### Group 2: Outlier Detection (1 claim)

| Claim ID | File:Line | Incorrect | Correct |
|----------|-----------|-----------|---------|
| CODE-IMPL-029 | threshold_adapters.py:152 | Efron & Tibshirani (1993) | **Barnett & Lewis (1994)** - Outlier Detection |

**Citation:** (Already in correct list, just reassign)
```bibtex
@book{barnett1994outliers,
  title={Outliers in statistical data},
  author={Barnett, Vic and Lewis, Toby},
  year={1994},
  publisher={Wiley},
  doi={10.1002/bimj.4710370219}
}
```

---

### Group 3: Super-Twisting Controller (5 claims)

| Claim ID | File:Line | Incorrect | Correct |
|----------|-----------|-----------|---------|
| CODE-IMPL-168 | super_twisting/controller.py:315 | Goldberg (1989) | **Levant (2003)** - Super-Twisting |
| CODE-IMPL-169 | super_twisting/controller.py:375 | Goldberg (1989) | **Levant (2003)** - Super-Twisting |
| CODE-IMPL-173 | super_twisting/twisting_algorithm.py:121 | Goldberg (1989) | **Levant (2003)** - Super-Twisting |
| CODE-IMPL-174 | super_twisting/twisting_algorithm.py:146 | Goldberg (1989) | **Levant (2003)** - Super-Twisting |
| CODE-IMPL-175 | super_twisting/twisting_algorithm.py:271 | Goldberg (1989) | **Levant (2003)** - Super-Twisting |

**Citation:** (Already in source list, just reassign)
```bibtex
@article{levant2003higher,
  title={Higher-order sliding modes, differentiation and output-feedback control},
  author={Levant, Arie},
  journal={International Journal of Control},
  volume={76},
  number={9-10},
  pages={924--941},
  year={2003},
  doi={10.1080/0020717031000099029}
}
```

---

### Group 4: SMC Sliding Surfaces (4 claims)

| Claim ID | File:Line | Incorrect | Correct |
|----------|-----------|-----------|---------|
| CODE-IMPL-186 | sliding_surface.py:132 | Camacho & Bordons (2013) | **Utkin (1977)** - Sliding Mode Control |
| CODE-IMPL-189 | switching_functions.py:22 | Camacho & Bordons (2013) | **Utkin (1977)** - Sliding Mode Control |
| CODE-IMPL-190 | switching_functions.py:38 | Camacho & Bordons (2013) | **Utkin (1977)** - Sliding Mode Control |
| CODE-IMPL-191 | switching_functions.py:56 | Camacho & Bordons (2013) | **Utkin (1977)** - Sliding Mode Control |

**Citation:** (Already in source list, just reassign)
```bibtex
@article{utkin1977variable,
  title={Variable structure systems with sliding modes},
  author={Utkin, Vadim Ivanovich},
  journal={IEEE Transactions on Automatic Control},
  volume={22},
  number={2},
  pages={212--222},
  year={1977},
  doi={10.1109/TAC.1977.1101446}
}
```

---

## Moderate Priority (Select Corrections)

### Stability Analysis Claims (Sample of 29)

**Many stability metrics incorrectly cited to statistical methods papers.**

**Recommended Addition:** Khalil "Nonlinear Systems" for stability analysis

```bibtex
@book{khalil2002nonlinear,
  title={Nonlinear Systems},
  author={Khalil, Hassan K},
  edition={3},
  year={2002},
  publisher={Prentice Hall},
  note={Standard reference for Lyapunov stability, convergence analysis}
}
```

**Sample Claims Needing This:**
- CODE-IMPL-047, 068, 083 (currently cited to Efron, Shapiro, Cohen)
- Actual content: Stability metrics, variance analysis, convergence monitoring

---

### Software Patterns (8 claims)

**These may not need academic citations (implementation details)**

| Claim IDs | Topic | Current (Wrong) | Recommendation |
|-----------|-------|----------------|----------------|
| CODE-IMPL-220, 221, 222, 223 | Factory patterns, serialization | Barnett (outlier detection) | **No citation needed** OR cite "Design Patterns" book |
| CODE-IMPL-224, 225, 226, 227 | Factory resilience | Efron (bootstrap) | **No citation needed** OR cite fault-tolerance references |

---

## Verification Status Summary

| Status | Count | Action Required |
|--------|-------|-----------------|
| ✅ Correct (no change) | 112 | None |
| 🚨 Critical Fix | 2 | Remove or replace citations |
| ❌ Severe Fix | 13 | Replace with correct citations (list above) |
| ⚠️ Moderate Review | 116 | Manual review recommended |
| ❓ Uncertain | 71 | Determine if citation needed |

---

## CSV Update Script Template

```python
import pandas as pd

# Load CSV
df = pd.read_csv('claims_research_tracker.csv')

# Critical fixes (remove citations)
critical_fixes = {
    'CODE-IMPL-086': {'Suggested_Citation': '', 'BibTeX_Key': '', 'Research_Notes': 'Implementation pattern - no citation needed'},
    'CODE-IMPL-109': {'Suggested_Citation': '', 'BibTeX_Key': '', 'Research_Notes': 'Implementation pattern - no citation needed'},
}

# Severe fixes (replace citations)
severe_fixes = {
    # Cross-validation group
    'CODE-IMPL-063': {'Suggested_Citation': 'Stone (1978)', 'BibTeX_Key': 'stone1978cross'},
    'CODE-IMPL-064': {'Suggested_Citation': 'Stone (1978)', 'BibTeX_Key': 'stone1978cross'},
    'CODE-IMPL-066': {'Suggested_Citation': 'Stone (1978)', 'BibTeX_Key': 'stone1978cross'},

    # Outlier detection
    'CODE-IMPL-029': {'Suggested_Citation': 'Barnett & Lewis (1994)', 'BibTeX_Key': 'barnett1994outliers'},

    # Super-twisting group
    'CODE-IMPL-168': {'Suggested_Citation': 'Levant (2003)', 'BibTeX_Key': 'levant2003higher'},
    'CODE-IMPL-169': {'Suggested_Citation': 'Levant (2003)', 'BibTeX_Key': 'levant2003higher'},
    'CODE-IMPL-173': {'Suggested_Citation': 'Levant (2003)', 'BibTeX_Key': 'levant2003higher'},
    'CODE-IMPL-174': {'Suggested_Citation': 'Levant (2003)', 'BibTeX_Key': 'levant2003higher'},
    'CODE-IMPL-175': {'Suggested_Citation': 'Levant (2003)', 'BibTeX_Key': 'levant2003higher'},

    # SMC sliding surfaces
    'CODE-IMPL-186': {'Suggested_Citation': 'Utkin (1977)', 'BibTeX_Key': 'utkin1977variable'},
    'CODE-IMPL-189': {'Suggested_Citation': 'Utkin (1977)', 'BibTeX_Key': 'utkin1977variable'},
    'CODE-IMPL-190': {'Suggested_Citation': 'Utkin (1977)', 'BibTeX_Key': 'utkin1977variable'},
    'CODE-IMPL-191': {'Suggested_Citation': 'Utkin (1977)', 'BibTeX_Key': 'utkin1977variable'},
}

# Apply fixes
all_fixes = {**critical_fixes, **severe_fixes}
for claim_id, updates in all_fixes.items():
    mask = df['Claim_ID'] == claim_id
    for col, value in updates.items():
        df.loc[mask, col] = value

# Save
df.to_csv('claims_research_tracker_CORRECTED.csv', index=False)
print(f"Fixed {len(all_fixes)} citations")
```

---

## Quality Metrics After Correction

### Before Correction
- Correct: 112 (35.7%)
- Incorrect: 131 (41.7%)
- Uncertain: 71 (22.6%)

### After Applying This Mapping
- Correct: 127 (40.4%) - *+15 from severe fixes*
- Incorrect: 116 (36.9%) - *only moderate mismatches remain*
- Uncertain: 71 (22.6%) - *unchanged, need manual review*

**Improvement:** +4.7% accuracy with minimal effort (15 targeted corrections)

---

## Recommended Workflow

1. ✅ **Apply 15 severe/critical fixes** (above) - 30 minutes
2. ⏸ **Manual review 29 stability analysis claims** - 2-3 hours
3. ⏸ **Triage 116 moderate mismatches** - determine if citations needed
4. ⏸ **Review 71 uncertain claims** - many may not need citations

**Total time for high-confidence corrections:** ~30 minutes
**Total time for comprehensive review:** ~10-15 hours

---

**Last Updated:** 2025-10-02
**Source:** Automated verification (verify_batch08_citations.py)
**Confidence:** HIGH for severe/critical fixes; MEDIUM for moderate recommendations
