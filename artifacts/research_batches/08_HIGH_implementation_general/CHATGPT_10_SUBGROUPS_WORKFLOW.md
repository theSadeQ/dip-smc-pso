# ChatGPT 10 Subgroups Workflow - Process 91 Remaining Claims

**Total Claims**: 91
**Strategy**: Split into 10 logical subgroups for easier ChatGPT processing
**Expected Time**: ~5 minutes per subgroup = ~50 minutes total

---

## Subgroup Summary

| # | Subgroup | Claims | Focus Area |
|---|----------|--------|------------|
| 1 | SMC Algorithms - Adaptive & Hybrid | 9 | RLS, parameter estimation, hybrid switching |
| 2 | SMC Core - Equivalent Control & Switching | 7 | Equivalent control, switching functions, chattering |
| 3 | SMC Controllers - Classical & Super-Twisting | 6 | Classical SMC, Super-Twisting initialization |
| 4 | Optimization Core & Interfaces | 10 | Optimization interfaces, factory methods |
| 5 | Multi-Objective Optimization | 10 | Pareto, weighted sum, robustness objectives |
| 6 | Plant Models - Full & Low-Rank | 6 | Full fidelity dynamics, low-rank models |
| 7 | Plant Models - Simplified & Interfaces | 10 | Simplified dynamics, physics matrices |
| 8 | Simulation Integrators - Euler & RK | 11 | Euler methods, RK45 adaptive integration |
| 9 | Simulation Core & Orchestrators | 10 | Simulation context, orchestrators, safety |
| 10 | Miscellaneous & Utilities | 12 | Benchmarks, MPC, compatibility, results |

**Total**: 91 claims

---

## Complete Workflow

### Step 1: Process Subgroup 1 (SMC Adaptive & Hybrid - 9 claims)

**Prompt file**: `prompts/group_01_smc_adaptive_hybrid_prompt.md`

1. Open the prompt file
2. Copy entire content (Ctrl+A, Ctrl+C)
3. Paste into ChatGPT
4. Wait for response (JSON array with 9 claims)
5. Copy ChatGPT's JSON output
6. Save as: `subgroups/group_01_smc_adaptive_hybrid_output.json`

**Expected Categories**:
- Category A: RLS algorithm (CODE-IMPL-135), hybrid switching (CODE-IMPL-152)
- Category C: Initialization, setters (CODE-IMPL-122, 150)

---

### Step 2: Process Subgroup 2 (SMC Core - 7 claims)

**Prompt file**: `prompts/group_02_smc_core_prompt.md`

1. Open the prompt file
2. Copy entire content
3. Paste into ChatGPT
4. Wait for response (JSON array with 7 claims)
5. Save as: `subgroups/group_02_smc_core_output.json`

**Expected Categories**:
- Category A: Equivalent control (CODE-IMPL-181)
- Category B: Chattering (CODE-IMPL-192, 195)
- Category C: Validation, utilities (CODE-IMPL-183, 193, 194)

---

### Step 3: Process Subgroup 3 (SMC Controllers - 6 claims)

**Prompt file**: `prompts/group_03_smc_controllers_prompt.md`

1. Open the prompt file
2. Copy entire content
3. Paste into ChatGPT
4. Wait for response (JSON array with 6 claims)
5. Save as: `subgroups/group_03_smc_controllers_output.json`

**Expected Categories**:
- Category A: Super-Twisting algorithm (CODE-IMPL-201, 204)
- Category C: Reset, initialization (CODE-IMPL-180, 167)

---

### Step 4: Process Subgroup 4 (Optimization Core - 10 claims)

**Prompt file**: `prompts/group_04_optimization_core_prompt.md`

1. Open the prompt file
2. Copy entire content
3. Paste into ChatGPT
4. Wait for response (JSON array with 10 claims)
5. Save as: `subgroups/group_04_optimization_core_output.json`

**Expected Categories**:
- Category C: Most claims (factory methods, interfaces, properties)
- Possibly Category A for population update (CODE-IMPL-331)

---

### Step 5: Process Subgroup 5 (Multi-Objective Optimization - 10 claims)

**Prompt file**: `prompts/group_05_optimization_multi_prompt.md`

1. Open the prompt file
2. Copy entire content
3. Paste into ChatGPT
4. Wait for response (JSON array with 10 claims)
5. Save as: `subgroups/group_05_optimization_multi_output.json`

**Expected Categories**:
- Category A: Pareto (CODE-IMPL-340), weighted sum (CODE-IMPL-342)
- Category B: Robustness concept (CODE-IMPL-336)
- Category C: Initialization, utilities

---

### Step 6: Process Subgroup 6 (Plant Full & Low-Rank - 6 claims)

**Prompt file**: `prompts/group_06_plant_full_lowrank_prompt.md`

1. Open the prompt file
2. Copy entire content
3. Paste into ChatGPT
4. Wait for response (JSON array with 6 claims)
5. Save as: `subgroups/group_06_plant_full_lowrank_output.json`

**Expected Categories**:
- Category C: Most claims (model implementations, physics computations)

---

### Step 7: Process Subgroup 7 (Plant Simplified - 10 claims)

**Prompt file**: `prompts/group_07_plant_simplified_prompt.md`

1. Open the prompt file
2. Copy entire content
3. Paste into ChatGPT
4. Wait for response (JSON array with 10 claims)
5. Save as: `subgroups/group_07_plant_simplified_output.json`

**Expected Categories**:
- Category C: All claims (simplified models, JIT compilation, interfaces)

---

### Step 8: Process Subgroup 8 (Integrators - 11 claims)

**Prompt file**: `prompts/group_08_integrators_prompt.md`

1. Open the prompt file
2. Copy entire content
3. Paste into ChatGPT
4. Wait for response (JSON array with 11 claims)
5. Save as: `subgroups/group_08_integrators_output.json`

**Expected Categories**:
- Category A: Euler methods (CODE-IMPL-451, 452, 454, 455, 457, 458, 460)
- Category A: RK45 (CODE-IMPL-437, 438)
- Category C: Base class initialization (CODE-IMPL-440, 443)

---

### Step 9: Process Subgroup 9 (Simulation Core - 10 claims)

**Prompt file**: `prompts/group_09_simulation_core_prompt.md`

1. Open the prompt file
2. Copy entire content
3. Paste into ChatGPT
4. Wait for response (JSON array with 10 claims)
5. Save as: `subgroups/group_09_simulation_core_output.json`

**Expected Categories**:
- Category A: Euler simulation step (CODE-IMPL-423)
- Category C: Context, orchestrators, infrastructure (rest)

---

### Step 10: Process Subgroup 10 (Miscellaneous - 12 claims)

**Prompt file**: `prompts/group_10_misc_utilities_prompt.md`

1. Open the prompt file
2. Copy entire content
3. Paste into ChatGPT
4. Wait for response (JSON array with 12 claims)
5. Save as: `subgroups/group_10_misc_utilities_output.json`

**Expected Categories**:
- Category C: Most claims (utilities, compatibility, safety, containers)

---

## After All 10 Subgroups Are Processed

### Merge Outputs

Run the merge script to combine all 10 subgroup outputs:

```bash
python .dev_tools/merge_subgroup_outputs.py
```

**This will**:
- Load all 10 output JSON files
- Merge into single `chatgpt_output_91_citations.json`
- Validate total count (should be 91)
- Show category breakdown

### Apply Citations to CSV

Run the citation application script:

```bash
python .dev_tools/apply_chatgpt_citations.py
```

**This will**:
- Load `chatgpt_output_91_citations.json`
- Apply citations to `claims_research_tracker.csv`
- Mark claims as completed
- Generate completion report

### Verify 100% Completion

Check final status:

```bash
python -c "import csv; rows = list(csv.DictReader(open('D:/Projects/main/artifacts/claims_research_tracker.csv', 'r', encoding='utf-8'))); batch08 = [r for r in rows if r['Claim_ID'].startswith('CODE-IMPL-')]; completed = sum(1 for r in batch08 if r['Research_Status'] == 'completed'); print(f'Batch 08: {completed}/314 completed')"
```

**Expected**: `Batch 08: 314/314 completed (100%)`

---

## File Locations

**Prompts** (input for ChatGPT):
- `prompts/group_01_smc_adaptive_hybrid_prompt.md`
- `prompts/group_02_smc_core_prompt.md`
- `prompts/group_03_smc_controllers_prompt.md`
- `prompts/group_04_optimization_core_prompt.md`
- `prompts/group_05_optimization_multi_prompt.md`
- `prompts/group_06_plant_full_lowrank_prompt.md`
- `prompts/group_07_plant_simplified_prompt.md`
- `prompts/group_08_integrators_prompt.md`
- `prompts/group_09_simulation_core_prompt.md`
- `prompts/group_10_misc_utilities_prompt.md`

**Outputs** (ChatGPT responses - YOU CREATE THESE):
- `subgroups/group_01_smc_adaptive_hybrid_output.json`
- `subgroups/group_02_smc_core_output.json`
- ... (10 files total)

**Merged Output** (auto-generated):
- `chatgpt_output_91_citations.json`

---

## Tips

1. **Process sequentially**: Do one subgroup at a time to avoid confusion
2. **Validate JSON**: Ensure ChatGPT's response is valid JSON (starts with `[`, ends with `]`)
3. **Check counts**: Each output should match the claim count (9, 7, 6, 10, 10, 6, 10, 11, 10, 12)
4. **Save carefully**: Use exact filenames (group_XX_*_output.json)
5. **ChatGPT model**: Use GPT-4 or Claude for best citation quality

---

## Expected Timeline

- **Subgroups 1-10**: ~5 minutes each = 50 minutes
- **Merge outputs**: <1 minute
- **Apply citations**: <1 minute
- **Total**: ~52 minutes to 100% completion

---

## Troubleshooting

**ChatGPT returns incomplete JSON**:
- Ask: "Please complete the JSON array"
- Or re-run with: "Continue from claim CODE-IMPL-XXX"

**Wrong number of claims in output**:
- Check if ChatGPT skipped any claim IDs
- Manually add missing claims using the prompt template

**Merge script fails**:
- Verify all 10 output files exist
- Check JSON validity of each file

**Apply script fails**:
- Run validation: `python .dev_tools/citation_validator.py`
- Fix any citation format issues
