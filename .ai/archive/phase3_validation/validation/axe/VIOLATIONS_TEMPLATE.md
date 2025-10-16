# axe-core Accessibility Violations Report - {WAVE_NAME}

**Date:** {DATE}
**Wave:** {WAVE_NUMBER} - {WAVE_DESCRIPTION}
**WCAG Level:** AA (2.1)
**URLs Tested:** {URL_COUNT}

---

## Executive Summary

| Severity | Threshold | Actual | Status |
|----------|-----------|--------|--------|
| **Critical** | 0 | {CRITICAL_COUNT} | {PASS/FAIL} |
| **Serious** | 0 | {SERIOUS_COUNT} | {PASS/FAIL} |
| **Moderate** | <=5 | {MODERATE_COUNT} | {PASS/WARN} |
| **Minor** | <=10 | {MINOR_COUNT} | {PASS/WARN} |

**Exit Criteria Status:** {PASS/FAIL}

---

## Critical Violations (Must Fix Immediately)

### Violation 1: {RULE_ID} - {RULE_DESCRIPTION}

- **Impact:** Critical
- **WCAG Criteria:** {WCAG_CODE} (e.g., 1.4.3 Contrast)
- **Affected Pages:** {PAGE_LIST}
- **Affected Elements:** {ELEMENT_COUNT}
- **Example:**
  ```html
  {HTML_SNIPPET}
  ```
- **Recommendation:** {FIX_DESCRIPTION}
- **Related Issue:** {UI_ISSUE_ID}

*(Repeat for each critical violation)*

---

## Serious Violations (High Priority)

### Violation X: {RULE_ID} - {RULE_DESCRIPTION}

*(Same format as above)*

---

## Moderate Violations (Medium Priority)

*(List with less detail if count >5)*

1. **{RULE_ID}:** {COUNT} elements on {PAGE_COUNT} pages
2. **{RULE_ID}:** {COUNT} elements on {PAGE_COUNT} pages

---

## Minor Violations (Low Priority)

*(List with minimal detail if count >10)*

1. **{RULE_ID}:** {COUNT} elements
2. **{RULE_ID}:** {COUNT} elements

---

## Per-Page Breakdown

### {PAGE_1_NAME} ({PAGE_1_URL})

| Severity | Count | Rules |
|----------|-------|-------|
| Critical | {COUNT} | {RULE_IDS} |
| Serious | {COUNT} | {RULE_IDS} |
| Moderate | {COUNT} | {RULE_IDS} |
| Minor | {COUNT} | {RULE_IDS} |

**Top Issues:**
1. {ISSUE_1}
2. {ISSUE_2}

---

## Comparison to Previous Wave

| Severity | Wave {N-1} | Wave {N} | Change |
|----------|------------|----------|--------|
| Critical | {PREV} | {CURR} | {DELTA} |
| Serious | {PREV} | {CURR} | {DELTA} |
| Moderate | {PREV} | {CURR} | {DELTA} |
| Minor | {PREV} | {CURR} | {DELTA} |

---

## Regressions Introduced

{LIST_OF_NEW_VIOLATIONS_NOT_PRESENT_IN_PREVIOUS_WAVE}

---

## Action Plan

### Immediate (Before Wave Exit):
1. {FIX_CRITICAL_1}
2. {FIX_CRITICAL_2}

### Wave {N+1}:
1. {DEFER_MODERATE_1}
2. {DEFER_MODERATE_2}

---

## Raw Reports

- JSON reports: `.axe/reports/{WAVE_NAME}/`
- Full details: Run `npx axe-cli {URL} --load-delay 1000`

---

**Validated By:** {VALIDATOR_NAME}
**Approval:** {APPROVED/NEEDS_FIXES}
**Rollback Triggered:** {YES/NO}

