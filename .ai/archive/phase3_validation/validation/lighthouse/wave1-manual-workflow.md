# Wave 1 Lighthouse Accessibility Audit - Manual Workflow

**Purpose**: Guide for running Chrome DevTools Lighthouse accessibility audits on localhost documentation.

**Target Score**: Accessibility >=95 (WCAG 2.1 Level AA compliance)

**Wave**: Wave 1 - Foundations & Accessibility

**Date**: 2025-10-15

---

## Prerequisites

### Required Software
- [ ] Google Chrome (version 90 or later)
- [ ] Documentation server running at `http://localhost:9000`
- [ ] Stable internet connection (for Lighthouse library CDN)

### Test Pages
1. Homepage: `http://localhost:9000/`
2. Getting Started: `http://localhost:9000/guides/getting-started.html`
3. Controller API Reference: `http://localhost:9000/reference/controllers/index.html`
4. SMC Theory Guide: `http://localhost:9000/guides/theory/smc-theory.html`
5. Benchmarks: `http://localhost:9000/benchmarks/index.html`

---

## Step-by-Step Workflow

### Step 1: Open Chrome DevTools

1. Launch Google Chrome
2. Navigate to test page (e.g., `http://localhost:9000/`)
3. Open DevTools:
   - **Windows/Linux**: Press `F12` or `Ctrl+Shift+I`
   - **Mac**: Press `Cmd+Option+I`
   - **Alternative**: Right-click page → "Inspect"

**Screenshot checkpoint**: DevTools panel should open at bottom or side of browser

---

### Step 2: Navigate to Lighthouse Tab

1. In DevTools, click the **Lighthouse** tab
   - If not visible, click the `>>` overflow menu → Select "Lighthouse"
2. The Lighthouse panel will display with audit options

**Screenshot checkpoint**: Lighthouse audit configuration panel visible

---

### Step 3: Configure Audit Settings

**Audit Categories** (Select):
- [ ] Performance (optional - for context)
- [x] **Accessibility** (REQUIRED)
- [ ] Best Practices (optional)
- [ ] SEO (optional)
- [ ] PWA (optional)

**Device**:
- [x] Desktop (recommended for consistency)
- [ ] Mobile (optional secondary test)

**Lighthouse Mode**:
- [x] Navigation (default) - Full page load
- [ ] Timespan - Not needed for accessibility

**Throttling** (Optional):
- Use "Applied Slow 4G throttling" for realistic network conditions
- Or "No throttling" for fastest audit

**Screenshot checkpoint**: Accessibility checkbox selected, Desktop mode chosen

---

### Step 4: Run the Audit

1. Click the blue **"Analyze page load"** button
2. Wait 30-60 seconds for audit to complete
   - Browser will reload page automatically
   - Progress indicator shows audit stages
3. Results will display when complete

**Expected Duration**: 30-90 seconds per page

**Screenshot checkpoint**: Audit running (progress bar visible)

---

### Step 5: Review Accessibility Score

1. Locate the **Accessibility** score at top of report (0-100 scale)
2. Check color-coded rating:
   - **Green (90-100)**: PASS - Good accessibility ✅
   - **Orange (50-89)**: WARN - Needs improvement ⚠️
   - **Red (0-49)**: FAIL - Critical issues ❌

**Wave 1 Target**: **Accessibility >= 95** (Green zone)

**Record Result**:
```
Page: ______________________________________________________
Accessibility Score: _____/100
Status: [ ] PASS (>=95) [ ] FAIL (<95)
```

**Screenshot checkpoint**: Accessibility score visible (take screenshot for evidence)

---

### Step 6: Review Passed Audits

1. Scroll to **"Passed audits"** section (green checkmarks)
2. Expand the section to see all passing tests
3. Verify critical WCAG criteria:
   - [x] Color contrast meets WCAG AA requirements
   - [x] ARIA attributes valid and required
   - [x] Button elements have accessible names
   - [x] Links have discernible text
   - [x] Images have alt attributes
   - [x] Form elements have labels

**Record Passed**: ___/28 audits passed

---

### Step 7: Review Failed Audits (If Any)

1. Scroll to **"Audits to fix"** section (red X marks)
2. Click each failed audit to expand details
3. Review:
   - **Description**: What the issue is
   - **Impact**: How it affects users
   - **Failing Elements**: Which HTML elements failed
   - **Learn more link**: WCAG 2.1 reference

**Critical Failures to Check**:
- [ ] Color contrast (UI-002/003 should fix this)
- [ ] ARIA required attributes (UI-004 should fix this)
- [ ] Missing button/link names
- [ ] Missing alt text on images

**Record Failed**: ___/__ audits failed

**Screenshot checkpoint**: Expanded failed audit details (if any failures exist)

---

### Step 8: Export Report (Evidence Collection)

**Method 1: HTML Report**
1. Click the **gear icon** (⚙️) in top-right of Lighthouse report
2. Select **"Save as HTML"**
3. Save to: `.codex/phase3/validation/lighthouse/wave1-[page-name]-report.html`
   - Example: `wave1-homepage-report.html`

**Method 2: JSON Report**
1. In DevTools Console tab, run:
   ```javascript
   JSON.stringify(lhr, null, 2)
   ```
2. Copy output
3. Save to: `.codex/phase3/validation/lighthouse/wave1-[page-name]-report.json`

**Method 3: Screenshot**
1. Press `PrtScn` (Windows) or `Cmd+Shift+4` (Mac)
2. Save to: `.codex/phase3/validation/lighthouse/wave1-[page-name]-screenshot.png`

**Required Evidence**:
- [ ] HTML report saved
- [ ] Screenshot of score page saved
- [ ] JSON export (optional, for CI integration)

---

### Step 9: Repeat for All Test Pages

Run Steps 1-8 for each of the 5 test pages:

**Page Checklist**:
1. [ ] Homepage (`/`) - Score: ___/100
2. [ ] Getting Started (`/guides/getting-started.html`) - Score: ___/100
3. [ ] Controller API (`/reference/controllers/index.html`) - Score: ___/100
4. [ ] SMC Theory (`/guides/theory/smc-theory.html`) - Score: ___/100
5. [ ] Benchmarks (`/benchmarks/index.html`) - Score: ___/100

**Average Score**: ___/100

---

### Step 10: Validate Against Wave 1 Fixes

**UI-002 Validation**: Muted Text Contrast
- Check: "Elements must meet minimum color contrast ratio"
- Look for: `.caption`, `.copyright`, `.last-updated` elements
- Expected: **PASS** (4.52:1 contrast ratio achieved)

**Result**: [ ] PASS [ ] FAIL
**Notes**: _________________________________________________________

---

**UI-003 Validation**: Collapsed Notice Contrast
- Check: Background/foreground color contrast on code collapse notice
- Look for: `.code-collapse-notice` element
- Expected: **PASS** (12.4:1 contrast ratio achieved)

**Result**: [ ] PASS [ ] FAIL
**Notes**: _________________________________________________________

---

**UI-004 Validation**: ARIA Accessibility
- Check: "ARIA attributes are valid and required" + "Buttons have accessible names"
- Look for: `role="region"`, `aria-live="polite"`, `aria-controls`, `aria-expanded`
- Expected: **PASS** (all ARIA attributes present and valid)

**Result**: [ ] PASS [ ] FAIL
**Notes**: _________________________________________________________

---

## Interpretation Guide

### Score Ranges
- **95-100**: Excellent - Wave 1 target MET ✅
- **90-94**: Good - Minor issues, likely non-blocking
- **85-89**: Fair - Review failed audits, may have accessibility barriers
- **<85**: Poor - Significant accessibility issues remain

### Common False Positives
Lighthouse may flag issues that are acceptable:
- **Low contrast on disabled elements**: Often intentional design
- **Missing labels on decorative images**: `alt=""` is correct for decorative images
- **ARIA attribute warnings**: May be false if using cutting-edge ARIA patterns

### When to Investigate
Investigate any failure related to:
- **Color contrast**: All text must meet 4.5:1 (normal) or 3:1 (large text)
- **Missing alt text**: Every `<img>` needs alt attribute (can be empty for decorative)
- **Missing button/link names**: Every interactive element needs accessible name
- **Invalid ARIA**: Incorrect ARIA usage worse than no ARIA

---

## Exit Criteria

### Wave 1 Lighthouse Validation: PASS Criteria

**Must Achieve**:
- [x] Accessibility score >=95 on all 5 test pages
- [x] No critical failures related to UI-002/003/004 fixes
- [x] All HTML reports saved to `.codex/phase3/validation/lighthouse/`
- [x] Screenshots captured for evidence

**Optional Stretch Goals**:
- [ ] Accessibility score 100 on any page
- [ ] Performance score >=90 (bonus, not required for Wave 1)
- [ ] No failed audits across all categories

---

## Troubleshooting

### Issue: Lighthouse Tab Not Visible

**Solution**:
1. Update Chrome to latest version (Help → About Google Chrome)
2. Clear DevTools cache (Settings → Preferences → Network → "Disable cache")
3. Close/reopen DevTools (F12 twice)
4. Try Incognito mode (Ctrl+Shift+N) to rule out extension conflicts

---

### Issue: Audit Fails with Error

**Common Causes**:
- Server not running at localhost:9000
- Page takes >60s to load (increase timeout in Lighthouse settings)
- Network issues preventing Lighthouse library load

**Solution**:
1. Verify server is running: `curl http://localhost:9000` should return HTML
2. Refresh page manually to test load time
3. Disable browser extensions (use Incognito mode)
4. Check browser console for JavaScript errors

---

### Issue: Score Changes Between Runs

**Explanation**: Lighthouse scores can vary ±5 points due to:
- Network latency fluctuations
- CPU load on testing machine
- Browser cache state
- Random sampling in some audits

**Solution**:
- Run audit 2-3 times and take average
- Use desktop mode (more consistent than mobile)
- Close other tabs/apps to reduce CPU load
- Use "No throttling" option for more stable scores

---

## Summary Report Template

**Test Date**: _______________
**Tester**: _______________
**Chrome Version**: _______________

| Page | Accessibility Score | Status | Notes |
|------|---------------------|--------|-------|
| Homepage | ___/100 | [ ] PASS [ ] FAIL | |
| Getting Started | ___/100 | [ ] PASS [ ] FAIL | |
| Controller API | ___/100 | [ ] PASS [ ] FAIL | |
| SMC Theory | ___/100 | [ ] PASS [ ] FAIL | |
| Benchmarks | ___/100 | [ ] PASS [ ] FAIL | |
| **Average** | **___/100** | [ ] PASS [ ] FAIL | |

**Wave 1 Lighthouse Validation**: [ ] PASS (All >=95) [ ] FAIL (Any <95)

**Evidence Files**:
- [ ] 5 HTML reports saved
- [ ] 5 screenshots saved
- [ ] Summary report completed

**Critical Issues Found**: __________________________________________

**Recommendations**: _______________________________________________

**Sign-Off**: ___________________________  **Date**: _______________

---

## Next Steps After Completion

1. Save all evidence files to `.codex/phase3/validation/lighthouse/`
2. Update changelog.md with Lighthouse validation results
3. If all scores >=95: Mark Wave 1 Lighthouse gate as **PASSED** ✅
4. If any score <95: Document failures and queue fixes for immediate resolution
5. Proceed to Wave 2 validation (or fix critical issues first)

---

## Appendix: Lighthouse CLI Alternative (Advanced)

For automated/CI validation, use Lighthouse CLI:

```bash
# Install Lighthouse globally
npm install -g lighthouse

# Run audit (saves HTML report)
lighthouse http://localhost:9000 \
  --only-categories=accessibility \
  --output=html \
  --output-path=./wave1-homepage-report.html

# Run audit (saves JSON report)
lighthouse http://localhost:9000 \
  --only-categories=accessibility \
  --output=json \
  --output-path=./wave1-homepage-report.json
```

**Prerequisites**: Node.js 18+ and Chrome installed

**Benefit**: Faster, reproducible, automatable in CI/CD pipelines

**Limitation**: Requires command line familiarity and npm setup
