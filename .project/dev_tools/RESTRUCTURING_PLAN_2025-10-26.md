# PROJECT RESTRUCTURING PLAN - October 26, 2025
## Comprehensive Production-Ready Directory Reorganization

**Status**: IN PROGRESS
**Started**: 2025-10-26 08:00 UTC
**Git Checkpoint**: `f2c3742d` (can rollback with `git reset --hard f2c3742d`)
**Tar Backup**: `../main_backup_YYYYMMDD_HHMMSS.tar.gz` (in parent directory)

---

## PROGRESS TRACKER

### ✅ COMPLETED PHASES

#### Phase 0: Safety Backups ✅
- Created git commit `f2c3742d`
- Started tar.gz backup (background process)
- **Rollback command**: `git reset --hard f2c3742d`

#### Phase 1: Emergency Cleanup ✅
**Deleted**:
- `D:Projectsmain.artifacts/` (corrupted Windows path)
- `.artifactsLT7_research_paperdata_extractiongenerate_figure4_pso_convergence.py` (corrupted filename)
- `.coverage` (stale test artifact)
- `.regression_baselines.json` (outdated)
- ANSI escape code directories (failed script remnants)
- `nul` file (Windows device name conflict)

**Result**: Root items reduced from 56 → ~52

#### Phase 2: Consolidate Configs ✅
**Moved to `.project/`**:
- `.claude/` → `.project/claude/`
- `.config/` → `.project/config/`
- `.dev_tools/` → `.project/dev_tools/`
- `.mcp_servers/` → `.project/mcp_servers/`
- `.archive/` → `.project/archive_temp/` (will merge later)

**Deleted**:
- `.deployment/` (old, inactive)
- `.orchestration/` (old, inactive)

**Result**: Hidden directories reduced from 17 → 11

---

### 🚧 IN PROGRESS

#### Phase 3: Cleanup Massive Archives
**Discovery**:
- `.ai/archive/phase3_validation/`: **848MB** (CULPRIT!)
- `.ai/archive/build_artifacts/`: 23MB
- `.ai/archive/testing/`: 3.2MB
- `.ai/archive/dev_tools_backup/`: 3.6MB
- `.ai/archive/planning/`: 661KB
- `docs/_build/`: **946MB** (generated Sphinx HTML - should be in .gitignore)

**Total bloat**: 1.8GB

**Current Action**: Investigating what can be safely deleted

---

### ⏸️ PENDING PHASES

#### Phase 4: Fix Artifacts Duplication
**Problem**: Both `artifacts/` and `.artifacts/` exist
**Solution**:
- Move `artifacts/production_readiness.db` → `.artifacts/testing/`
- Move `artifacts/testing/` → `.artifacts/testing/`
- Delete `artifacts/` directory
- **Single source**: `.artifacts/` only

#### Phase 5: Fix Benchmarks Duplication
**Problem**: Both `benchmarks/` (7.6MB code) and `.benchmarks/` (28KB cache)
**Solution**:
- Keep `benchmarks/` as visible directory (code + results)
- Move `.benchmarks/` → `.cache/benchmarks/` (pytest cache)

#### Phase 6: Move Misplaced Root Files
**Files to move**:
- `optimize_adaptive_boundary.py` → `.artifacts/scripts/optimize_adaptive_boundary_TIMESTAMP.py`
- `out.png` → `.artifacts/temp/out.png`
- `LT7_conference_overleaf.pdf` → `.artifacts/LT7_research_paper/deliverables/`
- `report.log` → `logs/` or delete if stale
- `temp_patch.txt` → delete if obsolete

#### Phase 7: Consolidate Runtime Caches
**Create `.cache/` for ephemeral artifacts**:
- `.pytest_cache/` → `.cache/pytest/`
- `.hypothesis/` → `.cache/hypothesis/`
- `.htmlcov/` → `.cache/htmlcov/`
- `.benchmarks/` → `.cache/benchmarks/`
- `__pycache__/` → `.cache/pycache/` (or symlink)

#### Phase 8: Update .gitignore
**Add patterns**:
```
.project/archive/
.cache/
docs/_build/
*.tar.gz
```

**Remove old patterns** (now in .project/):
```
.claude/
.config/
.dev_tools/
```

#### Phase 9: Update CLAUDE.md Section 14
**Update workspace organization rules**:
- Document `.project/` consolidation
- Update health check commands
- Add `.cache/` documentation
- Update directory rules

#### Phase 10: Verification
**Tests**:
- `ls | wc -l` → expect ≤15
- `find . -maxdepth 1 -type d -name ".*" | wc -l` → expect ~5
- `python -m pytest tests/ --collect-only` → verify imports work
- `streamlit run streamlit_app.py` → verify UI works
- `python simulate.py --print-config` → verify scripts work

---

## TARGET STRUCTURE

```
main/
├── [ROOT FILES - 7]
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── CLAUDE.md
│   ├── config.yaml
│   ├── requirements.txt
│   ├── simulate.py
│   └── streamlit_app.py
│
├── [ESSENTIAL DOTFILES - 5]
│   ├── .git/
│   ├── .github/
│   ├── .gitignore
│   ├── .vscode/
│   └── .env (if exists)
│
├── [CORE DIRS - 8 visible]
│   ├── src/
│   ├── tests/
│   ├── docs/
│   ├── scripts/
│   ├── notebooks/
│   ├── data/
│   ├── benchmarks/
│   └── optimization_results/
│
└── [CONSOLIDATED - 3 hidden]
    ├── .project/
    │   ├── ai/ (from .ai/)
    │   ├── claude/
    │   ├── dev_tools/
    │   ├── config/
    │   ├── mcp_servers/
    │   └── archive/
    │
    ├── .artifacts/ (runtime outputs)
    │
    └── .cache/ (ephemeral caches)
```

---

## SUCCESS METRICS

| Metric | Before | Current | Target |
|--------|--------|---------|--------|
| Root visible items | 56 | ~52 | ≤15 |
| Hidden directories | 17 | 11 | ~5 |
| `.ai/` size | 884MB | 884MB | <100MB |
| `docs/_build/` | 946MB | 946MB | 0 (gitignored) |
| Total bloat | ~2GB | ~1.8GB | <200MB |

---

## RECOVERY COMMANDS

### If Token Limit Hit Mid-Execution

```bash
# Check current status
git status
git log -1 --oneline  # Should show f2c3742d or later checkpoint

# View this plan
cat .project/dev_tools/RESTRUCTURING_PLAN_2025-10-26.md

# Check progress (count directories)
ls | wc -l                                    # Visible root items
find . -maxdepth 1 -type d -name ".*" | wc -l # Hidden directories

# Continue from where left off - check "IN PROGRESS" section above
```

### If Something Breaks

```bash
# Rollback to checkpoint
git reset --hard f2c3742d

# Or restore from tar backup
cd ..
tar -xzf main_backup_YYYYMMDD_HHMMSS.tar.gz
```

---

## NOTES FOR NEXT CLAUDE SESSION

1. **Current blocker**: Need to decide what to do with `.ai/archive/phase3_validation/` (848MB)
   - Options: Delete if redundant with git history, move to external backup, or keep last 6 months

2. **Quick wins available**:
   - Delete `docs/_build/` (946MB) - it's generated HTML, should be in .gitignore
   - Clean up `.ai/archive/phase3_validation/` (848MB) - likely old test artifacts

3. **Manual decisions needed**:
   - Confirm `node_modules/` can be deleted (MCP servers use npx)
   - Verify test fixtures in `tests/` (67MB) are necessary

4. **After cleanup finishes**:
   - Commit with: `git commit -m "chore: Complete project restructuring [AI]"`
   - Push to remote: `git push origin main`
   - Update CLAUDE.md section 14 with new structure

---

**Last updated**: Phase 3 in progress (investigating archives)
**Next action**: Decide on `.ai/archive/phase3_validation/` (848MB) - delete, backup, or keep?
