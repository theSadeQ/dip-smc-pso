#!/usr/bin/env python3
"""
Project State Manager - Track macro project state for multi-month recovery

Purpose: Enables 30-second recovery after token limits or multi-month gaps
Usage:
    python .dev_tools/project_state_manager.py init
    python .dev_tools/project_state_manager.py status
    python .dev_tools/project_state_manager.py complete MT-5
    python .dev_tools/project_state_manager.py recommend-next

Author: Recovery System Implementation (Oct 2025)
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re


# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent


def get_project_state_file() -> Path:
    """
    Get project state file path with dual-path support.

    During migration, checks both new (.ai_workspace/recovery/state/) and old
    (.ai_workspace/ai/config/) locations. Prioritizes new location if it exists.

    Returns:
        Path: Path to project_state.json file
    """
    new_path = PROJECT_ROOT / ".project" / "recovery" / "state" / "project_state.json"
    old_path = PROJECT_ROOT / ".project" / "ai" / "config" / "project_state.json"

    if new_path.exists():
        return new_path
    elif old_path.exists():
        import warnings
        warnings.warn(
            "Using deprecated state file path (.ai_workspace/ai/config/project_state.json). "
            "Please migrate to .ai_workspace/recovery/state/project_state.json",
            DeprecationWarning,
            stacklevel=2
        )
        return old_path
    else:
        # Create in new location by default
        new_path.parent.mkdir(parents=True, exist_ok=True)
        return new_path


PROJECT_STATE_FILE = get_project_state_file()
ROADMAP_FILE = PROJECT_ROOT / ".project" / "ai" / "planning" / "research" / "ROADMAP_EXISTING_PROJECT.md"


# ============================================================================
# Roadmap Parser
# ============================================================================

class RoadmapParser:
    """Parse ROADMAP_EXISTING_PROJECT.md to extract tasks and dependencies"""

    def __init__(self, roadmap_path: Path):
        self.roadmap_path = roadmap_path
        self.tasks = {}
        self._parse()

    def _parse(self):
        """Parse roadmap file and extract all tasks"""
        if not self.roadmap_path.exists():
            print(f"[WARNING] Roadmap not found: {self.roadmap_path}")
            return

        content = self.roadmap_path.read_text(encoding='utf-8')

        # Extract Quick Wins (QW-X)
        qw_pattern = r'\*\*QW-(\d+):\s*([^\(]+)\((\d+)\s*hours?\)'
        for match in re.finditer(qw_pattern, content):
            task_id = f"QW-{match.group(1)}"
            title = match.group(2).strip()
            hours = int(match.group(3))
            self.tasks[task_id] = {
                "id": task_id,
                "title": title,
                "hours": hours,
                "category": "Quick Wins",
                "dependencies": []
            }

        # Extract Medium-Term (MT-X)
        mt_pattern = r'\*\*MT-(\d+):\s*([^\(]+)\((\d+)\s*hours?\)'
        for match in re.finditer(mt_pattern, content):
            task_id = f"MT-{match.group(1)}"
            title = match.group(2).strip()
            hours = int(match.group(3))
            self.tasks[task_id] = {
                "id": task_id,
                "title": title,
                "hours": hours,
                "category": "Medium-Term",
                "dependencies": self._extract_dependencies(content, task_id)
            }

        # Extract Long-Term (LT-X)
        lt_pattern = r'\*\*LT-(\d+):\s*([^\(]+)\((\d+)\s*hours?\)'
        for match in re.finditer(lt_pattern, content):
            task_id = f"LT-{match.group(1)}"
            title = match.group(2).strip()
            hours = int(match.group(3))
            self.tasks[task_id] = {
                "id": task_id,
                "title": title,
                "hours": hours,
                "category": "Long-Term",
                "dependencies": self._extract_dependencies(content, task_id)
            }

    def _extract_dependencies(self, content: str, task_id: str) -> List[str]:
        """Extract dependencies for a task from **Depends**: lines"""
        dependencies = []

        # Find task section
        task_section_pattern = rf'\*\*{re.escape(task_id)}:.*?\n(.*?)(?=\n\*\*[A-Z]{{2}}-|\n---|\Z)'
        match = re.search(task_section_pattern, content, re.DOTALL)
        if not match:
            return dependencies

        section = match.group(1)

        # Find "**Depends**:" line
        depends_pattern = r'\*\*Depends\*\*:\s*(.+)'
        depends_match = re.search(depends_pattern, section)
        if depends_match:
            depends_text = depends_match.group(1)
            # Extract task IDs (QW-X, MT-X, LT-X)
            task_ids = re.findall(r'(QW-\d+|MT-\d+|LT-\d+)', depends_text)
            dependencies.extend(task_ids)

        return dependencies

    def get_all_tasks(self) -> Dict:
        """Return all parsed tasks"""
        return self.tasks

    def calculate_total_hours(self) -> int:
        """Calculate total hours across all tasks"""
        return sum(task["hours"] for task in self.tasks.values())


# ============================================================================
# Project State Manager
# ============================================================================

class ProjectStateManager:
    """Manage project-wide state for multi-month recovery"""

    def __init__(self, state_file: Path, roadmap_file: Path):
        self.state_file = state_file
        self.roadmap_file = roadmap_file
        self.parser = RoadmapParser(roadmap_file)
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load project state from JSON file"""
        if not self.state_file.exists():
            return self._create_default_state()

        try:
            return json.loads(self.state_file.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"[ERROR] Failed to load state: {e}")
            return self._create_default_state()

    def _create_default_state(self) -> Dict:
        """Create default project state"""
        return {
            "project_name": "Double Inverted Pendulum SMC with PSO",
            "repository": "https://github.com/theSadeQ/dip-smc-pso.git",
            "current_phase": {
                "name": "Research",
                "roadmap": str(self.roadmap_file.relative_to(PROJECT_ROOT)),
                "started": None,
                "description": "Validate, document, and benchmark existing 7 controllers"
            },
            "completed_phases": [
                {
                    "name": "Phase 3: UI/UX",
                    "result": "34/34 issues resolved (100%)",
                    "completion_date": "2025-10-17",
                    "status": "Maintenance mode"
                },
                {
                    "name": "Phase 4: Production Hardening",
                    "result": "4.1+4.2 complete (Thread safety validated)",
                    "completion_date": "2025-10-17",
                    "status": "4.3+4.4 deferred (Research-ready)"
                }
            ],
            "completed_tasks": [],
            "current_task": None,
            "last_updated": None,
            "notes": []
        }

    def _save_state(self):
        """Save project state to JSON file"""
        self.state["last_updated"] = datetime.now().isoformat()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self.state, indent=2), encoding='utf-8')
        print(f"[OK] State saved to {self.state_file}")

    def initialize(self):
        """Initialize project state (one-time setup)"""
        if self.state_file.exists():
            print(f"[WARNING] State file already exists: {self.state_file}")
            response = input("Overwrite? [y/N]: ")
            if response.lower() != 'y':
                print("[CANCELLED] Initialization cancelled")
                return

        self.state = self._create_default_state()
        self.state["current_phase"]["started"] = datetime.now().isoformat()
        self._save_state()
        print("[OK] Project state initialized")

    def complete_task(self, task_id: str, deliverables: Optional[List[str]] = None):
        """Mark a task as completed"""
        # Validate task exists
        all_tasks = self.parser.get_all_tasks()
        if task_id not in all_tasks:
            print(f"[ERROR] Unknown task: {task_id}")
            print(f"Available tasks: {', '.join(sorted(all_tasks.keys()))}")
            return

        # Check if already completed
        if task_id in self.state["completed_tasks"]:
            print(f"[WARNING] Task {task_id} already marked complete")
            return

        # Mark complete
        self.state["completed_tasks"].append(task_id)

        # Add to current task history
        task_info = all_tasks[task_id]
        self.state["current_task"] = {
            "id": task_id,
            "title": task_info["title"],
            "status": "completed",
            "completed_date": datetime.now().isoformat(),
            "deliverables": deliverables or []
        }

        self._save_state()
        print(f"[OK] Task {task_id} marked complete")

        # Show progress
        self._show_progress()

    def get_status(self) -> Dict:
        """Get current project status"""
        all_tasks = self.parser.get_all_tasks()
        completed = self.state["completed_tasks"]
        total_tasks = len(all_tasks)
        completed_count = len(completed)

        # Calculate hours
        total_hours = sum(task["hours"] for task in all_tasks.values())
        completed_hours = sum(all_tasks[tid]["hours"] for tid in completed if tid in all_tasks)
        remaining_hours = total_hours - completed_hours

        return {
            "phase": self.state["current_phase"]["name"],
            "roadmap": self.state["current_phase"]["roadmap"],
            "progress": f"{completed_count}/{total_tasks} tasks ({completed_count/total_tasks*100:.1f}%)",
            "hours": f"{completed_hours}/{total_hours} hours ({remaining_hours} remaining)",
            "completed_tasks": completed,
            "current_task": self.state.get("current_task"),
            "last_updated": self.state.get("last_updated")
        }

    def _show_progress(self):
        """Display progress statistics"""
        status = self.get_status()
        print(f"\n[PROGRESS] {status['progress']}")
        print(f"[HOURS] {status['hours']}")

    def recommend_next(self) -> List[Tuple[str, str, List[str]]]:
        """Recommend next tasks based on dependencies"""
        all_tasks = self.parser.get_all_tasks()
        completed = set(self.state["completed_tasks"])

        available_tasks = []

        for task_id, task_info in all_tasks.items():
            if task_id in completed:
                continue

            # Check if all dependencies met
            deps = task_info.get("dependencies", [])
            if all(dep in completed for dep in deps):
                available_tasks.append((
                    task_id,
                    task_info["title"],
                    task_info["category"],
                    task_info["hours"],
                    deps
                ))

        return available_tasks

    def set_phase(self, phase_name: str, roadmap_path: str, description: str):
        """Change current phase"""
        self.state["current_phase"] = {
            "name": phase_name,
            "roadmap": roadmap_path,
            "started": datetime.now().isoformat(),
            "description": description
        }
        self._save_state()
        print(f"[OK] Phase set to: {phase_name}")

    def add_note(self, note: str):
        """Add a timestamped note to project state"""
        self.state["notes"].append({
            "timestamp": datetime.now().isoformat(),
            "note": note
        })
        self._save_state()
        print(f"[OK] Note added")


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Project State Manager - Track macro project state for multi-month recovery"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # init
    subparsers.add_parser('init', help='Initialize project state (one-time setup)')

    # status
    subparsers.add_parser('status', help='Show current project status')

    # complete
    complete_parser = subparsers.add_parser('complete', help='Mark task as completed')
    complete_parser.add_argument('task_id', help='Task ID (e.g., MT-5, QW-1)')
    complete_parser.add_argument('--deliverables', nargs='+', help='Deliverable files')

    # recommend-next
    subparsers.add_parser('recommend-next', help='Recommend next tasks')

    # set-phase
    phase_parser = subparsers.add_parser('set-phase', help='Change current phase')
    phase_parser.add_argument('name', help='Phase name')
    phase_parser.add_argument('--roadmap', help='Roadmap file path')
    phase_parser.add_argument('--description', help='Phase description')

    # add-note
    note_parser = subparsers.add_parser('add-note', help='Add timestamped note')
    note_parser.add_argument('note', help='Note text')

    args = parser.parse_args()

    # Create manager
    manager = ProjectStateManager(PROJECT_STATE_FILE, ROADMAP_FILE)

    if args.command == 'init':
        manager.initialize()

    elif args.command == 'status':
        status = manager.get_status()
        print(f"\n{'='*70}")
        print(f"PROJECT STATUS")
        print(f"{'='*70}")
        print(f"Phase: {status['phase']}")
        print(f"Roadmap: {status['roadmap']}")
        print(f"Progress: {status['progress']}")
        print(f"Hours: {status['hours']}")
        print(f"\nCompleted Tasks: {', '.join(status['completed_tasks']) if status['completed_tasks'] else 'None'}")
        if status['current_task']:
            print(f"\nCurrent Task: {status['current_task']['id']} - {status['current_task']['title']}")
            print(f"Status: {status['current_task']['status']}")
        print(f"\nLast Updated: {status['last_updated']}")
        print(f"{'='*70}\n")

    elif args.command == 'complete':
        manager.complete_task(args.task_id, args.deliverables)

    elif args.command == 'recommend-next':
        available = manager.recommend_next()
        print(f"\n{'='*70}")
        print(f"RECOMMENDED NEXT TASKS")
        print(f"{'='*70}")
        if not available:
            print("All tasks complete!")
        else:
            for task_id, title, category, hours, deps in available:
                print(f"\n{task_id}: {title}")
                print(f"  Category: {category}")
                print(f"  Time: {hours} hours")
                if deps:
                    print(f"  Dependencies: {', '.join(deps)} ([OK] complete)")
                else:
                    print(f"  Dependencies: None (ready to start)")
        print(f"{'='*70}\n")

    elif args.command == 'set-phase':
        manager.set_phase(
            args.name,
            args.roadmap or str(ROADMAP_FILE.relative_to(PROJECT_ROOT)),
            args.description or ""
        )

    elif args.command == 'add-note':
        manager.add_note(args.note)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
