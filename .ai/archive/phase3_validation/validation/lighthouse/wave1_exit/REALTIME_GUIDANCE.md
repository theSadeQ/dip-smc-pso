# Wave 1 Lighthouse Audit - Real-Time Guidance

**Status**: 🟢 READY TO START
**Time**: 2025-10-15
**Estimated Duration**: 30-45 minutes

---

## 🎯 Current Task: Lighthouse Accessibility Audits

You should now see **test-urls.html** open in your browser with all 5 test URLs.

---

## ⚡ Quick Start Guide

### Step 1: Click First URL (Homepage)
- Click "Homepage" link in the test-urls.html page
- New tab opens with `http://localhost:9000/`

### Step 2: Open DevTools
- Press **F12** (or Ctrl+Shift+I)
- DevTools panel appears

### Step 3: Find Lighthouse Tab
- Look for **"Lighthouse"** tab in DevTools
- If not visible: Click **">>"** overflow menu → Select "Lighthouse"

### Step 4: Configure Audit
- **Uncheck all** except "Accessibility" ✅
- Select **"Desktop"** mode
- Leave other settings as default

### Step 5: Run Audit
- Click blue **"Analyze page load"** button
- Wait 30-60 seconds (progress bar shows stages)
- Score appears at top (0-100 scale)

### Step 6: Save Evidence
**Export HTML Report**:
1. Click **gear icon** (⚙️) in top-right
2. Select **"Save as HTML"**
3. Save to: `D:\Projects\main\.codex\phase3\validation\lighthouse\wave1_exit\`
4. Filename: `wave1-homepage-report.html`

**Take Screenshot**:
1. Press **PrtScn** (or Windows+Shift+S)
2. Save as: `wave1-homepage-screenshot.png`
3. Same directory as HTML report

### Step 7: Record Score
Open `RESULTS_TRACKING.md` and fill in:
```
| 1 | Homepage | http://localhost:9000/ | 95/100 | [x] PASS | Good accessibility |
```

### Step 8: Repeat for Remaining 4 Pages
Go back to test-urls.html → Click next URL → Repeat steps 2-7

---

## 🎨 Wave 1 Fixes to Validate

### UI-002: Muted Text Contrast ✅
**What to check**: Scroll through Lighthouse report
**Look for**: "Elements must meet minimum color contrast ratio" audit
**Expected**:
- ✅ PASS with green checkmark
- No failures on `.caption`, `.copyright`, `.last-updated` elements
- If failures exist on these classes, Wave 1 fix didn't work

**If you see failures**:
- Expand the "Color contrast" section
- Check which elements failed
- Note the contrast ratio shown (should be ≥4.5:1)

---

### UI-003: Collapsed Notice Contrast ✅
**What to check**: Look for code blocks with collapse buttons
**Visual check**:
- Click a code collapse button (▼ icon)
- Notice message appears: "Code hidden (click ▲ to expand)"
- Background should be dark (#1b2433)
- Text should be light (#f8fbff)
- High contrast should be obvious

**Lighthouse check**:
- "Color contrast" audit should NOT flag `.code-collapse-notice`

---

### UI-004: ARIA Accessibility ✅
**What to check**: Look for these audits in Lighthouse report
**Expected passes**:
1. ✅ "ARIA attributes are valid and required"
2. ✅ "Buttons have an accessible name"
3. ✅ "ARIA live regions have proper roles"

**Specifically for code blocks**:
- Collapse buttons should have clear labels
- `aria-expanded` state should be present
- `aria-controls` should link to code regions

**If failures exist**:
- Expand the failed audit
- Check if it's related to code collapse buttons
- Note specific elements that failed

---

## 📊 Score Interpretation

### Green Zone (90-100): PASS ✅
- **95-100**: Perfect! Wave 1 target met
- **90-94**: Very good, likely passes exit criteria

### Orange Zone (50-89): INVESTIGATE ⚠️
- **85-89**: Fair, review failures carefully
- **70-84**: Significant issues, may need fixes
- **50-69**: Many accessibility barriers

### Red Zone (0-49): FAIL ❌
- **Below 50**: Critical accessibility issues
- Likely blockers for Wave 1 completion

---

## 🔍 What Makes a Good Score?

**Typically passing audits** (should see green checkmarks):
- ✅ Color contrast meets WCAG AA
- ✅ ARIA attributes valid
- ✅ Buttons have accessible names
- ✅ Links have discernible text
- ✅ Images have alt text
- ✅ Form elements have labels
- ✅ HTML lang attribute set
- ✅ Heading elements in order

**Common acceptable "failures"** (not blockers):
- Low contrast on disabled elements (intentional)
- Missing labels on decorative images (correct if alt="")
- Some ARIA warnings (may be false positives)

---

## ⏱️ Time Management

**Per Page Timing**:
- Load page: 5 seconds
- Open DevTools: 5 seconds
- Configure Lighthouse: 15 seconds
- Run audit: 30-60 seconds
- Review score: 30 seconds
- Save evidence: 45 seconds
- Record results: 30 seconds
- **Total per page**: ~5-9 minutes

**Total for 5 pages**: 30-45 minutes

**Pro tip**: After first page, you'll get faster (muscle memory kicks in)

---

## 🚨 Troubleshooting

### Issue: Lighthouse Tab Not Showing
**Fix**:
1. Update Chrome: Menu → Help → About Google Chrome
2. Close DevTools (F12) and reopen
3. Try Incognito mode: Ctrl+Shift+N
4. Check for Chrome extensions blocking DevTools

---

### Issue: Audit Fails with Error
**Fix**:
1. Verify server: Run `curl http://localhost:9000` in terminal
2. Refresh page manually (Ctrl+R)
3. Close other tabs (reduce CPU load)
4. Disable browser extensions

---

### Issue: Score Changes Between Runs
**Why**: Network latency, CPU load, browser cache can cause ±5 point variance
**Fix**:
1. Run audit 2-3 times
2. Take average score
3. Use "No throttling" option
4. Close background apps

---

### Issue: Can't Find Export Button
**Location**: Top-right of Lighthouse report
**Look for**: Gear icon (⚙️) or three-dot menu
**Alternative**:
1. Right-click on report
2. Select "Save as..."
3. Choose "Webpage, Complete" format

---

## 📋 Progress Tracking

### Current Status
```
[x] test-urls.html opened in browser
[ ] Page 1/5: Homepage (___/100)
[ ] Page 2/5: Getting Started (___/100)
[ ] Page 3/5: Controller API (___/100)
[ ] Page 4/5: SMC Theory (___/100)
[ ] Page 5/5: Benchmarks (___/100)
```

### Evidence Checklist
```
[ ] 5 HTML reports saved
[ ] 5 screenshots captured
[ ] RESULTS_TRACKING.md updated
[ ] Wave 1 fixes validated
```

---

## 🎯 Next Steps After Completion

**When all 5 audits are done**:

1. **Review Results**:
   - Open `RESULTS_TRACKING.md`
   - Fill in all scores
   - Calculate average
   - Check if all ≥95

2. **Report to Claude**:
   - Share all 5 scores
   - Mention any critical failures
   - Confirm Wave 1 fixes validated

3. **Claude Will**:
   - Process your results
   - Update changelog
   - Mark Lighthouse validation complete
   - Guide you to NVDA/JAWS testing (next)

---

## 💡 Tips for Efficient Auditing

1. **Keep test-urls.html open** in one tab
2. **Open DevTools once** in first page, keep it open for all tabs
3. **Use keyboard shortcuts**: F12 (DevTools), Ctrl+Tab (switch tabs)
4. **Save all reports first**, then take all screenshots (batch operations)
5. **Use consistent file naming** (copy from QUICK_CHECKLIST.txt)

---

## ✅ Success Criteria Reminder

**Wave 1 Lighthouse Exit Criteria**:
- ✅ All 5 pages score ≥95 accessibility
- ✅ No critical failures on UI-002/003/004
- ✅ All evidence saved
- ✅ Results documented

**If ANY page scores <95**:
- Document failures in RESULTS_TRACKING.md
- Let Claude know which page(s) failed
- We'll investigate and plan fixes

---

**Good luck! You've got this! 🚀**

**Questions during audit?** Come back anytime - Claude is here to help!
