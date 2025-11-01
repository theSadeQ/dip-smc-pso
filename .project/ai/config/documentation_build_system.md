# Documentation Build System

**MANDATORY FOR CLAUDE**: After ANY changes to documentation source files or static assets, you MUST rebuild the HTML documentation and verify changes are live.

---

## 1) Auto-Rebuild Triggers

**Rebuild Required When Modifying:**
- Sphinx source files: `docs/*.md`, `docs/**/*.rst`
- Static assets: `docs/_static/*.css`, `docs/_static/*.js`, `docs/_static/*.png`
- Configuration: `docs/conf.py`, `docs/_templates/*`
- Navigation: `docs/index.rst`, any `toctree` directives

---

## 2) Mandatory Rebuild Workflow

```bash
# 1. Make changes to docs
# 2. ALWAYS rebuild:
sphinx-build -M html docs docs/_build -W --keep-going

# 3. Verify changes copied (timestamps):
stat docs/_static/your-file.css docs/_build/html/_static/your-file.css

# 4. Verify content matches (MD5):
md5sum docs/_static/your-file.css docs/_build/html/_static/your-file.css

# 5. Verify localhost serves new version:
curl -s "http://localhost:9000/_static/your-file.css" | grep "YOUR_CHANGE"
```

---

## 3) Browser Cache Handling

**CRITICAL**: Browsers cache static assets. After rebuild:

```bash
# Verify localhost serves your changes:
curl -s "http://localhost:9000/_static/code-collapse.css" | grep "YOUR_UNIQUE_COMMENT"
```

**Always tell user to hard refresh:**
- Chrome/Edge: Ctrl+Shift+R (Win) / Cmd+Shift+R (Mac)
- Firefox: Ctrl+F5 (Win) / Cmd+Shift+R (Mac)

---

## 4) Common Pitfalls

### Don't:
❌ **Don't assume changes are live** - always verify with `curl` or `stat`
❌ **Don't skip rebuild** - Sphinx doesn't auto-rebuild static files
❌ **Don't forget browser cache** - tell user to hard refresh

### Do:
✅ **Do verify timestamps** - `stat` both source and build files
✅ **Do check MD5 sums** - ensure files actually copied
✅ **Do test with curl** - verify localhost serves new content

---

## 5) Example: CSS/JS Changes

```bash
# After editing docs/_static/code-collapse.css:
sphinx-build -M html docs docs/_build -W --keep-going

# Verify copy succeeded:
stat docs/_static/code-collapse.css docs/_build/html/_static/code-collapse.css
md5sum docs/_static/code-collapse.css docs/_build/html/_static/code-collapse.css

# Verify localhost serves new version:
curl -s "http://localhost:9000/_static/code-collapse.css" | grep "CRITICAL FIX"

# Tell user: "Hard refresh browser (Ctrl+Shift+R) to clear cache"
```

---

## 6) Example: Markdown/RST Changes

```bash
# After editing docs/guides/getting-started.md:
sphinx-build -M html docs docs/_build -W --keep-going

# Verify HTML updated:
stat docs/guides/getting-started.md docs/_build/html/guides/getting-started.html
```

---

## See Also:
- `CLAUDE.md` Section 19 - Quick reference
- `docs/README.md` - Documentation structure
- `docs/conf.py` - Sphinx configuration
