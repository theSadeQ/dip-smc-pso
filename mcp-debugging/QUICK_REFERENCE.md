# MCP Debugging Quick Reference

**Fast lookup for common debugging tasks**

Last Updated: 2025-10-10

---

## Slash Commands

| Command | Purpose | Typical Use Case |
|---------|---------|-----------------|
| `/debug-with-mcp` | Multi-server integrated debugging | Start comprehensive debugging session |
| `/test-browser` | Streamlit dashboard testing | Screenshot, UI validation, performance testing |
| `/analyze-dashboard` | Dashboard comprehensive analysis | Full UI/UX/performance analysis |
| `/analyze-logs` | Automated log analysis | Parse simulation/PSO/test logs |
| `/analyze-pso-logs` | PSO convergence analysis | Debug optimization issues |
| `/test-controller` | Controller test suite | Run controller-specific tests |
| `/validate-simulation` | Simulation result validation | Verify control-theoretic criteria |
| `/optimize-controller` | PSO optimization workflow | Launch parameter tuning with monitoring |
| `/inspect-server` | MCP Inspector | Test and debug MCP servers |

---

## Common Tasks

### Code Quality Analysis (45 min)

```bash
# Step 1: RUFF analysis
ruff check src/ tests/ --output-format=json > mcp-debugging/analysis_results/ruff_$(date +%Y%m%d).json

# Step 2: VULTURE dead code detection
vulture src/ tests/ --min-confidence 80 > mcp-debugging/analysis_results/vulture_$(date +%Y%m%d).txt

# Step 3: Auto-fix safe issues
ruff check src/ tests/ --fix

# Step 4: Re-scan
ruff check src/ tests/ --statistics
```

**Expected Outcome:** 0 RUFF errors, documented unused code

---

### Streamlit Dashboard Testing (65 min)

```bash
# Step 1: Start Streamlit
streamlit run streamlit_app.py

# Step 2: Use slash command
/test-browser

# Step 3: Example requests
- "Screenshot Streamlit dashboard at localhost:8501"
- "Test classical SMC simulation workflow"
- "Measure dashboard load time"
- "Verify all plots render without errors"
```

**Expected Outcome:** Screenshots saved, performance metrics collected, UI validation report

---

### PSO Optimization Debugging

```bash
# Step 1: Analyze logs
/analyze-pso-logs

# Step 2: Check convergence
python simulate.py --ctrl classical_smc --run-pso --seed 42 --save gains_debug.json

# Step 3: Validate results
python -m pytest tests/test_optimization/ -v
```

**Expected Outcome:** PSO converges within iterations, gains within bounds

---

### Controller Testing

```bash
# Step 1: Run specific controller tests
/test-controller

# Step 2: Or manual pytest
pytest tests/test_controllers/test_classical_smc.py -v

# Step 3: Check coverage
pytest tests/test_controllers/ --cov=src/controllers --cov-report=html
```

**Expected Outcome:** All tests pass, coverage ≥95% for critical controllers

---

## MCP Server Quick Reference

### RUFF - Code Quality

**Check:**
```bash
ruff check src/ tests/ --statistics
```

**Auto-fix:**
```bash
ruff check src/ tests/ --fix
```

**Specific rules:**
```bash
ruff check src/ --select E,F,W  # Errors, pyflakes, warnings only
```

---

### VULTURE - Dead Code

**Standard scan:**
```bash
vulture src/ tests/ --min-confidence 80
```

**High confidence only:**
```bash
vulture src/ --min-confidence 90
```

**Exclude tests (avoid false positives):**
```bash
vulture src/ --min-confidence 80
```

---

### Playwright - Browser Automation

**Install browsers:**
```bash
npm run playwright:install
# or
npx playwright install
```

**Check version:**
```bash
npx playwright --version
```

**Usage with Claude Code:**
- Use `/test-browser` slash command
- Request: "Screenshot dashboard at localhost:8501"
- Request: "Test simulation workflow end-to-end"

---

### Pytest - Testing

**Run all tests:**
```bash
pytest tests/ -v
```

**With coverage:**
```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
```

**Specific tests:**
```bash
pytest tests/test_controllers/ -k "test_classical_smc"
```

**Benchmarks only:**
```bash
pytest tests/test_benchmarks/ --benchmark-only
```

---

## File Locations

### Workflows
- **Complete Debugging:** `mcp-debugging/workflows/complete-debugging-workflow.md`
- **Code Quality:** `mcp-debugging/workflows/code-quality-analysis.md`
- **Streamlit Testing:** `mcp-debugging/workflows/streamlit-testing-workflow.md`

### Templates
- **Analysis Report:** `mcp-debugging/templates/analysis-report-template.md`
- **Bug Report:** `mcp-debugging/templates/bug-report-template.md`

### Analysis Results
- **Reports:** `mcp-debugging/analysis_results/`
- **Naming:** `TOOL_FINDINGS_YYYYMMDD_HHMMSS.md`

### Slash Commands
- **All commands:** `.claude/commands/*.md`
- **Configuration:** `.claude/settings.local.json`

---

## Troubleshooting

### "Command not found" errors

```bash
# Check tool installation
which ruff vulture pytest

# Reinstall if missing
pip install ruff vulture pytest pytest-cov pytest-benchmark
```

### Playwright issues

```bash
# Reinstall browsers
npx playwright install --force

# Check installation
npx playwright --version
```

### Slash command not recognized

1. Check file exists: `ls .claude/commands/`
2. Verify description field in frontmatter
3. Restart Claude Code session if needed

### MCP server timeout

- Increase timeout in Claude Code settings
- Check server logs for errors
- Verify network connectivity

---

## Best Practices

### Before Debugging
- ✅ Pull latest: `git pull origin main`
- ✅ Clean workspace: `python scripts/cleanup/workspace_cleanup.py`
- ✅ Verify tools: `ruff --version && pytest --version`

### During Debugging
- ✅ Follow workflow steps sequentially
- ✅ Generate reports immediately
- ✅ Commit after each phase
- ✅ Validate fixes with tests

### After Debugging
- ✅ Push changes: `git push origin main`
- ✅ Update documentation
- ✅ Close related GitHub issues
- ✅ Share findings with team

---

## Emergency Procedures

### Critical Test Failures

1. Run isolated test: `pytest path/to/test.py::test_name -v`
2. Check recent commits: `git log --oneline -n 5`
3. Revert if needed: `git revert <commit-hash>`
4. Debug with breakpoint: Add `import pdb; pdb.set_trace()`

### Deployment Blockers

1. Run production validation: `python scripts/verify_dependencies.py`
2. Check thread safety: `python scripts/test_thread_safety_fixes.py`
3. Verify memory: `python scripts/test_memory_leak_fixes.py`
4. Review checklist: `docs/RELEASE_CHECKLIST.md`

### Performance Degradation

1. Run benchmarks: `pytest tests/test_benchmarks/ --benchmark-only`
2. Profile code: `python -m cProfile simulate.py --ctrl classical_smc`
3. Check logs: `/analyze-logs`
4. Analyze PSO: `/analyze-pso-logs`

---

## Support

- **Documentation:** `mcp-debugging/README.md`
- **Server Matrix:** `mcp-debugging/MCP_SERVER_CAPABILITIES_MATRIX.md`
- **Project Guide:** `CLAUDE.md`
- **GitHub Issues:** https://github.com/theSadeQ/dip-smc-pso/issues

---

**Version:** 1.0.0
**Status:** ✅ Production Ready
**Maintainer:** DIP-SMC-PSO Team
