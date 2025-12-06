# File Naming Issues - Citation Tracking Audit

**Date**: 2025-12-06
**Status**: [WARNING] Multiple file content mismatches discovered
**Impact**: 2 PDFs (9.1% of collection) have incorrect filename/content mappings

---

## Summary

During citation tracking work, we discovered that **2 out of 22 PDFs** have filenames that do NOT match their actual content. These files are NOT relevant to the DIP-SMC-PSO thesis and should be replaced with correct sources.

---

## Discovered Mismatches

### 1. dash2018.pdf - Power Systems (NOT Inverted Pendulum)

**Expected Content** (per INDEX.md):
- Title: "Sliding Mode Control of Rotary Inverted Pendulum"
- Domain: Inverted pendulum control
- Relevance: HIGH (thesis topic)

**Actual Content**:
- Title: "Adaptive fractional integral terminal sliding mode power control of UPFC in DFIG wind farm penetrated multimachine power system"
- Domain: Power systems, wind farm control
- Relevance: NONE (unrelated to thesis)

**File Details**:
- Filename: `dash2018.pdf`
- Size: 1.6 MB
- Location: `thesis/sources_archive/manually downloaded/`

**Recommendation**: Replace with actual rotary inverted pendulum SMC paper

---

### 2. collins2005.pdf - Bipedal Robotics (NOT PSO Review)

**Expected Content** (per INDEX.md):
- Title: "A Review of Particle Swarm Optimization"
- Domain: PSO algorithms, optimization
- Relevance: HIGH (thesis uses PSO)

**Actual Content**:
- Title: "Efficient Bipedal Robots Based on Passive-Dynamic Walkers"
- Domain: Robotics, passive-dynamic walking
- Relevance: NONE (unrelated to thesis)

**File Details**:
- Filename: `collins2005.pdf`
- Size: 418 KB
- Location: `thesis/sources_archive/manually downloaded/`

**Recommendation**: Replace with actual PSO review paper

---

## Correct Filename Mapping (Fixed)

### quanser2020.pdf → Quanser2012 DBPEN-LIN Manual

**Original INDEX Entry**:
- Expected: "Quanser2020 - QUBE-Servo 2 User Manual"

**Actual Content**:
- Correct title: "Linear Double Inverted Pendulum Experiment: Set Up and Configuration - User Manual (DBPEN-LIN)"
- Correct year: 2012 (not 2020)
- Relevance: **VERY HIGH** (Direct match to thesis topic - DIP hardware!)

**Status**: [OK] CORRECTED
- INDEX.md updated with correct citation: Quanser2012
- Tracking file created: `Quanser2012_tracking.md` (550+ lines)
- This is a CRITICAL resource for the thesis (contains exact DIP system parameters)

---

## Impact Analysis

### Statistics

| Status | Count | Percentage |
|--------|-------|------------|
| Correct Filename/Content Match | 19 | 86.4% |
| Filename Mismatch (Corrected) | 1 | 4.5% |
| Filename Mismatch (Unresolved) | 2 | 9.1% |
| **Total PDFs** | **22** | **100%** |

### Tracking Progress

| Category | Count |
|----------|-------|
| Successfully Tracked | 14 |
| File Mismatches (Not Tracked) | 2 |
| Remaining Valid PDFs to Track | 6 |
| **Total Trackable PDFs** | **20** |

---

## Recommendations

### Immediate Actions

1. **Replace dash2018.pdf**:
   - Find correct rotary inverted pendulum SMC paper
   - Verify author = Dash (2018) or update INDEX with correct citation

2. **Replace collins2005.pdf**:
   - Find actual PSO review paper by Collins (2005)
   - Verify content matches PSO optimization domain

3. **Update Tracking Statistics**:
   - Current: 14/22 tracked (63.6%)
   - Corrected: 14/20 tracked (70.0% of trackable PDFs)
   - Target: 20/20 tracked (100% of valid sources)

### Preventive Measures

1. **Filename Verification Protocol**:
   - Read first page of PDF before cataloging
   - Verify author, year, title match filename
   - Cross-check with BibTeX entry

2. **Content Relevance Check**:
   - Confirm domain relevance (SMC, PSO, inverted pendulum, control theory)
   - Flag off-topic PDFs immediately
   - Document mismatches in this file

---

## Corrected INDEX.md Sections

### Before (Incorrect)
```markdown
### 2. Dash2018 - Sliding Mode Control of Rotary Inverted Pendulum
**File**: `dash2018.pdf`
**Status**: [PENDING] Not yet tracked
```

### After (Corrected)
```markdown
### 2. Dash2018 - [FILE MISMATCH] Power Systems (UPFC/DFIG Wind Farm)
**File**: `dash2018.pdf` [WARNING] File content mismatch!
**Status**: [MISMATCH] File contains power systems paper, NOT inverted pendulum control
```

---

## Related Files

- **INDEX.md**: Main citation tracking index (updated with mismatch warnings)
- **Quanser2012_tracking.md**: Successfully created despite filename mismatch
- **ECP2020_tracking.md**: Successfully created (14th tracked PDF)

---

## Last Updated

**Date**: 2025-12-06
**By**: Claude Code (citation tracking audit)
**Next Review**: After replacing mismatched PDFs

---

**Note**: This document should be updated whenever new file naming issues are discovered during citation tracking work.
