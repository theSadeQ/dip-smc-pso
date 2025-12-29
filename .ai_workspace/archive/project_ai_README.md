# .ai_workspace/ai - AI Configuration & Documentation

**Purpose**: Lifecycle-organized AI configurations, orchestration patterns, educational content, and quality standards.

## Directory Structure

```
ai/
├─ orchestration/     # Multi-agent orchestration and coordination
├─ education/         # Educational materials and NotebookLM guides
├─ planning/          # Project planning, roadmaps, and phase tracking
├─ quality/           # Quality assurance, testing standards, audits
├─ guides/            # Technical guides, phase status, and how-tos
└─ collaboration/     # Collaboration guidelines (deprecated)
```

## Subdirectories

### orchestration/
**Purpose**: Multi-agent workflows, checkpoint systems, and agent coordination

**Contents**:
- `agent_orchestration.md` - Ultimate Orchestrator pattern (6-agent)
- `agent_checkpoint_system.md` - Checkpoint design and API
- `agents/` - Individual agent specifications (8 agents)
- `agents.json` - Agent registry and capabilities

**Integration**: Used by `.ai_workspace/tools/checkpoints/` for crash recovery

### education/
**Purpose**: Learning roadmaps, NotebookLM podcast guides, and beginner materials

**Contents**:
- `beginner-roadmap.md` - 125-150 hour beginner curriculum (Phases 1-2 complete)
- `notebooklm_guide.md` - TTS optimization requirements for podcast generation
- `notebooklm/episode_guides/` - 44 episodes across 4 phases (~40 hours audio)
- `phase1/` - Computing basics, Python fundamentals, physics, math

**Status**: Phase 4 complete (November 2025), 44 episodes generated

**See**: `.ai_workspace/education/README.md` for complete learning paths

### planning/
**Purpose**: Strategic roadmaps, phase tracking, and execution plans

**Contents**:
- `CURRENT_STATUS.md` - Real-time project status and priorities
- `STRATEGIC_ROADMAP.md` - Multi-level enhancement roadmap
- `research/` - Research phase roadmaps (72-hour, 8-week)
- `phase3/`, `phase4/` - Phase-specific execution plans and handoffs

**Key Documents**:
- Research Roadmap: 72 hours over 8 weeks (11/11 tasks complete)
- Phase 3 Handoff: UI/UX 34/34 issues (maintenance mode)
- Phase 4 Plan: Production hardening 4.1+4.2 complete

### quality/
**Purpose**: Quality standards, testing policies, and audit reports

**Contents**:
- `documentation_quality.md` - AI pattern detection, style guide
- `testing_standards.md` - Coverage gates (85% overall, 95% critical)
- QA audit reports (QA-02, QA-03) - Configuration and dynamics audits
- `proposed_config_additions.yaml` - Validated config changes

**Coverage Standards**: 85% overall, 95% critical, 100% safety-critical

### guides/
**Purpose**: Technical how-tos, phase status reports, and configuration guides

**Contents**:
- Phase status: `phase3_status.md` (UI complete), `phase4_status.md` (thread safety)
- Project guides: `workspace_organization.md`, `session_continuity.md`
- Integration guides: `mcp_usage_guide.md`, `perplexity_setup.md`
- Technical: `controller_memory.md`, `documentation_build_system.md`

**Key Guides**: Repository management, session continuity, MCP auto-triggers

### collaboration/ (Deprecated)
**Purpose**: Legacy collaboration guidelines (empty after migration)

**Status**: Content migrated to `guides/` and `orchestration/`

## Common Workflows

### Multi-Agent Orchestration
```bash
# View agent specifications
ls .ai_workspace/orchestration/agents/

# Check orchestration pattern
cat .ai_workspace/orchestration/agent_orchestration.md

# Agent checkpoint API
python .ai_workspace/tools/checkpoints/agent_checkpoint.py --help
```

### Learning Path
```bash
# Start beginner roadmap (Path 0)
cat .ai_workspace/education/beginner-roadmap.md

# Generate NotebookLM podcast
cat .ai_workspace/education/notebooklm_guide.md

# Browse episode guides
ls .ai_workspace/education/notebooklm/episode_guides/phase4/
```

### Project Planning
```bash
# Check current status
cat .ai_workspace/planning/CURRENT_STATUS.md

# View research roadmap
cat .ai_workspace/planning/research/ROADMAP_EXISTING_PROJECT.md

# Phase 3 handoff
cat .ai_workspace/planning/phase3/HANDOFF.md
```

### Quality Assurance
```bash
# Check testing standards
cat .ai_workspace/quality/testing_standards.md

# Run documentation quality scan
python .ai_workspace/tools/automation/scripts/docs/detect_ai_patterns.py

# View QA audit results
cat .ai_workspace/quality/QA-03_DYNAMICS_CONFIG_AUDIT_REPORT.md
```

## Migration History

**2025-12-18**: Consolidated from 5 legacy locations:
- `.ai_workspace/config/` (orchestration, guides) -> `ai/orchestration/`, `ai/guides/`
- `.ai_workspace/edu/` -> `ai/education/`
- `.ai_workspace/qa/` -> `ai/quality/`
- `.ai_workspace/planning/` (merged with `.ai_workspace/planning/`) -> `ai/planning/`

**Result**: 4 lifecycle-based directories (orchestration, education, planning, quality) + 1 technical (guides)
