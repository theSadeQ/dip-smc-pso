#!/usr/bin/env python
"""
Generate all episode customization files for NotebookLM
Creates podcast_customization.md and presentation_customization.md for all 44 episodes
"""

import os
from pathlib import Path

# Episode metadata
EPISODES = {
    "phase1": [
        ("episode01", "Your Computer as a Filing Cabinet", "DONE"),  # Already exists
        ("episode02", "Your First Python Program", "TODO"),
        ("episode03", "Control Flow and Loops", "TODO"),
        ("episode04", "Functions and Reusability", "TODO"),
        ("episode05", "Lists and Dictionaries", "TODO"),
        ("episode06", "NumPy and Matplotlib Basics", "TODO"),
        ("episode07", "Virtual Environments and Git", "TODO"),
        ("episode08", "Newton's Laws and Pendulum Physics", "TODO"),
        ("episode09", "Double-Inverted Pendulum and Stability", "TODO"),
        ("episode10", "Functions, Graphing, and Trigonometry", "TODO"),
        ("episode11", "Derivatives and Differential Equations", "TODO"),
    ],
    "phase2": [
        ("episode01", "Control Systems Everywhere", "TODO"),
        ("episode02", "Open-Loop vs Closed-Loop Control", "TODO"),
        ("episode03", "PID Control Fundamentals", "TODO"),
        ("episode04", "Why PID Fails for DIP", "TODO"),
        ("episode05", "The Sliding Surface Concept", "TODO"),
        ("episode06", "Control Law and Chattering", "TODO"),
        ("episode07", "SMC Variants", "TODO"),
        ("episode08", "Manual Tuning Nightmare", "TODO"),
        ("episode09", "PSO Algorithm", "TODO"),
        ("episode10", "DIP System Structure", "TODO"),
        ("episode11", "Why DIP Is Hard", "TODO"),
        ("episode12", "System Dynamics and Control Objectives", "DONE"),  # Just created
    ],
    "phase3": [
        ("episode01", "Environment Setup", "TODO"),
        ("episode02", "The First Simulation", "TODO"),
        ("episode03", "Controller Showdown", "TODO"),
        ("episode04", "Performance Metrics Deep Dive", "TODO"),
        ("episode05", "Config Modification", "TODO"),
        ("episode06", "PSO Optimization", "TODO"),
        ("episode07", "Troubleshooting Guide", "TODO"),
        ("episode08", "Phase 3 Complete", "TODO"),
    ],
    "phase4": [
        ("episode01", "Welcome to Advanced Skills", "TODO"),
        ("episode02", "OOP Foundations", "TODO"),
        ("episode03", "Inheritance in Controller Design", "TODO"),
        ("episode04", "Decorators and Type Hints", "TODO"),
        ("episode05", "Testing with pytest", "TODO"),
        ("episode06", "Navigating the Codebase", "TODO"),
        ("episode07", "Classical SMC - Imports and Initialization", "TODO"),
        ("episode08", "Classical SMC - Control Law Implementation", "TODO"),
        ("episode09", "Classical SMC - Math Breakdown", "TODO"),
        ("episode10", "Controller Comparison", "TODO"),
        ("episode11", "Lagrangian Mechanics", "TODO"),
        ("episode12", "Vector Calculus for Control", "TODO"),
        ("episode13", "Lyapunov Stability and Phase Space", "TODO"),
    ],
}

BASE_DIR = Path(__file__).parent


def create_podcast_customization(phase, episode_num, episode_title):
    """Create podcast customization markdown file"""

    content = f"""# {phase.title()} {episode_num.title()}: {episode_title}
## Ultra-Detailed Podcast Customization

**Episode**: {phase.title()}, {episode_num.title()}
**Topic**: {episode_title}
**Duration Target**: 30-45 minutes
**Format**: Deep Dive | Length: Long

---

## PASTE THIS ENTIRE PROMPT INTO NOTEBOOKLM

```
Create an ultra-detailed, comprehensive discussion covering every aspect of {episode_title}.

[CUSTOMIZE THIS SECTION WITH EPISODE-SPECIFIC CONTENT]

START with motivation and real-world context explaining WHY {episode_title} matters. Provide 2-3 paragraphs with concrete examples, real-world applications, what problem this topic solves.

INTRODUCE core concept with extended analogy relating {episode_title} to physical/everyday experience. Explore the analogy from multiple angles (3-4 paragraphs) making the abstract concept tangible.

EXPLAIN fundamental theory exhaustively. Break down the concept into smallest possible pieces, define every term, show mathematical foundations if applicable, trace execution step-by-step, provide multiple representations (verbal, visual description, code examples).

DEMONSTRATE with 3-5 complete worked examples showing the concept in action. Trace execution line by line, show inputs and outputs, explain what's happening at each step.

SHOW variations and edge cases. Cover different scenarios, parameter variations, boundary conditions, special cases, what happens when things go wrong.

CONNECT to control systems context. Explain specific applications in DIP-SMC-PSO project, how this concept appears in simulation code, why it's essential for control engineering.

ADDRESS common mistakes exhaustively. List 5-10 typical beginner errors, why they happen, exact error messages, how to recognize them, step-by-step solutions.

PROVIDE practice exercises. Give 5+ exercises progressing from simple to complex, with hints about expected results.

TROUBLESHOOT potential issues. Cover platform differences (Windows/Mac/Linux), installation problems, version conflicts, debugging strategies.

END with synthesis and preview. Summarize key takeaways in 2-3 paragraphs, connect to previous episodes, preview how this builds toward next topics, emphasize mastery progression and confidence building.
```

---

## USAGE INSTRUCTIONS

1. **Open NotebookLM** at https://notebooklm.google.com
2. **Upload**: `{phase}_{episode_num}.md`
3. **Click "Generate Audio Overview"**
4. **Click "Customize"**
5. **Copy entire prompt above**
6. **Paste into text box**
7. **Format: "Deep Dive" | Length: "Long"**
8. **Generate**
9. **Wait 3-5 minutes** for 30-45 min podcast

---

## EXPECTED OUTPUT

- **Duration**: 30-45 minutes of detailed discussion
- **Depth**: Every concept explained with multiple analogies
- **Examples**: 5-10 concrete examples throughout
- **Platforms**: Windows, Mac, Linux covered where applicable
- **Common mistakes**: 5-10 pitfalls with solutions
- **Practice**: Exercises provided at end
- **Connections**: Links to programming/control context

---

**File**: `episode_guides/{phase}/{episode_num}/podcast_customization.md`
**Created**: November 2025
**Status**: Template - Customize with episode-specific content
**Project**: DIP-SMC-PSO Educational Materials
"""

    return content


def create_presentation_customization(phase, episode_num, episode_title):
    """Create presentation document customization markdown file"""

    content = f"""# {phase.title()} {episode_num.title()}: {episode_title}
## Ultra-Detailed Presentation Document Customization

**Episode**: {phase.title()}, {episode_num.title()}
**Topic**: {episode_title}
**Document Type**: Study Guide / Briefing Doc / Cheat Sheet

---

## FOR STUDY GUIDE: PASTE THIS PROMPT

```
Create exhaustive study guide for {episode_title} that serves as complete standalone learning material. This should be textbook-quality content suitable for deep study, review, and reference.

## LEARNING OBJECTIVES
By completing this study guide, you will be able to:
1. [Objective 1 - specific, measurable learning outcome for {episode_title}]
2. [Objective 2 - another measurable outcome]
3. [Objective 3 - another outcome]
4. [Objective 4 - another outcome]
5. [Objective 5 - another outcome]
6. [Objective 6 - another outcome]
7. [Objective 7 - another outcome]
8. [Objective 8 - another outcome]
9. [Objective 9 - another outcome]
10. [Objective 10 - another outcome]

## PREREQUISITE KNOWLEDGE CHECK
**What You Should Already Know**:
- [Prerequisite 1]
- [Prerequisite 2]
- [Prerequisite 3]
- [Prerequisite 4]
- [Prerequisite 5]

**Self-Assessment Quiz** (2 minutes):
1. Q: [Question 1]? A: [Answer 1]
2. Q: [Question 2]? A: [Answer 2]
3. Q: [Question 3]? A: [Answer 3]
4. Q: [Question 4]? A: [Answer 4]
5. Q: [Question 5]? A: [Answer 5]

## CONCEPT MAP
```
[Main Concept: {episode_title}]
├─ [Sub-concept 1]
│   ├─ [Detail A]
│   ├─ [Detail B]
│   └─ [Detail C]
├─ [Sub-concept 2]
│   ├─ [Detail D]
│   └─ [Detail E]
└─ [Sub-concept 3]
    ├─ [Detail F]
    └─ [Detail G]
```

## CORE CONTENT

### Section 1: Introduction and Motivation
[3-4 paragraphs explaining WHY {episode_title} matters, real-world applications, historical context]

### Section 2: Fundamental Theory
[Exhaustive explanation breaking down concept layer by layer, defining every term, showing mathematical foundations, providing multiple analogies]

### Section 3: Detailed Examples (5-7 Complete Examples)
**Example 1: [Scenario Name]**
- Setup: [What we're trying to accomplish]
- Given: [Initial conditions, parameters]
- Process: [Step-by-step walkthrough]
- Result: [Output with interpretation]
- Variations: [What if we change X?]
- Common Errors: [Mistakes here and how to fix]

[Repeat for Examples 2-7]

### Section 4: Edge Cases and Special Scenarios
[Boundary conditions, empty inputs, max/min values, error conditions, platform differences]

### Section 5: Practical Applications in Control Systems
[Specific uses in DIP-SMC-PSO project, code snippets, how concept appears in simulations]

### Section 6: Worked Problems (10-15 Problems with Full Solutions)
**Easy (Problems 1-5)**:
[Simple, direct applications, one concept at a time, full solutions]

**Medium (Problems 6-10)**:
[Combine 2-3 concepts, require reasoning, multiple solution approaches]

**Hard (Problems 11-15)**:
[Complex, multi-step, integrate many concepts, common mistake analysis]

### Section 7: Common Mistakes Encyclopedia (15-20 Mistakes)
[Each mistake: description, why it happens, symptoms, diagnosis, solution, prevention]

### Section 8: Quick Reference
[Command syntax table, function signatures, formulas, decision trees, troubleshooting flowchart]

### Section 9: Self-Assessment Test
[20 multiple choice (5 easy, 10 medium, 5 hard), 5 short answer, 2 coding challenges, answer key, scoring rubric]

### Section 10: Further Exploration
[Advanced topics, related episodes, external resources, practice projects]

### Section 11: Summary and Key Takeaways
[One-page executive summary, top 10 key points, concept checklist, connections to other topics]

TARGET: 5000-8000 words, no concept unexplained, every example fully worked, all edge cases covered.
```

---

## FOR BRIEFING DOCUMENT: USE THIS PROMPT

```
Create executive-level technical briefing on {episode_title} suitable for engineering managers or researchers.

Structure: Executive Summary (1 page) → Situation Analysis (2-3 pages) → Technical Deep Dive (5-7 pages) → Practical Applications (3-4 pages) → Risk Analysis (1-2 pages) → Recommendations (1 page) → Appendices

TARGET: 3000-5000 words, professional tone, data-driven, actionable recommendations.
```

---

## FOR CHEAT SHEET: USE THIS PROMPT

```
Create ultra-comprehensive reference cheat sheet for {episode_title} - densely packed 20-30 pages when printed.

Include: One-page quick reference, comprehensive command/function reference, syntax patterns, comparison tables, troubleshooting flowcharts, best practices checklist, code snippets library, quick glossary, platform differences matrix, error message decoder.

TARGET: Maximum information density, organized for quick lookup, printer-friendly.
```

---

## USAGE INSTRUCTIONS

1. **Choose document type**: Study Guide, Briefing, or Cheat Sheet
2. **Open NotebookLM**
3. **Upload episode markdown**
4. **Use document generation feature**
5. **Paste appropriate prompt**
6. **Generate written output**
7. **Export to PDF**

---

**File**: `episode_guides/{phase}/{episode_num}/presentation_customization.md`
**Created**: November 2025
**Status**: Template - Customize with episode-specific content
**Project**: DIP-SMC-PSO Educational Materials
"""

    return content


def main():
    """Generate all episode files"""
    print("Generating episode customization files...")
    print("=" * 60)

    total_created = 0
    total_skipped = 0

    for phase, episodes in EPISODES.items():
        print(f"\n{phase.upper()}:")
        for episode_num, episode_title, status in episodes:
            episode_dir = BASE_DIR / phase / episode_num

            podcast_file = episode_dir / "podcast_customization.md"
            presentation_file = episode_dir / "presentation_customization.md"

            if status == "DONE":
                print(f"  [OK] {episode_num}: {episode_title} (already exists)")
                total_skipped += 2
                continue

            # Create podcast customization
            if not podcast_file.exists():
                podcast_content = create_podcast_customization(phase, episode_num, episode_title)
                podcast_file.write_text(podcast_content, encoding='utf-8')
                print(f"  [+] Created {phase}/{episode_num}/podcast_customization.md")
                total_created += 1
            else:
                print(f"  [-] {episode_num}/podcast_customization.md already exists")
                total_skipped += 1

            # Create presentation customization
            if not presentation_file.exists():
                presentation_content = create_presentation_customization(phase, episode_num, episode_title)
                presentation_file.write_text(presentation_content, encoding='utf-8')
                print(f"  [+] Created {phase}/{episode_num}/presentation_customization.md")
                total_created += 1
            else:
                print(f"  [-] {episode_num}/presentation_customization.md already exists")
                total_skipped += 1

    print("\n" + "=" * 60)
    print(f"SUMMARY:")
    print(f"  Created: {total_created} files")
    print(f"  Skipped: {total_skipped} files (already exist)")
    print(f"  Total: {total_created + total_skipped} files")
    print("\nDone! All episode folders now have customization files.")
    print("\nIMPORTANT: These are TEMPLATES. Each file has placeholder text marked")
    print("with [CUSTOMIZE THIS SECTION]. Replace with episode-specific content from")
    print("the actual episode markdown files for maximum quality.")


if __name__ == "__main__":
    main()
