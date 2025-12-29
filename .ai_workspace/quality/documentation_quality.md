# Documentation Quality Standards

## Overview

All project documentation must meet professional writing standards that sound human-written, not AI-generated. Following a comprehensive audit in October 2025 (784 files, 308,853 lines), this section documents quality requirements and anti-patterns to avoid.

**Official Style Guide:** `docs/DOCUMENTATION_STYLE_GUIDE.md`

## Core Writing Principles

1. **Direct, not conversational** - Get to the point immediately
2. **Specific, not generic** - Show concrete features, not abstract claims
3. **Technical, not marketing** - Facts over enthusiasm
4. **Show, don't tell** - Concrete examples over buzzwords
5. **Cite, don't hype** - References over marketing language

## Anti-Patterns (AVOID)

### Greeting & Conversational Language

❌ **DO NOT USE:**
- "Let's explore...", "Let us examine..."
- "Welcome! You'll love..."
- "In this section we will..."
- "Now let's look at..."

✅ **USE INSTEAD:**
- Direct topic sentence: "The PSO optimizer minimizes..."
- "This section covers..."
- "The following demonstrates..."

### Enthusiasm & Marketing Buzzwords

❌ **DO NOT USE:**
- "comprehensive framework" (unless backed by metrics)
- "powerful capabilities"
- "seamless integration"
- "cutting-edge algorithms" (without citations)
- "state-of-the-art" (without citations)
- "robust implementation" (use specific reliability features)

✅ **USE INSTEAD:**
- "framework" (let features speak)
- List specific capabilities
- "integration" (describe, don't hype)
- "PSO optimization (Kennedy & Eberhart, 1995)"
- "Achieves 30% faster convergence vs baseline"
- "Handles edge cases A, B, C"

### Hedge Words

❌ **DO NOT USE:**
- "leverage the power of" → ✅ "use"
- "utilize the optimizer" → ✅ "use the optimizer"
- "delve into the details" → ✅ "examine", "analyze"
- "facilitate testing" → ✅ "enables testing" or be specific

### Unnecessary Transitions

❌ **DO NOT USE:**
- "As we can see..." (redundant)
- "It's worth noting that..." (remove or integrate)
- "Additionally, it should be mentioned..." (verbose)
- "Furthermore, we observe that..." (simplify)

✅ **USE INSTEAD:**
- Remove entirely or state directly
- "The results show..."
- "Additionally," (shorter)
- "The data shows..."

## Context-Aware Exceptions

**When Technical Terms Are Acceptable:**

These terms are acceptable when used in proper technical context:

- **"robust control"** - Formal control theory term (H∞ robustness, μ-synthesis)
- **"comprehensive test coverage: 95%"** - Backed by metrics
- **"enable logging"** - Software configuration terminology
- **"advanced MPC"** - Distinguishing from basic variants

**Rule:** If it has a precise technical definition, it's acceptable. If it's marketing fluff, remove it.

**When "Let's" Is Acceptable:**

In interactive tutorial contexts (Jupyter notebooks, live demos):

```python
# Interactive Jupyter notebook cell
# Let's run a quick simulation to see the controller response
result = simulate(controller, duration=5.0)
plot(result)
```

This mirrors natural teaching flow in interactive environments.

## Validation Workflow

### Before Committing Documentation

Run pattern detection:
```bash
python scripts/docs/detect_ai_patterns.py --file path/to/file.md
```

**Pre-Commit Checklist:**
- [ ] No greeting language ("Let's", "Welcome")
- [ ] No marketing buzzwords ("seamless", "cutting-edge", "revolutionary")
- [ ] No hedge words ("leverage", "utilize", "delve into")
- [ ] No unnecessary transitions ("As we can see")
- [ ] Direct, factual statements
- [ ] Specific examples over generic claims
- [ ] Active voice (except for technical accuracy)
- [ ] Citations for advanced claims
- [ ] Quantified performance claims
- [ ] Technical terms used correctly (not as filler)

**Acceptance Criteria:**
- Pattern scan passes (<5 AI-ish patterns detected per file)
- Technical accuracy preserved
- Readability maintained or improved

### Automated Quality Checks

**Pattern Detection Tools:**
- `scripts/docs/detect_ai_patterns.py` - Identify AI-ish language
- `scripts/docs/generate_audit_report.py` - Generate audit reports
- `scripts/docs/suggest_fixes.py` - Automated fix suggestions

## References

**Official Documentation:**
- `docs/DOCUMENTATION_STYLE_GUIDE.md` - Professional writing standards
- `academic/docs_audit/AI_PATTERN_AUDIT_REPORT.md` - Full audit results
- `academic/docs_audit/REPLACEMENT_GUIDELINES.md` - Pattern replacements

**Detection Tools:**
- `scripts/docs/detect_ai_patterns.py` - Pattern detection engine
- `scripts/docs/generate_audit_report.py` - Report generator
- `scripts/docs/suggest_fixes.py` - Automated fix suggestions

**Validation Commands:**
```bash
# Detect AI patterns in a file
python scripts/docs/detect_ai_patterns.py --file docs/README.md

# Generate full audit report
python scripts/docs/generate_audit_report.py --input academic/docs_audit/ai_pattern_detection_report.json --output academic/docs_audit/AI_PATTERN_AUDIT_REPORT.md

# Get fix suggestions
python scripts/docs/suggest_fixes.py --file docs/README.md
```
