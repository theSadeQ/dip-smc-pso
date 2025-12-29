# Link Validation Tool

Comprehensive documentation link validator for the DIP SMC PSO project.

## Features

- Validates all link types: markdown, Sphinx directives (`:doc:`, `:ref:`, `toctree`), grid cards, anchors
- Aggressive auto-fix for common issues (.html→.md, case sensitivity, path depth)
- External URL validation with rate limiting
- Interactive orphan file cleanup
- Parallel processing for performance
- ASCII-only output (Windows cp1252 safe)
- Multiple output formats (console, JSON, markdown)

## Quick Start

### Fast Mode (Internal Links Only, ~10 seconds)
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --fast
```

### Full Mode (All Except External URLs, ~30 seconds)
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --full --verbose
```

### External Mode (Includes HTTP Validation, ~3 minutes)
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --external
```

## Auto-Fix Usage

### Preview Fixes (Dry-Run)
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --full --fix --dry-run
```

### Apply Fixes
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --full --fix --apply
```

## Orphan Cleanup

### List Orphaned Files
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --full --no-orphans
```

### Interactive Cleanup
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --full --cleanup-orphans
```

## Output Formats

### JSON Export
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --full --output validation_report.json
```

### Markdown Report (for GitHub)
```python
from validate_docs_links import ReportGenerator
report_md = ReportGenerator.markdown_report(result)
```

## Integration

### Pre-commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python .ai_workspace/dev_tools/validate_docs_links.py --fast --staged-only
```

### CI/CD (GitHub Actions)
```yaml
- name: Validate Documentation Links
  run: python .ai_workspace/dev_tools/validate_docs_links.py --full --fail-fast
```

### Sphinx Linkcheck
```bash
# Validate external URLs using Sphinx
sphinx-build -b linkcheck docs docs/_build/linkcheck

# Combine with custom validator
sphinx-build -M html docs docs/_build && \
  python .ai_workspace/dev_tools/validate_docs_links.py --full
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `--fast` | Fast mode: internal links only (~10s) |
| `--full` | Full mode: all validation except external URLs (~30s) |
| `--external` | External mode: includes HTTP validation (~3min) |
| `--fix` | Enable auto-fix mode |
| `--dry-run` | Preview fixes without applying (requires `--fix`) |
| `--apply` | Apply fixes (requires `--fix`) |
| `--cleanup-orphans` | Interactive orphan file cleanup |
| `--output FILE` | Write JSON report to file |
| `--verbose, -v` | Verbose output with detailed issues |
| `--incremental` | Validate only changed files (git diff) |
| `--no-orphans` | Skip orphan detection |

## Validation Rules

### Link Types Validated

| Link Type | Example | Validation Method |
|-----------|---------|-------------------|
| **Markdown** | `[text](file.md)` | File existence + path resolution |
| **Anchors** | `[text](#heading)` | Heading extraction + anchor matching |
| **Sphinx :doc:** | `{doc}\`path\`` | File lookup with .md extension |
| **Sphinx :ref:** | `{ref}\`label\`` | Partial (complex label parsing) |
| **Toctree** | ` ```{toctree}` | Path validation + glob expansion |
| **Grid Cards** | `:::{grid-item-card} :link:` | Target file existence |
| **External URLs** | `https://...` | HTTP HEAD/GET requests |

### Auto-Fix Patterns

| Issue | Detection | Fix | Confidence |
|-------|-----------|-----|------------|
| `.md` vs `.html` | Link ends with `.html` | Replace with `.md` | 95% |
| Case sensitivity | `README.md` vs `readme.md` | Match filesystem case | 90% |
| Relative path depth | `../../` incorrect | Recalculate depth | 95% |
| Anchor format | Heading exists, anchor wrong | Regenerate anchor | 85% |
| Moved files | File not found | Search git history | 70% |

## Error Categories

| Severity | Category | Exit Code | Description |
|----------|----------|-----------|-------------|
| **CRITICAL** | Broken internal link | 1 | File not found |
| **ERROR** | Invalid anchor | 1 | Anchor doesn't exist in target |
| **WARNING** | External URL failure | 1 | HTTP error or timeout |
| **INFO** | Orphaned file | 0 | File not linked from anywhere |

## Performance

| Mode | Duration | Links Validated | Parallelism |
|------|----------|-----------------|-------------|
| `--fast` | ~10s | ~4,800 internal | 8 threads |
| `--full` | ~30s | ~5,800 all | 8 threads |
| `--external` | ~3min | ~6,000 + HTTP | 5 threads (rate limited) |

## Troubleshooting

### Slow Performance
- Use `--fast` mode for quick checks
- Use `--incremental` for CI (only changed files)
- Reduce `MAX_WORKERS_FILES` in script for lower CPU usage

### False Positives
- Check Sphinx directive syntax (`:doc:\` vs `{doc}\``)
- Verify toctree paths (no `.md` extension needed)
- Exclude URLs with `linkcheck_ignore` in `docs/conf.py`

### External URL Timeouts
- Increase `linkcheck_timeout` in `docs/conf.py`
- Add problematic URLs to `linkcheck_ignore`
- Use `--full` mode to skip external validation

## Examples

### Find All Broken Internal Links
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --fast --verbose | grep CRITICAL
```

### Fix Common Issues Automatically
```bash
# Preview
python .ai_workspace/dev_tools/validate_docs_links.py --full --fix --dry-run

# Apply
python .ai_workspace/dev_tools/validate_docs_links.py --full --fix --apply

# Verify
git diff docs/
```

### Generate JSON Report for Analysis
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --external --output report.json
cat report.json | jq '.summary'
```

### Clean Up Orphaned Files
```bash
python .ai_workspace/dev_tools/validate_docs_links.py --full --cleanup-orphans
# Follow interactive prompts to move/delete orphans
```

## Architecture

```
validate_docs_links.py
├─ LinkExtractor       # Markdown + Sphinx parser
├─ LinkValidator       # Core validation engine
├─ ExternalURLValidator # HTTP validation with retries
├─ AutoFixer           # Aggressive auto-fix engine
├─ OrphanDetector      # Link graph analysis
├─ ReportGenerator     # Console, JSON, Markdown output
└─ DocumentationValidator # Main orchestrator
```

## Configuration

### Sphinx Integration (`docs/conf.py`)
```python
linkcheck_ignore = [r'http://localhost:\d+', ...]
linkcheck_timeout = 15
linkcheck_workers = 8
linkcheck_retries = 2
```

### Script Constants
```python
MAX_WORKERS_FILES = 8   # Parallel file processing
MAX_WORKERS_URLS = 5    # Parallel URL validation
URL_TIMEOUT = 15        # Seconds per URL
URL_RETRIES = 2         # Retry attempts
URL_RATE_LIMIT = 0.1    # Seconds between requests
```

## See Also

- [Documentation Build System](.ai_workspace/config/documentation_build_system.md)
- [Workspace Organization](.ai_workspace/config/workspace_organization.md)
- [Navigation System](docs/NAVIGATION.md)
