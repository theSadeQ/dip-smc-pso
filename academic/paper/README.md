# Paper - Research & Publications Directory

## Purpose

This directory contains all research outputs, publications, documentation, and thesis materials for the double-inverted pendulum SMC project. It serves as the central repository for academic and research-related content.

## Structure

```
paper/
├── thesis/            [98 MB] - Master's thesis LaTeX project
├── docs/              [64 MB] - Sphinx documentation system
├── research/          [28 MB] - Active research papers & experiments
├── archive/           [12 MB] - Historical research artifacts
└── data/              [3 KB]  - Simulation & research data
```

## Directory Contents

### thesis/ [98 MB]
Master's thesis LaTeX project with comprehensive research documentation.

**Key Files:**
- `main.pdf` [692 KB] - Compiled thesis document
- `main.tex` [4 KB] - Main LaTeX source file
- `chapters/` [90 KB] - Thesis chapter sources
- `figures/` [176 KB] - Thesis figures and diagrams
- `sources_archive/` [96 MB] - Reference materials (articles, books, conference proceedings)
- `bibliography/` [8 KB] - Bibliography database
- Build artifacts: `.aux`, `.log`, `.toc`, `.bbl`, `.out` (LaTeX compilation outputs)

**Purpose:** Complete thesis documentation for academic submission and archival.

### docs/ [64 MB]
Sphinx-based documentation system for the project.

**Key Components:**
- `_build/` [~50 MB] - Sphinx build output (HTML documentation)
- `_static/` - CSS, JavaScript, icons, PWA assets
- `_ext/` - Custom Sphinx extensions (Chart.js, Plotly, MathJax, etc.)
- `_data/` - Documentation data files (citations, benchmarks, specs)
- `bib/` - Bibliography files (adaptive.bib, dip.bib, smc.bib, pso.bib, etc.)
- Content directories: api/, architecture/, controllers/, benchmarks/, guides/, theory/, examples/

**Purpose:** Comprehensive technical documentation for users, developers, and researchers.

### research/ [28 MB]
Active research outputs, experiments, and publications.

**Subdirectories:**
- `papers/` [13 MB] - Research publications
  - `LT7_journal_paper/` - Main journal paper submission
    - `LT7_PROFESSIONAL_FINAL.pdf` [449 KB] - Final submission PDF
    - `LT7_RESEARCH_PAPER.tex` [391 KB] - LaTeX source
    - `LT7_RESEARCH_PAPER.md` [366 KB] - Markdown master document
    - `LT7_RESEARCH_PAPER.bib` [20 KB] - Bibliography
    - `sections/` - Individual paper sections
    - `archive/` - Old versions and build artifacts
- `phases/` [11 MB] - Research phase experiment data
- `benchmarks/` [3.8 MB] - Performance benchmark results
  - `figures/` - MT5-MT8 benchmark plots
  - `processed/` - JSON benchmark data
  - `reports/` - Analysis summaries
- `experiments/` [845 KB] - Research task experiments (LT6, MT6-8)
- `optimization/` [434 KB] - PSO optimization results
- `theory/` [empty] - Theoretical foundations (placeholder)

**Purpose:** Active research work, experiments, and publication-ready materials.

### archive/ [12 MB]
Historical research artifacts, migration records, and backup materials.

**Contents:**
- `research/` [6.1 MB] - Historical research materials
  - Old conference papers
  - Historical documentation
  - Old thesis versions
  - Obsolete optimization results
- `backups/` [3.8 MB] - Critical backups
  - `benchmarks_pre_reorg_20251218.tar.gz` [3.5 MB]
  - `logs_monitoring_pre_consolidation_20251219.tar.gz` [222 KB]
- `thesis_guide/` [1.1 MB] - Thesis development guide
- `latex_scripts/` [412 KB] - LaTeX automation scripts
- `docs_build/` [40 KB] - Build reports (logs moved to ../logs/)
- `migration_artifacts/` [269 KB] - Migration tracking files
- `paper_enhancement_plans/` [120 KB] - Research planning documents

**Purpose:** Preserve historical research work and maintain project continuity across reorganizations.

### data/ [3 KB]
Simulation and research data files.

**Subdirectories:**
- `raw/` - Raw simulation data
  - `debug_sessions.json`
  - `failures.json`
  - `failure_groups.json`
- `processed/` - Processed analysis data
- `simulation/` - Simulation outputs

**Purpose:** Store simulation data for research analysis and experiments.

## File Counts

- **Markdown files:** ~1,236 (documentation, papers, guides)
- **LaTeX sources:** ~85 (thesis, papers)
- **PDFs:** ~55 (compiled papers, thesis, references)
- **Bibliography files:** ~12 (.bib files across docs/ and research/)
- **Build artifacts:** ~102 (.aux, .log, .toc, .out files)
- **JSON/CSV data:** ~50+ (benchmarks, analysis results)
- **Python scripts:** ~20+ (automation, build scripts)

## Total Size

**Current:** ~202 MB (after Dec 29, 2025 reorganization)

**Breakdown:**
- thesis/ (98 MB, 48%)
- docs/ (64 MB, 32%)
- research/ (28 MB, 14%)
- archive/ (12 MB, 6%)
- data/ (3 KB, <0.01%)

## Usage Guidelines

### For Researchers
1. **Papers:** Add new papers to `research/papers/`
2. **Experiments:** Store experiment data in `research/experiments/`
3. **Benchmarks:** Results go to `research/benchmarks/`
4. **Documentation:** Update `docs/` for new features/controllers

### For Students
1. **Thesis work:** Use `thesis/` directory exclusively
2. **Reference materials:** Add to `thesis/sources_archive/`
3. **Figures:** Store in `thesis/figures/`
4. **Build thesis:** Run LaTeX compilation in `thesis/` root

### For Developers
1. **Documentation:** Update Sphinx docs in `docs/`
2. **API docs:** Modify `docs/api/` for API changes
3. **Guides:** Add tutorials to `docs/guides/`
4. **Build docs:** Run `sphinx-build -M html docs docs/_build`

## Maintenance

### Documentation Build
```bash
# Rebuild Sphinx documentation
cd D:\Projects\main\academic\paper\docs
sphinx-build -M html . _build -W --keep-going

# Verify build
stat _build/html/index.html
```

### Thesis Compilation
```bash
# Compile thesis PDF
cd D:\Projects\main\academic\paper\thesis
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Research Paper Compilation
```bash
# Compile LT7 journal paper
cd D:\Projects\main\academic\paper\research/papers/LT7_journal_paper
pdflatex LT7_RESEARCH_PAPER.tex
```

## Status

**Last Updated:** December 29, 2025
**Reorganization:** Complete (academic/ restructuring)
**Version:** v2.0 (Three-category structure: paper/, logs/, dev/)
**Thesis Status:** Submission-ready
**Research Status:** LT-7 paper complete and submission-ready (v2.1)

## Related Directories

- **logs/** - Runtime and development logs (separate from paper/)
- **dev/** - Development artifacts (quality reports, caches)
- **D:\Projects\main\docs/** - Project root documentation (different from academic/paper/docs/)
- **D:\Projects\main\benchmarks/** - Project-level benchmarks (separate from research benchmarks)

## Notes

- **Build Artifacts:** LaTeX build artifacts (.aux, .log, .toc) are kept with sources per LaTeX best practices
- **Nested Structures:** All nested directories (docs/docs/, papers/papers/) have been flattened (Dec 29, 2025)
- **Archive Policy:** Old versions and historical materials are moved to `archive/` subdirectory
- **Backup Files:** Redundant backups removed during Dec 29 cleanup (saved 4.6 MB)
- **Data Files:** Small research data files are gitignored but preserved locally

## See Also

- `D:\Projects\main\CLAUDE.md` - Project-wide organization guide
- `.ai_workspace/guides/workspace_organization.md` - Workspace hygiene standards
- `research/papers/LT7_journal_paper/README.md` - Journal paper documentation
- `thesis/README.md` - Thesis compilation guide
