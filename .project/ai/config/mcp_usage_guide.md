# Model Context Protocol (MCP) Usage Guide

**See:** `docs/mcp-debugging/README.md` for complete workflows | `.mcp.json` for server configuration

---

## 1) Automatic MCP Usage Rules

**FOR CLAUDE**: These rules are instructions for AI behavior, NOT requirements for user prompts.

**USER NOTE**: You DON'T need to use exact keywords or craft special prompts. Just ask naturally!
- "Where's the adaptive SMC?" → Claude uses context7 + filesystem automatically
- "Check code quality" → Claude uses mcp-analyzer + filesystem automatically
- "Test the dashboard" → Claude uses puppeteer automatically

**MANDATORY FOR CLAUDE**: Claude MUST automatically use MCP servers when these conditions are detected:

### Pandas MCP - Auto-trigger when:
- Analyzing CSV/JSON data files (PSO results, simulation logs)
- Computing statistics (mean, std, confidence intervals)
- Plotting convergence curves or performance metrics
- Keywords: "analyze data", "plot results", "statistical analysis", "convergence"

### Context7 MCP - Auto-trigger when:
- Searching documentation for specific topics
- Finding related code/docs across the project
- Validating cross-references between files
- Keywords: "find", "search docs", "where is", "related to", "references"

### Puppeteer MCP - Auto-trigger when:
- Testing Streamlit dashboard functionality
- Validating UI elements or layouts
- Taking screenshots of dashboard views
- Keywords: "test dashboard", "streamlit UI", "screenshot", "validate interface"

### NumPy MCP - Auto-trigger when:
- Matrix operations (inversion, decomposition, eigenvalues)
- Numerical computations for control theory
- Linear algebra validations
- Keywords: "matrix", "eigenvalue", "numerical", "compute"

### Git MCP - Auto-trigger when:
- Analyzing commit history beyond basic `git log`
- Complex branch operations
- Commit statistics or contributor analysis
- Keywords: "commit history", "branch analysis", "git stats"

### SQLite MCP - Auto-trigger when:
- Querying PSO optimization results database
- Analyzing historical optimization runs
- Generating reports from stored results
- Keywords: "query results", "optimization history", "database"

### Pytest MCP - Auto-trigger when:
- Debugging test failures with detailed traces
- Analyzing test patterns or flaky tests
- Keywords: "test failure", "pytest debug", "why test failed"

### Sequential-Thinking MCP - Auto-trigger when:
- **Planning complex multi-step projects** (CRITICAL - often missed!)
- Debugging complex issues requiring systematic investigation
- Analyzing unclear situations needing step-by-step reasoning
- Cross-referencing multiple files to verify information
- Making decisions with multiple competing factors
- Keywords: "plan", "figure out", "investigate", "verify", "analyze situation", "debug", "systematic", "multi-step"

**Planning Examples** (MUST trigger sequential-thinking):
- "Plan how to complete 17 deferred issues" → systematic breakdown needed
- "Figure out which issues are actually done" → investigation required
- "Verify what remains to be completed" → cross-reference analysis
- "Create execution strategy for Phase X" → multi-factor decision-making
- "Analyze project status and recommend next steps" → systematic evaluation

**Red Flags** (trigger sequential-thinking immediately):
- ❗ "Need to figure out..." → Investigation required
- ❗ "Cross-reference X with Y" → Multi-file systematic analysis
- ❗ "Verify whether..." → Evidence-based reasoning
- ❗ "Plan to..." → Multi-step planning
- ❗ "Unclear status of..." → Systematic investigation needed

---

## 2) Configuration

**All servers enabled:** `.ai/config/settings.local.json` sets `"enableAllProjectMcpServers": true`

**Server definitions:** `.mcp.json` (11 configured servers)

---

## 3) Multi-MCP Collaboration Examples

### Single-MCP Tasks:
```bash
# Context7 only
"Find documentation about sliding mode control"

# Pandas only
"Load and describe optimization_results/latest.csv"
```

### Multi-MCP Workflows (ENCOURAGED):
```bash
# 3-MCP Pipeline: Research → Analysis → Computation
"Search documentation for PSO theory, then analyze convergence data from
optimization_results/pso_run_20250113.csv and compute statistical significance"
→ Triggers: context7 → pandas-mcp → numpy-mcp

# 4-MCP Pipeline: Search → Read → Test → Analyze
"Find the adaptive SMC controller code, inspect its implementation,
test it on the dashboard, and analyze its performance metrics"
→ Triggers: context7 → filesystem → puppeteer → pandas-mcp

# 5-MCP Pipeline: Quality → Lint → History → Fix → Test
"Analyze code quality issues in controllers, trace when they were introduced,
suggest fixes, and validate with pytest"
→ Triggers: mcp-analyzer → git-mcp → filesystem → pytest-mcp → sequential-thinking

# Database + Analysis Pipeline
"Query all PSO runs from the database where convergence < 0.01,
load the corresponding CSV files, and compute confidence intervals"
→ Triggers: sqlite-mcp → filesystem → pandas-mcp → numpy-mcp

# Complete Documentation Pipeline
"Search for all references to chattering mitigation, read the related files,
analyze git blame for authorship, and generate a cross-reference report"
→ Triggers: context7 → filesystem → git-mcp → pandas-mcp
```

---

## 4) Custom Slash Commands with MCP

- `/analyze-logs` → Pandas MCP + SQLite MCP for log analysis
- `/debug-with-mcp` → Multi-server integrated debugging
- `/inspect-server` → MCP Inspector for server testing
- `/analyze-dashboard` → Puppeteer MCP for UI validation
- `/test-browser` → Playwright/Puppeteer for dashboard testing

---

## 5) Development Guidelines

### Adding New MCP Servers:
1. Add server config to `.mcp.json` with clear description
2. Add to `mcp_usage` section with specific use cases
3. Define auto-trigger keywords in this section
4. Document in `docs/mcp-debugging/`
5. Test with relevant workflows

### Auto-trigger Requirements:
- Clear keyword matching (e.g., "analyze data" → pandas-mcp)
- **Multiple servers SHOULD activate simultaneously for complex tasks**
- No user confirmation needed (auto-approved)
- Fallback to manual tools if MCP unavailable

### MCP Collaboration Patterns (MANDATORY):
- **Data Analysis Pipeline**: filesystem → sqlite-mcp → mcp-analyzer
- **Documentation Workflow**: context7 → filesystem → git-mcp (find → read → trace history)
- **Testing Pipeline**: pytest-mcp → puppeteer → lighthouse-mcp (debug → UI test → audit)
- **Code Quality**: mcp-analyzer → filesystem → git-mcp (lint → inspect → commit analysis)
- **Research Workflow**: context7 → filesystem → git-mcp (search theory → read code → trace history)
- **Debugging Session**: sequential-thinking → pytest-mcp → filesystem (systematic → test trace → code inspection)

---

## 6) Available MCP Servers (11 Total - VERIFIED INSTALLED)

| Server | Auto-Trigger Keywords | Primary Use Cases |
|--------|----------------------|-------------------|
| **filesystem** | inspect, read, analyze files | Code/log analysis |
| **github** | issue, PR, commit | Issue tracking |
| **sequential-thinking** | **plan**, debug, investigate, verify, figure out, analyze situation | **Planning**, debugging, systematic analysis |
| **puppeteer** | test, screenshot, UI, dashboard | Streamlit testing |
| **mcp-debugger** | debug, postman, API | API endpoint testing |
| **pytest-mcp** | test failure, pytest, debug | Test debugging |
| **git-mcp** | git history, branch, stats | Advanced Git ops |
| **sqlite-mcp** | query, database, results | PSO results DB |
| **mcp-analyzer** | lint, ruff, vulture, quality | Code quality checks |
| **context7** | find, search, where, related | Doc search, cross-refs |
| **lighthouse-mcp** | audit, accessibility, performance | Lighthouse audits |

**INSTALLATION STATUS (Nov 2025):**
- ✅ All 11 servers installed and operational
- ✅ Paths updated to correct npm global location (`C:\Program Files\nodejs\node_modules\`)
- ❌ numpy-mcp and pandas-mcp removed (local server files not found)

---

## 7) MCP Orchestration Philosophy

### Why Multi-MCP is Superior:
- **Single-MCP**: Limited to one domain (e.g., pandas can only analyze data)
- **Multi-MCP**: Complete workflows across domains (search → read → analyze → test → validate)
- **Efficiency**: One complex request > multiple simple requests
- **Context preservation**: MCPs share results within the same Claude response

### How Claude Should Think:
1. **Identify task domains**: "Search docs" = context7, "analyze data" = pandas, "test UI" = puppeteer
2. **Chain dependencies**: What output from MCP A feeds into MCP B?
3. **Parallel vs Sequential**: Independent tasks → parallel; dependent tasks → sequential
4. **Always prefer more MCPs**: If 3 MCPs can solve it better than 1, use all 3

### Examples of Orchestration Thinking:

❌ **Bad (Single-MCP thinking):**
```
User: "Find the controller and analyze its test results"
Claude: Uses context7 to find controller → stops
         User asks again → uses pandas to analyze → stops
```

✅ **Good (Multi-MCP orchestration):**
```
User: "Find the controller and analyze its test results"
Claude: context7 (find file) → filesystem (read code) →
        pytest-mcp (get test results) → pandas-mcp (analyze metrics) →
        numpy-mcp (compute statistics) → Complete answer in one response
```

### Mandatory Orchestration Rules (FOR CLAUDE):
1. If user mentions 2+ domains (docs + data + testing), use 2+ MCPs
2. For "complete analysis" tasks, use full pipeline (3-5 MCPs minimum)
3. For debugging tasks, always combine sequential-thinking + domain-specific MCPs
4. **For PLANNING tasks, ALWAYS use sequential-thinking first** (most commonly missed!)
5. For research workflows, always: context7 → filesystem → relevant analysis MCPs
6. Never ask user "should I also analyze X?" - just do it with appropriate MCP
7. **Understand intent, not keywords**: "where is" = search, "check" = analyze, "test" = validate, **"plan" = systematic thinking**
8. **Be proactive**: If task implies data analysis, use pandas even if not explicitly requested
9. **Chain automatically**: Don't wait for user to ask for next step, complete the full workflow

---

## 8) Natural Language Flexibility (For Users)

**You can ask in ANY of these ways - all work the same:**

| Your Natural Request | What Claude Understands | MCPs Used |
|---------------------|------------------------|-----------|
| "Where's the code for X?" | Search + Read | context7 → filesystem |
| "Show me X" | Search + Read | context7 → filesystem |
| "Find X implementation" | Search + Read | context7 → filesystem |
| "I need to see X" | Search + Read | context7 → filesystem |
| **All trigger same MCPs** | ↑ | ↑ |
|  |  |  |
| "Is this CSV any good?" | Load + Analyze | pandas-mcp → numpy-mcp |
| "Check this data file" | Load + Analyze | pandas-mcp → numpy-mcp |
| "What's in this optimization result?" | Load + Analyze | pandas-mcp → numpy-mcp |
| "Analyze these numbers" | Load + Analyze | pandas-mcp → numpy-mcp |
| **All trigger same MCPs** | ↑ | ↑ |
|  |  |  |
| "Does the UI work?" | Test Interface | puppeteer |
| "Test the dashboard" | Test Interface | puppeteer |
| "Check if page loads" | Test Interface | puppeteer |
| "Screenshot the app" | Test Interface | puppeteer |
| **All trigger same MCPs** | ↑ | ↑ |

### The Point:
Speak naturally! Claude figures out intent → picks right MCPs → chains them intelligently.

### DON'T STRESS ABOUT:
- Exact keywords ("analyze" vs "check" vs "look at")
- MCP names (never say "use pandas-mcp")
- Prompt structure (questions, commands, descriptions all work)
- Triggering tools (Claude does this automatically)

### JUST ASK NATURALLY:
- "What's wrong with this controller?" (triggers: filesystem → pytest-mcp → sequential-thinking)
- "Check code quality in controllers" (triggers: mcp-analyzer → filesystem)
- "Find docs about PSO and show me the code" (triggers: context7 → filesystem)

---

## 9) Troubleshooting

### Server won't start:
```bash
# Verify configuration
cat .mcp.json | grep -A5 "server-name"

# Check if npx/node available
npx --version

# Check Python servers
python -m pip list | grep mcp
```

### See Also:
- `docs/mcp-debugging/QUICK_REFERENCE.md` - Quick troubleshooting
- `docs/mcp-debugging/workflows/` - Complete workflows
- `.mcp.json` - Full server configuration
- `CLAUDE.md` Section 20 - Quick reference
