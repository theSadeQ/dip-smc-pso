# NotebookLM Podcast Generation Guide

**Purpose**: Convert written educational content into podcast-style audio for commute/exercise learning

**Available Series** (Phases 1-4):
- **Phase 1 - Foundations**: `docs/learning/notebooklm/phase1/` (11 episodes, ~3.5-4 hours audio, 40 hours learning content)
- **Phase 2 - Core Concepts**: `.ai/edu/notebooklm/phase2/` (12 episodes, ~5 hours audio, 30 hours learning content)
- **Phase 3 - Hands-On Learning**: `.ai/edu/notebooklm/phase3/` (8 episodes, ~2.5 hours audio, 25 hours learning content)
- **Phase 4 - Advancing Skills**: `docs/learning/notebooklm/phase4/` (13 episodes, ~12-15 hours audio, 30 hours learning content)

**Series Totals**: 44 episodes, ~40 hours audio, 125 hours learning content

**Status**: [OK] Series complete at Phase 4 (November 2025)

**Phase 5 Note**: Phase 5 (Mastery Path) is NOT included in the podcast series because it uses a branching "choose-your-own-adventure" structure with interactive decision trees, which is incompatible with linear podcast format. Phase 5 remains available as written documentation: `.ai/edu/beginner-roadmap.md` (Phase 5 section).

## What Is NotebookLM?

Google's AI-powered tool that generates podcast-style audio discussions from documents:
- Upload markdown files to [notebooklm.google.com](https://notebooklm.google.com)
- Click "Generate Audio Overview" button
- AI creates 20-30 minute conversational podcast with two hosts
- Technical terms pronounced correctly via TTS optimization

## Quick Start (for Claude)

When user requests podcast generation for educational content:

**1. Identify Source Content**: Which phase/topic needs podcast optimization?
**2. Create Episode Structure**: Break content into 2-2.5 hour chunks (20-30 min audio each)
**3. Apply TTS Optimization**: Use enhanced narrative style + verbalized equations
**4. Generate Episodes**: Create separate markdown files per episode
**5. Create README**: Usage instructions for NotebookLM upload

## TTS Optimization Requirements (MANDATORY)

**Mathematical Expressions - Verbalized Format**:
```
NOT: u = -K·sign(s)
BUT: u equals negative K times sign of s

NOT: s = k₁·θ₁ + k₂·θ̇₁
BUT: s equals k-one times theta-one plus k-two times theta-one-dot
```

**Greek Letters - Spelled Out**:
```
θ -> "theta"
ε -> "epsilon"
λ -> "lambda"
Δ -> "delta"
ω -> "omega"
```

**Mathematical Notation - Verbal Equivalents**:
```
θ̇ -> "theta-dot" (time derivative)
θ̂ -> "theta-hat" (estimate)
∫ -> "integral of"
∂ -> "partial derivative of"
≈ -> "approximately equals"
≤ -> "less than or equal to"
```

**Code Examples - Narrated Format**:
```markdown
Let's see this concept in action with a Python simulation.
First, we import NumPy for numerical operations...

[CODE BLOCK]
import numpy as np
...
[/CODE BLOCK]

Walking through the main loop: For each time step,
we calculate the error as setpoint minus current position...
```

**Diagrams - Verbal Descriptions**:
```markdown
Picture a flowchart with four boxes connected by arrows.
Starting at the top, we have the setpoint. An arrow flows down...
```

## Enhanced Narrative Style Guidelines

**Conversational Framing**:
- Start with relatable scenario or question
- Use "imagine", "picture this", "let's think about"
- Progressive revelation (build complexity gradually)

**Analogy-First Approach**:
- Begin major concepts with physical analogies
- Transition to technical explanation
- Connect back to analogy for reinforcement

**Retention Techniques**:
- Recap every 5-7 minutes of content
- Callbacks to previous episodes
- "Pause and reflect" sections
- Preview of next episode

**Question-Driven Narrative**:
- Pose questions learners would ask
- Answer with examples first, then formalism
- "Now you might be wondering..." transitions

## Episode Structure Template

```markdown
# Episode N: [Catchy Title]

**Duration**: 20-30 minutes | **Learning Time**: 2-2.5 hours | **Difficulty**: [Level]

## Opening Hook
[Relatable scenario that introduces the concept]

## What You'll Discover
[Bullet list of key takeaways]

## [Section 1]: [Main Content]
[Enhanced narrative with analogies, examples, TTS-optimized equations]

## [Section 2]: [Code/Visualization]
[Narrated walkthrough with verbal descriptions]

## Key Takeaways
[Numbered recap of essential insights]

## Pronunciation Guide
[Technical terms with phonetic spellings]

## What's Next
[Preview of next episode]

## Pause and Reflect
[Questions to consider before continuing]

---

**Episode N of M** | [Phase/Topic]

**Previous**: [Link] | **Next**: [Link]
```

## Phase 2 Example (Reference Implementation)

**Location**: `.ai/edu/notebooklm/phase2/`

**Structure**:
- 12 episodes covering Control Theory, SMC, Optimization, DIP System
- Episodes 1-2: Control theory fundamentals
- Episodes 3-4: PID control and limitations
- Episodes 5-7: Sliding Mode Control trilogy
- Episodes 8-9: Optimization and PSO
- Episodes 10-12: DIP system understanding

**Key Files**:
- `phase2_episode01.md` through `phase2_episode12.md`: Individual episodes
- `README.md`: Complete usage guide for NotebookLM

**Total Output**: ~150 KB markdown, generates ~5 hours podcast audio

## Phase 3 Example (Reference Implementation)

**Location**: `.ai/edu/notebooklm/phase3/`

**Structure**:
- 8 episodes covering Hands-On Learning, Simulations, Controller Comparison
- Episodes 1-2: Environment setup, first simulation, plot interpretation
- Episodes 3-4: Controller comparison, performance metrics
- Episodes 5-6: Config modification, PSO optimization
- Episodes 7-8: Troubleshooting, phase wrap-up

**Key Features**:
- Rich verbal descriptions of 6 simulation plots (multi-pass: sketch → story → meaning)
- Commands spelled out phonetically ("dash dash ctrl classical underscore s-m-c")
- YAML hierarchy verbalized for configuration edits
- "Tour guide + sports commentary" style for live plot narration

**Key Files**:
- `phase3_episode01.md` through `phase3_episode08.md`: Individual episodes
- `README.md`: Complete usage guide for NotebookLM

**Total Output**: ~85 KB markdown, generates ~2.5 hours podcast audio

**Key Difference from Phase 2**: Focuses on hands-on workflows and plot interpretation rather than theory

## Phase 1 Example (Reference Implementation)

**Location**: `docs/learning/notebooklm/phase1/`

**Structure**:
- 11 episodes covering Computing Basics, Python, Environment Setup, Physics, Math
- Episodes 1-2: File systems, command line, Python installation, variables (40-44 min)
- Episodes 3-6: Control flow, functions, lists/dicts, NumPy/Matplotlib (80-88 min)
- Episode 7: Virtual environments, Git, DIP-SMC-PSO project setup (22-25 min)
- Episodes 8-9: Newton's laws, pendulums, double-inverted pendulum system (40-45 min)
- Episodes 10-11: Functions, trigonometry, derivatives, differential equations (38-42 min)

**Key Features**:
- Complete beginner focus (ZERO prior knowledge assumed)
- Multi-platform commands (Windows, Mac, Linux variations)
- Commands spelled phonetically ("pip install" → "p-i-p space install")
- Code narration with indentation cues ("Four spaces indent, then type...")
- Error message pronunciation and diagnosis
- Physical analogies before formalism (filing cabinet → file systems)

**Key Files**:
- `phase1_episode01.md` through `phase1_episode11.md`: Individual episodes
- `README.md`: Complete usage guide for NotebookLM

**Total Output**: ~34,800 words, generates ~3.5-4 hours podcast audio

**Key Difference from Phases 2-3**: Entry point for absolute beginners, covers programming and computing fundamentals before control theory

## Phase 4 Example (Reference Implementation)

**Location**: `docs/learning/notebooklm/phase4/`

**Structure**:
- 13 episodes covering Advanced Python, Source Code Reading, Advanced Math
- Episodes 1-5: OOP, inheritance, decorators, type hints, testing (12 hours → ~6 hours audio)
- Episodes 6-10: Codebase navigation, Classical SMC line-by-line walkthrough, controller comparison (8 hours → ~4 hours audio)
- Episodes 11-13: Lagrangian mechanics, vector calculus, Lyapunov stability, phase space (10 hours → ~5 hours audio)

**Key Features**:
- Mindset shift: user → developer (transparent box, code literacy)
- Python OOP: Abstract base classes, inheritance, decorators, type hints verbalized
- Code walkthroughs: Line-by-line narration of classical_smc.py with phonetic syntax
- Advanced math: Lagrangian L = T - V, mass matrix M(θ), Lyapunov V̇ < 0
- Prerequisites: Phases 1-3 completion (60 hours) required
- TTS optimization: `__init__` → "dunder init", θ̇ → "theta-dot", ∇V → "del V"

**Key Files**:
- `phase4_episode01.md` through `phase4_episode13.md`: Individual episodes
- `README.md`: Complete usage guide for NotebookLM with Phase 4-specific instructions

**Total Output**: ~29,000 words, generates ~12-15 hours podcast audio

**Key Difference from Phases 1-3**: Advanced learners only, opens black box to understand controller internals, mathematical rigor

## Validation Checklist (Per Episode)

Before finalizing any NotebookLM episode:

- [ ] **Length**: 2,500-3,500 words (~130-150 lines)
- [ ] **TTS Optimization**: All equations verbalized phonetically
- [ ] **Greek Letters**: Spelled out on first use
- [ ] **Code Examples**: Narrated with context
- [ ] **Diagrams**: Verbally described in detail
- [ ] **Analogies**: At least 2 physical examples per episode
- [ ] **Retention**: Recap section every 700-1,000 words
- [ ] **Callbacks**: Reference to previous episodes (Episodes 2+)
- [ ] **Preview**: Teaser for next episode at end
- [ ] **Technical Accuracy**: All formulas verified
- [ ] **Pronunciation Guide**: Included for technical terms
- [ ] **Self-Contained**: Understandable independently

## User Workflow

**For Listeners**:
1. Visit [notebooklm.google.com](https://notebooklm.google.com), create notebook
2. Upload episode markdown files (one or multiple)
3. Click "Generate Audio Overview"
4. Listen during commute/exercise (20-30 min per episode)
5. Read detailed roadmap for exercises and deeper understanding

**For Content Creators (Claude)**:
1. Identify educational content needing audio format
2. Generate TTS-optimized episodes using guidelines above
3. Create README with NotebookLM usage instructions
4. Test by uploading to NotebookLM and verifying audio quality
5. Update CLAUDE.md section 6.4 with new content location

## Success Metrics

Podcast content is successful when:
- Users can follow along by audio alone (no visual needed)
- Technical terms pronounced correctly by TTS
- Concepts build progressively without confusion
- Listeners can explain key ideas after one listen
- Retention matches or exceeds reading comprehension

**See Also**:
- Phase 1 usage guide: `docs/learning/notebooklm/phase1/README.md`
- Phase 2 usage guide: `.ai/edu/notebooklm/phase2/README.md`
- Phase 3 usage guide: `.ai/edu/notebooklm/phase3/README.md`
- Phase 4 usage guide: `docs/learning/notebooklm/phase4/README.md`
