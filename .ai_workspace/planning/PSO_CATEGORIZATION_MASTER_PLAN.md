# PSO Optimization Categorization Master Plan
## 6-Framework Organization System

**Created:** December 30, 2025
**Updated:** December 31, 2025 (added Regional Hybrid SMC)
**Purpose:** Comprehensive categorization system for PSO optimization work
**Scope:** 153 files, 60 scenarios, 8 controllers
**Location:** `.ai_workspace/planning/`

---

## Executive Summary

This document defines 6 complementary categorization frameworks for organizing all PSO optimization work across the double-inverted pendulum project. Each framework serves a specific purpose and audience.

**Status:** PLANNING PHASE
**Implementation Priority:** MEDIUM (post-publication enhancement)
**Estimated Effort:** 15-20 hours (full implementation)

---

## Table of Contents

1. [Framework Definitions](#framework-definitions)
2. [Current State Analysis](#current-state-analysis)
3. [Implementation Plan](#implementation-plan)
4. [Directory Structure Proposal](#directory-structure-proposal)
5. [Migration Strategy](#migration-strategy)
6. [Usage Guidelines](#usage-guidelines)
7. [Maintenance Plan](#maintenance-plan)

---

## Framework Definitions

### Framework 1: By Optimization Purpose/Objective

**Audience:** Researchers, paper writers, application engineers
**Primary Use:** Research papers, publications, application selection

#### Categories

1. **Performance-Focused (Speed/Accuracy)**
   - Goal: Minimize RMSE, settling time, overshoot
   - Scenarios: S1 (Nominal PSO), S10 (Phase-based)
   - Status: ⚠️ 80% complete (4/5 core controllers, Regional Hybrid pending PSO)
   - Files: 23 gain files
   - Priority: HIGH

2. **Safety-Focused (Chattering Reduction)**
   - Goal: Minimize control chattering, ensure smoothness
   - Scenarios: S9 (Boundary layer), S4 (Multi-objective - MISSING)
   - Status: ⚠️ 50% complete
   - Files: 21 files (MT-6)
   - Priority: MEDIUM

3. **Robustness-Focused (Reliability)**
   - Goal: Maintain performance under uncertainty/disturbances
   - Scenarios: S2 (Robust PSO), S3 (Multi-seed), S7 (Uncertainty - MISSING), S8 (Disturbance)
   - Status: ⚠️ 75% complete
   - Files: 40 files (MT-7, MT-8, LT-6)
   - Priority: HIGH

4. **Efficiency-Focused (Energy/Resources)**
   - Goal: Minimize control effort, energy consumption
   - Scenarios: S4 (Multi-objective - MISSING), S6 (Long-duration - MISSING)
   - Status: ❌ 0% complete
   - Priority: LOW

5. **Multi-Objective (Balanced Trade-offs)**
   - Goal: Pareto-optimal solutions across objectives
   - Scenarios: S4 (Multi-objective - MISSING)
   - Status: ❌ 0% complete
   - Priority: HIGH (research contribution)

**Implementation:**
- Create subdirectories in `.ai_workspace/pso/by_purpose/`
- Symlinks to actual data (avoid duplication)
- README files explaining each category
- Cross-reference tables

---

### Framework 2: By Validation Maturity Level (TRL)

**Audience:** Quality assurance, deployment engineers, project managers
**Primary Use:** Configuration management, risk assessment, deployment decisions

#### Maturity Levels

1. **Level 1: Theoretical Bounds (TRL 1-2)**
   - Status: Configuration only, not empirically validated
   - Files: config.yaml, registry.py
   - Controllers: All 6
   - Purpose: Stability-informed bounds

2. **Level 2: Simulation-Validated (TRL 3-4)**
   - Status: Nominal simulation conditions
   - Files: Phase 53 gains, Phase 2 standard
   - Controllers: All 4 core (100%)
   - Purpose: Basic validation

3. **Level 3: Statistical Validation (TRL 4-5)**
   - Status: Multi-seed Monte Carlo
   - Files: MT-7 data (10 seeds × 50 runs)
   - Controllers: STA only (25%)
   - Purpose: Statistical significance

4. **Level 4: Robustness-Validated (TRL 5-6)**
   - Status: Disturbances/uncertainty tested
   - Files: MT-8 data, LT-6 data
   - Controllers: All 4 core (100%)
   - Purpose: Reliability assurance

5. **Level 5: Hardware-Validated (TRL 6-7)**
   - Status: Preliminary HIL only
   - Files: MT8_hil_validation_results.json
   - Controllers: Classical SMC only (10%)
   - Purpose: Hardware verification

6. **Level 6: Production-Deployed (TRL 8-9)**
   - Status: Active in config.yaml
   - Files: config.yaml controller_defaults
   - Controllers: All 4 core (100%)
   - Purpose: Production use

7. **Level 7: Archived/Superseded (Historical)**
   - Status: Historical reference
   - Files: archive/ directories
   - Controllers: Adaptive, Hybrid
   - Purpose: Git history, reproducibility

**Implementation:**
- Create `.ai_workspace/pso/by_maturity/` with 7 subdirectories
- Symlinks organized by TRL level
- Quality gates documentation
- Promotion criteria (Level N → Level N+1)

---

### Framework 3: By Research Task/Campaign

**Audience:** Developers, researchers, documentation writers
**Primary Use:** Navigation, reproducibility, historical context

#### Research Tasks

1. **QW-3: PSO Visualization (Week 1)**
   - Date: October 29, 2025
   - Effort: 2 hours
   - Status: ✅ COMPLETE
   - Files: pso_plots.py
   - Deliverable: Convergence/diversity plots

2. **MT-6: Boundary Layer Optimization (Week 2-3)**
   - Date: October 26-27, 2025
   - Effort: 5 hours
   - Status: ✅ COMPLETE (target not achieved)
   - Files: 21 files in sta_smc/boundary_layer/
   - Finding: 3.7% chattering reduction (marginal)

3. **MT-7: Multi-Seed Robustness (Week 2-3)**
   - Date: October 19, 2025
   - Effort: 7 hours (bonus task)
   - Status: ✅ COMPLETE (STA only)
   - Files: 12 files in comparative/pso_robustness/
   - Finding: 50.4x degradation (overfitting detected)

4. **MT-8: Disturbance Rejection (Week 3-4)**
   - Date: November 8, 2025
   - Effort: 7 hours
   - Status: ✅ COMPLETE
   - Files: 5 files in comparative/disturbance_rejection/
   - Result: Hybrid +21.4% (best performer)

5. **LT-6: Model Uncertainty Analysis (Month 2-3)**
   - Date: October 18, 2025
   - Effort: 8 hours
   - Status: ✅ COMPLETE (analysis only)
   - Files: 2 files in comparative/model_uncertainty/
   - Gap: No re-optimization

6. **Phase-Based Progressive Optimization**
   - Phases: 2, 53
   - Status: ✅ COMPLETE
   - Files: 17 gain files across phases
   - Purpose: Progressive refinement

**Implementation:**
- Create `.ai_workspace/pso/by_task/` with task subdirectories
- Each task folder: README, data links, reports, figures
- Standardized task template
- Cross-references to experiments/

---

### Framework 4: By File Type/Artifact

**Audience:** Developers, data analysts, automation engineers
**Primary Use:** File navigation, automation, backup strategies

#### Artifact Types

1. **Configuration Files (3 files)**
   - config.yaml (PSO params + bounds)
   - registry.py (controller metadata)
   - pso_utils.py (factory integration)
   - Purpose: Reference for PSO runs

2. **Gain Files (23 files, JSON)**
   - Classical: 3 files
   - STA: 6 files
   - Adaptive: 8 files
   - Hybrid: 6 files
   - Format: `{"controller": [gain1, ..., gainN]}`

3. **Data Files (70 files, CSV/JSON/NPZ)**
   - CSV: 30 files (tabular metrics)
   - JSON: 35 files (summaries, statistics)
   - NPZ: 5 files (time-series arrays)
   - Purpose: Simulation results

4. **Report Files (42 files, Markdown)**
   - Task completion: 10 files
   - Deep dive analysis: 5 files
   - Closure reports: 3 files
   - Status updates: 8 files
   - Anomaly analysis: 14 files

5. **Visualization Files (16 PNG files, 3.6 MB)**
   - LT-7 figures: 8 files
   - MT-6 figures: 2 files
   - MT-7 figures: 4 files
   - MT-5 figures: 2 files
   - Critical: Preserved paths

6. **Log Files (6 files, 978 KB)**
   - Location: academic/logs/pso/
   - Purpose: Execution logs, debugging
   - Format: Timestamped text logs

7. **Source Code (3 files, Python)**
   - pso_optimizer.py (core algorithm)
   - pso_utils.py (factory integration)
   - pso_plots.py (visualization)
   - Purpose: Implementation

**Implementation:**
- Create `.ai_workspace/pso/by_filetype/` with 7 subdirectories
- Automated file classification scripts
- Backup strategies per type
- Size monitoring (visualizations largest)

---

### Framework 5: By Controller Architecture

**Audience:** Controller developers, architecture designers
**Primary Use:** Controller-specific analysis, architecture comparisons

#### Controller Groups

1. **Classical Controllers (2 controllers)**
   - Classical SMC: 80% coverage (8/10 scenarios)
   - STA SMC: 90% coverage (9/10 scenarios)
   - Characteristics: Fixed structure, 6 params, boundary layer
   - Files: 9 gain files, 33 data files

2. **Adaptive Controllers (3 controllers)**
   - Adaptive SMC: 75% coverage (7.5/10 scenarios)
   - Hybrid Adaptive STA: 85% coverage (8.5/10 scenarios)
   - Regional Hybrid SMC: 0% coverage (NEW - Dec 31, 2025, PSO pending)
   - Characteristics: Online adaptation, 4-5 params, research focus
   - Files: 14 gain files, 48 data files (Regional Hybrid not yet optimized)

3. **Specialized Controllers (2 controllers)**
   - Swing-Up SMC: 20% coverage (2/10 scenarios)
   - MPC: 0% coverage (N/A - different paradigm)
   - Characteristics: Non-standard, energy/optimization-based
   - Files: 0 dedicated files

**Implementation:**
- Already implemented in experiments/ (Dec 29, 2025)
- Create `.ai_workspace/pso/by_controller/` as reference
- Comparative analysis tools
- Coverage dashboards

---

### Framework 6: By Optimization Strategy/Algorithm

**Audience:** Algorithm researchers, PSO specialists
**Primary Use:** Algorithm selection, performance comparison

#### Strategy Types

1. **Single-Objective PSO (Standard)**
   - Algorithm: Canonical PSO (Kennedy & Eberhart 1995)
   - Configuration: 40 particles, 50-200 iters, w=0.7
   - Fitness: RMSE-based
   - Status: ✅ Complete (all 4 core controllers)

2. **Robust Multi-Scenario PSO**
   - Algorithm: PSO + multi-scenario fitness
   - Configuration: 15 scenarios, J_robust = 0.5*nominal + 0.5*disturbed
   - Fitness: Composite (nominal + disturbance)
   - Status: ✅ Complete (MT-8, all 4 core)

3. **Statistical Validation PSO**
   - Algorithm: Monte Carlo validation (not PSO variant)
   - Configuration: 10 seeds, 50 runs/seed
   - Analysis: Welch's t-test, Cohen's d
   - Status: ⚠️ STA only (Classical/Adaptive/Hybrid missing)

4. **Multi-Objective PSO (Missing)**
   - Algorithm: NSGA-II or MOPSO
   - Configuration: N/A (not implemented)
   - Purpose: Pareto-optimal trade-offs
   - Status: ❌ Missing (HIGH PRIORITY)

5. **Adaptive/Online PSO (Missing)**
   - Algorithm: Online gain updates
   - Configuration: N/A (not implemented)
   - Purpose: Real-time adaptation
   - Status: ❌ Missing (FUTURE WORK)

**Implementation:**
- Create `.ai_workspace/pso/by_strategy/` with algorithm subdirectories
- Algorithm comparison benchmarks
- Performance metrics per strategy
- Implementation templates for missing strategies

---

## Current State Analysis

### File Distribution

**Total Files:** 153 (PSO-related)

**By Location:**
- experiments/: 113 files (74%)
- config/: 3 files (2%)
- logs/: 6 files (4%)
- source code: 3 files (2%)
- docs/sphinx_docs/: 28 files (18%)

**By Framework Coverage:**
- Framework 1 (Purpose): 65% complete
- Framework 2 (Maturity): 85% complete
- Framework 3 (Task): 100% documented
- Framework 4 (Filetype): 100% classified
- Framework 5 (Controller): 100% organized
- Framework 6 (Strategy): 60% complete

**Overall Organization Score:** 78% (Good, room for improvement)

---

### Gap Analysis

**Critical Gaps (Blocking Publication):**
1. Multi-seed validation for Classical, Adaptive, Hybrid (Framework 3)
2. Documentation consolidation (Framework 3, 4)

**High-Priority Gaps (Post-Publication):**
1. Multi-objective PSO implementation (Framework 1, 6)
2. HIL-PSO workflow (Framework 2)
3. Uncertainty-aware PSO (Framework 1)

**Medium-Priority Gaps:**
1. Long-duration stability PSO (Framework 1)
2. Swing-up specific PSO (Framework 5)

**Low-Priority Gaps:**
1. MPC weight tuning (Framework 5 - different paradigm)
2. Adaptive/online PSO (Framework 6 - future research)

---

## Implementation Plan

### Phase 1: Documentation & Reference (Immediate - 3-5 hours)

**Goal:** Create reference structure without moving files

**Tasks:**
1. Create `.ai_workspace/pso/` root directory
2. Create 6 framework subdirectories
3. Generate README files for each framework
4. Create symlink structures (no file moves)
5. Document current state mapping

**Deliverables:**
- `.ai_workspace/pso/README.md` (master index)
- 6 framework READMEs
- Symlink structure
- Current state inventory

**Risk:** LOW (no file moves, reference only)

---

### Phase 2: Master Index & Cross-References (Short-term - 2-3 hours)

**Goal:** Create navigable index system

**Tasks:**
1. Generate cross-reference tables
2. Create framework mapping matrix
3. Document usage guidelines
4. Add quick-reference cheatsheets

**Deliverables:**
- `PSO_MASTER_INDEX.md`
- `FRAMEWORK_CROSSREF.md`
- `USAGE_GUIDE.md`
- Quick-reference cards

**Risk:** LOW (documentation only)

---

### Phase 3: Maturity-Based Config Organization (Medium-term - 5-8 hours)

**Goal:** Organize gains by deployment maturity

**Tasks:**
1. Create `config/gains/` directory structure
2. Classify all 23 gain files by TRL level
3. Move to production/validated/experimental/archived
4. Update config.yaml references
5. Document promotion criteria

**Deliverables:**
- `config/gains/production/` (Level 6 gains)
- `config/gains/validated/` (Level 4 gains)
- `config/gains/experimental/` (Level 2 gains)
- `config/gains/archived/` (Level 7 gains)
- Promotion workflow documentation

**Risk:** MEDIUM (file moves, config updates required)

---

### Phase 4: Automation & Tooling (Long-term - 5-7 hours)

**Goal:** Automated classification and navigation

**Tasks:**
1. Create file classification scripts
2. Build framework navigation CLI tool
3. Generate coverage dashboards
4. Implement automated cross-referencing

**Deliverables:**
- `classify_pso_files.py` (auto-categorization)
- `pso_navigator.py` (CLI tool)
- Coverage dashboard (HTML/Markdown)
- Automated README generation

**Risk:** LOW (tooling, no file moves)

---

### Phase 5: Publication Integration (Pre-submission - 2-3 hours)

**Goal:** Integrate frameworks into LT-7 paper

**Tasks:**
1. Map paper sections to frameworks
2. Generate framework-based figure organization
3. Create supplementary materials
4. Add framework references to paper

**Deliverables:**
- Paper section mapping
- Supplementary materials package
- Framework citations in paper
- Data availability statement

**Risk:** LOW (documentation additions)

---

## Directory Structure Proposal

### Proposed `.ai_workspace/pso/` Structure

```
.ai_workspace/pso/
├── README.md                          # Master index, navigation guide
├── PSO_MASTER_INDEX.md               # Complete file inventory
├── FRAMEWORK_CROSSREF.md             # Cross-reference matrix
├── USAGE_GUIDE.md                    # How to use each framework
│
├── by_purpose/                       # Framework 1
│   ├── README.md
│   ├── performance/                  # S1, S10
│   │   ├── README.md
│   │   ├── gains@ -> ../../experiments/.../
│   │   └── data@ -> ../../experiments/.../
│   ├── safety/                       # S9, S4
│   ├── robustness/                   # S2, S3, S7, S8
│   ├── efficiency/                   # S4, S6 (MISSING)
│   └── multi_objective/              # S4 (MISSING)
│
├── by_maturity/                      # Framework 2
│   ├── README.md
│   ├── level_1_theoretical/
│   ├── level_2_simulation/
│   ├── level_3_statistical/
│   ├── level_4_robustness/
│   ├── level_5_hardware/
│   ├── level_6_production/
│   └── level_7_archived/
│
├── by_task/                          # Framework 3
│   ├── README.md
│   ├── QW-3_visualization/
│   ├── MT-6_boundary_layer/
│   ├── MT-7_robustness/
│   ├── MT-8_disturbance/
│   ├── LT-6_uncertainty/
│   └── phase_based/
│
├── by_filetype/                      # Framework 4
│   ├── README.md
│   ├── config/                       # 3 files
│   ├── gains/                        # 23 files
│   ├── data/                         # 70 files
│   ├── reports/                      # 42 files
│   ├── visualizations/               # 16 files
│   ├── logs/                         # 6 files
│   └── source/                       # 3 files
│
├── by_controller/                    # Framework 5
│   ├── README.md
│   ├── classical/
│   │   ├── classical_smc/
│   │   └── sta_smc/
│   ├── adaptive/
│   │   ├── adaptive_smc/
│   │   ├── hybrid_adaptive_sta/
│   │   └── regional_hybrid_smc/     # NEW (Dec 31, 2025)
│   └── specialized/
│       ├── swing_up_smc/
│       └── mpc/
│
├── by_strategy/                      # Framework 6
│   ├── README.md
│   ├── single_objective/             # Standard PSO
│   ├── robust_multiscenario/         # MT-8 approach
│   ├── statistical_validation/       # MT-7 approach
│   ├── multi_objective/              # MISSING
│   └── adaptive_online/              # MISSING
│
├── tools/                            # Automation & navigation
│   ├── classify_pso_files.py
│   ├── pso_navigator.py
│   ├── generate_coverage_dashboard.py
│   └── validate_framework_links.py
│
└── reports/                          # Framework analysis
    ├── PSO_CATEGORIZATION_MASTER_PLAN.md (this file)
    ├── PSO_COMPREHENSIVE_STATUS_REPORT.md
    ├── FRAMEWORK_COVERAGE_ANALYSIS.md
    └── GAP_ANALYSIS_PRIORITIES.md
```

**Note:** Most directories contain symlinks (`@`) to actual files in `experiments/` to avoid duplication.

---

## Migration Strategy

### Option A: Symlink-Based (Recommended)

**Approach:** Create reference structure with symlinks, keep files in current locations

**Pros:**
- No file moves (zero risk)
- Multiple views of same data
- Easy to maintain
- Backward compatible

**Cons:**
- Symlinks on Windows (requires developer mode or admin)
- Slightly more complex navigation

**Implementation:**
```bash
# Example
cd .ai_workspace/pso/by_purpose/performance/gains/
ln -s ../../../../experiments/classical_smc/optimization/phases/phase53/optimized_gains_classical_smc_phase53.json classical_smc_phase53.json
```

---

### Option B: Copy-Based with Manifest

**Approach:** Copy files to framework directories, maintain manifest

**Pros:**
- No symlink issues
- Self-contained directories
- Easy backup/archiving

**Cons:**
- File duplication (~12 MB × 6 = 72 MB)
- Sync issues (must update multiple copies)
- Higher maintenance burden

**Implementation:**
```bash
# Not recommended
cp experiments/classical_smc/optimization/phases/phase53/*.json .ai_workspace/pso/by_purpose/performance/gains/
```

---

### Option C: Hybrid (Production Gains Only)

**Approach:** Move production gains to config/gains/, symlinks for everything else

**Pros:**
- Clear deployment status (production separate)
- Minimal duplication
- Easy to find production-ready gains

**Cons:**
- Breaks current paths (requires config.yaml updates)
- Migration effort required

**Recommended:** Phase 3 only (maturity-based config organization)

---

## Usage Guidelines

### For Researchers Writing Papers

**Use Framework 1 (Purpose) + Framework 2 (Maturity)**

Example workflow:
1. Navigate to `.ai_workspace/pso/by_purpose/robustness/`
2. Find MT-8 data (disturbance rejection)
3. Check maturity level: Level 4 (robustness-validated)
4. Cite in paper: "We applied robust PSO (MT-8, TRL 5) for disturbance rejection..."

**Quick Reference:**
- Performance optimization → by_purpose/performance/
- Safety optimization → by_purpose/safety/
- Robustness → by_purpose/robustness/

---

### For Developers Debugging

**Use Framework 3 (Task) + Framework 4 (Filetype)**

Example workflow:
1. Navigate to `.ai_workspace/pso/by_task/MT-8_disturbance/`
2. Check logs/ subdirectory for execution logs
3. Find data/ for CSV/JSON results
4. Read reports/ for analysis

**Quick Reference:**
- Logs → by_filetype/logs/ or by_task/<TASK>/logs/
- Gain files → by_filetype/gains/ or by_controller/<CTRL>/gains/
- Data → by_task/<TASK>/data/

---

### For Configuration Management

**Use Framework 2 (Maturity)**

Example workflow:
1. Navigate to `config/gains/production/`
2. Find MT-8 robust gains (Level 6 - production)
3. Copy to config.yaml controller_defaults
4. Validate with integration tests

**Quality Gates:**
- Experimental (Level 2) → Simulation validation required
- Validated (Level 4) → Statistical + robustness validation
- Production (Level 6) → Deployed, documented, version-controlled

**Promotion Criteria:**
- Level 2 → 3: Multi-seed validation (10+ seeds)
- Level 3 → 4: Robustness testing (disturbances + uncertainty)
- Level 4 → 5: HIL validation (hardware testing)
- Level 5 → 6: Production deployment + documentation

---

### For Algorithm Selection

**Use Framework 6 (Strategy)**

Example workflow:
1. Navigate to `.ai_workspace/pso/by_strategy/`
2. Compare single_objective vs robust_multiscenario
3. Check performance metrics
4. Select algorithm for new controller

**Quick Reference:**
- Standard PSO → by_strategy/single_objective/
- Robust PSO (MT-8) → by_strategy/robust_multiscenario/
- Multi-seed validation → by_strategy/statistical_validation/

---

## Maintenance Plan

### Weekly Tasks (5 minutes)

1. **Validate symlinks:**
   ```bash
   python .ai_workspace/pso/tools/validate_framework_links.py
   ```

2. **Check for new files:**
   ```bash
   python .ai_workspace/pso/tools/classify_pso_files.py --scan
   ```

3. **Update coverage dashboard:**
   ```bash
   python .ai_workspace/pso/tools/generate_coverage_dashboard.py
   ```

---

### Monthly Tasks (15 minutes)

1. **Review framework coverage:**
   - Check gap analysis
   - Update priorities
   - Document new scenarios

2. **Update cross-references:**
   - Regenerate PSO_MASTER_INDEX.md
   - Update FRAMEWORK_CROSSREF.md
   - Verify README accuracy

3. **Quality audit:**
   - Check for dead links
   - Verify file classifications
   - Update maturity levels

---

### Quarterly Tasks (30 minutes)

1. **Framework effectiveness review:**
   - Survey team for usability
   - Identify navigation pain points
   - Propose framework improvements

2. **Documentation refresh:**
   - Update usage examples
   - Add new use cases
   - Improve quick-reference guides

3. **Automation improvements:**
   - Enhance classification scripts
   - Add new navigation features
   - Optimize dashboard generation

---

### Annual Tasks (2-3 hours)

1. **Comprehensive audit:**
   - Full file inventory
   - Framework coverage analysis
   - Gap analysis update

2. **Strategic planning:**
   - Review missing optimizations
   - Prioritize new scenarios
   - Allocate research effort

3. **Archive old data:**
   - Identify superseded gains
   - Move to Level 7 (archived)
   - Update git history

---

## Success Metrics

### Quantitative Metrics

1. **Framework Coverage:**
   - Target: 80% of files classified in all 6 frameworks
   - Current: 78%
   - Measurement: Automated script

2. **Navigation Efficiency:**
   - Target: <2 minutes to find any PSO artifact
   - Current: ~5 minutes (unstructured)
   - Measurement: User surveys

3. **Documentation Completeness:**
   - Target: 100% of frameworks have READMEs
   - Current: 0% (frameworks not yet created)
   - Measurement: File count

4. **Automation Level:**
   - Target: 90% of framework updates automated
   - Current: 0%
   - Measurement: Manual effort tracking

---

### Qualitative Metrics

1. **User Satisfaction:**
   - Target: 4/5 average rating
   - Measurement: Monthly surveys

2. **Framework Utility:**
   - Target: All 6 frameworks used monthly
   - Measurement: Access logs, user feedback

3. **Onboarding Time:**
   - Target: New researchers find data in <10 minutes
   - Measurement: Onboarding sessions

---

## Risk Assessment

### Implementation Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Symlink issues on Windows** | MEDIUM | MEDIUM | Use Option B (copy) or enable developer mode |
| **Broken links after file moves** | LOW | HIGH | Use symlinks initially (Option A), validate frequently |
| **User confusion (6 frameworks)** | MEDIUM | MEDIUM | Clear usage guide, training sessions |
| **Maintenance burden** | LOW | MEDIUM | Automation scripts, quarterly reviews |
| **Duplication errors** | LOW | MEDIUM | Manifest tracking, validation scripts |

---

### Deployment Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Config.yaml breakage** | LOW | HIGH | Test in dev environment, version control |
| **Experiment path changes** | LOW | HIGH | Phase 3 only (gains), keep experiments/ intact |
| **LT-7 paper reference breaks** | LOW | CRITICAL | Preserve experiments/figures/ paths (do not move) |
| **Git history loss** | VERY LOW | CRITICAL | Use git mv, test before commit |

---

## Implementation Roadmap

### Timeline

```
Phase 1: Documentation (Immediate)
└─ Week 1: 3-5 hours
   ├─ Day 1: Create directory structure (1 hr)
   ├─ Day 2: Write README files (2 hrs)
   └─ Day 3: Generate symlinks (1-2 hrs)

Phase 2: Master Index (Short-term)
└─ Week 2: 2-3 hours
   ├─ Day 4: Cross-reference tables (1 hr)
   ├─ Day 5: Usage guidelines (1 hr)
   └─ Day 6: Quick-reference cards (0.5 hr)

Phase 3: Maturity Config (Medium-term)
└─ Week 3-4: 5-8 hours
   ├─ Week 3: Create config/gains/ structure (2 hrs)
   ├─ Week 3: Classify and move gains (2 hrs)
   ├─ Week 4: Update config.yaml (1 hr)
   ├─ Week 4: Test integration (1-2 hrs)
   └─ Week 4: Document promotion workflow (1 hr)

Phase 4: Automation (Long-term)
└─ Week 5-6: 5-7 hours
   ├─ Week 5: Classification scripts (2 hrs)
   ├─ Week 5: Navigation CLI (2 hrs)
   ├─ Week 6: Coverage dashboard (1-2 hrs)
   └─ Week 6: Automated README generation (1 hr)

Phase 5: Publication (Pre-submission)
└─ Week 7: 2-3 hours
   ├─ Map paper sections (1 hr)
   ├─ Generate supplementary materials (1 hr)
   └─ Add framework citations (0.5 hr)

Total Effort: 17-26 hours over 7 weeks
```

---

### Dependencies

**Phase 1 → Phase 2:** Must complete directory structure before indexing
**Phase 2 → Phase 3:** Need cross-references before maturity organization
**Phase 3 → Phase 4:** Maturity structure informs automation requirements
**Phase 4 → Phase 5:** Automation tools aid publication integration

**Critical Path:** Phase 1 → Phase 2 → Phase 5 (minimal viable documentation)

---

### Milestones

| Milestone | Completion Criteria | Target Date |
|-----------|---------------------|-------------|
| **M1: Framework Reference Created** | 6 framework directories with READMEs | Week 1 |
| **M2: Master Index Published** | Complete file inventory + cross-refs | Week 2 |
| **M3: Maturity Config Operational** | config/gains/ structure + promotion workflow | Week 4 |
| **M4: Automation Deployed** | Classification + navigation tools working | Week 6 |
| **M5: Publication-Ready** | LT-7 paper integrated with frameworks | Week 7 |

---

## Approval & Sign-off

### Stakeholders

- **Primary Owner:** Research lead (PSO optimization strategy)
- **Technical Owner:** Software architect (directory structure, automation)
- **Users:** Researchers, developers, documentation writers

### Approval Process

1. **Review:** Stakeholder review of this plan (1 week)
2. **Pilot:** Implement Phase 1 in dev branch (1 week)
3. **Feedback:** Collect user feedback on pilot (3 days)
4. **Revise:** Update plan based on feedback (2 days)
5. **Approve:** Final sign-off by research lead
6. **Deploy:** Merge to main, implement remaining phases

### Rollback Plan

If frameworks prove too complex or confusing:
1. **Preserve:** Keep experiments/ structure intact (already good)
2. **Archive:** Move `.ai_workspace/pso/` to `.ai_workspace/archive/`
3. **Document:** Lessons learned for future attempts
4. **Communicate:** Inform team of rollback

---

## Appendix A: Quick Start Guide

### 30-Second Quick Start

```bash
# Navigate to PSO workspace
cd D:\Projects\main\.ai_workspace\pso

# View master index
cat README.md

# Find performance optimization data
cd by_purpose/performance/
ls -lah

# Find MT-8 task data
cd ../by_task/MT-8_disturbance/
ls -lah

# Check production gains
cd ../../by_maturity/level_6_production/
ls -lah
```

---

### Common Use Cases

**"I need MT-8 disturbance rejection data"**
```bash
cd .ai_workspace/pso/by_task/MT-8_disturbance/data/
# Or
cd .ai_workspace/pso/by_purpose/robustness/MT-8/
```

**"I want production-ready gains for Hybrid controller"**
```bash
cd .ai_workspace/pso/by_maturity/level_6_production/hybrid_adaptive_sta/
# Or
cd .ai_workspace/pso/by_controller/adaptive/hybrid_adaptive_sta/production/
```

**"I need to validate statistical significance (MT-7)"**
```bash
cd .ai_workspace/pso/by_task/MT-7_robustness/reports/
cat MT7_COMPLETE_REPORT.md
```

**"I want to compare PSO algorithms"**
```bash
cd .ai_workspace/pso/by_strategy/
cat README.md  # Algorithm comparison table
```

---

## Appendix B: File Naming Conventions

### Gain Files
**Format:** `<controller>_<variant>_<phase/task>.json`

**Examples:**
- `classical_smc_phase53.json` (Phase 53 gains)
- `sta_smc_mt8_robust.json` (MT-8 robust gains)
- `hybrid_adaptive_sta_production.json` (Production gains)

### Data Files
**Format:** `<TASK>_<metric>_<variant>.csv|json|npz`

**Examples:**
- `MT7_seed_42_results.csv` (MT-7 seed 42 results)
- `MT8_disturbance_rejection.json` (MT-8 disturbance data)
- `MT6_adaptive_timeseries.npz` (MT-6 time-series)

### Report Files
**Format:** `<TASK>_<TYPE>_REPORT.md`

**Examples:**
- `MT6_COMPLETE_REPORT.md` (Task completion)
- `MT7_STATISTICAL_ANALYSIS.md` (Analysis report)
- `MT8_HIL_VALIDATION_SUMMARY.md` (Validation summary)

---

## Appendix C: Framework Selection Decision Tree

```
START: I need PSO data...

┌─ What is your goal?
│
├─[1] Find data for research paper?
│   └─> Use Framework 1 (Purpose) + Framework 2 (Maturity)
│       Example: "by_purpose/robustness/" + check TRL level
│
├─[2] Debug PSO execution issue?
│   └─> Use Framework 3 (Task) + Framework 4 (Filetype)
│       Example: "by_task/MT-8/" + "by_filetype/logs/"
│
├─[3] Select gains for deployment?
│   └─> Use Framework 2 (Maturity)
│       Example: "by_maturity/level_6_production/"
│
├─[4] Compare controllers?
│   └─> Use Framework 5 (Controller)
│       Example: "by_controller/classical/" vs "by_controller/adaptive/"
│
├─[5] Compare PSO algorithms?
│   └─> Use Framework 6 (Strategy)
│       Example: "by_strategy/single_objective/" vs "by_strategy/robust_multiscenario/"
│
└─[6] Browse all PSO work?
    └─> Use PSO_MASTER_INDEX.md
        Example: "PSO_MASTER_INDEX.md" → complete inventory
```

---

## Appendix D: Validation Checklist

### Phase 1 Validation
- [ ] `.ai_workspace/pso/` directory created
- [ ] 6 framework subdirectories exist
- [ ] Each framework has README.md
- [ ] Symlinks work on target platform
- [ ] No broken links detected

### Phase 2 Validation
- [ ] PSO_MASTER_INDEX.md complete
- [ ] FRAMEWORK_CROSSREF.md accurate
- [ ] USAGE_GUIDE.md clear and helpful
- [ ] Quick-reference cards created
- [ ] User feedback positive (4/5 average)

### Phase 3 Validation
- [ ] config/gains/ structure created
- [ ] All 23 gain files classified by TRL
- [ ] config.yaml updated successfully
- [ ] Integration tests passing (100%)
- [ ] Promotion workflow documented

### Phase 4 Validation
- [ ] classify_pso_files.py working
- [ ] pso_navigator.py working
- [ ] Coverage dashboard generated
- [ ] Automated README generation working
- [ ] Weekly maintenance automated

### Phase 5 Validation
- [ ] LT-7 paper sections mapped
- [ ] Supplementary materials complete
- [ ] Framework citations added
- [ ] Data availability statement complete
- [ ] Reviewer guidelines updated

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-30 | Research Team | Initial master plan |
| - | - | - | - |

---

**END OF MASTER PLAN**

Total Pages: 38
Total Sections: 15
Appendices: 4
Estimated Reading Time: 25 minutes
