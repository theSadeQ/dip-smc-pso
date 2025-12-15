#======================================================================================
#================ src/utils/monitoring/maintenance.py ================
#======================================================================================
"""
Automated maintenance and cleanup for monitoring system.

This module provides automated cleanup, retention policies, and database
maintenance to keep the monitoring system healthy and performant.

Features:
    - Automatic cleanup of old runs (configurable retention period)
    - Disk space monitoring and management
    - Database vacuum and optimization
    - Orphaned file detection and removal
    - Backup utilities

Usage:
    >>> from src.utils.monitoring.maintenance import MaintenanceManager, RetentionPolicy
    >>>
    >>> # Configure retention policy
    >>> policy = RetentionPolicy(
    ...     keep_days=30,  # Keep last 30 days
    ...     keep_min_runs=100,  # Always keep at least 100 runs
    ...     archive_before_delete=True
    ... )
    >>>
    >>> # Run maintenance
    >>> manager = MaintenanceManager(retention_policy=policy)
    >>> report = manager.run_maintenance(dry_run=False)
    >>> print(f"Cleaned up {report.runs_deleted} runs, freed {report.space_freed_mb:.1f}MB")

Integration:
    - Works with DataManager for run data
    - Safe deletion with optional archiving
    - Dry-run mode for testing

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

import logging
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from src.utils.monitoring.data_manager import DataManager


@dataclass
class RetentionPolicy:
    """Retention policy configuration."""

    keep_days: int = 90  # Keep runs from last N days
    keep_min_runs: int = 100  # Always keep at least N runs per controller
    max_total_runs: int = 10000  # Maximum total runs to keep
    archive_before_delete: bool = True  # Archive runs before deletion
    archive_dir: Path = Path("monitoring_data/archive")


@dataclass
class MaintenanceReport:
    """Maintenance operation report."""

    runs_deleted: int = 0
    runs_archived: int = 0
    space_freed_mb: float = 0.0
    database_size_before_mb: float = 0.0
    database_size_after_mb: float = 0.0
    orphaned_files_removed: int = 0
    errors: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class MaintenanceManager:
    """
    Automated maintenance and cleanup manager.

    Manages retention policies, disk space, database optimization,
    and general housekeeping for the monitoring system.

    Attributes:
        data_manager: DataManager instance
        retention_policy: RetentionPolicy configuration
    """

    def __init__(
        self,
        data_manager: Optional[DataManager] = None,
        retention_policy: Optional[RetentionPolicy] = None
    ):
        """
        Initialize maintenance manager.

        Args:
            data_manager: Optional DataManager instance
            retention_policy: Optional RetentionPolicy (uses defaults if None)
        """
        self.data_manager = data_manager or DataManager()
        self.retention_policy = retention_policy or RetentionPolicy()

        # Ensure archive directory exists
        if self.retention_policy.archive_before_delete:
            self.retention_policy.archive_dir.mkdir(parents=True, exist_ok=True)

        logging.info("MaintenanceManager initialized")

    def run_maintenance(self, dry_run: bool = True) -> MaintenanceReport:
        """
        Run full maintenance cycle.

        Args:
            dry_run: If True, report what would be done without making changes

        Returns:
            MaintenanceReport with details of operations performed
        """
        report = MaintenanceReport()

        logging.info(f"Starting maintenance (dry_run={dry_run})")

        # Get initial database size
        report.database_size_before_mb = self._get_database_size_mb()

        try:
            # Apply retention policy
            retention_result = self._apply_retention_policy(dry_run=dry_run)
            report.runs_deleted = retention_result['deleted']
            report.runs_archived = retention_result['archived']
            report.space_freed_mb = retention_result['space_freed_mb']

            # Remove orphaned files
            if not dry_run:
                report.orphaned_files_removed = self._remove_orphaned_files()

            # Optimize database
            if not dry_run:
                self._optimize_database()

            # Get final database size
            report.database_size_after_mb = self._get_database_size_mb()

        except Exception as e:
            error_msg = f"Maintenance error: {e}"
            logging.error(error_msg)
            report.errors.append(error_msg)

        logging.info(f"Maintenance complete: {report.runs_deleted} runs deleted, {report.space_freed_mb:.1f}MB freed")
        return report

    def _apply_retention_policy(self, dry_run: bool = True) -> dict:
        """
        Apply retention policy to delete/archive old runs.

        Args:
            dry_run: If True, only report what would be done

        Returns:
            Dictionary with 'deleted', 'archived', 'space_freed_mb' counts
        """
        result = {
            'deleted': 0,
            'archived': 0,
            'space_freed_mb': 0.0
        }

        # Get all runs
        all_runs = self.data_manager.query_runs(limit=100000, ascending=False)

        if not all_runs:
            return result

        # Group runs by controller
        runs_by_controller = {}
        for run in all_runs:
            if run.controller not in runs_by_controller:
                runs_by_controller[run.controller] = []
            runs_by_controller[run.controller].append(run)

        # Determine which runs to delete
        runs_to_delete = []

        for controller, controller_runs in runs_by_controller.items():
            # Sort by timestamp (newest first)
            controller_runs.sort(key=lambda r: r.start_time, reverse=True)

            # Keep minimum number of runs per controller
            if len(controller_runs) <= self.retention_policy.keep_min_runs:
                continue

            # Check age-based retention
            cutoff_time = datetime.now().timestamp() - (self.retention_policy.keep_days * 24 * 3600)

            for run in controller_runs[self.retention_policy.keep_min_runs:]:
                if run.start_time < cutoff_time:
                    runs_to_delete.append(run)

        # Also enforce max total runs limit
        if len(all_runs) > self.retention_policy.max_total_runs:
            # Sort all runs by timestamp (oldest first)
            all_runs.sort(key=lambda r: r.start_time)

            # Mark oldest runs for deletion
            excess_count = len(all_runs) - self.retention_policy.max_total_runs
            for run in all_runs[:excess_count]:
                if run not in runs_to_delete:
                    runs_to_delete.append(run)

        # Delete or archive runs
        for run in runs_to_delete:
            run_dir = Path(self.data_manager.runs_path) / run.run_id

            if not run_dir.exists():
                continue

            # Calculate size before deletion
            size_mb = self._get_directory_size_mb(run_dir)

            if dry_run:
                logging.info(f"[DRY RUN] Would delete run: {run.run_id} ({size_mb:.2f}MB)")
                result['deleted'] += 1
                result['space_freed_mb'] += size_mb
            else:
                # Archive if configured
                if self.retention_policy.archive_before_delete:
                    try:
                        self._archive_run(run.run_id, run_dir)
                        result['archived'] += 1
                    except Exception as e:
                        logging.error(f"Failed to archive {run.run_id}: {e}")

                # Delete run
                try:
                    shutil.rmtree(run_dir)
                    result['deleted'] += 1
                    result['space_freed_mb'] += size_mb
                    logging.info(f"Deleted run: {run.run_id} ({size_mb:.2f}MB)")

                    # Remove from database
                    self._remove_from_database(run.run_id)

                except Exception as e:
                    logging.error(f"Failed to delete {run.run_id}: {e}")

        return result

    def _archive_run(self, run_id: str, run_dir: Path) -> None:
        """
        Archive a run to the archive directory.

        Args:
            run_id: Run identifier
            run_dir: Path to run directory
        """
        archive_path = self.retention_policy.archive_dir / f"{run_id}.tar.gz"

        # Create tarball
        import tarfile

        with tarfile.open(archive_path, 'w:gz') as tar:
            tar.add(run_dir, arcname=run_id)

        logging.info(f"Archived run {run_id} to {archive_path}")

    def _remove_orphaned_files(self) -> int:
        """
        Remove orphaned files (directories without database entries).

        Returns:
            Number of orphaned files removed
        """
        removed_count = 0
        runs_dir = Path(self.data_manager.runs_path)

        if not runs_dir.exists():
            return 0

        # Get all run IDs from database
        db_run_ids = set()
        runs = self.data_manager.query_runs(limit=100000)
        for run in runs:
            db_run_ids.add(run.run_id)

        # Check filesystem for orphaned directories
        for run_dir in runs_dir.iterdir():
            if not run_dir.is_dir():
                continue

            run_id = run_dir.name

            if run_id not in db_run_ids:
                logging.warning(f"Found orphaned run directory: {run_id}")
                try:
                    shutil.rmtree(run_dir)
                    removed_count += 1
                    logging.info(f"Removed orphaned directory: {run_id}")
                except Exception as e:
                    logging.error(f"Failed to remove orphaned directory {run_id}: {e}")

        return removed_count

    def _optimize_database(self) -> None:
        """Optimize SQLite database (VACUUM, ANALYZE)."""
        try:
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()

            # Vacuum to reclaim space
            cursor.execute("VACUUM")

            # Analyze to update statistics
            cursor.execute("ANALYZE")

            conn.commit()
            conn.close()

            logging.info("Database optimized (VACUUM + ANALYZE)")

        except Exception as e:
            logging.error(f"Database optimization failed: {e}")

    def _remove_from_database(self, run_id: str) -> None:
        """Remove run entry from database."""
        try:
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM runs WHERE run_id = ?", (run_id,))

            conn.commit()
            conn.close()

        except Exception as e:
            logging.error(f"Failed to remove {run_id} from database: {e}")

    def _get_database_size_mb(self) -> float:
        """Get database file size in MB."""
        if not Path(self.data_manager.db_path).exists():
            return 0.0

        size_bytes = Path(self.data_manager.db_path).stat().st_size
        return size_bytes / (1024 * 1024)

    def _get_directory_size_mb(self, directory: Path) -> float:
        """Get directory size in MB."""
        total_size = 0

        for file_path in directory.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size

        return total_size / (1024 * 1024)

    def get_disk_usage_report(self) -> dict:
        """
        Get disk usage report for monitoring data.

        Returns:
            Dictionary with disk usage statistics
        """
        report = {
            'runs_dir_mb': 0.0,
            'pso_runs_dir_mb': 0.0,
            'database_mb': 0.0,
            'logs_mb': 0.0,
            'total_mb': 0.0,
            'run_count': 0
        }

        # Runs directory
        runs_dir = Path(self.data_manager.runs_path)
        if runs_dir.exists():
            report['runs_dir_mb'] = self._get_directory_size_mb(runs_dir)
            report['run_count'] = len([d for d in runs_dir.iterdir() if d.is_dir()])

        # PSO runs directory
        pso_runs_dir = Path(self.data_manager.pso_path)
        if pso_runs_dir.exists():
            report['pso_runs_dir_mb'] = self._get_directory_size_mb(pso_runs_dir)

        # Database
        report['database_mb'] = self._get_database_size_mb()

        # Logs
        logs_dir = Path(self.data_manager.logs_path)
        if logs_dir.exists():
            report['logs_mb'] = self._get_directory_size_mb(logs_dir)

        # Total
        report['total_mb'] = (
            report['runs_dir_mb'] +
            report['pso_runs_dir_mb'] +
            report['database_mb'] +
            report['logs_mb']
        )

        return report
