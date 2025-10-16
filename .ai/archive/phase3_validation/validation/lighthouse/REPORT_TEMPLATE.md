# Lighthouse Validation Report - {WAVE_NAME}

**Date:** {DATE}
**Wave:** {WAVE_NUMBER} - {WAVE_DESCRIPTION}
**URLs Tested:** {URL_COUNT}
**Runs Per URL:** 3 (median values reported)

---

## Executive Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Accessibility Score** | >=95 | {ACCESSIBILITY_SCORE} | {PASS/FAIL} |
| **Performance Score** | >=80 | {PERFORMANCE_SCORE} | {PASS/WARN} |
| **Best Practices** | >=90 | {BEST_PRACTICES_SCORE} | {PASS/WARN} |
| **SEO Score** | >=85 | {SEO_SCORE} | {PASS/WARN} |

**Exit Criteria Status:** {PASS/FAIL}

---

## Accessibility Metrics (Detailed)

### Critical Checks (All Must Pass)

| Check | Status | Details |
|-------|--------|---------|
| color-contrast | {PASS/FAIL} | {DETAILS} |
| button-name | {PASS/FAIL} | {DETAILS} |
| link-name | {PASS/FAIL} | {DETAILS} |
| aria-allowed-attr | {PASS/FAIL} | {DETAILS} |
| aria-required-attr | {PASS/FAIL} | {DETAILS} |
| aria-valid-attr | {PASS/FAIL} | {DETAILS} |
| aria-valid-attr-value | {PASS/FAIL} | {DETAILS} |
| image-alt | {PASS/FAIL} | {DETAILS} |

### Per-Page Results

#### {PAGE_1_NAME} ({PAGE_1_URL})

- **Accessibility:** {SCORE}/100
- **Performance:** {SCORE}/100
- **First Contentful Paint:** {VALUE}ms (target: <2000ms)
- **Largest Contentful Paint:** {VALUE}ms (target: <2500ms)
- **Cumulative Layout Shift:** {VALUE} (target: <0.1)
- **Violations:** {COUNT}
  - {VIOLATION_1}
  - {VIOLATION_2}

#### {PAGE_2_NAME} ({PAGE_2_URL})

*(Repeat for all pages)*

---

## Comparison to Previous Wave

| Metric | Wave {N-1} | Wave {N} | Change |
|--------|------------|----------|--------|
| Accessibility | {PREV_SCORE} | {CURR_SCORE} | {DELTA} |
| Performance | {PREV_SCORE} | {CURR_SCORE} | {DELTA} |
| Best Practices | {PREV_SCORE} | {CURR_SCORE} | {DELTA} |

---

## Regressions Detected

{LIST_OF_REGRESSIONS_OR_NONE}

---

## Action Items

1. {ACTION_ITEM_1}
2. {ACTION_ITEM_2}

---

## Raw Reports

- Full JSON reports: `.lighthouse/reports/{WAVE_NAME}/`
- HTML reports: Open `.lighthouse/reports/{WAVE_NAME}/*.html` in browser

---

**Validated By:** {VALIDATOR_NAME}
**Approval:** {APPROVED/NEEDS_FIXES}

