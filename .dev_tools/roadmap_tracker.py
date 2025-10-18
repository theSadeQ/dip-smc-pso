#!/usr/bin/env python3
"""
Roadmap Tracker - Quick visualization of roadmap progress

Purpose: Parse ROADMAP_EXISTING_PROJECT.md and show progress
Usage:
    python .dev_tools/roadmap_tracker.py
    python .dev_tools/roadmap_tracker.py --verbose

Author: Recovery System Implementation (Oct 2025)
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
ROADMAP_FILE = PROJECT_ROOT / ".ai" / "planning" / "research" / "ROADMAP_EXISTING_PROJECT.md"
STATE_FILE = PROJECT_ROOT / ".ai" / "config" / "project_state.json"


# ============================================================================
# Roadmap Parser
# ============================================================================

class RoadmapTracker:
    """Parse and visualize roadmap progress"""

    def __init__(self, roadmap_path: Path, state_path: Path):
        self.roadmap_path = roadmap_path
        self.state_path = state_path
        self.tasks = self._parse_roadmap()
        self.completed = self._load_completed_tasks()

    def _parse_roadmap(self) -> Dict[str, Dict]:
        """Parse roadmap and extract all tasks"""
        if not self.roadmap_path.exists():
            print(f"[ERROR] Roadmap not found: {self.roadmap_path}")
            return {}

        content = self.roadmap_path.read_text(encoding='utf-8')
        tasks = {}

        # Pattern to match task headers
        # Examples: **QW-1: Document Existing SMC Theory** (2 hours)
        #           **MT-5: Comprehensive Benchmark - Existing 7 Controllers** (6 hours)
        task_pattern = r'\*\*([A-Z]{2}-\d+):\s*([^\(]+)\((\d+)\s*hours?\)'

        for match in re.finditer(task_pattern, content):
            task_id = match.group(1)
            title = match.group(2).strip()
            hours = int(match.group(3))

            # Determine category
            if task_id.startswith("QW"):
                category = "Quick Wins"
            elif task_id.startswith("MT"):
                category = "Medium-Term"
            elif task_id.startswith("LT"):
                category = "Long-Term"
            else:
                category = "Unknown"

            tasks[task_id] = {
                "id": task_id,
                "title": title,
                "hours": hours,
                "category": category
            }

        return tasks

    def _load_completed_tasks(self) -> List[str]:
        """Load completed tasks from project state"""
        if not self.state_path.exists():
            return []

        try:
            import json
            state = json.loads(self.state_path.read_text(encoding='utf-8'))
            return state.get("completed_tasks", [])
        except Exception as e:
            print(f"[WARNING] Could not load state: {e}")
            return []

    def calculate_progress(self) -> Tuple[int, int, int, int]:
        """Calculate progress statistics"""
        total_tasks = len(self.tasks)
        completed_tasks = len(self.completed)
        total_hours = sum(task["hours"] for task in self.tasks.values())
        completed_hours = sum(
            self.tasks[tid]["hours"] for tid in self.completed if tid in self.tasks
        )
        return completed_tasks, total_tasks, completed_hours, total_hours

    def show_summary(self):
        """Show roadmap summary"""
        completed_tasks, total_tasks, completed_hours, total_hours = self.calculate_progress()
        remaining_hours = total_hours - completed_hours
        percent_complete = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        print("=" * 70)
        print("ROADMAP PROGRESS SUMMARY")
        print("=" * 70)
        print(f"Roadmap: {self.roadmap_path.relative_to(PROJECT_ROOT)}")
        print(f"\nProgress: {completed_tasks}/{total_tasks} tasks ({percent_complete:.1f}% complete)")
        print(f"Hours: {completed_hours}/{total_hours} hours ({remaining_hours} hours remaining)")
        print("=" * 70)
        print()

    def show_by_category(self):
        """Show tasks grouped by category"""
        categories = {}

        # Group tasks by category
        for task_id, task_info in self.tasks.items():
            category = task_info["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((task_id, task_info))

        # Display each category
        for category in ["Quick Wins", "Medium-Term", "Long-Term"]:
            if category not in categories:
                continue

            tasks_in_category = categories[category]
            completed_in_category = [
                tid for tid, _ in tasks_in_category if tid in self.completed
            ]

            print(f"{category} ({len(completed_in_category)}/{len(tasks_in_category)} complete)")
            print("-" * 70)

            for task_id, task_info in sorted(tasks_in_category, key=lambda x: x[0]):
                status = "[X]" if task_id in self.completed else "[ ]"
                print(f"  {status} {task_id}: {task_info['title']} ({task_info['hours']}h)")

            print()

    def show_detailed(self):
        """Show detailed roadmap with all tasks"""
        print("=" * 70)
        print("DETAILED ROADMAP")
        print("=" * 70)
        print()

        self.show_by_category()

        # Show next available tasks
        available = self._get_available_tasks()
        if available:
            print("NEXT AVAILABLE TASKS (dependencies met)")
            print("-" * 70)
            for task_id, task_info in available[:5]:  # Show top 5
                print(f"  {task_id}: {task_info['title']} ({task_info['hours']}h)")
            print()

    def _get_available_tasks(self) -> List[Tuple[str, Dict]]:
        """Get tasks that are available to start (dependencies met)"""
        # For simplicity, show all incomplete tasks
        # (Full dependency checking is in project_state_manager.py)
        available = []
        for task_id, task_info in self.tasks.items():
            if task_id not in self.completed:
                available.append((task_id, task_info))
        return sorted(available, key=lambda x: x[0])


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Roadmap Tracker - Visualize roadmap progress"
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed task list'
    )

    args = parser.parse_args()

    tracker = RoadmapTracker(ROADMAP_FILE, STATE_FILE)

    if args.verbose:
        tracker.show_detailed()
    else:
        tracker.show_summary()
        tracker.show_by_category()


if __name__ == '__main__':
    main()
