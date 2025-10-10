# MCP Comprehensive Debugging Workflows

**Locally-Available Debugging Infrastructure for DIP-SMC-PSO Project**

This directory contains reusable, session-persistent debugging workflows using Multiple Model Context Protocol (MCP) servers to systematically debug, analyze, and validate the double inverted pendulum control system.

## Quick Start

### Available MCP Servers

| Server | Purpose | Key Capabilities |
|--------|---------|------------------|
| **ruff** | Code quality linting | PEP 8 compliance, auto-fixes, style enforcement |
| **vulture** | Dead code detection | Unused variables, functions, imports |
| **playwright** | Browser automation | Streamlit testing, screenshots, UI validation |
| **pytest-mcp** | Test execution | Run tests, collect coverage, analyze failures |
| **git-mcp** | Version control | Commits, history, diffs, blame analysis |
| **filesystem** | File operations | Search, read, analyze project files |
| **sequential-thinking** | Methodical analysis | Step-by-step problem decomposition |
| **numpy-mcp** | Numerical computing | Array operations, linear algebra validation |
| **github** | Issue management | Create issues, track bugs, project management |
| **sqlite-mcp** | Data analysis | Query metrics, analyze results databases |

### Workflows Available

1. **[Complete Debugging Workflow](workflows/complete-debugging-workflow.md)** - Master 6-phase systematic debugging
2. **[Code Quality Analysis](workflows/code-quality-analysis.md)** - RUFF + VULTURE code quality checks
3. **[Streamlit Testing](workflows/streamlit-testing-workflow.md)** - Playwright browser automation
4. **[Test Debugging](workflows/test-debugging-workflow.md)** - Pytest collection, execution, coverage
5. **[Production Validation](workflows/production-validation-workflow.md)** - Readiness checks, dependencies, safety
6. **[Performance Analysis](workflows/performance-analysis-workflow.md)** - Benchmarking, profiling, optimization

## Usage Patterns

### Slash Commands

Use these commands to invoke workflows:

```bash
/debug-with-mcp          # Start integrated multi-server debugging
/test-browser            # Test Streamlit dashboard with Playwright
/analyze-logs            # Automated log analysis
/test-controller         # Run controller test suite
/validate-simulation     # Validate simulation results
/optimize-controller     # Launch PSO optimization workflow
```

### Direct Workflow Execution

Copy-paste workflow steps from `workflows/` directory for systematic debugging.

### Report Templates

Use templates from `templates/` directory to generate standardized reports.

## Directory Structure

```
mcp-debugging/
├── README.md                          # This file
├── workflows/                         # Reusable debugging workflows
│   ├── complete-debugging-workflow.md # Master 6-phase workflow
│   ├── code-quality-analysis.md       # RUFF/VULTURE workflow
│   ├── streamlit-testing-workflow.md  # Playwright UI testing
│   ├── test-debugging-workflow.md     # Pytest debugging
│   ├── production-validation-workflow.md  # Production checks
│   └── performance-analysis-workflow.md   # Benchmarking
├── templates/                         # Report templates
│   ├── analysis-report-template.md    # Standard analysis format
│   ├── bug-report-template.md         # Bug reporting format
│   └── test-plan-template.md          # Test planning format
└── analysis_results/                  # Generated reports (date-stamped)
    ├── RUFF_FINDINGS_*.md
    ├── VULTURE_FINDINGS_*.md
    ├── MCP_DEBUGGING_PROGRESS_*.md
    └── ...
```

## Workflow Philosophy

### 1. Systematic Approach
- **Phase-based:** Break complex debugging into manageable phases
- **Documented:** Every step generates artifacts for future reference
- **Reproducible:** Workflows can be repeated across sessions

### 2. Multi-Tool Integration
- **Parallel execution:** Run multiple MCP servers concurrently
- **Cross-validation:** Use multiple tools to verify findings
- **Comprehensive coverage:** Address code, tests, deployment, performance

### 3. Session Persistence
- **Locally available:** All workflows stored in repository
- **Version controlled:** Track improvements to debugging processes
- **Team accessible:** Share debugging knowledge across contributors

## Common Use Cases

### Debugging PSO Convergence Issues

1. Use `/analyze-pso-logs` to examine optimization logs
2. Follow **Performance Analysis** workflow to identify bottlenecks
3. Run **Test Debugging** workflow to validate PSO implementation
4. Generate convergence report using analysis template

### Fixing Controller Instability

1. Run **Code Quality Analysis** to check for numerical errors
2. Execute **Test Debugging** to isolate failing stability tests
3. Use **Production Validation** to verify gain bounds
4. Apply fixes and re-run validation suite

### Streamlit Dashboard Testing

1. Start Streamlit: `streamlit run streamlit_app.py`
2. Use `/test-browser` with Playwright MCP
3. Follow **Streamlit Testing Workflow** for UI validation
4. Capture screenshots and performance metrics
5. Generate UI/UX report

### Preparing for Production Deployment

1. Run **Production Validation Workflow** (all scripts)
2. Execute **Code Quality Analysis** (target: 0 errors)
3. Run **Test Debugging** (target: ≥85% coverage)
4. Verify thread safety, memory management, SPOF removal
5. Generate production readiness report (target: ≥7.5/10)

## Best Practices

### Before Starting a Workflow

1. **Pull latest changes:** `git pull origin main`
2. **Check environment:** Verify Python, Node.js, dependencies
3. **Clean workspace:** Remove stale logs, artifacts
4. **Read workflow first:** Understand steps before execution

### During Workflow Execution

1. **Follow step-by-step:** Don't skip phases
2. **Generate reports:** Document all findings immediately
3. **Commit incrementally:** Small, focused commits after each phase
4. **Validate continuously:** Run smoke tests after fixes

### After Workflow Completion

1. **Push changes:** `git push origin main`
2. **Update documentation:** Add lessons learned
3. **Close issues:** Link commits to GitHub issues
4. **Share results:** Update team on findings

## Integration with Claude Code

### Automatic Workflow Detection

Claude Code automatically suggests workflows based on context:

- **Linting errors detected** → Suggests Code Quality Analysis
- **Tests failing** → Suggests Test Debugging Workflow
- **Streamlit mentioned** → Suggests Streamlit Testing Workflow
- **PSO issues** → Suggests Performance Analysis

### Session Continuity

Workflows integrate with `.claude/session_continuity.md` for seamless cross-session debugging.

## Playwright MCP Integration

### Installation

```bash
# Install Playwright browsers
npm run playwright:install

# Or directly
npx playwright install
```

### Usage with Streamlit

```bash
# 1. Start Streamlit dashboard
streamlit run streamlit_app.py

# 2. In Claude Code, use Playwright MCP
/test-browser

# 3. Example requests:
- "Screenshot Streamlit dashboard at localhost:8501"
- "Test classical SMC simulation workflow"
- "Verify all plots render without errors"
- "Measure dashboard load time"
```

### Playwright Capabilities

- ✅ Screenshot capture (full page, specific elements)
- ✅ UI interaction (clicks, form filling, navigation)
- ✅ Performance monitoring (load times, rendering speed)
- ✅ Visual regression testing
- ✅ Console error detection
- ✅ Network request monitoring
- ✅ Mobile/tablet viewport testing

## Troubleshooting

### MCP Server Not Available

```bash
# Check installed MCP servers
npm list -g

# Install missing server
npx @modelcontextprotocol/server-playwright
```

### Playwright Installation Issues

```bash
# Manually install browsers
npx playwright install chromium firefox webkit

# Check installation
npx playwright --version
```

### Workflow Steps Fail

1. Check file paths (use absolute paths)
2. Verify permissions (`.claude/settings.local.json`)
3. Ensure dependencies installed (`pip install -r requirements.txt`)
4. Review error messages in analysis reports

## Contributing to Workflows

### Adding New Workflows

1. Create workflow in `workflows/` directory
2. Follow existing format (phases, tools, validation)
3. Test workflow end-to-end
4. Add to this README
5. Create slash command if appropriate

### Improving Existing Workflows

1. Document pain points encountered
2. Propose improvements with examples
3. Test modifications
4. Update workflow file
5. Commit with detailed message

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-10 | Initial release with 6 workflows, Playwright integration |

## References

- **MCP Documentation:** https://modelcontextprotocol.io/
- **Playwright Docs:** https://playwright.dev/
- **Project Repository:** https://github.com/theSadeQ/dip-smc-pso
- **CLAUDE.md:** Project conventions and standards

---

**Maintainers:** DIP-SMC-PSO Team
**Last Updated:** 2025-10-10
**Status:** ✅ Production Ready
