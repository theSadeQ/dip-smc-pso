# LT7 Research Paper - M.Sc. Thesis & Conference Paper

**Project**: PSO-Optimized Adaptive Boundary Layer Sliding Mode Control for Double Inverted Pendulum
**Status**: Thesis 5/9 chapters complete (56%) | Conference paper complete
**Last Updated**: 2025-10-26

---

## Quick Navigation

**Working on thesis?** → `thesis/THESIS_README_AND_ROADMAP.md`
**Need conference paper?** → `conference_paper/main.tex`
**Final deliverables?** → `deliverables/`
**Experimental data?** → `experiments/results/`
**Defense presentation?** → `defense/`

---

## Directory Structure

### Active Work

```
├── thesis/                      # M.Sc. Thesis (90 pages target)
│   ├── chapters/                # LaTeX chapters (Ch1-5 complete ✅)
│   ├── SESSION*_SUMMARY.md      # Session completion reports
│   └── THESIS_README_AND_ROADMAP.md  ← Main thesis navigation
│
├── conference_paper/            # IEEE Conference Paper (6 pages)
│   ├── main.tex                 # LaTeX source (950 lines, complete)
│   └── (Markdown drafts archived - see archive/)
│
├── defense/                     # Defense Presentation Materials
│   ├── defense_presentation.tex # Beamer slides
│   ├── defense_speaker_notes.md # Speaker notes
│   └── README.md
│
├── figures/                     # Publication-Quality Figures
│   ├── fig2_adaptive_boundary.pdf/png
│   ├── fig3_baseline_radar.pdf/png
│   ├── fig4_pso_convergence.pdf/png
│   ├── fig5_chattering_boxplot.pdf/png
│   ├── fig6_robustness_degradation.pdf/png
│   ├── fig7_disturbance_rejection.pdf/png
│   └── figure_vi1_*.pdf/png     # Chapter 6 figures
│
├── tables/                      # Generated Tables
│   ├── *.tex                    # LaTeX table files
│   └── *.md                     # Markdown source tables
│
├── data_extraction/             # Python Scripts for Figures/Tables
│   ├── generate_figure*.py     # Figure generation scripts
│   └── generate_table*.py      # Table generation scripts
│
├── experiments/                 # PSO Experimental Results
│   ├── results/
│   │   ├── results_seed{42,123,...,2526}.json  # 10 PSO runs
│   │   ├── grid_search.log
│   │   └── random_search.log
│   ├── run_pso_batch.bat        # Batch experiment launcher
│   └── README.md
│
└── reports/                     # Statistical Analysis Reports
    ├── B1_normality_validation_report.md
    ├── B2_bootstrap_convergence_report.md
    └── B3_sensitivity_analysis_report.md
```

### Deliverables

```
deliverables/
├── conference_paper.pdf         # Final 6-page IEEE paper (353 KB)
├── conference_overleaf.zip      # Overleaf upload package (1.1 MB)
├── defense_materials.tar.gz     # Defense presentation package (356 KB)
└── defense_overleaf.zip         # Defense Overleaf package (14 KB)
```

### Archive

```
archive/
├── completion_summaries/        # Historical completion reports (17 files)
│   ├── CHAPTER6_IMPLEMENTATION_COMPLETE.md
│   ├── CHAPTER7_*.md            # 7 validation/integration reports
│   ├── PHASE2_*.md              # 4 Phase 2 summaries
│   ├── PHASE3_*.md              # 4 Phase 3 summaries
│   ├── SESSION_2025-10-20*.md   # 2 session summaries
│   ├── POLISHING_PHASE_COMPLETION_SUMMARY.md
│   ├── FIRST_DRAFT_COMPLETE.md
│   └── LATEX_CONVERSION_COMPLETE.md
│
├── manuscript_drafts/           # Markdown section drafts (9 files)
│   └── section_*.md             # Pre-LaTeX conversion drafts
│
├── duplicate_defense/           # Duplicate defense materials
│   └── defense_overleaf/
│
└── guides/                      # One-time setup guides
    ├── OVERLEAF_SETUP_GUIDE.md
    └── OVERLEAF_UPLOAD_GUIDE.md
```

---

## Key Files (Root Level)

- **data_inventory.md** - Dataset catalog (MT-5, MT-6, MT-7, MT-8 experiments)
- **key_results_summary.md** - Quick reference for research findings
- **references.bib** - Bibliography (50+ references)

---

## Thesis Status (5/9 Chapters Complete)

**Completed** (48 pages, ~18,000 words):
- ✅ Ch1: Introduction (12 pages, 5,500 words)
- ✅ Ch2: Literature Review (18 pages, 5,350 words, 4 comparison tables)
- ✅ Ch3: System Modeling (10 pages, complete Lagrangian derivation)
- ✅ Ch4: Controller Design (8 pages, adaptive SMC + Lyapunov proofs)
- ✅ Ch5: PSO Optimization (10 pages, 10-run statistical validation)

**Pending** (42 pages, ~10-12 hours):
- ⏸️ Ch6: Experimental Setup (8 pages, 1-2 hours)
- ⏸️ Ch7: Results Analysis (10 pages, 2-3 hours)
- ⏸️ Ch8: Discussion (8 pages, 2-3 hours)
- ⏸️ Ch9: Conclusions (6 pages, 1-2 hours)

**Optional**:
- ⏸️ Appendices (10 pages, 4-6 hours)
- ⏸️ Persian translation (8-10 hours if required)

**Time to Completion**: 3-4 weeks (English thesis)

---

## Conference Paper Status

**Status**: ✅ **COMPLETE** (LaTeX conversion done)

**Current**: 950-line LaTeX manuscript (main.tex) with 9 sections, 25+ equations
**Target**: 6 pages (currently ~8-10 pages, needs condensing)

**Next Steps**:
1. Compile to PDF (1 hour)
2. Condense to 6 pages (4-5 hours)
3. Create Figure 1 DIP schematic (1 hour)
4. Final proofreading (1 hour)

**Total Effort Remaining**: 6-8 hours

---

## Key Research Results

**Primary Finding**: 66.5% chattering reduction (p < 0.001, Cohen's d = 5.29)

**Datasets**:
- **MT-5**: Baseline controller comparison (400 runs)
- **MT-6**: Adaptive boundary layer validation (200 runs)
- **MT-7**: Robustness analysis (500 attempts, 9.8% success)
- **MT-8**: Disturbance rejection (12 runs, 0% convergence)

**Experimental Data**: `experiments/results/` (10 PSO runs with statistical validation)

---

## Organization Principles

**Active vs. Archive**:
- **Active directories**: Current work (thesis, conference paper, defense, figures, experiments)
- **Archive**: Historical artifacts (completion summaries, draft manuscripts, duplicate files)
- **Deliverables**: Final outputs (PDFs, ZIP packages for Overleaf)

**File Naming**:
- Thesis chapters: `chapters/0N_chapter_name.tex`
- Figures: `fig{N}_{description}.pdf/png`
- Tables: `table_{N}_{description}.tex/md`
- Session summaries: `SESSIONN_COMPLETION_SUMMARY.md`

**No Root Clutter**:
- Root contains only 4 files: README.md + 3 reference docs
- All completion summaries archived
- All deliverables in `deliverables/`

---

## Cleanup History

**Last Cleanup**: 2025-10-26

**Actions**:
- Created `deliverables/` directory (4 files moved)
- Created `archive/` with 4 subdirectories
- Archived 17 completion summaries
- Archived 9 Markdown manuscript drafts
- Deleted `overleaf_upload/` (redundant with conference_paper/)
- Deleted 5 obsolete planning/validation docs
- Renamed `manuscript/` → `conference_paper/` for clarity

**Result**: Root reduced from 33 → 4 files

---

## Maintenance Notes

**When to Archive**:
- Session summaries: After thesis chapter completion
- Completion reports: When milestone reached (e.g., FIRST_DRAFT_COMPLETE.md)
- One-time guides: After setup complete (e.g., OVERLEAF_SETUP_GUIDE.md)

**What NOT to Archive**:
- Active thesis chapters (keep in `thesis/chapters/`)
- Current experimental data (keep in `experiments/results/`)
- Bibliography (keep `references.bib` in root)
- Key reference docs (keep `data_inventory.md`, `key_results_summary.md`)

---

**For detailed thesis roadmap, see**: `thesis/THESIS_README_AND_ROADMAP.md`
**For experiment documentation, see**: `experiments/README.md`
**For defense materials, see**: `defense/README.md`
