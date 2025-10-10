# Quick Start: Issue #12 Validation

**When PSO completes, run ONE command:**

```bash
python scripts/optimization/monitor_and_validate.py --auto-update-config
```

That's it! This will:
- ✅ Validate all optimized gains
- ✅ Update config.yaml if validation passes
- ✅ Show clear next steps



## Alternative: Manual Workflow

### Step 1: Validate

```bash
python scripts/optimization/validate_and_summarize.py
```

### Step 2: Check Results

Look for output:
```
Chattering target met: X/3
  classical_smc: chattering=XXX.XXX [PASS/FAIL]
  adaptive_smc: chattering=XXX.XXX [PASS/FAIL]
  sta_smc: chattering=XXX.XXX [PASS/FAIL]
```

### Step 3A: If ALL PASS

```bash
# Update config
python scripts/optimization/update_config_with_gains.py

# Test
python simulate.py --ctrl classical_smc --plot

# Commit
git add config.yaml docs/issue_12_validation_summary_*.json
git commit -m "RESOLVED: Issue #12 - Chattering reduction validated"
git push origin main
```

## Step 3B: If ANY FAIL

```bash
# Re-optimize with corrected fitness function
python scripts/optimization/optimize_chattering_focused.py --controller classical_smc --iters 150
python scripts/optimization/optimize_chattering_focused.py --controller adaptive_smc --iters 150
python scripts/optimization/optimize_chattering_focused.py --controller sta_smc --iters 150

# Wait ~3-4 hours, then validate again
python scripts/optimization/validate_and_summarize.py
```



## Expected Outcome

**Likely:** Validation will FAIL (chattering still high)

**Why:** Current PSO used tracking-focused fitness function

**Solution:** Re-run with `optimize_chattering_focused.py` (corrected fitness)



## Success Criteria

✅ **PASS if:** Chattering < 2.0 for all controllers
❌ **FAIL if:** Any controller has chattering >= 2.0



## Need Help?

See full documentation: `scripts/optimization/README.md`