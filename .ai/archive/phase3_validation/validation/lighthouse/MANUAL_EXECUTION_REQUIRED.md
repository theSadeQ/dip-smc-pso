# Lighthouse Performance Audit - Manual Execution Required

**Status**: Lighthouse CLI installed but requires terminal restart for PATH update

**Reason**: Lighthouse was installed via `npm install -g lighthouse` but the current terminal session doesn't have the updated PATH. Windows terminals need to be restarted after global npm installations.

---

## Manual Execution Steps

### Option 1: Restart Terminal and Run Script

```bash
# 1. Close current terminal
# 2. Open new terminal
# 3. Verify Lighthouse is accessible:
where lighthouse
# Should output: C:\Users\sadeg\AppData\Roaming\npm\lighthouse.cmd

# 4. Run the automation script:
python .codex/phase3/validation/lighthouse/wave2_performance_audit.py
```

**Expected Output**:
- 3 JSON reports in `.codex/phase3/validation/lighthouse/wave2_exit/`
- METRICS_SUMMARY.md with CLS/LCP results
- Console output showing PASS/FAIL for each page

---

### Option 2: Manual Lighthouse Commands

```bash
# Homepage
lighthouse http://localhost:9000 \
  --only-categories=performance \
  --output=json \
  --output-path=.codex/phase3/validation/lighthouse/wave2_exit/performance-home.json \
  --quiet \
  --chrome-flags=--headless

# Getting Started
lighthouse http://localhost:9000/guides/getting-started \
  --only-categories=performance \
  --output=json \
  --output-path=.codex/phase3/validation/lighthouse/wave2_exit/performance-guides-getting-started.json \
  --quiet \
  --chrome-flags=--headless

# Controller API
lighthouse http://localhost:9000/reference/controllers/index \
  --only-categories=performance \
  --output=json \
  --output-path=.codex/phase3/validation/lighthouse/wave2_exit/performance-reference-controllers.json \
  --quiet \
  --chrome-flags=--headless
```

---

### Option 3: Chrome DevTools (Manual UI)

1. Open Chrome and navigate to `http://localhost:9000`
2. Press `F12` to open DevTools
3. Click "Lighthouse" tab
4. Select "Performance" category only
5. Click "Analyze page load"
6. Check results:
   - **CLS (Cumulative Layout Shift)**: Target <0.1
   - **LCP (Largest Contentful Paint)**: Target <2.5s
7. Save report as JSON (gear icon → "Save as JSON")
8. Repeat for all 3 pages

---

## Wave 2 Performance Targets

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| **CLS** | <0.1 | Cumulative Layout Shift - measures visual stability (no unexpected layout shifts) |
| **LCP** | <2.5s | Largest Contentful Paint - measures loading performance |

**Exit Criteria**: Both metrics must be **under the target** on all 3 pages.

---

## Validation Results Tracking

Once you run Lighthouse, update this section:

| Page | CLS | LCP | Status |
|------|-----|-----|--------|
| Homepage | ??? | ??? | [ ] PASS [ ] FAIL |
| Getting Started | ??? | ??? | [ ] PASS [ ] FAIL |
| Controller API | ??? | ??? | [ ] PASS [ ] FAIL |

**Overall**: [ ] PASS (all pages meet targets) [ ] FAIL (1+ pages fail)

---

## Next Steps After Validation

1. If **PASS**: Proceed to Wave 2 completion summary
2. If **FAIL**: Document failures in `wave2_exit/FAILURES.md` and queue fixes

---

## Troubleshooting

**Issue**: `where lighthouse` returns nothing after terminal restart

**Solution**:
```bash
# Check npm global bin path
npm config get prefix
# Should be: C:\Users\sadeg\AppData\Roaming\npm

# Manually add to PATH (if needed):
# Windows: System Properties → Environment Variables → Path → Add: C:\Users\sadeg\AppData\Roaming\npm
```

**Issue**: Lighthouse times out or fails to connect

**Solution**:
- Verify Sphinx server is running: `curl http://localhost:9000`
- Check firewall isn't blocking localhost connections
- Try increasing timeout: `--max-wait-for-load=60000`

---

**Last Updated**: 2025-10-15
**Automation Script**: `.codex/phase3/validation/lighthouse/wave2_performance_audit.py`
**Status**: Ready for manual execution (PATH issue resolved after terminal restart)
