# PROJECT NAMING CONVENTIONS
## Professional Directory and File Naming Standards

**Last Updated**: October 26, 2025
**Status**: MANDATORY for all new directories and files

---

## PURPOSE

This document establishes **single source of truth** naming conventions to ensure:
- **Human-Readable**: Future you (and collaborators) understand what's inside from the name
- **Professional**: No task IDs, no "failed", no meaningless codes
- **Consistent**: One standard across entire project
- **Searchable**: Descriptive names easy to grep/find
- **Maintainable**: Clear rules prevent naming chaos

---

## CORE PRINCIPLES

### Principle 1: DESCRIPTIVE NAMES (No Task IDs)
**WHY**: Task IDs (LT7, MT4, QW-3) are meaningless outside your planning context. Future you won't remember what "LT7" means.

❌ **BAD**: `LT7_research_paper`, `MT6_experiment`, `QW_notes`
✅ **GOOD**: `masters_research_paper`, `boundary_layer_experiment`, `control_theory_notes`

### Principle 2: snake_case for ALL Directories
**WHY**: Consistent, readable, works across Windows/Linux/Mac

❌ **BAD**: `MyResearch`, `Research-Paper`, `research.paper`
✅ **GOOD**: `my_research`, `research_paper`

### Principle 3: lowercase for ALL Directories
**WHY**: Prevents case-sensitivity issues across operating systems

❌ **BAD**: `ResearchPaper`, `MASTERS_THESIS`, `ExperimentData`
✅ **GOOD**: `research_paper`, `masters_thesis`, `experiment_data`

### Principle 4: Dates ONLY When Meaningful
**WHY**: Dates clutter names. Use only for archived/versioned content.

**When to use dates**:
- Archived experiments: `pso_stability_experiment_2024_09`
- Backup snapshots: `config_backup_2024_10_15`
- Versioned data: `benchmark_results_2024_q4`

**When NOT to use dates**:
- Active work: `research_paper` (NOT `research_paper_2024`)
- Current directories: `workspace`, `notes`, `drafts`

**Format**: `YYYY_MM` or `YYYY_MM_DD` (ISO 8601 compatible)

### Principle 5: Purpose-Based, Not Status-Based
**WHY**: "Failed" is meaningless for archives. Describe WHAT was tested.

❌ **BAD**: `pso_failed_run`, `broken_experiment`, `old_code`
✅ **GOOD**: `pso_stability_test`, `convergence_experiment`, `legacy_controller`

### Principle 6: No Abbreviations (Unless Standard)
**WHY**: Abbreviations lose meaning over time

❌ **BAD**: `tmp`, `misc`, `aux`, `bkp`
✅ **GOOD**: `temporary`, `miscellaneous`, `auxiliary`, `backup`

**Exceptions** (industry standard abbreviations OK):
- `pso` (Particle Swarm Optimization)
- `smc` (Sliding Mode Control)
- `dip` (Double Inverted Pendulum)
- `api`, `cli`, `gui` (common tech terms)

---

## DIRECTORY NAMING RULES

### Rule 1: Workspace Directories
**Format**: `{subject}_workspace` or `{subject}_notes`

**Examples**:
- `control_theory_workspace`
- `smc_design_notes`
- `pso_tuning_workspace`

### Rule 2: Archived Experiments
**Format**: `{algorithm}_{purpose}_experiment_{YYYY_MM}`

**Examples**:
- `pso_stability_experiment_2024_09`
- `smc_chattering_test_2024_10`
- `hybrid_controller_validation_2024_q4`

### Rule 3: Backup/Archive Directories
**Format**: `{content}_archive_{YYYY_MM}` or `{content}_backup_{YYYY_MM_DD}`

**Examples**:
- `documentation_archive_2024_10`
- `config_backup_2024_10_15`
- `notebooks_legacy_2024_09`

### Rule 4: Research/Paper Directories
**Format**: `{academic_level}_{type}` or `{purpose}_paper`

**Examples**:
- `masters_research_paper` (NOT `LT7_research_paper`)
- `conference_paper_2024`
- `thesis_chapters`

### Rule 5: Testing/Validation Directories
**Format**: `{component}_testing` or `test_{purpose}`

**Examples**:
- `controller_testing`
- `integration_testing`
- `test_artifacts`

---

## FILE NAMING RULES

### Rule 1: Scripts
**Format**: `{verb}_{purpose}.py` or `{tool}_{action}.py`

**Examples**:
- `generate_convergence_plots.py`
- `validate_controller_performance.py`
- `extract_benchmark_results.py`

### Rule 2: Configuration Files
**Format**: `{component}_config.{ext}` or `{purpose}.yaml`

**Examples**:
- `controller_config.yaml`
- `pso_parameters.json`
- `test_suite_config.ini`

### Rule 3: Data Files
**Format**: `{content}_{YYYY_MM_DD}.{ext}` or `{experiment}_{run_id}.csv`

**Examples**:
- `benchmark_results_2024_10_15.csv`
- `pso_convergence_run_42.json`
- `controller_performance_metrics.csv`

### Rule 4: Documentation Files
**Format**: `{SUBJECT}.md` (UPPERCASE for important docs)

**Examples**:
- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `setup_guide.md` (lowercase for regular docs)

---

## ANTI-PATTERNS (NEVER DO THIS)

### ❌ Task IDs in Names
```
lt4_theory/             → control_theory_workspace/
LT7_research_paper/     → masters_research_paper/
MT6_experiment/         → boundary_layer_experiment/
QW-3_notes/             → pso_tuning_notes/
```

### ❌ "Failed" in Names
```
pso_failed_run/                    → pso_stability_experiment_2024_09/
broken_controller/                 → legacy_controller_archive/
old_backup/                        → config_backup_2024_09/
```

### ❌ Mixed Case
```
MyResearch/                        → my_research/
ResearchPaper/                     → research_paper/
TestData/                          → test_data/
```

### ❌ Meaningless Abbreviations
```
tmp/                               → temporary/
misc/                              → miscellaneous/
aux/                               → auxiliary/
bkp_20241015/                      → backup_2024_10_15/
```

### ❌ Dates Everywhere
```
research_paper_2024/               → research_paper/ (active work)
notes_2024_10/                     → control_theory_notes/ (current)
```
(Dates only for archives/backups!)

### ❌ Duplicate Nesting
```
testing/testing/                   → testing/ (flatten)
archive/archive/                   → archive/ (flatten)
data/data_files/                   → data/ (flatten)
```

---

## VALIDATION CHECKLIST

Before creating a new directory or file, ask:

1. [ ] **Descriptive**: Can someone understand purpose from name alone?
2. [ ] **No Task IDs**: Removed all LT/MT/QW/etc codes?
3. [ ] **snake_case**: All lowercase with underscores?
4. [ ] **Purpose-Based**: Describes WHAT, not status (failed/broken/old)?
5. [ ] **Date Justified**: Only used if archived/versioned?
6. [ ] **Standard Abbreviations**: Only PSO/SMC/DIP/API-type terms?

If all ✅, proceed. If any ❌, revise name.

---

## EXAMPLES OF GOOD RENAMING

### Before (CHAOTIC)
```
.artifacts/
├── lt4_theory_scratch/
├── LT7_research_paper/
├── testing/testing/

.project/archive_temp/
├── pso_failed_run_20250930/
├── pso_hybrid_failed_20250930/
├── docs_archive_20251009/
```

### After (PROFESSIONAL)
```
.artifacts/
├── control_theory_workspace/
├── masters_research_paper/
├── testing/

.project/archive/
├── pso_stability_experiment_2024_09/
├── pso_hybrid_algorithm_test_2024_09/
├── documentation_archive_2024_10/
```

---

## ENFORCEMENT

### Mandatory
- **All new directories**: MUST follow these conventions
- **All new files**: MUST follow these conventions
- **Code reviews**: Check naming compliance
- **Documentation updates**: Reference this file when adding directories

### Optional (But Encouraged)
- Rename existing directories during cleanup phases
- Update old scripts to use new paths
- Maintain backward compatibility symlinks if needed

---

## FUTURE EXPANSIONS

**If project grows**, consider:
- **Module prefixes**: `controller_`, `optimizer_`, `plant_` for categorization
- **Version suffixes**: `_v1`, `_v2` for major architectural changes
- **Environment markers**: `_dev`, `_prod` for deployment-specific configs

**But only add complexity when truly needed!**

---

## REFERENCES

- **CLAUDE.md Section 14**: Workspace organization rules
- **Restructuring Plan**: `.project/dev_tools/RESTRUCTURING_PLAN_2025-10-26.md`
- **ISO 8601 Dates**: https://en.wikipedia.org/wiki/ISO_8601
- **snake_case Reference**: https://en.wikipedia.org/wiki/Snake_case

---

**Questions?** See `.project/dev_tools/` or ask the team lead.

**When in doubt**: Descriptive + snake_case + lowercase = ✅
