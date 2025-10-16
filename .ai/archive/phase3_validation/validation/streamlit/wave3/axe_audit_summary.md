# Wave 3 Accessibility Audit (axe-core)

**Date**: 2025-10-16T12:49:08.511988
**Wave**: Wave 3 - Streamlit Theme Parity
**axe-core Version**: 4.8.2

## Summary

| Severity | Count |
|----------|-------|
| **Critical** | 2 |
| Serious | 0 |
| Moderate | 0 |
| Minor | 0 |
| **Total** | 2 |

## Wave 3 Exit Criteria Assessment

[FAIL] **FAIL**: 2 critical + 0 serious violations found

## Violations

### Critical Violations (2)

#### aria-allowed-attr

- **Description**: Ensures an element's role supports its ARIA attributes
- **Impact**: critical
- **Affected elements**: 1
- **Tags**: cat.aria, wcag2a, wcag412, EN-301-549, EN-9.4.1.2
- **Help**: Elements must only use supported ARIA attributes
- [More info](https://dequeuniversity.com/rules/axe/4.8/aria-allowed-attr?application=axeAPI)

#### button-name

- **Description**: Ensures buttons have discernible text
- **Impact**: critical
- **Affected elements**: 1
- **Tags**: cat.name-role-value, wcag2a, wcag412, section508, section508.22.a, TTv5, TT6.a, EN-301-549, EN-9.4.1.2, ACT
- **Help**: Buttons must have discernible text
- [More info](https://dequeuniversity.com/rules/axe/4.8/button-name?application=axeAPI)

## Recommendations

- 2 critical/serious violations must be resolved
- Review detailed JSON report for full violation details
- Focus on color contrast and focus indicators
