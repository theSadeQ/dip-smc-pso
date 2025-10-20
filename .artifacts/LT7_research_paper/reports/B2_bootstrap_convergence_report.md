# Task B.2: Bootstrap Convergence Analysis Report

**Date:** 2025-10-20
**Phase:** LT-7 Phase 2, Category B
**Objective:** Validate that B=10,000 iterations used in MT-6 analysis were sufficient

---

## 1. Data Summary

| Metric | Fixed Boundary | Adaptive Boundary |
|--------|----------------|-------------------|
| Sample Size (n) | 100 | 100 |
| Mean | 6.3705 | 2.1214 |
| Std Dev | 1.2003 | 0.1222 |

---

## 2. Bootstrap Convergence Results

### Fixed Boundary

| B (iterations) | CI Lower | CI Upper | CI Width | Computation Time |
|----------------|----------|----------|----------|------------------|
| 1,000.0 | 6.1384 | 6.5896 | 0.4512 | 0.04s |
| 5,000.0 | 6.1342 | 6.6028 | 0.4686 | 0.19s |
| 10,000.0 | 6.1385 | 6.6014 | 0.4629 | 0.34s |
| 20,000.0 | 6.1383 | 6.6010 | 0.4627 | 0.73s |

### Adaptive Boundary

| B (iterations) | CI Lower | CI Upper | CI Width | Computation Time |
|----------------|----------|----------|----------|------------------|
| 1,000.0 | 2.0987 | 2.1439 | 0.0451 | 0.05s |
| 5,000.0 | 2.0970 | 2.1446 | 0.0475 | 0.18s |
| 10,000.0 | 2.0974 | 2.1448 | 0.0475 | 0.38s |
| 20,000.0 | 2.0976 | 2.1450 | 0.0474 | 0.92s |

---

## 3. Convergence Analysis (10K to 20K)

**Convergence Criterion:** CI width change < 5%

### Fixed Boundary
- **B=10,000:** CI width = 0.4629
- **B=20,000:** CI width = 0.4627
- **Change:** 0.04%
- **Status:** ✓ CONVERGED

### Adaptive Boundary
- **B=10,000:** CI width = 0.0475
- **B=20,000:** CI width = 0.0474
- **Change:** 0.14%
- **Status:** ✓ CONVERGED

---

## 4. Conclusion


✓ **VALIDATION SUCCESSFUL:** Both distributions show convergence at B=10,000

**Implications:**
- The 10,000 bootstrap iterations used in MT-6 analysis were **sufficient**
- Confidence intervals reported in Chapter 6 are **stable and reliable**
- Increasing to B=20,000 produces negligible improvement (<5% change)
- Current bootstrap methodology is **computationally efficient** without sacrificing accuracy

**Recommendation:** Continue using B=10,000 for future bootstrap analyses in this project.


---

## 5. Computational Efficiency

**Total Bootstrap Time (all tests):**
- Fixed: 1.31s
- Adaptive: 1.53s
- **Combined:** 2.83s

**Time per iteration (B=10,000):**
- Fixed: 0.0336 ms/iter
- Adaptive: 0.0385 ms/iter

---

**Figure:** `figure_vi_1_bootstrap_convergence.pdf`
**Generated:** 2025-10-20
**Script:** `scripts/lt7_bootstrap_convergence.py`
