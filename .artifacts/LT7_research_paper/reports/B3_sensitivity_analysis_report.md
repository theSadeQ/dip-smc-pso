# Task B.3: Sensitivity Analysis Report

**Date:** 2025-10-20
**Phase:** LT-7 Phase 2, Category B
**Objective:** Test sensitivity of statistical results to analysis parameters

---

## 1. Sensitivity Parameter 1: Sample Size

**Test:** Random subsampling to n=60, 80, 100

### Results

| n | Mean (Fixed) | 95% CI (Fixed) | CI Width | Mean (Adaptive) | 95% CI (Adaptive) | CI Width |
|---|--------------|----------------|----------|-----------------|-------------------|----------|
| 60.0 | 6.5759 | [6.2898, 6.8697] | 0.5799 | 2.1201 | [2.0884, 2.1516] | 0.0632 |
| 80.0 | 6.5446 | [6.3007, 6.7881] | 0.4874 | 2.1116 | [2.0843, 2.1393] | 0.0550 |
| 100.0 | 6.3705 | [6.1385, 6.6014] | 0.4629 | 2.1214 | [2.0974, 2.1448] | 0.0475 |

**Analysis:**
- **Fixed boundary:** Mean changes by 3.22% across sample sizes
- **Adaptive boundary:** Mean changes by 0.46% across sample sizes
- **CI width increases as n decreases** (expected behavior)

**Conclusion:** Results are robust to sample size variations

---

## 2. Sensitivity Parameter 2: Outlier Removal

**Test:** No removal, 3-sigma threshold, 2-sigma threshold

### Results

| Threshold | n (Fixed) | Mean (Fixed) | CI Width | n (Adaptive) | Mean (Adaptive) | CI Width |
|-----------|-----------|--------------|----------|--------------|-----------------|----------|
| None | 100 | 6.3705 | 0.4629 | 100 | 2.1214 | 0.0475 |
| 3.0-sigma | 100 | 6.3705 | 0.4629 | 100 | 2.1214 | 0.0475 |
| 2.0-sigma | 97 | 6.4593 | 0.4339 | 95 | 2.1301 | 0.0431 |

**Analysis:**
- **3-sigma removal:** Fixed=0 outliers, Adaptive=0 outliers
- **Mean change:** Minimal impact from outlier removal
- **CI width:** Slightly narrows with outlier removal (expected)

**Conclusion:** Results are robust to outlier removal (no outliers detected at 3-sigma threshold)

---

## 3. Sensitivity Parameter 3: Bootstrap CI Method

**Test:** Percentile vs BCa (bias-corrected accelerated)

### Results

| Method | CI (Fixed) | CI Width | CI (Adaptive) | CI Width |
|--------|-----------|----------|---------------|----------|
| PERCENTILE | [6.1385, 6.6014] | 0.4629 | [2.0974, 2.1448] | 0.0475 |
| BCA | [6.1342, 6.5976] | 0.4634 | [2.0975, 2.1450] | 0.0475 |

**Analysis:**
- **Fixed boundary:** CI width differs by 0.0005 between methods
- **Adaptive boundary:** CI width differs by 0.0000 between methods
- **BCa typically produces narrower CIs** when data is skewed or biased

**Conclusion:** Minimal difference between percentile and BCa methods (data is approximately normal)

---

## 4. Overall Sensitivity Assessment

### Robustness Summary

| Parameter | Fixed Boundary | Adaptive Boundary | Overall |
|-----------|----------------|-------------------|---------|
| Sample Size | Robust (3.22% change) | Robust (0.46% change) | Robust |
| Outlier Removal | Robust (no outliers) | Robust (no outliers) | Robust |
| CI Method | Robust (< 0.01 diff) | Robust (< 0.01 diff) | Robust |

### Implications for Chapter 6


✓ **RESULTS ARE ROBUST:** Statistical findings are insensitive to reasonable variations in analysis parameters

**Recommendations:**
1. Continue using n=100, percentile bootstrap, no outlier removal
2. Report confidence intervals without adjustment
3. No need for sensitivity disclaimers in the manuscript


---

**Figure:** `figure_vi_1_sensitivity_analysis.pdf`
**Generated:** 2025-10-20
**Script:** `scripts/lt7_sensitivity_analysis.py`
