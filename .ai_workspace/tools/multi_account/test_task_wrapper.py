"""
Test Suite for Task Wrapper Checkpoint System
==============================================

Tests automatic checkpointing, output capture, recovery, and cleanup.

Run: python -m pytest .ai_workspace/dev_tools/test_task_wrapper.py -v
"""

import json
import shutil
import tempfile
from pathlib import Path

# Test setup
TEST_ARTIFACTS_DIR = Path(".artifacts")
TEST_TASK_ID = "TEST_LT"
TEST_AGENT_ID = "test_agent1"


def setup_test_env():
    """Create temporary test environment."""
    # Ensure artifacts directory exists
    TEST_ARTIFACTS_DIR.mkdir(exist_ok=True)


def teardown_test_env():
    """Clean up test files."""
    # Remove all test checkpoint files
    for test_file in TEST_ARTIFACTS_DIR.glob(f"{TEST_TASK_ID.lower()}_*.json"):
        try:
            test_file.unlink()
        except:
            pass


def test_checkpoint_task_launch_creates_files():
    """Test that checkpoint_task_launch creates required checkpoint files."""
    from .task_wrapper import checkpoint_task_launch

    setup_test_env()

    try:
        result = checkpoint_task_launch(
            task_id=TEST_TASK_ID,
            agent_id=TEST_AGENT_ID,
            task_config={
                "subagent_type": "general-purpose",
                "description": "Test task",
                "prompt": "Test prompt"
            },
            role="Test Agent"
        )

        # Verify result structure
        assert result["success"] is True
        assert "checkpoint_file" in result
        assert "hours_spent" in result
        assert "output_artifact" in result

        # Verify checkpoint files exist
        launched_file = TEST_ARTIFACTS_DIR / f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_launched.json"
        complete_file = TEST_ARTIFACTS_DIR / f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_complete.json"
        output_file = TEST_ARTIFACTS_DIR / f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_output.json"

        assert launched_file.exists(), f"Launched checkpoint not found: {launched_file}"
        assert complete_file.exists(), f"Complete checkpoint not found: {complete_file}"
        assert output_file.exists(), f"Output artifact not found: {output_file}"

        # Verify checkpoint content
        with open(complete_file) as f:
            complete_data = json.load(f)
        assert complete_data["status"] == "COMPLETE"
        assert complete_data["task_id"] == TEST_TASK_ID
        assert complete_data["agent_id"] == TEST_AGENT_ID

        print("[OK] test_checkpoint_task_launch_creates_files passed")

    finally:
        teardown_test_env()


def test_checkpoint_agent_progress_updates():
    """Test that progress updates are saved correctly."""
    from .task_wrapper import checkpoint_agent_progress

    setup_test_env()

    try:
        # Create progress checkpoint
        checkpoint_agent_progress(
            task_id=TEST_TASK_ID,
            agent_id=TEST_AGENT_ID,
            hours_completed=2.5,
            deliverables_created=["test_file.md"],
            current_phase="Testing phase",
            notes="Test notes"
        )

        # Verify progress file exists
        progress_file = TEST_ARTIFACTS_DIR / f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_progress.json"
        assert progress_file.exists(), f"Progress checkpoint not found: {progress_file}"

        # Verify progress content
        with open(progress_file) as f:
            progress_data = json.load(f)
        assert progress_data["status"] == "IN_PROGRESS"
        assert progress_data["hours_completed"] == 2.5
        assert progress_data["current_phase"] == "Testing phase"

        print("[OK] test_checkpoint_agent_progress_updates passed")

    finally:
        teardown_test_env()


def test_checkpoint_agent_failed_creates_failed_checkpoint():
    """Test that failure checkpoints are created correctly."""
    from .task_wrapper import checkpoint_agent_failed

    setup_test_env()

    try:
        # Create failed checkpoint
        checkpoint_agent_failed(
            task_id=TEST_TASK_ID,
            agent_id=TEST_AGENT_ID,
            hours_spent=1.5,
            failure_reason="Test timeout",
            partial_deliverables=["partial_file.md"],
            recovery_recommendation="Re-run from beginning"
        )

        # Verify failed file exists
        failed_file = TEST_ARTIFACTS_DIR / f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_failed.json"
        assert failed_file.exists(), f"Failed checkpoint not found: {failed_file}"

        # Verify failed content
        with open(failed_file) as f:
            failed_data = json.load(f)
        assert failed_data["status"] == "FAILED"
        assert failed_data["failure_reason"] == "Test timeout"

        print("[OK] test_checkpoint_agent_failed_creates_failed_checkpoint passed")

    finally:
        teardown_test_env()


def test_get_incomplete_agents_detects_unfinished():
    """Test that incomplete agents are detected correctly."""
    from .task_wrapper import checkpoint_task_launch, get_incomplete_agents

    setup_test_env()

    try:
        # Create a launched checkpoint (without completing it)
        from .task_wrapper import _write_checkpoint
        _write_checkpoint(
            f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_launched.json",
            {
                "task_id": TEST_TASK_ID,
                "agent_id": TEST_AGENT_ID,
                "status": "RUNNING",
                "role": "Test Agent",
                "started_timestamp": "2025-11-11T10:00:00"
            }
        )

        # Get incomplete agents
        incomplete = get_incomplete_agents(TEST_TASK_ID)

        # Verify detection
        assert len(incomplete) > 0, "No incomplete agents detected"
        found = [a for a in incomplete if a["agent_id"] == TEST_AGENT_ID]
        assert len(found) > 0, f"Agent {TEST_AGENT_ID} not in incomplete list"

        print("[OK] test_get_incomplete_agents_detects_unfinished passed")

    finally:
        teardown_test_env()


def test_resume_incomplete_agents_provides_recommendations():
    """Test that resume function provides recovery recommendations."""
    from .project.dev_tools.agent_checkpoint import resume_incomplete_agents
    from .task_wrapper import _write_checkpoint

    setup_test_env()

    try:
        # Create incomplete agent
        _write_checkpoint(
            f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_launched.json",
            {
                "task_id": TEST_TASK_ID,
                "agent_id": TEST_AGENT_ID,
                "status": "RUNNING",
                "role": "Test Agent"
            }
        )

        # Create progress
        _write_checkpoint(
            f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_progress.json",
            {
                "task_id": TEST_TASK_ID,
                "agent_id": TEST_AGENT_ID,
                "status": "IN_PROGRESS",
                "hours_completed": 2.5,
                "current_phase": "Testing phase"
            }
        )

        # Get resume recommendations
        incomplete = resume_incomplete_agents(TEST_TASK_ID)

        # Verify recommendations
        assert len(incomplete) > 0, "No incomplete agents for resume"
        found = [a for a in incomplete if a["agent_id"] == TEST_AGENT_ID]
        assert len(found) > 0, f"Agent {TEST_AGENT_ID} not in resume list"
        assert "recommendation" in found[0], "No recommendation provided"

        print("[OK] test_resume_incomplete_agents_provides_recommendations passed")

    finally:
        teardown_test_env()


def test_output_capture_saves_to_artifacts():
    """Test that agent output is captured and saved to .artifacts/."""
    from .task_wrapper import _capture_output

    setup_test_env()

    try:
        task_result = {
            "status": "success",
            "output": "Test output"
        }

        output_path = _capture_output(
            task_id=TEST_TASK_ID,
            agent_id=TEST_AGENT_ID,
            task_result=task_result
        )

        # Verify output artifact exists
        assert output_path.exists(), f"Output artifact not found: {output_path}"

        # Verify content
        with open(output_path) as f:
            output_data = json.load(f)
        assert output_data["task_id"] == TEST_TASK_ID
        assert output_data["task_result"]["status"] == "success"

        print("[OK] test_output_capture_saves_to_artifacts passed")

    finally:
        teardown_test_env()


def test_cleanup_task_checkpoints_removes_files():
    """Test that cleanup removes checkpoint files after task completion."""
    from .project.dev_tools.agent_checkpoint import cleanup_task_checkpoints
    from .task_wrapper import _write_checkpoint

    setup_test_env()

    try:
        # Create test checkpoints
        _write_checkpoint(
            f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_launched.json",
            {"task_id": TEST_TASK_ID, "status": "COMPLETE"}
        )
        _write_checkpoint(
            f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_complete.json",
            {"task_id": TEST_TASK_ID, "status": "COMPLETE"}
        )

        # Verify files exist
        assert (TEST_ARTIFACTS_DIR / f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_launched.json").exists()

        # Cleanup
        cleanup_task_checkpoints(TEST_TASK_ID)

        # Verify files removed
        assert not (TEST_ARTIFACTS_DIR / f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_launched.json").exists()
        assert not (TEST_ARTIFACTS_DIR / f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_complete.json").exists()

        print("[OK] test_cleanup_task_checkpoints_removes_files passed")

    finally:
        teardown_test_env()


def test_parallel_agents_independent_checkpoints():
    """Test that parallel agents maintain independent checkpoints."""
    from .task_wrapper import _write_checkpoint, get_task_status

    setup_test_env()

    try:
        # Create checkpoints for two parallel agents
        agent2 = "test_agent2"

        _write_checkpoint(
            f"{TEST_TASK_ID.lower()}_{TEST_AGENT_ID}_complete.json",
            {"task_id": TEST_TASK_ID, "agent_id": TEST_AGENT_ID, "status": "COMPLETE"}
        )
        _write_checkpoint(
            f"{TEST_TASK_ID.lower()}_{agent2}_launched.json",
            {"task_id": TEST_TASK_ID, "agent_id": agent2, "status": "RUNNING"}
        )

        # Get task status
        status = get_task_status(TEST_TASK_ID)

        # Verify both agents tracked independently
        assert status["completed_agents"] >= 1
        assert status["running_agents"] >= 1

        print("[OK] test_parallel_agents_independent_checkpoints passed")

    finally:
        teardown_test_env()


if __name__ == "__main__":
    """Manual test runner for debugging."""
    print("[TEST] Running Task Wrapper Test Suite\n")

    tests = [
        test_checkpoint_task_launch_creates_files,
        test_checkpoint_agent_progress_updates,
        test_checkpoint_agent_failed_creates_failed_checkpoint,
        test_get_incomplete_agents_detects_unfinished,
        test_resume_incomplete_agents_provides_recommendations,
        test_output_capture_saves_to_artifacts,
        test_cleanup_task_checkpoints_removes_files,
        test_parallel_agents_independent_checkpoints,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"[ERROR] {test.__name__} failed: {e}")
            failed += 1

    print(f"\n[OK] Test Summary: {passed}/{len(tests)} passed")
    if failed > 0:
        print(f"[ERROR] {failed} tests failed")
        exit(1)
