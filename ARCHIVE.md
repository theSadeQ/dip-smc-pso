# Archived Materials - Restoration Guide

**Archive Date:** 2025-12-16
**Archive Location:** `D:/Projects/main_archive/`
**Archive Size:** ~1.1 GB (1,492 files)
**Repository:** https://github.com/theSadeQ/dip-smc-pso.git

---

## Archive Contents

### ai_materials/ - AI Development Materials (1,065 MB)

**config/ai_config/** (1 file)
- `.ai/config/session_state.json` - Claude Code session state

**config/project_ai_config/** (50 files)
- Agent orchestration configurations
- Repository management rules
- Documentation quality standards
- MCP usage guides
- Session continuity system
- Testing standards

**planning/** (78 files)
- Research task completion summaries (CA-02, CA-03, LT-4)
- Agent checkpoint reports
- Implementation status documents
- Recovery procedures

**educational/** (166 files, 783 MB)
- 17 NotebookLM podcast audio files (.m4a)
- 147 markdown episode guides (Phases 1-4)
- Beginner roadmap materials

---

### artifacts/ - Runtime Artifacts (42 MB, 841 files)

**qa_audits/** - Quality assurance audit reports
- CA-01: Controller simulation audit
- CA-02: Memory management audit
- CA-03: Architecture compliance
- MA-01: Guides audit
- MA-02: Hybrid adaptive STA-SMC audit

**thesis_guide/** - Thesis automation materials
- 30-day thesis writing guide
- Automation scripts (LaTeX conversion, figure generation)
- Validation results

---

### logs/ - Operational Logs (9.1 MB)
- Historical simulation logs
- PSO optimization traces
- Test execution logs

---

### cache/ - Build Caches (6.9 MB)
- pytest cache
- hypothesis database
- coverage HTML reports
- benchmark results

---

### claude_config/ - Claude Code Configuration (12 KB)
- Command definitions
- Slash command implementations
- IDE integration settings

---

### live_state/ - Runtime State (85 KB)
- Job registry and history
- Background task metadata
- Progress tracking

---

### dev_tools/ - AI Development Tools (35 files)

**Archived Tools:**
- Multi-account management (Switch-ClaudeAccount.ps1 - **PRESERVED IN REPO**)
- Checkpoint and recovery systems
- Session management utilities
- Token monitoring tools

**Protected File (NOT ARCHIVED):**
- `.project/dev_tools/Switch-ClaudeAccount.ps1` - Preserved in repository

---

### metadata/ - Archive Metadata
- Baseline file manifests (3,359 files)
- Phase-specific inventories
- Validation checksums

---

## Restoration Instructions

### Full Restoration
```bash
# Restore all archived materials to original locations
cd D:/Projects/main

# AI materials
cp -r D:/Projects/main_archive/ai_materials/config/ai_config .ai/config/
cp -r D:/Projects/main_archive/ai_materials/config/project_ai_config .project/ai/config/
cp -r D:/Projects/main_archive/ai_materials/planning .project/ai/planning/
cp -r D:/Projects/main_archive/ai_materials/educational .ai/edu/

# Artifacts
cp -r D:/Projects/main_archive/artifacts .artifacts/

# Logs
cp -r D:/Projects/main_archive/logs .logs/

# Cache
cp -r D:/Projects/main_archive/cache .cache/

# Claude config
cp -r D:/Projects/main_archive/claude_config .claude/

# Live state
cp -r D:/Projects/main_archive/live_state .live_state/

# MCP config
cp D:/Projects/main_archive/mcp_config.json .mcp.json

# Dev tools (AI-specific only)
cp -r D:/Projects/main_archive/dev_tools/.project/dev_tools/* .project/dev_tools/
```

### Selective Restoration

**Restore AI configuration only:**
```bash
cp -r D:/Projects/main_archive/ai_materials/config .project/ai/
```

**Restore NotebookLM episodes only:**
```bash
cp -r D:/Projects/main_archive/ai_materials/educational/notebooklm .ai/edu/
```

**Restore development tools:**
```bash
cp -r D:/Projects/main_archive/dev_tools/.project/dev_tools/.artifacts .project/dev_tools/
cp D:/Projects/main_archive/dev_tools/.project/dev_tools/agent_checkpoint.py .project/dev_tools/
# (Restore specific tools as needed)
```

---

## Verification After Restoration

### Check File Counts
```bash
# AI config
find .ai/config -type f | wc -l  # Expected: 1
find .project/ai/config -type f | wc -l  # Expected: 50
find .project/ai/planning -type f | wc -l  # Expected: 78

# Educational
find .ai/edu -name "*.m4a" | wc -l  # Expected: 17
find .ai/edu -name "*.md" | wc -l  # Expected: 147

# Artifacts
find .artifacts -type f | wc -l  # Expected: 841
```

### Verify Integrity
```bash
# Compare MD5 checksums (sample)
md5sum .ai/config/session_state.json D:/Projects/main_archive/ai_materials/config/ai_config/session_state.json

# Check audio files
find .ai/edu -name "*.m4a" -exec md5sum {} \; > restored_audio.md5
# Compare with archive
```

---

## Why These Files Were Archived

### Performance & Cleanliness
- Repository size reduced: 1.5 GB → 400 MB (73% reduction)
- Root visible directories: 49 → 19 (CLAUDE.md compliant)
- Hidden directories: Reduced from multiple AI-specific directories

### Production Readiness
- AI development materials separated from production code
- Session continuity preserved in archive (recoverable if needed)
- Clean repository structure for external users

### Selective Access
- Research materials remain in `research/` (organized, not archived)
- Production code and docs intact
- Testing infrastructure preserved

---

## Important Notes

### Protected Files (NOT Archived)
- `.project/dev_tools/Switch-ClaudeAccount.ps1` - **PRESERVED IN REPO**
- All production validators and git hooks
- Core development scripts

### Permanent Removal (Not in Archive)
- None - All materials safely archived
- Reversible via restoration commands above

### Archive Integrity
- All files verified with MD5 checksums during archival
- File counts match source manifests
- Structure preserved for easy navigation

---

## Archive Maintenance

### Backup Archive
```bash
# Create backup of archive
tar -czf main_archive_backup_$(date +%Y%m%d).tar.gz D:/Projects/main_archive/
```

### Verify Archive Health
```bash
# Check archive exists
[ -d "D:/Projects/main_archive" ] && echo "[OK] Archive exists"

# Check size
du -sh D:/Projects/main_archive  # Expected: ~1.1 GB
```

---

**Document Version:** 1.0
**Last Updated:** 2025-12-16
**Archive Validated:** ✓ All files verified with checksums
**Restoration Tested:** ✓ Sample restoration successful
