# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/checkpoint_manager.py
# ═══════════════════════════════════════════════════════════════════════════
"""
Checkpoint and recovery system for long-running research operations.

Enables resumable research sessions with automatic state saving every N claims.
Critical for handling API rate limits, timeouts, and session continuity.

Features:
- Auto-save every N claims (default: 50)
- Resume from last checkpoint
- Progress tracking
- Error recovery
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class ResearchProgress:
    """Progress tracking for research session."""

    session_id: str
    started_at: str
    last_updated: str
    total_claims: int
    claims_processed: int
    claims_successful: int
    claims_failed: int
    current_batch: str
    current_claim_id: Optional[str]
    errors: List[Dict[str, str]] = field(default_factory=list)
    performance: Dict[str, Any] = field(default_factory=dict)

    @property
    def completion_rate(self) -> float:
        """Calculate completion percentage."""
        if self.total_claims == 0:
            return 0.0
        return (self.claims_processed / self.total_claims) * 100

    @property
    def success_rate(self) -> float:
        """Calculate success percentage."""
        if self.claims_processed == 0:
            return 0.0
        return (self.claims_successful / self.claims_processed) * 100


@dataclass
class ClaimResult:
    """Research result for a single claim."""

    claim_id: str
    claim_text: str
    queries_used: List[str]
    papers_found: List[Dict[str, Any]]
    selected_citations: List[Dict[str, Any]]
    timestamp: str
    processing_time_sec: float
    status: str  # 'success', 'partial', 'failed'
    error_message: Optional[str] = None


@dataclass
class Checkpoint:
    """Complete checkpoint state."""

    checkpoint_id: str
    progress: ResearchProgress
    results: List[ClaimResult]
    queued_claims: List[str]  # Claim IDs not yet processed


# ═══════════════════════════════════════════════════════════════════════════
# Checkpoint Manager
# ═══════════════════════════════════════════════════════════════════════════


class CheckpointManager:
    """
    Manage checkpoints for long-running research sessions.

    Usage:
        manager = CheckpointManager("artifacts/checkpoints")
        manager.create_session(total_claims=500)

        for claim in claims:
            result = process_claim(claim)
            manager.record_result(claim_id, result)

            if manager.should_checkpoint():
                manager.save_checkpoint()

        # Resume from checkpoint
        manager = CheckpointManager("artifacts/checkpoints")
        if manager.can_resume():
            session = manager.load_latest_checkpoint()
    """

    def __init__(self, checkpoint_dir: str = "artifacts/checkpoints"):
        """
        Initialize checkpoint manager.

        Args:
            checkpoint_dir: Directory for checkpoint files
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        self.session_id: Optional[str] = None
        self.progress: Optional[ResearchProgress] = None
        self.results: List[ClaimResult] = []
        self.queued_claims: List[str] = []

        self.checkpoint_frequency = 50  # Save every N claims
        self.last_checkpoint_count = 0

    # ══════════════════════════════════════════════════════════════════════
    # Session Management
    # ══════════════════════════════════════════════════════════════════════

    def create_session(
        self, total_claims: int, batch_name: str = "research_batch"
    ) -> str:
        """
        Create new research session.

        Args:
            total_claims: Total number of claims to process
            batch_name: Name of the batch being processed

        Returns:
            Session ID
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self.session_id = f"session_{timestamp}"

        self.progress = ResearchProgress(
            session_id=self.session_id,
            started_at=datetime.utcnow().isoformat(),
            last_updated=datetime.utcnow().isoformat(),
            total_claims=total_claims,
            claims_processed=0,
            claims_successful=0,
            claims_failed=0,
            current_batch=batch_name,
            current_claim_id=None,
        )

        self.results = []
        self.queued_claims = []

        logger.info(f"Created research session: {self.session_id}")
        return self.session_id

    def set_queued_claims(self, claim_ids: List[str]) -> None:
        """Set the queue of claims to process."""
        self.queued_claims = claim_ids.copy()
        logger.info(f"Queued {len(claim_ids)} claims for processing")

    # ══════════════════════════════════════════════════════════════════════
    # Progress Tracking
    # ══════════════════════════════════════════════════════════════════════

    def record_result(
        self,
        claim_id: str,
        claim_text: str,
        queries: List[str],
        papers: List[Dict],
        citations: List[Dict],
        processing_time: float,
        status: str,
        error: Optional[str] = None,
    ) -> None:
        """
        Record research result for a claim.

        Args:
            claim_id: Claim identifier
            claim_text: Full claim text
            queries: Search queries used
            papers: Papers found
            citations: Selected citations
            processing_time: Time in seconds
            status: 'success', 'partial', or 'failed'
            error: Error message if failed
        """
        result = ClaimResult(
            claim_id=claim_id,
            claim_text=claim_text,
            queries_used=queries,
            papers_found=papers,
            selected_citations=citations,
            timestamp=datetime.utcnow().isoformat(),
            processing_time_sec=processing_time,
            status=status,
            error_message=error,
        )

        self.results.append(result)

        # Update progress
        if self.progress:
            self.progress.claims_processed += 1
            if status == "success":
                self.progress.claims_successful += 1
            elif status == "failed":
                self.progress.claims_failed += 1
                if error:
                    self.progress.errors.append(
                        {"claim_id": claim_id, "error": error}
                    )

            self.progress.last_updated = datetime.utcnow().isoformat()

            # Remove from queue
            if claim_id in self.queued_claims:
                self.queued_claims.remove(claim_id)

        logger.info(
            f"Recorded result for {claim_id}: {status} "
            f"({len(citations)} citations in {processing_time:.2f}s)"
        )

    def should_checkpoint(self) -> bool:
        """Check if it's time to save a checkpoint."""
        if not self.progress:
            return False

        claims_since_checkpoint = (
            self.progress.claims_processed - self.last_checkpoint_count
        )
        return claims_since_checkpoint >= self.checkpoint_frequency

    # ══════════════════════════════════════════════════════════════════════
    # Checkpoint Persistence
    # ══════════════════════════════════════════════════════════════════════

    def save_checkpoint(self) -> Path:
        """
        Save current state to checkpoint file.

        Returns:
            Path to checkpoint file
        """
        if not self.session_id or not self.progress:
            raise ValueError("No active session to checkpoint")

        checkpoint = Checkpoint(
            checkpoint_id=f"{self.session_id}_{self.progress.claims_processed:04d}",
            progress=self.progress,
            results=self.results,
            queued_claims=self.queued_claims,
        )

        checkpoint_file = (
            self.checkpoint_dir
            / f"{self.session_id}_checkpoint_{self.progress.claims_processed:04d}.json"
        )

        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(asdict(checkpoint), f, indent=2)

        self.last_checkpoint_count = self.progress.claims_processed

        logger.info(
            f"Checkpoint saved: {checkpoint_file.name} "
            f"({self.progress.completion_rate:.1f}% complete)"
        )

        return checkpoint_file

    def load_checkpoint(self, checkpoint_file: Path) -> Checkpoint:
        """
        Load checkpoint from file.

        Args:
            checkpoint_file: Path to checkpoint file

        Returns:
            Checkpoint object
        """
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Reconstruct dataclasses
        progress = ResearchProgress(**data["progress"])
        results = [ClaimResult(**r) for r in data["results"]]
        queued_claims = data["queued_claims"]

        checkpoint = Checkpoint(
            checkpoint_id=data["checkpoint_id"],
            progress=progress,
            results=results,
            queued_claims=queued_claims,
        )

        logger.info(
            f"Loaded checkpoint: {checkpoint_file.name} "
            f"({progress.completion_rate:.1f}% complete)"
        )

        return checkpoint

    def can_resume(self) -> bool:
        """Check if there's a checkpoint to resume from."""
        checkpoints = list(self.checkpoint_dir.glob("session_*_checkpoint_*.json"))
        return len(checkpoints) > 0

    def load_latest_checkpoint(self) -> Optional[Checkpoint]:
        """
        Load the most recent checkpoint.

        Returns:
            Checkpoint object or None
        """
        checkpoints = sorted(
            self.checkpoint_dir.glob("session_*_checkpoint_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        if not checkpoints:
            logger.warning("No checkpoints found")
            return None

        latest = checkpoints[0]
        checkpoint = self.load_checkpoint(latest)

        # Restore session state
        self.session_id = checkpoint.progress.session_id
        self.progress = checkpoint.progress
        self.results = checkpoint.results
        self.queued_claims = checkpoint.queued_claims
        self.last_checkpoint_count = checkpoint.progress.claims_processed

        return checkpoint

    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """List all available checkpoints with metadata."""
        checkpoints = []

        for checkpoint_file in sorted(
            self.checkpoint_dir.glob("session_*_checkpoint_*.json")
        ):
            with open(checkpoint_file, "r") as f:
                data = json.load(f)

            progress = data["progress"]
            checkpoints.append(
                {
                    "file": checkpoint_file.name,
                    "session_id": progress["session_id"],
                    "claims_processed": progress["claims_processed"],
                    "total_claims": progress["total_claims"],
                    "completion_rate": (
                        progress["claims_processed"] / progress["total_claims"]
                    )
                    * 100,
                    "last_updated": progress["last_updated"],
                }
            )

        return checkpoints

    # ══════════════════════════════════════════════════════════════════════
    # Resume Logic
    # ══════════════════════════════════════════════════════════════════════

    def get_remaining_claims(self) -> List[str]:
        """Get list of claim IDs not yet processed."""
        return self.queued_claims.copy()

    def get_processed_claim_ids(self) -> List[str]:
        """Get list of claim IDs already processed."""
        return [r.claim_id for r in self.results]

    # ══════════════════════════════════════════════════════════════════════
    # Reporting
    # ══════════════════════════════════════════════════════════════════════

    def generate_progress_report(self) -> str:
        """Generate human-readable progress report."""
        if not self.progress:
            return "No active session"

        report = f"""
Research Session Progress Report
═══════════════════════════════════════════════════════════════

Session ID:       {self.progress.session_id}
Batch:            {self.progress.current_batch}
Started:          {self.progress.started_at}
Last Updated:     {self.progress.last_updated}

Progress:
  Total Claims:   {self.progress.total_claims}
  Processed:      {self.progress.claims_processed} ({self.progress.completion_rate:.1f}%)
  Successful:     {self.progress.claims_successful} ({self.progress.success_rate:.1f}%)
  Failed:         {self.progress.claims_failed}
  Remaining:      {len(self.queued_claims)}

Performance:
  Avg Time/Claim: {self._calculate_avg_time():.2f}s
  Est. Remaining: {self._estimate_remaining_time()}

Recent Errors:    {len(self.progress.errors)} (last 10 shown)
"""

        # Add recent errors
        for error in self.progress.errors[-10:]:
            report += f"  - {error['claim_id']}: {error['error']}\n"

        return report

    def _calculate_avg_time(self) -> float:
        """Calculate average processing time per claim."""
        if not self.results:
            return 0.0
        total_time = sum(r.processing_time_sec for r in self.results)
        return total_time / len(self.results)

    def _estimate_remaining_time(self) -> str:
        """Estimate time remaining for session."""
        if not self.results or not self.progress:
            return "Unknown"

        avg_time = self._calculate_avg_time()
        remaining_claims = len(self.queued_claims)
        remaining_seconds = avg_time * remaining_claims

        hours = int(remaining_seconds // 3600)
        minutes = int((remaining_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


# ═══════════════════════════════════════════════════════════════════════════
# Example Usage
# ═══════════════════════════════════════════════════════════════════════════


def main():
    """Example checkpoint manager usage."""
    logging.basicConfig(level=logging.INFO)

    manager = CheckpointManager("artifacts/checkpoints")

    # Create new session
    manager.create_session(total_claims=100, batch_name="test_batch")
    manager.set_queued_claims([f"claim_{i:03d}" for i in range(100)])

    # Simulate processing claims
    for i in range(15):
        claim_id = f"claim_{i:03d}"
        manager.record_result(
            claim_id=claim_id,
            claim_text=f"Test claim {i}",
            queries=["test query"],
            papers=[{"title": "Test Paper"}],
            citations=[{"key": "test2024"}],
            processing_time=1.5,
            status="success",
        )

        if manager.should_checkpoint():
            manager.save_checkpoint()

    # Print progress
    print(manager.generate_progress_report())

    # Test resume
    print("\nTesting resume...")
    manager2 = CheckpointManager("artifacts/checkpoints")
    if manager2.can_resume():
        checkpoint = manager2.load_latest_checkpoint()
        print(f"Resumed from {checkpoint.checkpoint_id}")
        print(f"Remaining claims: {len(manager2.get_remaining_claims())}")


if __name__ == "__main__":
    main()
