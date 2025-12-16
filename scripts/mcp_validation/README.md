# MCP Validation Scripts

Automation scripts for validating and testing all MCP server integrations in the DIP-SMC-PSO project.

##  Overview

This directory contains scripts that leverage the 11 configured MCP servers for complete codebase validation:

- **mcp-analyzer**: Code quality (RUFF linting + VULTURE dead code detection)
- **pytest-mcp**: Test failure analysis and debugging
- **numpy-mcp**: Numerical analysis and matrix operations
- **pandas-mcp**: Data analysis and visualization
- **sqlite-mcp**: Database operations for PSO results
- *Plus 6 more servers for Git, filesystem, browser automation, etc.*

##  Available Scripts

### 1. Complete Code Quality Analysis
**Script**: `run_complete_code_quality_analysis.py`

Systematically analyzes all 604 Python files in the codebase using mcp-analyzer.

**Features**:
- 4-phase execution strategy (critical → standard priority)
- RUFF linting + VULTURE dead code detection
- Checkpoint/resume capability for long-running analysis
- complete reporting (JSON + Markdown)
- Progress monitoring with ETA estimates

**Usage**:
```bash
# Fresh start (7-12 hours)
python scripts/mcp_validation/run_complete_code_quality_analysis.py

# Resume from checkpoint
python scripts/mcp_validation/run_complete_code_quality_analysis.py --resume

# Specific phase only
python scripts/mcp_validation/run_complete_code_quality_analysis.py --phase 1

# Dry run (file discovery)
python scripts/mcp_validation/run_complete_code_quality_analysis.py --dry-run
```

**Outputs**:
- `docs/mcp-debugging/analysis_results/RUFF_FINDINGS_{timestamp}.md`
- `docs/mcp-debugging/analysis_results/VULTURE_FINDINGS_{timestamp}.md`
- `docs/mcp-debugging/analysis_results/SUMMARY_REPORT_{timestamp}.json`

**Documentation**: See `docs/mcp-debugging/workflows/CODE_QUALITY_ANALYSIS_PLAN.md`

---

### 2. Test Failure Analysis (Coming Soon)
**Script**: `analyze_pytest_failures.py`

Integrates pytest-mcp to analyze and categorize test failures.

**Features** (Planned):
- Automatic failure categorization (assertions, exceptions, timeouts)
- Historical failure tracking
- Root cause suggestions using sequential-thinking MCP
- Integration with issue tracker via github MCP

---

### 3. Numerical Stability Validation (Coming Soon)
**Script**: `validate_numerical_stability.py`

Uses numpy-mcp to analyze matrix conditioning and numerical stability.

**Features** (Planned):
- Matrix condition number analysis
- Eigenvalue decomposition for stability
- Ill-conditioned matrix detection
- Regularization recommendations

---

### 4. PSO Results Analysis (Coming Soon)
**Script**: `analyze_pso_convergence.py`

Combines sqlite-mcp + pandas-mcp for PSO optimization analysis.

**Features** (Planned):
- Query PSO results from database
- Statistical analysis of convergence
- Interactive visualization generation
- Performance comparison across controllers

---

##  Directory Structure

```
scripts/mcp_validation/
 README.md (this file)
 run_complete_code_quality_analysis.py   #  Implemented
 analyze_pytest_failures.py              #  Coming Soon
 validate_numerical_stability.py         #  Coming Soon
 analyze_pso_convergence.py              #  Coming Soon
 utils/
     mcp_client.py                       # MCP client utilities
     report_generators.py                # Report generation helpers
```

##  Technical Details

### MCP Integration Pattern

All scripts follow this pattern for MCP server interaction:

```python
# Direct tool invocation (via subprocess)
# Example: RUFF linting
result = subprocess.run(
    ["ruff", "check", file_path, "--output-format=json"],
    capture_output=True,
    text=True,
    timeout=60
)
issues = json.loads(result.stdout)

# Example: VULTURE dead code detection
result = subprocess.run(
    ["vulture", directory, "--min-confidence=80"],
    capture_output=True,
    text=True,
    timeout=120
)
dead_code = parse_vulture_output(result.stdout)
```

### Checkpoint System

Long-running analyses use checkpoints for resume capability:

```python
# Checkpoint structure
checkpoint = {
    "timestamp": "2025-10-06T14:30:00Z",
    "current_phase": 2,
    "current_file_index": 150,
    "results": [phase1_results, phase2_partial_results]
}

# Save location
.mcp_validation/checkpoints/code_quality_20251006_143000.json
```

### Error Handling

- **Transient errors**: Auto-retry with exponential backoff (max 3 attempts)
- **Timeouts**: 60s per file, skip and log if exceeded
- **Permanent errors**: Log and continue (don't block full analysis)

##  Output Formats

### Markdown Reports
- Human-readable analysis results
- Summary statistics and breakdowns
- Top problematic files and patterns
- Actionable recommendations

### JSON Summaries
- Machine-readable metrics
- CI/CD integration ready
- Historical comparison support
- Quality gate enforcement

### Progress Monitoring
```
Phase 2/4: Optimization & Analysis
Progress: [] 45/62 files (72.6%)
Current: pso_optimizer.py
RUFF: 298 issues | VULTURE: 67 items
Elapsed: 1h 15m | ETA: 0h 35m remaining
```

##  Validation Scenarios

All scripts implement validation scenarios from:
`docs/mcp-debugging/workflows/VALIDATION_WORKFLOW.md`

### Scenario 1: Code Quality Analysis
- **Script**: `run_complete_code_quality_analysis.py` 
- **MCP Servers**: mcp-analyzer
- **Status**: Implemented

### Scenario 2: Numerical Analysis
- **Script**: `validate_numerical_stability.py` 
- **MCP Servers**: numpy-mcp, sequential-thinking
- **Status**: Planned

### Scenario 3: PSO Results Analysis
- **Script**: `analyze_pso_convergence.py` 
- **MCP Servers**: sqlite-mcp, pandas-mcp
- **Status**: Planned

### Scenario 4: Test Failure Debugging
- **Script**: `analyze_pytest_failures.py` 
- **MCP Servers**: pytest-mcp, mcp-analyzer
- **Status**: Planned

### Scenario 5: Multi-Server Integrated Workflow
- **Script**: TBD 
- **MCP Servers**: 6+ servers orchestrated
- **Status**: Planned

##  Quality Standards

All validation scripts must meet:

-  **Reproducibility**: Identical results on repeat runs
-  **Checkpoint Support**: Resume capability for long operations
-  **complete Logging**: Detailed execution logs
-  **Error Resilience**: Graceful degradation on failures
-  **Documentation**: Inline comments and docstrings
-  **Testing**: Unit tests for core functions

##  Quick Start

### First-Time Setup

1. **Verify MCP servers are installed**:
   ```bash
   # Check installation status
   cat docs/mcp-debugging/INSTALLATION_LOG.md
   ```

2. **Run dry run to verify file discovery**:
   ```bash
   python scripts/mcp_validation/run_complete_code_quality_analysis.py --dry-run
   ```

3. **Execute full analysis** (can run overnight):
   ```bash
   python scripts/mcp_validation/run_complete_code_quality_analysis.py
   ```

4. **Review results**:
   ```bash
   ls docs/mcp-debugging/analysis_results/
   ```

### Resuming Interrupted Analysis

If analysis is interrupted (Ctrl+C, token limit, system restart):

```bash
# Resume from last checkpoint
python scripts/mcp_validation/run_complete_code_quality_analysis.py --resume
```

The script will automatically:
- Locate the most recent checkpoint
- Resume from the last completed file
- Continue all remaining phases

##  Related Documentation

- **Execution Plan**: `docs/mcp-debugging/workflows/CODE_QUALITY_ANALYSIS_PLAN.md`
- **Validation Workflow**: `docs/mcp-debugging/workflows/VALIDATION_WORKFLOW.md`
- **MCP Installation**: `docs/mcp-debugging/INSTALLATION_LOG.md`
- **Results Directory**: `docs/mcp-debugging/analysis_results/README.md`

##  Contributing

To add a new validation script:

1. **Follow the naming convention**: `{verb}_{noun}.py`
   - Examples: `analyze_pytest_failures.py`, `validate_numerical_stability.py`

2. **Implement required features**:
   - Checkpoint/resume support for long operations
   - Progress monitoring with ETA
   - Error handling with retry logic
   - complete logging
   - Report generation (Markdown + JSON)

3. **Add documentation**:
   - Docstrings for all functions
   - Usage examples in script header
   - Update this README

4. **Create validation scenario**:
   - Document in `VALIDATION_WORKFLOW.md`
   - Define expected inputs and outputs
   - Provide acceptance criteria

5. **Test thoroughly**:
   - Unit tests for core functions
   - Integration tests with MCP servers
   - Checkpoint/resume functionality
   - Error handling edge cases

##  Important Notes

### Time Considerations
- **Complete code quality analysis**: 7-12 hours (604 files)
- **Single phase analysis**: 1-4 hours (varies by phase)
- **Checkpoint saves**: Every 50 files (~10-15 minutes)

### Resource Usage
- **CPU**: Moderate (RUFF/VULTURE are fast)
- **Memory**: ~500MB peak (JSON report aggregation)
- **Disk**: ~50MB for reports and checkpoints
- **Network**: None (all local processing)

### Best Practices
- Run during off-peak hours for full analysis
- Monitor first phase to verify MCP server connectivity
- Keep checkpoint directory for historical tracking
- Review auto-fix suggestions before applying

---

**Last Updated**: 2025-10-06
**Status**: Active development
**Maintainer**: Claude Code MCP Integration Team
