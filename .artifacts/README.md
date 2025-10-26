# Research Artifacts Directory

**Last Updated**: 2025-10-26
**Total Size**: ~10 MB
**Status**: Organized and cleaned

---

## Active Work

### LT7_research_paper/ - M.Sc. Thesis & Conference Paper

**Status**: 5/9 thesis chapters complete (56% progress)

**Completed**:
- ✅ Chapter 1: Introduction (12 pages, 5,500 words)
- ✅ Chapter 2: Literature Review (18 pages, 5,350 words, 4 comparison tables)
- ✅ Chapter 3: System Modeling (10 pages, 3,500 words, complete Lagrangian derivation)
- ✅ Chapter 4: Controller Design (8 pages, adaptive SMC + Lyapunov stability)
- ✅ Chapter 5: PSO Optimization (10 pages, 3,500 words, 10-run statistical validation)

**Pending**:
- ⏸️ Chapter 6: Experimental Setup (planned, ultra-detailed plan available in archive)
- ⏸️ Chapter 7: Results Analysis
- ⏸️ Chapter 8: Discussion
- ⏸️ Chapter 9: Conclusions & Future Work

**Directory Structure**:
```
LT7_research_paper/
├── thesis/                         # M.Sc. thesis LaTeX files
│   ├── chapters/                   # Chapter .tex files (00-05 complete)
│   ├── SESSION{1-5}_COMPLETION_SUMMARY.md
│   └── THESIS_README_AND_ROADMAP.md  ← Main navigation file
│
├── manuscript/                     # IEEE conference paper (6 pages)
│   └── main.tex                    # LaTeX source (950 lines, complete)
│
├── figures/                        # Publication-quality figures
│   ├── fig2_adaptive_boundary.pdf  # Adaptive boundary layer concept
│   ├── fig3_baseline_radar.pdf     # Controller comparison radar
│   ├── fig4_pso_convergence.pdf    # PSO convergence curves
│   ├── fig5_chattering_boxplot.pdf # Chattering reduction results
│   ├── fig6_robustness_degradation.pdf  # MT-7 robustness analysis
│   └── fig7_disturbance_rejection.pdf   # MT-8 disturbance results
│
├── data_extraction/                # Python scripts for figure/table generation
│   ├── generate_figure*.py
│   └── generate_table*.py
│
├── experiments/                    # PSO experimental data (10 runs)
│   ├── results/
│   │   ├── results_seed{42,123,...,2526}.json  (10 PSO runs)
│   │   ├── grid_search.log
│   │   └── random_search.log
│   ├── run_pso_batch.bat           # Batch experiment launcher
│   └── README.md                   # Experiment documentation
│
├── data_inventory.md               # Dataset catalog (MT-5, MT-6, MT-7, MT-8)
├── key_results_summary.md          # Quick reference for key findings
├── FIRST_DRAFT_COMPLETE.md         # Milestone marker
└── LATEX_CONVERSION_COMPLETE.md    # Milestone marker
```

**Key Files**:
- **Thesis navigation**: `LT7_research_paper/thesis/THESIS_README_AND_ROADMAP.md`
- **Conference paper**: `LT7_research_paper/manuscript/main.tex`
- **Experimental data**: `LT7_research_paper/experiments/results/*.json`

---

## Archive

### archive/planning/ - Ultra-Detailed Planning Documents

**Purpose**: Historical planning documents for complex chapters (Ch5, Ch6)

**Contents**:
- `chapter5_ultradetailed_plan.md` (15,000 words, PSO chapter blueprint)
- `chapter6_ultradetailed_plan.md` (13,000 words, experimental setup blueprint)
- `control_systems_theory_skill_plan.md` (skill development roadmap)

**Note**: These are reference documents. Actual chapter work is in `LT7_research_paper/thesis/chapters/`.

### archive/audits/ - Historical Audit Reports

**Purpose**: One-time code quality and security audits

**Contents**:
- `docs_audit/` (4 documentation audit reports)
- `security_audit_report_2025-10-19.md` (security scan results)
- `advanced_threat_scan_2025-10-19.md` (advanced security analysis)

**Note**: Audits were performed in October 2025. Archived for historical reference.

---

## Quick Navigation

**Working on thesis?** → See `LT7_research_paper/thesis/THESIS_README_AND_ROADMAP.md`
**Need experimental data?** → See `LT7_research_paper/experiments/results/`
**Looking for figures?** → See `LT7_research_paper/figures/`
**Checking planning docs?** → See `archive/planning/`

---

## Maintenance Notes

**Cleanup performed**: 2025-10-26
- Archived 3 planning documents (2.3 MB)
- Deleted 8 legacy LT-4 checkpoint files (0.5 MB)
- Archived 6 audit reports (0.8 MB)
- Cleaned Python bytecode (__pycache__ directories)

**Next cleanup**: When thesis Ch6-9 are complete, archive session completion summaries

---

**Total files**: ~50-55 active files
**Total directories**: 8 active + 2 archive
**Organization**: Clean separation between active work and historical artifacts
