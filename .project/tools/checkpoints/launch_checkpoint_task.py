#!/usr/bin/env python
"""
Simple CLI wrapper for Task Wrapper checkpoint system.

Makes it easy to launch multi-agent tasks with checkpointing from command line.

Usage:
    python launch_checkpoint_task.py --task LT-4 --agent agent1_theory --prompt "Your prompt here"

    python launch_checkpoint_task.py \
        --task MT-6 \
        --agent agent1_pso \
        --description "Optimize PSO" \
        --prompt "Run PSO optimization..." \
        --role "PSO Engineer" \
        --type general-purpose
"""

import sys
import argparse
from pathlib import Path

# Add dev_tools to path so we can import task_wrapper
sys.path.insert(0, str(Path(__file__).parent))

from task_wrapper import checkpoint_task_launch


def main():
    parser = argparse.ArgumentParser(
        description="Launch multi-agent task with automatic checkpointing"
    )

    parser.add_argument(
        "--task", "-t",
        required=True,
        help="Task ID (e.g., LT-4, MT-6, QW-1)"
    )

    parser.add_argument(
        "--agent", "-a",
        required=True,
        help="Agent ID (e.g., agent1_theory, agent1_pso)"
    )

    parser.add_argument(
        "--description", "-d",
        required=True,
        help="Brief task description (e.g., 'Derive Lyapunov proofs')"
    )

    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Full prompt for the agent"
    )

    parser.add_argument(
        "--role", "-r",
        required=True,
        help="Agent role (e.g., 'Theory Specialist - Derive proofs')"
    )

    parser.add_argument(
        "--type", "-T",
        default="general-purpose",
        choices=["general-purpose", "Explore", "Plan"],
        help="Subagent type (default: general-purpose)"
    )

    parser.add_argument(
        "--poll-interval",
        type=int,
        default=300,
        help="Progress polling interval in seconds (default: 300 = 5 min)"
    )

    parser.add_argument(
        "--auto-progress",
        action="store_true",
        default=True,
        help="Enable auto-polling for progress (default: enabled)"
    )

    parser.add_argument(
        "--no-auto-progress",
        action="store_true",
        help="Disable auto-polling (manual updates only)"
    )

    args = parser.parse_args()

    # Override auto-progress if --no-auto-progress specified
    auto_progress = not args.no_auto_progress

    print("[INFO] Launching checkpoint task...")
    print(f"[INFO] Task: {args.task}")
    print(f"[INFO] Agent: {args.agent}")
    print(f"[INFO] Role: {args.role}")
    print(f"[INFO] Type: {args.type}")
    print()

    try:
        result = checkpoint_task_launch(
            task_id=args.task,
            agent_id=args.agent,
            task_config={
                "subagent_type": args.type,
                "description": args.description,
                "prompt": args.prompt
            },
            role=args.role,
            auto_progress=auto_progress,
            poll_interval_seconds=args.poll_interval
        )

        print("[OK] Task completed successfully!")
        print()
        print("=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"Hours spent: {result['hours_spent']:.2f}")
        print(f"Checkpoint file: {result['checkpoint_file']}")
        print(f"Output artifact: {result['output_artifact']}")
        print(f"Success: {result['success']}")
        print()
        print("Recovery command (if needed):")
        print(f"  /resume {args.task} {args.agent}")
        print()

        return 0

    except Exception as e:
        print(f"[ERROR] Task failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
