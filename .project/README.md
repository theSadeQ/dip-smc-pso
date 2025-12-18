# .project - Project Configuration Root

**Purpose**: Canonical root for ALL AI/development configurations, tools, and project metadata.

## Overview

The `.project/` directory is the single source of truth for:
- Project state tracking and recovery workflows
- AI orchestration patterns and educational content
- Development tools and automation scripts
- Quality standards and testing policies

## Directory Structure

```
.project/
├─ state/             # Project state files (canonical location)
├─ tools/             # Development and automation tools
├─ ai/                # AI configurations and documentation
├─ archive/           # Archived artifacts and old configs
├─ claude/            # Claude Code CLI settings
├─ mcp/               # MCP server configurations
└─ NAMING_CONVENTIONS.md
```

## Quick Navigation

### Recovery & State Management
- **30-Second Recovery**: `bash tools/recovery/recover_project.sh`
- **Project State**: `state/project_state.json`
- **Checkpoint Analysis**: `python tools/checkpoints/analyze_checkpoints.py`

**See**: `tools/recovery/README.md` for complete recovery guide

### Development Tools
- **Recovery Tools**: `tools/recovery/` (state manager, roadmap tracker)
- **Checkpoint System**: `tools/checkpoints/` (agent checkpoints, crash recovery)
- **Multi-Account**: `tools/multi_account/` (account switching, task wrapper)
- **Automation**: `tools/automation/` (200+ scripts for docs, citations, quality)
- **Analysis**: `tools/analysis/` (performance, code quality)

**See**: `tools/README.md` for complete tool index

### AI Configuration
- **Orchestration**: `ai/orchestration/` (6-agent pattern, checkpoint design)
- **Education**: `ai/education/` (beginner roadmap, NotebookLM guides)
- **Planning**: `ai/planning/` (roadmaps, phase tracking, status)
- **Quality**: `ai/quality/` (testing standards, QA audits)
- **Guides**: `ai/guides/` (technical how-tos, phase status)

**See**: `ai/README.md` for complete AI documentation

### Other Directories
- **archive/**: Old restructuring plans, archived configs
- **claude/**: Claude Code CLI settings (editor, model preferences)
- **mcp/**: MCP server configurations (12 servers)

## Key Files

### NAMING_CONVENTIONS.md
**Purpose**: Project-wide naming conventions for files, directories, and identifiers

**Standards**:
- File naming: `snake_case.py`, `kebab-case.md`, `PascalCase.tsx`
- Task IDs: `QW-1` (quick win), `MT-6` (medium-term), `LT-7` (long-term)
- Branch names: `feature/task-id-description`

## Migration History

### 2025-12-18: Major Reorganization
**Goal**: Consolidate from 11 directories (569 files, 7.3 MB) to 7 cleaner directories

**Changes**:
1. **State Consolidation**: `.project/ai/config/` + `recovery/state/` -> `.project/state/`
2. **AI Reorganization**: Lifecycle-based structure (orchestration, education, planning, quality, guides)
3. **Tools Consolidation**: Function-based structure (recovery, checkpoints, multi_account, automation, analysis)
4. **Cleanup**: Removed empty templates, obsolete directories

**Result**:
- 7 top-level directories (down from 11)
- 0 duplicate state files (was 2 duplicates)
- 0 empty directories (was 25+ empty)
- Preserved git history for all 450+ renamed files

**Validation**: All migrations verified with md5sum checks, backup created

## Usage Patterns

### Daily Development
```bash
# Check project status
cat .project/state/project_state.json | jq '.current_phase'

# Run recovery after token limit
bash .project/tools/recovery/recover_project.sh

# Launch task with checkpointing
python .project/tools/checkpoints/launch_checkpoint_task.py --task MT-6
```

### Multi-Agent Workflows
```bash
# View orchestration pattern
cat .project/ai/orchestration/agent_orchestration.md

# Check agent specs
ls .project/ai/orchestration/agents/

# Analyze checkpoint progress
python .project/tools/checkpoints/analyze_checkpoints.py
```

### Quality Assurance
```bash
# Check testing standards
cat .project/ai/quality/testing_standards.md

# Run documentation quality scan
python .project/tools/automation/scripts/docs/detect_ai_patterns.py

# View QA audit results
cat .project/ai/quality/QA-03_DYNAMICS_CONFIG_AUDIT_REPORT.md
```

## Deprecated Aliases (DO NOT USE)

- [ERROR] `.ai/` -> use `.project/ai/`
- [ERROR] `.dev_tools/` at root -> use `.project/tools/`
- [ERROR] `recovery/state/` -> use `.project/state/`

**Reason**: Consolidated to `.project/` as canonical root (2025-12-18 migration)

## Related Documentation

- **CLAUDE.md**: Master project instructions and conventions (root directory)
- **Workspace Organization**: `.project/ai/guides/workspace_organization.md`
- **Session Continuity**: `.project/ai/guides/session_continuity.md`
- **MCP Usage Guide**: `.project/ai/guides/mcp_usage_guide.md`

## Support

For questions or issues:
1. Check README files in subdirectories
2. Review `.project/ai/guides/` for how-tos
3. Analyze project state: `bash .project/tools/recovery/recover_project.sh`
4. Check Git history: `git log .project/ --oneline`

**Recovery Reliability**: 10/10 Git commits, 9/10 project state, 9/10 checkpoints
