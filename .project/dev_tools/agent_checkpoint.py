"""
Agent Orchestration Checkpoint System
=====================================

Tracks multi-agent task execution state to enable recovery after:
- Session timeouts
- Token limits
- Crashes/interruptions
- Multi-month gaps

Usage:
    from .dev_tools.agent_checkpoint import (
        checkpoint_plan_approved,
        checkpoint_agent_launched,
        checkpoint_agent_progress,
        checkpoint_agent_complete,
        checkpoint_agent_failed
    )

    # When user approves plan
    checkpoint_plan_approved("LT-4", plan_data)

    # When agent starts
    checkpoint_agent_launched("LT-4", "agent1_theory")

    # Every 5-10 minutes during execution
    checkpoint_agent_progress("LT-4", "agent1_theory",
                             hours_completed=2.5,
                             deliverables=["file1.md", "file2.json"])

    # When agent finishes
    checkpoint_agent_complete("LT-4", "agent1_theory",
                             deliverables=[...],
                             summary="...")

Recovery:
    Run: bash .dev_tools/recover_project.sh
    Section [5] will show incomplete agent work automatically

Author: Claude Code Agent Orchestration System
Date: October 2025
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================================
# Configuration
# ============================================================================

CHECKPOINT_DIR = Path(".artifacts")
CHECKPOINT_DIR.mkdir(exist_ok=True)


# ============================================================================
# Checkpoint Writers
# ============================================================================

def _write_checkpoint(filename: str, data: Dict[str, Any]) -> None:
    """Write checkpoint data to JSON file.

    Args:
        filename: Checkpoint filename (e.g., "lt4_plan_approved.json")
        data: Dictionary to write
    """
    filepath = CHECKPOINT_DIR / filename
    data["_checkpoint_timestamp"] = datetime.now().isoformat()

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[CHECKPOINT] {filename} written")


def checkpoint_plan_approved(
    task_id: str,
    plan_summary: str,
    estimated_hours: float,
    agents: List[Dict[str, Any]],
    deliverables: List[str],
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """Checkpoint when user approves multi-agent orchestration plan.

    Args:
        task_id: Task identifier (e.g., "LT-4")
        plan_summary: Brief plan description
        estimated_hours: Total time estimate
        agents: List of agent specs [{"id": "agent1", "role": "Theory", "hours": 12}, ...]
        deliverables: Expected output files
        metadata: Additional data (optional)

    Example:
        checkpoint_plan_approved(
            "LT-4",
            "Lyapunov stability proofs for 5 controllers",
            18.0,
            [
                {"id": "agent1_theory", "role": "Theory Specialist", "hours": 12},
                {"id": "agent2_validation", "role": "Implementation Validator", "hours": 8}
            ],
            ["docs/theory/lyapunov_stability_proofs.md", "scripts/validate_stability.py"]
        )
    """
    data = {
        "task_id": task_id,
        "status": "APPROVED",
        "plan_summary": plan_summary,
        "estimated_hours": estimated_hours,
        "agents": agents,
        "expected_deliverables": deliverables,
        "approved_timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }

    filename = f"{task_id.lower().replace('-', '')}_plan_approved.json"
    _write_checkpoint(filename, data)


def checkpoint_agent_launched(
    task_id: str,
    agent_id: str,
    role: str,
    estimated_hours: float,
    dependencies: Optional[List[str]] = None
) -> None:
    """Checkpoint when agent starts execution.

    Args:
        task_id: Task identifier (e.g., "LT-4")
        agent_id: Agent identifier (e.g., "agent1_theory")
        role: Agent role description
        estimated_hours: Agent time budget
        dependencies: Required files/agents (optional)

    Example:
        checkpoint_agent_launched(
            "LT-4",
            "agent1_theory",
            "Theory Specialist - Derive Lyapunov proofs",
            12.0,
            ["docs/theory/smc_theory_complete.md"]
        )
    """
    data = {
        "task_id": task_id,
        "agent_id": agent_id,
        "role": role,
        "status": "RUNNING",
        "estimated_hours": estimated_hours,
        "launched_timestamp": datetime.now().isoformat(),
        "dependencies": dependencies or []
    }

    filename = f"{task_id.lower().replace('-', '')}_{agent_id}_launched.json"
    _write_checkpoint(filename, data)


def checkpoint_agent_progress(
    task_id: str,
    agent_id: str,
    hours_completed: float,
    deliverables_created: List[str],
    current_phase: str,
    notes: Optional[str] = None
) -> None:
    """Checkpoint agent progress (call every 5-10 minutes during execution).

    Args:
        task_id: Task identifier (e.g., "LT-4")
        agent_id: Agent identifier (e.g., "agent1_theory")
        hours_completed: Hours of work done so far
        deliverables_created: Files written so far
        current_phase: What agent is currently doing
        notes: Additional context (optional)

    Example:
        checkpoint_agent_progress(
            "LT-4",
            "agent1_theory",
            hours_completed=4.5,
            deliverables_created=[
                "docs/theory/lyapunov_stability_proofs.md",
                ".artifacts/lt4_classical_proof.tex"
            ],
            current_phase="Proving STA SMC (Hour 3.5-5)",
            notes="Classical + Adaptive proofs complete, STA in progress"
        )
    """
    data = {
        "task_id": task_id,
        "agent_id": agent_id,
        "status": "IN_PROGRESS",
        "hours_completed": hours_completed,
        "deliverables_created": deliverables_created,
        "current_phase": current_phase,
        "last_progress_timestamp": datetime.now().isoformat(),
        "notes": notes or ""
    }

    filename = f"{task_id.lower().replace('-', '')}_{agent_id}_progress.json"
    _write_checkpoint(filename, data)


def checkpoint_agent_complete(
    task_id: str,
    agent_id: str,
    hours_spent: float,
    deliverables: List[str],
    summary: str,
    handoff_to_next_agent: Optional[Dict[str, Any]] = None
) -> None:
    """Checkpoint when agent completes successfully.

    Args:
        task_id: Task identifier (e.g., "LT-4")
        agent_id: Agent identifier (e.g., "agent1_theory")
        hours_spent: Actual time spent
        deliverables: Files created
        summary: Completion summary
        handoff_to_next_agent: Data for next agent (optional)

    Example:
        checkpoint_agent_complete(
            "LT-4",
            "agent1_theory",
            hours_spent=11.5,
            deliverables=[
                "docs/theory/lyapunov_stability_proofs.md",
                ".artifacts/lt4_handoff.json"
            ],
            summary="All 5 proofs complete (Classical, STA, Adaptive, Hybrid, Swing-Up)",
            handoff_to_next_agent={
                "next_agent": "agent2_validation",
                "handoff_file": ".artifacts/lt4_handoff.json",
                "critical_findings": ["STA proof uses generalized gradient", "Hybrid needs ISS framework"]
            }
        )
    """
    data = {
        "task_id": task_id,
        "agent_id": agent_id,
        "status": "COMPLETE",
        "hours_spent": hours_spent,
        "deliverables": deliverables,
        "summary": summary,
        "completed_timestamp": datetime.now().isoformat(),
        "handoff_to_next_agent": handoff_to_next_agent or {}
    }

    filename = f"{task_id.lower().replace('-', '')}_{agent_id}_complete.json"
    _write_checkpoint(filename, data)


def checkpoint_agent_failed(
    task_id: str,
    agent_id: str,
    hours_spent: float,
    failure_reason: str,
    partial_deliverables: List[str],
    recovery_recommendation: str
) -> None:
    """Checkpoint when agent fails or is interrupted.

    Args:
        task_id: Task identifier (e.g., "LT-4")
        agent_id: Agent identifier (e.g., "agent1_theory")
        hours_spent: Time spent before failure
        failure_reason: Why agent failed
        partial_deliverables: Files created before failure
        recovery_recommendation: How to resume

    Example:
        checkpoint_agent_failed(
            "LT-4",
            "agent1_theory",
            hours_spent=1.5,
            failure_reason="Session timeout (token limit)",
            partial_deliverables=[],
            recovery_recommendation="Re-launch Agent 1 from Hour 0"
        )
    """
    data = {
        "task_id": task_id,
        "agent_id": agent_id,
        "status": "FAILED",
        "hours_spent": hours_spent,
        "failure_reason": failure_reason,
        "partial_deliverables": partial_deliverables,
        "recovery_recommendation": recovery_recommendation,
        "failed_timestamp": datetime.now().isoformat()
    }

    filename = f"{task_id.lower().replace('-', '')}_{agent_id}_failed.json"
    _write_checkpoint(filename, data)


# ============================================================================
# Checkpoint Readers (for recovery script)
# ============================================================================

def get_incomplete_agents() -> List[Dict[str, Any]]:
    """Find agents that were launched but never completed.

    Returns:
        List of incomplete agent info [{"task": "LT-4", "agent": "agent1", ...}, ...]

    Used by recovery script to detect interrupted work.
    """
    incomplete = []

    # Find all *_launched.json files
    launched_files = list(CHECKPOINT_DIR.glob("*_launched.json"))

    for launched_file in launched_files:
        # Parse filename to extract task + agent
        # Format: {task}_{agent}_launched.json
        stem = launched_file.stem  # Remove .json
        parts = stem.split("_")

        if len(parts) < 3:
            continue  # Invalid format

        task_id = parts[0]  # e.g., "lt4"
        agent_id = "_".join(parts[1:-1])  # e.g., "agent1_theory"

        # Check if complete file exists
        complete_file = CHECKPOINT_DIR / f"{task_id}_{agent_id}_complete.json"
        failed_file = CHECKPOINT_DIR / f"{task_id}_{agent_id}_failed.json"

        if not complete_file.exists() and not failed_file.exists():
            # Agent is incomplete!
            with open(launched_file, 'r', encoding='utf-8') as f:
                launch_data = json.load(f)

            # Check for progress checkpoint
            progress_file = CHECKPOINT_DIR / f"{task_id}_{agent_id}_progress.json"
            progress_data = None
            if progress_file.exists():
                with open(progress_file, 'r', encoding='utf-8') as f:
                    progress_data = json.load(f)

            incomplete.append({
                "task_id": launch_data.get("task_id", task_id.upper()),
                "agent_id": agent_id,
                "role": launch_data.get("role", "Unknown"),
                "launched_timestamp": launch_data.get("launched_timestamp", "Unknown"),
                "last_progress": progress_data,
                "launched_file": str(launched_file)
            })

    return incomplete


# ============================================================================
# Utility Functions
# ============================================================================

def cleanup_task_checkpoints(task_id: str) -> None:
    """Remove all checkpoints for a completed task.

    Args:
        task_id: Task identifier (e.g., "LT-4")

    Use after task is fully complete and committed to git.
    """
    task_prefix = task_id.lower().replace('-', '')
    checkpoint_files = list(CHECKPOINT_DIR.glob(f"{task_prefix}_*.json"))

    for file in checkpoint_files:
        file.unlink()
        print(f"[CLEANUP] Removed {file.name}")

    print(f"[CLEANUP] Removed {len(checkpoint_files)} checkpoint files for {task_id}")


def get_task_status(task_id: str) -> Dict[str, Any]:
    """Get complete status of a task's agent orchestration.

    Args:
        task_id: Task identifier (e.g., "LT-4")

    Returns:
        Status summary with all agents' states
    """
    task_prefix = task_id.lower().replace('-', '')

    # Check for plan approval
    plan_file = CHECKPOINT_DIR / f"{task_prefix}_plan_approved.json"
    plan_data = None
    if plan_file.exists():
        with open(plan_file, 'r', encoding='utf-8') as f:
            plan_data = json.load(f)

    # Find all agents
    launched_files = list(CHECKPOINT_DIR.glob(f"{task_prefix}_*_launched.json"))
    agents = []

    for launched_file in launched_files:
        stem = launched_file.stem
        parts = stem.split("_")
        agent_id = "_".join(parts[1:-1])

        with open(launched_file, 'r', encoding='utf-8') as f:
            launch_data = json.load(f)

        # Check status
        complete_file = CHECKPOINT_DIR / f"{task_prefix}_{agent_id}_complete.json"
        failed_file = CHECKPOINT_DIR / f"{task_prefix}_{agent_id}_failed.json"
        progress_file = CHECKPOINT_DIR / f"{task_prefix}_{agent_id}_progress.json"

        status = "RUNNING"
        if complete_file.exists():
            status = "COMPLETE"
        elif failed_file.exists():
            status = "FAILED"

        agent_info = {
            "agent_id": agent_id,
            "role": launch_data.get("role"),
            "status": status,
            "launched": launch_data.get("launched_timestamp")
        }

        if progress_file.exists():
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
            agent_info["last_progress"] = progress_data.get("last_progress_timestamp")
            agent_info["hours_completed"] = progress_data.get("hours_completed")
            agent_info["current_phase"] = progress_data.get("current_phase")

        agents.append(agent_info)

    return {
        "task_id": task_id,
        "plan_approved": plan_data is not None,
        "plan_data": plan_data,
        "agents": agents,
        "total_agents": len(agents),
        "completed_agents": sum(1 for a in agents if a["status"] == "COMPLETE"),
        "running_agents": sum(1 for a in agents if a["status"] == "RUNNING"),
        "failed_agents": sum(1 for a in agents if a["status"] == "FAILED")
    }


# ============================================================================
# Main (for testing)
# ============================================================================

if __name__ == "__main__":
    # Test checkpoint system
    print("Testing Agent Checkpoint System\n")

    # Simulate LT-4 workflow
    print("1. Plan approved...")
    checkpoint_plan_approved(
        "LT-4",
        "Lyapunov stability proofs for 5 controllers",
        18.0,
        [
            {"id": "agent1_theory", "role": "Theory Specialist", "hours": 12},
            {"id": "agent2_validation", "role": "Implementation Validator", "hours": 8}
        ],
        ["docs/theory/lyapunov_stability_proofs.md"]
    )

    print("\n2. Agent 1 launched...")
    checkpoint_agent_launched(
        "LT-4",
        "agent1_theory",
        "Theory Specialist - Derive Lyapunov proofs",
        12.0
    )

    print("\n3. Agent 1 progress update...")
    checkpoint_agent_progress(
        "LT-4",
        "agent1_theory",
        hours_completed=2.5,
        deliverables_created=["docs/theory/lyapunov_stability_proofs.md"],
        current_phase="Proving Classical SMC (Hour 2-3.5)",
        notes="Classical proof 50% complete"
    )

    print("\n4. Checking for incomplete agents...")
    incomplete = get_incomplete_agents()
    print(f"Found {len(incomplete)} incomplete agents:")
    for agent in incomplete:
        print(f"  - {agent['task_id']}: {agent['agent_id']} ({agent['role']})")
        print(f"    Launched: {agent['launched_timestamp']}")
        if agent['last_progress']:
            print(f"    Last progress: {agent['last_progress']['current_phase']}")

    print("\n5. Getting task status...")
    status = get_task_status("LT-4")
    print(f"Task: {status['task_id']}")
    print(f"Plan approved: {status['plan_approved']}")
    print(f"Agents: {status['total_agents']} total, {status['running_agents']} running, {status['completed_agents']} complete")

    print("\n[OK] Checkpoint system test complete!")
    print(f"Check {CHECKPOINT_DIR} for generated files")
