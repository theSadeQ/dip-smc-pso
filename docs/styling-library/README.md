# Documentation Styling Library This directory contains documentation styling templates and patterns inspired by the **react-bits-library** project, adapted for the DIP-SMC-PSO control systems framework.

##  Directory Structure ```

docs/styling-library/
 README.md (this file)
 templates/ # Reusable documentation templates
 examples/ # Example adaptations for DIP project
 assets/ # Visual assets (badges, logos)
```

---

##  Template Collection ### 1. **quick-start-template.md**
**Purpose:** Create fast onboarding guides (< 5 minutes to productivity) **Key Features:**
- Visual organization with emojis
- "3 Ways to Use" structure
- Popular component quick-reference
- Copy-paste examples **Use For:**
- Controller quick-start guides
- PSO optimization quick-start
- Simulation workflow quick-start ### 2. **cheat-sheet-template.md**
**Purpose:** One-page reference for most-used features **Key Features:**
- Table-based organization
- Use-case driven sections
- Top 20 most useful items
- Common patterns with code snippets **Use For:**
- Controller selection cheat sheet
- PSO parameter tuning cheat sheet
- Configuration reference cheat sheet ### 3. **component-index-template.md**
**Purpose:** catalog of all components/modules **Key Features:**
- Categorical organization
- Complete inventories
- Consistent numbering
- Easy navigation **Use For:**
- Controllers module index
- Analysis tools index
- Utility functions index ### 4. **integration-guide-template.md**
**Purpose:** Step-by-step integration instructions **Key Features:**
- Prerequisites section
- Detailed setup steps
- Configuration examples
- Troubleshooting guide **Use For:**
- PSO integration guide
- HIL system setup guide
- Testing framework integration ### 5. **module-readme-template.md**
**Purpose:** High-level project/module README **Key Features:**
- Badges (stars, license, version)
- Visual hierarchy
- Key features list
- Quick navigation **Use For:**
- Updated main README.md
- Module-level README files
- Subproject documentation

---

##  Usage Guide ### Step 1: Choose Template
Select the template that matches your documentation goal:
- **Learning path** → quick-start-template.md
- **Quick reference** → cheat-sheet-template.md
- **Complete catalog** → component-index-template.md
- **Setup instructions** → integration-guide-template.md
- **Project overview** → module-readme-template.md ### Step 2: Adapt Content
1. Copy template to target location
2. Replace placeholder content with DIP-specific information
3. Adapt examples for control systems domain
4. Update section headers as needed ### Step 3: Apply Styling Patterns
Use these visual patterns from react-bits:
- **Emojis for navigation:**  Controllers,  Analysis,  Utils,  Config
- **Tables for parameters:** Component, Use-Case, Props columns
- **Code blocks with context:** Always show before/after or usage example
- **Progressive disclosure:** Overview → Details → Advanced

---

##  Styling Patterns ### Visual Hierarchy
```markdown
# H1: Page Title (one per document)

## H2: Major Section

### H3: Subsection

#### H4: Detail (rare) **Bold**: Important concepts

`code`: Technical terms, file paths
> Blockquote: Important notes
``` ### Tables
```markdown

| Component | Use Case | Parameters |
|-----------|----------|------------|
| ClassicalSMC | Basic stabilization | gains[], max_force |
``` ### Code Snippets
```markdown

​```python
# example-metadata:

# runnable: false # Context comment

from src.controllers import ClassicalSMC controller = ClassicalSMC(gains=[...]) # Inline explanation
​```
``` ### Lists with Icons
```markdown

 **Completed** - Feature implemented
 **In Progress** - Under development
 **Planned** - Future enhancement
 **Not Supported** - Out of scope
```

---

##  Examples (To Be Created) ### Example 1: Controller Quick Start
**Template:** quick-start-template.md
**Target:** `docs/guides/controllers-quick-start.md` **Adaptation:**
- Replace "115+ animated components" → "7 controller implementations"
- Replace "Text Animations, Backgrounds" → "SMC, MPC, Adaptive Controllers"
- Adapt examples for controller instantiation ### Example 2: PSO Optimization Cheat Sheet
**Template:** cheat-sheet-template.md
**Target:** `docs/guides/pso-cheat-sheet.md` **Adaptation:**
- Table of PSO parameters (swarm_size, iterations, bounds)
- Common patterns (basic optimization, custom cost functions)
- Quick code snippets for tuning workflows ### Example 3: Module Index
**Template:** component-index-template.md
**Target:** `docs/api/module-index.md` **Adaptation:**
- Categorize by module: controllers/, optimization/, analysis/, utils/
- List all Python files in each category
- Include brief descriptions (1-2 sentences)

---

##  Visual Asset Guidelines ### Badges
Store in `assets/badges/`:
- **License badge**: MIT license indicator
- **Build status**: CI/CD status
- **Coverage badge**: Test coverage percentage
- **Version badge**: Current release version ### Logos
- Project logo (light/dark variants)
- Controller type icons (SMC, MPC, Adaptive)

---

##  Documentation Standards ### Writing Style
1. **Conversational tone**: "You can..." not "One can..."
2. **Active voice**: "Run the simulation" not "The simulation should be run"
3. **Present tense**: "The controller computes" not "The controller will compute"
4. **Concrete examples**: Always show working code ### Cross-References
```markdown

See [Controller Factory](../controllers/factory-system-guide.md) for details.
``` ### Code-to-Docs Traceability
```markdown

Implemented in `src/controllers/classical_smc.py:45-67`
```

---

##  Resources **Inspiration:**
- [react-bits-library](https://github.com/davidhdev/react-bits) - Original styling source
- [reactbits.dev](https://reactbits.dev/) - Live documentation example **DIP Project Docs:**
- [Documentation Plan](../plans/documentation/README.md) - Overall documentation roadmap
- [Week 7 Plan](../plans/documentation/week_7_architecture_diagrams.md) - Visual documentation plans

---

##  Maintenance **When to Update:**
- Adding new controllers/modules → Update component-index
- New user workflows → Create quick-start guide
- Common questions → Add to cheat-sheet **Quality Checklist:**
- [ ] Visual hierarchy clear (H1/H2/H3 used correctly)
- [ ] Tables formatted consistently
- [ ] Code examples tested and working
- [ ] Cross-references valid
- [ ] Emojis used sparingly (navigation only)

---

**Created:** 2025-10-06
**Purpose:** Future Week 7 documentation beautification
**Status:** Template library ready for use
