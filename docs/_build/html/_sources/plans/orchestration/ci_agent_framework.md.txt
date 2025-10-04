# CI Agent Orchestration Framework

**Document Version:** 1.0.0
**Created:** 2025-01-15
**Purpose:** Multi-agent CI orchestration system for Windows PowerShell environments

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Agent Selection Decision Tree](#agent-selection-decision-tree)
3. [Artifact Schema Design](#artifact-schema-design)
4. [Windows PowerShell Integration](#windows-powershell-integration)
5. [Usage Examples](#usage-examples)

---

## Architecture Overview

### **Hub-and-Spoke with Minimal Coupling**

```
                    ┌─────────────────────────┐
                    │ Ultimate Orchestrator   │
                    │ (Headless CI Agent)     │
                    └───────────┬─────────────┘
                                │
                    ┌───────────┴───────────┐
                    │  Delegation Layer     │
                    │  (2-4 subagents)      │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
   ┌────▼────┐           ┌─────▼─────┐          ┌─────▼─────┐
   │ Agent 1 │           │  Agent 2  │          │  Agent 3  │
   │ (Reused)│           │ (Reused)  │          │  (New?)   │
   └────┬────┘           └─────┬─────┘          └─────┬─────┘
        │                      │                       │
        └──────────────────────┼───────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Artifact Integration│
                    │ (JSON + Patches)    │
                    └─────────────────────┘
```

### **Core Design Principles**

1. **Reuse First, Create When Justified**
   - Existing agents cover 80% of common tasks
   - Create new agents only for skill gaps >30%

2. **Minimal Coupling**
   - Agents work independently on non-overlapping tasks
   - Shared artifact contracts prevent tight dependencies
   - Orchestrator handles conflict resolution

3. **Parallelization Opportunities**
   - 2-4 agents can work concurrently
   - Speedup: 1.5x-2x vs sequential execution
   - Token efficiency: Reusing existing agents minimizes context

4. **Windows-First Design**
   - PowerShell command templates
   - Path handling (`\` separators)
   - Environment-specific validation

---

## Agent Selection Decision Tree

### **Available Agent Pool**

| Agent | Skills | Typical Duration | Parallelization |
|-------|--------|------------------|-----------------|
| **Integration Coordinator** | Cross-domain orchestration, system health, config validation, debugging | 30-90min | Medium |
| **Control Systems Specialist** | SMC design, stability analysis, Lyapunov functions, controller implementation | 45-120min | Low |
| **PSO Optimization Engineer** | PSO tuning, convergence analysis, multi-objective optimization, fitness design | 60-180min | Medium |
| **Documentation Expert** | LaTeX math, Sphinx docs, API documentation, scientific writing, citations | 30-90min | High |
| **Code Beautification Specialist** | ASCII headers, type hints, directory organization, PEP 8, architecture patterns | 20-60min | High |

### **Decision Matrix: Reuse vs Create**

```python
class AgentSelectionStrategy:
    """
    Decision framework for optimal agent configuration.
    """

    def should_reuse(self, issue_requirements: Set[str]) -> Dict[str, float]:
        """
        Calculate skill match scores for existing agents.

        Returns: {agent_name: match_score (0.0-1.0)}
        """
        scores = {}

        for agent_name, agent_spec in self.EXISTING_AGENTS.items():
            agent_skills = set(agent_spec['skills'])

            # Jaccard similarity
            intersection = issue_requirements & agent_skills
            union = issue_requirements | agent_skills

            scores[agent_name] = len(intersection) / len(union) if union else 0.0

        return scores

    def should_create_new(self, best_match_score: float,
                         workload_estimate: int) -> Dict[str, Any]:
        """
        Create new agent if:
        1. Skill gap > 30% (best_match < 0.7)
        2. Throughput gap: workload > 4 hours AND parallelizable
        3. Policy gap: CLAUDE.md mandates specialist
        """

        if best_match_score < 0.7:
            return {
                'create': True,
                'reason': 'SKILL_GAP',
                'blocking': True,
                'justification': f'No existing agent covers >70% of required skills'
            }

        if workload_estimate > 240:  # 4 hours
            return {
                'create': True,
                'reason': 'THROUGHPUT_GAP',
                'blocking': False,  # Can proceed slower
                'justification': f'{workload_estimate}min workload benefits from parallelization'
            }

        return {'create': False}
```

### **Example: Citation System**

**Issue Requirements:**
```python
issue_requirements = {
    'citation_extraction',      # NEW SKILL (0% match)
    'academic_search',          # NEW SKILL (0% match)
    'BibTeX_management',       # NEW SKILL (0% match)
    'scientific_writing',      # Documentation Expert (100% match)
    'API_integration',         # NEW SKILL (0% match)
    'cross_reference_validation' # Integration Coordinator (80% match)
}
```

**Agent Selection:**
```json
{
  "selected_agents": [
    {
      "role": "Academic Research Automation Engineer",
      "status": "NEW - BLOCKING",
      "match_score": 0.0,
      "reason": "Skill gap: 4/6 requirements (67%) not covered by existing pool"
    },
    {
      "role": "Documentation Expert",
      "status": "REUSED",
      "match_score": 0.35,
      "reason": "Handles scientific writing and BibTeX formatting"
    },
    {
      "role": "Integration Coordinator",
      "status": "REUSED",
      "match_score": 0.25,
      "reason": "Cross-reference validation and QA"
    }
  ],

  "justification": "3-agent configuration optimal: NEW agent for specialized research automation, 2 existing agents for formatting/validation. Parallelization: NEW agent + DOC work simultaneously on different claim batches."
}
```

---

## Artifact Schema Design

### **Shared JSON Schema**

All agents produce JSON artifacts with standardized structure:

```json
{
  "metadata": {
    "agent_name": "string",
    "timestamp": "ISO8601",
    "issue_id": "string",
    "confidence": "float (0.0-1.0)"
  },

  "changes": [
    {
      "type": "code_change | doc_change | config_change",
      "file": "relative\\path\\to\\file",  // Windows paths
      "patch": "unified diff format",
      "rationale": "why this change",
      "validation": ["test_command", "expected_result"]
    }
  ],

  "dependencies": {
    "requires": ["other_agent_artifacts.json"],
    "provides": ["interfaces for downstream"]
  }
}
```

### **Integration Algorithm**

```python
def integrate_artifacts(agent_outputs: List[Dict]) -> Dict:
    """
    Reconcile multiple agent outputs.

    Conflict resolution order:
    1. Domain expert wins (Control Specialist > Integration Coordinator for SMC)
    2. Higher confidence wins (confidence > 0.8 overrides < 0.8)
    3. More specific wins (file-level > directory-level)
    4. Manual review required (flag for human)
    """

    DOMAIN_PRIORITY = {
        'Academic Research Automation Engineer': 90,
        'Control Systems Specialist': 80,
        'PSO Optimization Engineer': 70,
        'Documentation Expert': 60,
        'Integration Coordinator': 50
    }

    merged = {
        'changes': [],
        'conflicts': []
    }

    # Group changes by file
    by_file = defaultdict(list)
    for output in agent_outputs:
        for change in output['changes']:
            by_file[change['file']].append((output['metadata']['agent_name'], change))

    # Detect and resolve conflicts
    for file_path, changes in by_file.items():
        if len(changes) > 1:
            # Multiple agents modified same file - resolve conflict
            winner = max(changes, key=lambda x: (
                DOMAIN_PRIORITY.get(x[0], 0),  # Domain expert priority
                x[1].get('confidence', 0.0)     # Confidence tiebreaker
            ))

            merged['changes'].append(winner[1])
            merged['conflicts'].append({
                'file': file_path,
                'agents': [c[0] for c in changes],
                'resolution': f"Used {winner[0]} (domain priority + confidence)"
            })
        else:
            merged['changes'].append(changes[0][1])

    return merged
```

### **Example Artifact**

**Agent 1 Output** (`artifacts/formal_claims.json`):
```json
{
  "metadata": {
    "agent_name": "Academic Research Automation Engineer",
    "timestamp": "2025-01-15T10:30:00Z",
    "confidence": 0.92
  },
  "changes": [
    {
      "type": "doc_change",
      "file": "docs\\theory\\smc_theory_complete.md",
      "patch": "diff --git a/docs/theory/smc_theory_complete.md ...",
      "rationale": "Add citation for Theorem 1 (Levant 2003)",
      "validation": ["sphinx-build -b html docs docs\\_build", "0 warnings"]
    }
  ]
}
```

**Agent 2 Output** (`artifacts/citation_style.json`):
```json
{
  "metadata": {
    "agent_name": "Documentation Expert",
    "timestamp": "2025-01-15T10:32:00Z",
    "confidence": 0.95
  },
  "changes": [
    {
      "type": "doc_change",
      "file": "docs\\references\\bibliography.md",
      "patch": "diff --git a/docs/references/bibliography.md ...",
      "rationale": "Format bibliography in IEEE style",
      "validation": ["bibtex docs\\references\\enhanced_bibliography.bib", "0 errors"]
    }
  ]
}
```

**Integrated Output:**
```json
{
  "changes": [
    {
      "file": "docs\\theory\\smc_theory_complete.md",
      "source": "Academic Research Automation Engineer",
      "confidence": 0.92
    },
    {
      "file": "docs\\references\\bibliography.md",
      "source": "Documentation Expert",
      "confidence": 0.95
    }
  ],
  "conflicts": []
}
```

---

## Windows PowerShell Integration

### **Environment Setup**

```powershell
# Standard environment variables
$env:REPO_ROOT = "D:\Projects\main"
$env:PYTHON_PATH = "python"
$env:GIT_PATH = "git"

# Error handling
$ErrorActionPreference = 'Stop'
```

### **Validation Command Templates**

#### **Template 1: Static Analysis**

```powershell
# Step 1: Type checking
Set-Location $env:REPO_ROOT
python -m mypy src\ --strict --show-error-codes
if ($LASTEXITCODE -ne 0) { throw "mypy failed" }

# Step 2: Linting
python -m ruff check src\ tests\
if ($LASTEXITCODE -ne 0) { throw "ruff failed" }

# Step 3: Import validation
python -c "import src; print('Imports OK')"
if ($LASTEXITCODE -ne 0) { throw "Import check failed" }
```

#### **Template 2: Unit Tests**

```powershell
# Fast unit tests (controllers only)
python -m pytest tests\test_controllers\ `
  -v `
  --maxfail=3 `
  --tb=short `
  --durations=10
if ($LASTEXITCODE -ne 0) { throw "Unit tests failed" }
```

#### **Template 3: Integration Tests**

```powershell
# Slower integration tests
python -m pytest tests\test_integration\ `
  -v `
  --maxfail=1 `
  --durations=5 `
  --timeout=300
if ($LASTEXITCODE -ne 0) { throw "Integration tests failed" }
```

#### **Template 4: Coverage Gates**

```powershell
# Coverage enforcement
python -m pytest `
  --cov=src `
  --cov-report=term `
  --cov-report=html `
  --cov-fail-under=85
if ($LASTEXITCODE -ne 0) { throw "Coverage below 85%" }

# Open coverage report
start htmlcov\index.html
```

#### **Template 5: Performance Benchmarks**

```powershell
# Performance regression detection
python -m pytest tests\test_benchmarks\ `
  --benchmark-only `
  --benchmark-compare `
  --benchmark-compare-fail=mean:5%
if ($LASTEXITCODE -ne 0) { throw "Performance regression >5%" }
```

### **Complete Validation Pipeline**

```powershell
# File: .dev_tools\validation\run_ci_validation.ps1

param(
    [switch]$SkipSlow,
    [switch]$SkipBenchmarks
)

$ErrorActionPreference = 'Stop'
Set-Location "D:\Projects\main"

Write-Host "===== CI Validation Pipeline =====" -ForegroundColor Cyan

# Phase 1: Static Analysis
Write-Host "`n[1/5] Static Analysis..." -ForegroundColor Yellow
python -m mypy src\ --strict --show-error-codes
python -m ruff check src\ tests\

# Phase 2: Unit Tests
Write-Host "`n[2/5] Unit Tests..." -ForegroundColor Yellow
python -m pytest tests\test_controllers\ -v --maxfail=3

# Phase 3: Integration Tests (optional)
if (-not $SkipSlow) {
    Write-Host "`n[3/5] Integration Tests..." -ForegroundColor Yellow
    python -m pytest tests\test_integration\ -v --maxfail=1
} else {
    Write-Host "`n[3/5] Integration Tests (SKIPPED)" -ForegroundColor Gray
}

# Phase 4: Coverage
Write-Host "`n[4/5] Coverage Analysis..." -ForegroundColor Yellow
python -m pytest --cov=src --cov-report=term --cov-fail-under=85

# Phase 5: Benchmarks (optional)
if (-not $SkipBenchmarks) {
    Write-Host "`n[5/5] Performance Benchmarks..." -ForegroundColor Yellow
    python -m pytest tests\test_benchmarks\ --benchmark-only
} else {
    Write-Host "`n[5/5] Benchmarks (SKIPPED)" -ForegroundColor Gray
}

Write-Host "`n===== All Gates Passed =====" -ForegroundColor Green
```

**Usage:**
```powershell
# Full validation
.\\.dev_tools\\validation\\run_ci_validation.ps1

# Skip slow tests
.\\.dev_tools\\validation\\run_ci_validation.ps1 -SkipSlow

# Skip benchmarks
.\\.dev_tools\\validation\\run_ci_validation.ps1 -SkipBenchmarks
```

---

## Usage Examples

### **Example 1: Citation System (3 Agents)**

**Orchestrator JSON Output:**

```json
{
  "summary": "Build citation verification system with AI research + formatting + validation",
  "severity": "high",
  "justification": "3-agent optimal: NEW agent (research automation), DOC expert (formatting), INT coordinator (QA). Parallelization: 2x speedup. Token efficiency: Reuse 2 existing.",

  "selected_agents": [
    {
      "role": "Academic Research Automation Engineer",
      "reason": "Specialized AI research + citation extraction (62.5% skill gap)"
    },
    {
      "role": "Documentation Expert",
      "reason": "BibTeX formatting + Sphinx integration (35% match)"
    },
    {
      "role": "Integration Coordinator",
      "reason": "Cross-reference validation + coverage gates (25% match)"
    }
  ],

  "plan": [
    "Step 1 (NEW): Extract 500+ claims from docs + code",
    "Step 2 (NEW): AI research via Semantic Scholar + ArXiv",
    "Step 3 (DOC): Format citations in Sphinx {cite} syntax",
    "Step 4 (INT): Validate coverage gates (100% theorems cited)"
  ],

  "delegation": [
    {
      "role": "Academic Research Automation Engineer",
      "inputs": ["docs/**/*.md (259 files)", "src/**/*.py (165 files)"],
      "deliverables": ["artifacts\\claims_inventory.json", "artifacts\\research_results.json"],
      "definition_of_done": ["≥500 claims extracted", "≥85% CRITICAL claims have refs"]
    },
    {
      "role": "Documentation Expert",
      "inputs": ["artifacts\\citation_mapping.json", "docs\\references\\enhanced_bibliography.bib"],
      "deliverables": ["patches\\citation_insertions.patch", "docs\\references\\bibliography.md"],
      "definition_of_done": ["100% theorems cited", "Sphinx builds without warnings"]
    },
    {
      "role": "Integration Coordinator",
      "inputs": ["artifacts\\claims_inventory.json", "patches\\citation_insertions.patch"],
      "deliverables": ["artifacts\\coverage_gate_results.json", ".github\\workflows\\citation_validation.yml"],
      "definition_of_done": ["Coverage gates pass", "CI workflow active"]
    }
  ],

  "verification": {
    "commands_ps": [
      "Set-Location D:\\Projects\\main",
      "python .dev_tools\\citation_validation\\validate_json_schemas.py artifacts\\*.json",
      "bibtex docs\\references\\enhanced_bibliography.bib",
      "sphinx-build -b html docs docs\\_build -W",
      "python .dev_tools\\citation_validation\\enforce_coverage_gates.py"
    ],
    "expected": [
      "JSON schemas valid",
      "BibTeX compiles (0 errors)",
      "Sphinx builds (0 warnings)",
      "Coverage: 100% theorems, 90% implementations"
    ],
    "risk_notes": [
      "API rate limits: Implement exponential backoff",
      "Citation key conflicts: Dedup with existing 39 refs",
      "Sphinx build time: +30% acceptable for quality"
    ]
  },

  "subagent_requests": [
    {
      "name": "Academic Research Automation Engineer",
      "blocking": true,
      "why": "Skill gap: 62.5% of requirements (AI research + citation extraction) not covered",
      "scope": [
        "Multi-stage claim extraction (regex + AST + NLP)",
        "Academic API integration (Semantic Scholar, ArXiv, CrossRef)",
        "Citation quality scoring and ranking",
        "BibTeX generation from API responses"
      ],
      "inputs_contract": ["docs/**/*.md", "src/**/*.py", ".env (API keys)"],
      "outputs_contract": [
        "claims_inventory.json: {claims: [...], research_queue: {...}}",
        "research_results.json: {claim_id: [ranked_refs]}",
        "enhanced_bibliography.bib: BibTeX entries",
        "citation_mapping.json: {claim_id: [citation_keys]}"
      ],
      "handoff": "DOC expert consumes citation_mapping.json for insertion. INT coordinator validates coverage."
    }
  ],

  "confidence": 0.88
}
```

### **Example 2: Chattering Reduction (2 Agents)**

**Orchestrator JSON Output:**

```json
{
  "summary": "Reduce chattering in classical SMC by 50% via boundary layer tuning + PSO optimization",
  "severity": "low",
  "justification": "2-agent optimal: Control Systems Specialist (100% match for SMC/Lyapunov), PSO Engineer (90% match for gain tuning). Sequential workflow (theory → optimization). No parallelization benefit.",

  "selected_agents": [
    {
      "role": "Control Systems Specialist",
      "reason": "Core SMC expert: boundary layer design, Lyapunov stability, chattering theory (100% match)"
    },
    {
      "role": "PSO Optimization Engineer",
      "reason": "Tunes epsilon and gains with chattering-focused fitness function (90% match)"
    }
  ],

  "plan": [
    "Step 1 (Control): Analyze chattering sources, design boundary layer modifications",
    "Step 2 (PSO): Optimize epsilon + gains with chattering-focused fitness",
    "Step 3 (Control): Validate stability + performance with optimized params",
    "Step 4 (Both): Integration test + documentation"
  ],

  "delegation": [
    {
      "role": "Control Systems Specialist",
      "inputs": ["src\\controllers\\smc\\classic_smc.py", "docs\\theory\\smc_theory_complete.md"],
      "deliverables": ["patches\\boundary_layer_modifications.patch", "artifacts\\lyapunov_stability_proof.md"],
      "definition_of_done": ["Lyapunov stability proven", "Chattering-focused design validated"]
    },
    {
      "role": "PSO Optimization Engineer",
      "inputs": ["artifacts\\chattering_fitness_function.py", "config.yaml"],
      "deliverables": ["optimization_results\\chattering_gains.json", "artifacts\\pso_convergence_plot.png"],
      "definition_of_done": ["Chattering reduced by ≥50%", "Stability margins maintained"]
    }
  ],

  "verification": {
    "commands_ps": [
      "python simulate.py --ctrl classical_smc --load optimization_results\\chattering_gains.json --plot",
      "python -m pytest tests\\test_controllers\\smc\\test_chattering_reduction.py -v"
    ],
    "expected": [
      "Chattering metric reduced by ≥50%",
      "Lyapunov stability tests pass",
      "Settling time unchanged (< 2s)"
    ],
    "risk_notes": [
      "Trade-off: Larger boundary layer may increase steady-state error",
      "Validation: Ensure stability margins >20% for robustness"
    ]
  },

  "subagent_requests": [],

  "confidence": 0.95
}
```

---

## Best Practices

### **1. Agent Selection**

✅ **DO:**
- Reuse existing agents when skill match >70%
- Create new agents for skill gaps >30%
- Justify agent count (2-4 optimal for speed/token balance)

❌ **DON'T:**
- Create redundant agents (check existing pool first)
- Use >4 agents (overhead > benefit)
- Use 1 agent for multi-domain tasks (token inefficient)

### **2. Artifact Design**

✅ **DO:**
- Use standardized JSON schema across all agents
- Include confidence scores for conflict resolution
- Provide validation commands for each artifact

❌ **DON'T:**
- Create tight dependencies between agents
- Mix artifact types (keep JSON separate from patches)
- Omit metadata (timestamp, agent name, confidence)

### **3. Windows Integration**

✅ **DO:**
- Use PowerShell-native commands (`Set-Location`, not `cd`)
- Handle paths with `\` separators
- Set `$ErrorActionPreference = 'Stop'` for safety

❌ **DON'T:**
- Use bash commands (`find`, `grep`) - use PowerShell equivalents
- Assume Unix-style paths (`/` separators)
- Ignore exit codes (`$LASTEXITCODE`)

---

## Related Documents

- [../citation_system/00_master_roadmap.md](../citation_system/00_master_roadmap.md) - Citation system implementation
- [../../CLAUDE.md](../../CLAUDE.md) - Project conventions and agent pool

---

**Document Revision History:**

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-15 | Initial framework documentation |

**Status:** ✅ **FRAMEWORK DEFINED - READY FOR USE**

**End of CI Agent Orchestration Framework**
