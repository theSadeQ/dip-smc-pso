# Perplexity MCP Integration Test Queries

Use these test queries after setting up the API key and restarting Claude Code.

## Quick Tests (Single MCP)

### Test 1: Basic Research Query
```
Research recent papers on chattering mitigation in sliding mode control
```
**Expected**: Perplexity MCP triggers → Returns papers from 2024-2025 on chattering reduction

### Test 2: Theory Validation
```
What does recent research say about optimal PSO parameters for control systems?
```
**Expected**: Perplexity finds recommended parameter ranges from literature

### Test 3: Citation Discovery
```
Find citations for boundary layer thickness in super-twisting algorithms
```
**Expected**: Perplexity returns papers with DOI/citations on STA boundary layers

## Advanced Tests (Multi-MCP Orchestration)

### Test 4: Literature + Local Implementation
```
Research recent work on adaptive SMC for underactuated systems, then compare
with our implementation in src/controllers/adaptive_smc.py
```
**Expected Pipeline**: perplexity → filesystem → context7
**Result**: Literature summary + code comparison

### Test 5: Complete Research Workflow
```
Research optimal lambda values for STA-SMC in DIP systems, find our current
implementation, and suggest improvements based on recent papers
```
**Expected Pipeline**: perplexity → filesystem → sequential-thinking
**Result**: Literature review → Implementation analysis → Recommendations

### Test 6: Citation + Documentation Workflow
```
Find citations for our PSO convergence methodology, search our documentation
for where it's explained, and generate a bibliography entry
```
**Expected Pipeline**: perplexity → context7 → filesystem
**Result**: Citations + local doc references + formatted bibliography

## Validation Checklist

After each test, verify:
- [ ] Perplexity MCP was triggered (check Claude's response mentions research/papers)
- [ ] Results include recent papers (2023-2025)
- [ ] Citations are properly formatted (author, year, title)
- [ ] Multi-MCP tests show chained outputs (e.g., literature + code analysis)

## Troubleshooting Test Failures

**MCP Not Triggering:**
- Verify environment variable: `echo $env:PERPLEXITY_API_KEY` (PowerShell)
- Restart Claude Code if variable was just set
- Use explicit keywords: "research", "literature", "papers on"

**No Results Returned:**
- Check API key is valid at https://www.perplexity.ai/settings/api
- Verify "Last Used" timestamp updates after query
- Check for rate limit errors in Claude's response

**Partial Results:**
- MCP triggered but no literature found: Query may be too specific
- Try broader terms: "sliding mode control" vs "STA-SMC for triple pendulum"

## Success Criteria

✅ All 3 quick tests return relevant papers
✅ At least 2 advanced tests successfully chain MCPs
✅ API key "Last Used" timestamp updates after queries
✅ No error messages about missing/invalid API key

## Next Steps After Successful Tests

Once integration is validated:

1. **Add Custom Slash Command**:
   Create `.claude/commands/research.md`:
   ```markdown
   Research control systems literature and compare with our implementation.

   Query: $ARGS
   Focus areas: SMC, PSO, DIP dynamics, chattering mitigation
   ```

2. **Integrate with Citation System**:
   Use Perplexity to auto-populate `.ai/planning/phase2-5/` citation data

3. **Controller Development Workflow**:
   Before implementing new controllers:
   - Research latest papers with Perplexity
   - Compare with existing controllers in `src/controllers/`
   - Implement with literature-backed parameter ranges

4. **Documentation Enhancement**:
   Use Perplexity to validate claims in:
   - `docs/mathematical_foundations/`
   - `docs/guides/theory/`
   - Controller docstrings

## Example Output (Expected)

**Test Query**: "Research recent papers on chattering mitigation in SMC"

**Expected Response**:
```
Based on recent literature (2024-2025), here are key findings on chattering mitigation:

1. **Boundary Layer Adaptation** (Chen et al., 2024)
   - DOI: 10.1109/TAC.2024.xxxxx
   - Recommends φ = 0.1-0.5 for DIP systems
   - Adaptive boundary layer outperforms fixed by 30%

2. **Higher-Order Sliding Modes** (Kumar, 2024)
   - Journal: IEEE Trans. Control Systems
   - Super-twisting shows 85% chattering reduction
   - Optimal α₁ = 1.5, α₂ = 1.1 for underactuated systems

3. **Fuzzy Boundary Layers** (Lee & Park, 2025)
   - Conference: ACC 2025
   - Fuzzy logic boundary adaptation
   - Reduces chattering while maintaining accuracy

[Claude then compares these findings with your implementation in
 src/controllers/sta_smc.py:156-178 and suggests parameter updates]
```

## Reference

- Setup guide: `.ai/config/perplexity_setup.md`
- MCP configuration: `.mcp.json`
- Auto-trigger rules: `CLAUDE.md` Section 20.1
- Perplexity dashboard: https://www.perplexity.ai/settings/api
