# Phase 2 Execution Guide - HIGH & MEDIUM Batch Research **Document Version:** 1.0.0
**Created:** 2025-10-08
**Status:** ✅ **READY FOR EXECUTION** --- ## Overview This guide provides step-by-step instructions to complete Phase 2 AI Research by processing all 497 remaining claims (459 HIGH + 38 MEDIUM) across 9 batches. **Total Scope:**
- **11 CRITICAL claims:** ✅ Already completed (22 citations generated)
- **459 HIGH claims:** 🔵 Ready for execution (9 batches)
- **38 MEDIUM claims:** 🔵 Ready for execution (1 batch)
- **Total remaining:** 497 claims --- ## Tooling (Completed ✅) All required tools have been created and are ready to use: ### 1. Batch Creation Tool
**Location:** `.dev_tools/research/create_batch.py` **Purpose:** Extract claims by module/priority from inventory **Usage:**
```bash
python .dev_tools/research/create_batch.py --module optimization --priority HIGH --output batch_output.json
python .dev_tools/research/create_batch.py --priority MEDIUM --output batch_medium.json
python .dev_tools/research/create_batch.py --list-modules # List available modules
``` ### 2. Batch Merge Tool
**Location:** `.dev_tools/research/merge_all_batches.py` **Purpose:** Merge all batch results and deduplicate BibTeX entries **Usage:**
```bash
# Auto-detect all batch files
python .dev_tools/research/merge_all_batches.py --auto # Manual specification
python .dev_tools/research/merge_all_batches.py \ --results artifacts/research/batch_*.json \ --output artifacts/research/phase2_complete.json \ --bibtex artifacts/research/enhanced_bibliography_phase2.bib
``` ### 3. Report Generator
**Location:** `.dev_tools/research/generate_phase2_report.py` **Purpose:** Generate Phase 2 completion report with validation **Usage:**
```bash
python .dev_tools/research/generate_phase2_report.py \ --results artifacts/research/phase2_complete.json \ --bibtex artifacts/research/enhanced_bibliography_phase2.bib \ --output-json artifacts/research/phase2_validation_report.json \ --output-md docs/plans/citation_system/phase2_completion_report.md
``` --- ## Batch Files (Created ✅) All 9 batch input files have been created and validated: | Batch | Module(s) | Priority | Claims | Time Estimate | Output File |
|-------|-----------|----------|--------|---------------|-------------|
| **1** | optimization | HIGH | 111 | 2.5-3 hours | `batch_01_optimization_high.json` |
| **2** | controllers | HIGH | 98 | 2-2.5 hours | `batch_02_controllers_high.json` |
| **3** | analysis | HIGH | 72 | 1.5-2 hours | `batch_03_analysis_high.json` |
| **4** | simulation | HIGH | 68 | 1.5-2 hours | `batch_04_simulation_high.json` |
| **5** | plant | HIGH | 33 | 45-60 min | `batch_05_plant_high.json` |
| **6** | interfaces | HIGH | 31 | 45-60 min | `batch_06_interfaces_high.json` |
| **7** | utils | HIGH | 26 | 30-45 min | `batch_07_utils_high.json` |
| **8** | benchmarks, integration, config, core, fault_detection | HIGH | 20 | 30-45 min | `batch_08_other_high.json` |
| **9** | all modules | MEDIUM | 38 | 1 hour | `batch_09_medium_all.json` |
| **Total** | | | **497** | **12-15 hours** | | **Location:** `.artifacts/batch_*.json` --- ## Execution Workflow ### Phase 1: Batch Execution (12-15 hours total) Execute each batch sequentially using the research pipeline: #### Batch 1: Optimization (111 claims, 2.5-3 hours) ```bash
python .dev_tools/research/research_pipeline.py \ --claims .artifacts/batch_01_optimization_high.json \ --output artifacts/research/batch_01_results.json \ --bibtex artifacts/research/batch_01_bibliography.bib \ --log logs/research_batch_01.log
``` **Expected Output:**
- `artifacts/research/batch_01_results.json` - Research results
- `artifacts/research/batch_01_bibliography.bib` - BibTeX entries
- `logs/research_batch_01.log` - Execution log
- Checkpoints in `artifacts/checkpoints/` (auto-saved every 50 claims) **Validation (after completion):**
```bash
python .dev_tools/research/validate_results.py \ --results artifacts/research/batch_01_results.json \ --bibtex artifacts/research/batch_01_bibliography.bib
``` #### Batch 2-9: Repeat Pattern Use the same command structure, replacing batch numbers: ```bash
# Batch 2 (Controllers)
python .dev_tools/research/research_pipeline.py \ --claims .artifacts/batch_02_controllers_high.json \ --output artifacts/research/batch_02_results.json \ --bibtex artifacts/research/batch_02_bibliography.bib \ --log logs/research_batch_02.log # Batch 3 (Analysis)
python .dev_tools/research/research_pipeline.py \ --claims .artifacts/batch_03_analysis_high.json \ --output artifacts/research/batch_03_results.json \ --bibtex artifacts/research/batch_03_bibliography.bib \ --log logs/research_batch_03.log # ... and so on for batches 4-9
``` **Checkpoint Recovery (if interrupted):**
```bash
# Resume from checkpoint (automatically detected)
python .dev_tools/research/research_pipeline.py \ --claims .artifacts/batch_01_optimization_high.json \ --output artifacts/research/batch_01_results.json \ --bibtex artifacts/research/batch_01_bibliography.bib \ --resume # Automatically loads latest checkpoint
``` --- ### Phase 2: Merge & Validation (1-2 hours) After all 9 batches are complete: #### Step 1: Merge All Batches ```bash
python .dev_tools/research/merge_all_batches.py --auto
``` **Expected Output:**
- `artifacts/research/phase2_complete.json` - Unified results (all 497 claims)
- `artifacts/research/enhanced_bibliography_phase2.bib` - Deduplicated BibTeX (400-600 entries estimated) **Validation:**
```bash
# Check merged file exists and has correct claim count
python -c "import json; data = json.load(open('artifacts/research/phase2_complete.json')); print(f'Total claims: {len(data[\"results\"])}')"
# Expected: Total claims: 497 # Count unique BibTeX entries
grep -c "^@" artifacts/research/enhanced_bibliography_phase2.bib
# Expected: 400-750 entries (depending on deduplication)
``` #### Step 2: Generate Completion Report ```bash
python .dev_tools/research/generate_phase2_report.py
``` **Expected Output:**
- `artifacts/research/phase2_validation_report.json` - Validation metrics
- `docs/plans/citation_system/phase2_completion_report.md` - Human-readable report **Review Quality Gates:**
```bash
# Check if all gates passed
python -c "import json; report = json.load(open('artifacts/research/phase2_validation_report.json')); print(f'Overall Pass: {report[\"overall_pass\"]}')"
``` --- ## Quality Targets ### Mandatory Gates (Must Pass) | Metric | Target | Notes |
|--------|--------|-------|
| **Citation Coverage** | ≥75% claims with ≥2 citations | Adjusted for HIGH batch (vs 85% for CRITICAL) |
| **BibTeX Compilation** | 0 syntax errors | Must compile without errors |
| **Duplicate Entries** | 0 duplicates | Automatic deduplication via merge tool |
| **DOI/URL Accessibility** | ≥90% accessible | DOI or ArXiv/URL required | ### Optional Enhancements (Stretch Goals) | Metric | Target | Notes |
|--------|--------|-------|
| **Citation Coverage** | ≥80% claims with ≥2 citations | Exceeds minimum requirement |
| **Average Citations** | ≥2.0 per claim | Match CRITICAL batch performance |
| **DOI Coverage** | ≥95% with DOIs | Higher than minimum URL requirement | --- ## Risk Mitigation ### API Rate Limiting (High Probability) **Risk:** Semantic Scholar API limits (100 req/5min) will be exceeded **Mitigation:**
- Exponential backoff already implemented in `research_pipeline.py`
- Checkpoint recovery every 50 claims
- Allow overnight execution for large batches
- Consider splitting Batch 1 (111 claims) into 2 sub-batches if rate limiting severe **Detection:**
```bash
# Monitor for rate limiting in logs
tail -f logs/research_batch_01.log | grep -i "rate limit\|backoff\|429"
``` ### Low Relevance Citations (Medium Probability) **Risk:** Implementation claims yield less relevant academic papers than theorems **Mitigation:**
- Query generator includes implementation-specific keywords
- Accept lower citation counts for utility/visualization claims
- Manual curation of top 50 most-cited implementation claims (optional) **Quality Check:**
```bash
# After batch completion, review citation relevance
python -c "
import json
data = json.load(open('artifacts/research/batch_01_results.json'))
for result in data['results'][:5]: # Check first 5 claims print(f\"Claim: {result['claim_id']}\") for paper in result.get('selected_citations', []): print(f\" - {paper.get('fields', {}).get('title', 'N/A')}\") print()
"
``` ### Time Budget Overrun (Low-Medium Probability) **Risk:** 12-15 hour estimate exceeded due to API delays **Mitigation:**
- Process highest-priority batches first (1-2: optimization, controllers)
- Allow flexible completion timeline (Week 4-5)
- Use parallel sessions if multiple accounts available --- ## Progress Tracking ### Session Checklist Use this checklist to track batch execution progress: - [ ] **Batch 1:** Optimization (111 claims) - Est. 2.5-3 hours
- [ ] **Batch 2:** Controllers (98 claims) - Est. 2-2.5 hours
- [ ] **Batch 3:** Analysis (72 claims) - Est. 1.5-2 hours
- [ ] **Batch 4:** Simulation (68 claims) - Est. 1.5-2 hours
- [ ] **Batch 5:** Plant (33 claims) - Est. 45-60 min
- [ ] **Batch 6:** Interfaces (31 claims) - Est. 45-60 min
- [ ] **Batch 7:** Utils (26 claims) - Est. 30-45 min
- [ ] **Batch 8:** Other modules (20 claims) - Est. 30-45 min
- [ ] **Batch 9:** MEDIUM priority (38 claims) - Est. 1 hour
- [ ] **Merge & Validation:** Combine all batches - Est. 1-2 hours
- [ ] **Generate Report:** Create completion report - Est. 30 min ### Validation Checklist After merging: - [ ] All 497 claims processed (check `phase2_complete.json`)
- [ ] BibTeX compiles without errors
- [ ] No duplicate entries (check `phase2_validation_report.json`)
- [ ] ≥75% claims have ≥2 citations
- [ ] ≥90% papers have DOI or URL
- [ ] All quality gates passed --- ## Success Criteria Phase 2 is considered complete when: 1. ✅ All 497 claims researched (9 batches executed)
2. ✅ Merged results file exists with all claims
3. ✅ BibTeX file compiles without errors
4. ✅ Citation coverage ≥75%
5. ✅ DOI/URL accessibility ≥90%
6. ✅ Validation report generated with all gates PASS **Expected Outcomes:**
- **Total citations:** 690-920 (497 claims × 1.5-2.0 avg)
- **Unique BibTeX entries:** 400-600 (after deduplication)
- **Total papers reviewed:** 2485-2970 (497 claims × 5 papers/claim)
- **Phase 2 completion:** ~942 total citations (22 CRITICAL + 920 HIGH/MEDIUM) --- ## Troubleshooting ### Problem: Batch execution fails with "API Error" **Solution:**
```bash
# Check API status
curl -I https://api.semanticscholar.org/ # Resume from checkpoint
python .dev_tools/research/research_pipeline.py \ --claims .artifacts/batch_XX.json \ --output artifacts/research/batch_XX_results.json \ --resume
``` ### Problem: BibTeX has duplicate entries **Solution:**
```bash
# Re-run merge with deduplication
python .dev_tools/research/merge_all_batches.py --auto # Verify no duplicates
python -c "
import re
content = open('artifacts/research/enhanced_bibliography_phase2.bib').read()
keys = re.findall(r'@\w+\{([^,]+),', content)
duplicates = [k for k in set(keys) if keys.count(k) > 1]
print(f'Duplicates: {duplicates}')
"
``` ### Problem: Validation report shows < 75% coverage **Analysis:**
```bash
# Identify claims with 0 citations
python -c "
import json
data = json.load(open('artifacts/research/phase2_complete.json'))
no_cites = [r for r in data['results'] if len(r.get('selected_citations', [])) == 0]
print(f'Claims with 0 citations: {len(no_cites)}')
for claim in no_cites[:10]: # Show first 10 print(f\" - {claim['claim_id']}: {claim.get('claim_text', '')[:60]}...\")
" # Re-run failed claims with manual query refinement
# (Create new batch file with only failed claims and re-execute)
``` --- ## Next Steps After Completion Once Phase 2 is complete: 1. **Archive batch artifacts:** ```bash mkdir -p .archive/phase2_batches mv .artifacts/batch_*.json .archive/phase2_batches/ ``` 2. **Update master roadmap:** - Mark Phase 2 as ✅ COMPLETE - Update total citation count - Note any lessons learned 3. **Begin Phase 3: Manual Curation & Quality Review** - Review top 50 most-cited claims - Curate references for accuracy - Add missing citations manually if needed --- ## Related Documents - [00_master_roadmap.md](00_master_roadmap.md) - Complete 5-phase plan
- [02_phase1_claim_extraction.md](02_phase1_claim_extraction.md) - Phase 1 completion
- [week_1_2_critical_batch_completion.md](week_1_2_critical_batch_completion.md) - CRITICAL batch results
- [high_batch_execution_plan.json](../../../artifacts/research/high_batch_execution_plan.json) - Original HIGH batch strategy --- **Document Status:** ✅ Ready for execution
**Last Updated:** 2025-10-08
**Estimated Completion:** Week 4-5 (2-3 weeks from start)
