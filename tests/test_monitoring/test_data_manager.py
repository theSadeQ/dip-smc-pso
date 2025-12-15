#==================================================================================== #============== tests/test_monitoring/test_data_manager.py ==============
#====================================================================================

"""
Unit tests for DataManager production monitoring system.

Tests cover:
- Initialization and directory creation
- Run storage and retrieval
- Query functionality with filters
- LRU cache operations
- Live session management
- Cleanup operations
- Error handling and edge cases

Target coverage: ≥95%
"""

import pytest
import json
import tempfile
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.utils.monitoring.data_manager import DataManager, LRUCache
from src.utils.monitoring.data_model import (
    DashboardData,
    PerformanceSummary,
    MetricsSnapshot,
    RunStatus
)


# Fixtures

@pytest.fixture
def temp_monitoring_dir():
    """Create temporary directory for monitoring data."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def data_manager(temp_monitoring_dir):
    """Create DataManager with temporary directory."""
    return DataManager(base_path=temp_monitoring_dir)


@pytest.fixture
def sample_dashboard_data():
    """Create sample DashboardData for testing."""
    summary = PerformanceSummary(
        settling_time_s=2.34,
        rise_time_s=0.89,
        overshoot_pct=12.5,
        steady_state_error=0.003,
        energy_j=45.67,
        total_variation=123.45,
        peak_control=89.12,
        stability_margin=0.85,
        lyapunov_decrease_rate=-0.12,
        bounded_states=True,
        chattering_frequency_hz=12.5,
        chattering_amplitude=0.23,
        chattering_total_variation=67.89
    )

    snapshots = []
    for i in range(10):
        snapshot = MetricsSnapshot(
            timestamp_s=i * 0.01,
            time_step=i,
            controller_type="adaptive_smc",
            state=[0.1 - i*0.01, 0.0, 0.05 - i*0.005, 0.0],
            control_output=2.5 * (1 - i*0.1),
            error_norm=0.1 - i*0.01,
            angle1_rad=0.1 - i*0.01,
            angle2_rad=0.0,
            velocity1_rad_s=0.05 - i*0.005,
            velocity2_rad_s=0.0
        )
        snapshots.append(snapshot)

    data = DashboardData(
        run_id="2025-12-15_140000_adaptive_smc_nominal",
        controller="adaptive_smc",
        scenario="nominal",
        config={"gains": [10.0, 5.0, 8.0]},
        snapshots=snapshots,
        summary=summary,
        status=RunStatus.COMPLETE
    )

    return data


# Test LRU Cache

class TestLRUCache:
    """Test LRU cache functionality."""

    def test_cache_initialization(self):
        """Test cache initializes with correct size."""
        cache = LRUCache(max_size=5)
        assert cache.max_size == 5
        assert len(cache.cache) == 0
        assert cache.hits == 0
        assert cache.misses == 0

    def test_cache_put_and_get(self, sample_dashboard_data):
        """Test storing and retrieving items from cache."""
        cache = LRUCache(max_size=3)

        cache.put("run1", sample_dashboard_data)
        assert cache.get("run1") == sample_dashboard_data
        assert cache.hits == 1
        assert cache.misses == 0

    def test_cache_miss(self):
        """Test cache miss increments miss counter."""
        cache = LRUCache(max_size=3)

        result = cache.get("nonexistent")
        assert result is None
        assert cache.misses == 1
        assert cache.hits == 0

    def test_cache_lru_eviction(self, sample_dashboard_data):
        """Test LRU eviction when cache is full."""
        cache = LRUCache(max_size=2)

        # Add 3 items (should evict oldest)
        cache.put("run1", sample_dashboard_data)
        cache.put("run2", sample_dashboard_data)
        cache.put("run3", sample_dashboard_data)

        # run1 should be evicted
        assert cache.get("run1") is None
        assert cache.get("run2") is not None
        assert cache.get("run3") is not None

    def test_cache_lru_access_order(self, sample_dashboard_data):
        """Test LRU maintains access order."""
        cache = LRUCache(max_size=2)

        cache.put("run1", sample_dashboard_data)
        cache.put("run2", sample_dashboard_data)

        # Access run1 to make it most recent
        cache.get("run1")

        # Add run3 (should evict run2, not run1)
        cache.put("run3", sample_dashboard_data)

        assert cache.get("run1") is not None  # Still in cache
        assert cache.get("run2") is None      # Evicted
        assert cache.get("run3") is not None

    def test_cache_clear(self, sample_dashboard_data):
        """Test cache clear resets all state."""
        cache = LRUCache(max_size=3)

        cache.put("run1", sample_dashboard_data)
        cache.get("run1")
        cache.get("nonexistent")

        cache.clear()

        assert len(cache.cache) == 0
        assert cache.hits == 0
        assert cache.misses == 0

    def test_cache_get_stats(self, sample_dashboard_data):
        """Test cache statistics calculation."""
        cache = LRUCache(max_size=5)

        cache.put("run1", sample_dashboard_data)
        cache.put("run2", sample_dashboard_data)

        cache.get("run1")  # hit
        cache.get("run1")  # hit
        cache.get("run3")  # miss

        stats = cache.get_stats()
        assert stats['size'] == 2
        assert stats['max_size'] == 5
        assert stats['hits'] == 2
        assert stats['misses'] == 1
        assert stats['hit_rate_pct'] == pytest.approx(66.67, rel=0.01)


# Test DataManager Initialization

class TestDataManagerInitialization:
    """Test DataManager initialization."""

    def test_initialization_creates_directories(self, temp_monitoring_dir):
        """Test initialization creates all required directories."""
        dm = DataManager(base_path=temp_monitoring_dir)

        assert dm.runs_path.exists()
        assert dm.pso_path.exists()
        assert dm.benchmarks_path.exists()
        assert dm.cache_path.exists()
        assert dm.logs_path.exists()

    def test_initialization_creates_database(self, temp_monitoring_dir):
        """Test initialization creates SQLite database."""
        dm = DataManager(base_path=temp_monitoring_dir)

        assert dm.db_path.exists()

        # Check tables exist
        conn = sqlite3.connect(dm.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        assert 'runs' in tables
        assert 'pso_runs' in tables
        assert 'benchmarks' in tables

        conn.close()

    def test_initialization_creates_indexes(self, temp_monitoring_dir):
        """Test initialization creates database indexes."""
        dm = DataManager(base_path=temp_monitoring_dir)

        conn = sqlite3.connect(dm.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]

        assert 'idx_runs_controller' in indexes
        assert 'idx_runs_timestamp' in indexes
        assert 'idx_runs_score' in indexes
        assert 'idx_pso_controller' in indexes

        conn.close()

    def test_initialization_creates_cache(self, data_manager):
        """Test initialization creates LRU cache."""
        assert isinstance(data_manager.cache, LRUCache)
        assert data_manager.cache.max_size == 100


# Test Run Storage and Retrieval

class TestRunStorage:
    """Test run storage and retrieval operations."""

    def test_generate_run_id(self, data_manager):
        """Test run ID generation format."""
        run_id = data_manager.generate_run_id("adaptive_smc", "nominal")

        assert "adaptive_smc" in run_id
        assert "nominal" in run_id
        assert len(run_id.split('_')) == 4  # date_time_controller_scenario

    def test_store_run_creates_files(self, data_manager, sample_dashboard_data):
        """Test storing run creates all required files."""
        run_id = data_manager.store_run(sample_dashboard_data, save_timeseries=True)

        run_dir = data_manager.runs_path / run_id

        assert (run_dir / "metadata.json").exists()
        assert (run_dir / "timeseries.csv").exists()
        assert (run_dir / "config.yaml").exists()

    def test_store_run_metadata_structure(self, data_manager, sample_dashboard_data):
        """Test metadata JSON has correct structure."""
        run_id = data_manager.store_run(sample_dashboard_data, save_timeseries=False)

        metadata_path = data_manager.runs_path / run_id / "metadata.json"

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        assert 'run_id' in metadata
        assert 'controller' in metadata
        assert 'scenario' in metadata
        assert 'performance' in metadata
        assert 'status' in metadata

        # Check performance metrics
        perf = metadata['performance']
        assert 'settling_time_s' in perf
        assert 'overshoot_pct' in perf
        assert 'energy_j' in perf

    def test_store_run_without_timeseries(self, data_manager, sample_dashboard_data):
        """Test storing run without time-series data."""
        run_id = data_manager.store_run(sample_dashboard_data, save_timeseries=False)

        run_dir = data_manager.runs_path / run_id

        assert (run_dir / "metadata.json").exists()
        assert not (run_dir / "timeseries.csv").exists()

    def test_store_run_updates_index(self, data_manager, sample_dashboard_data):
        """Test storing run updates SQLite index."""
        run_id = data_manager.store_run(sample_dashboard_data)

        conn = sqlite3.connect(data_manager.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT run_id, controller, scenario FROM runs WHERE run_id = ?", (run_id,))
        row = cursor.fetchone()

        assert row is not None
        assert row[1] == "adaptive_smc"
        assert row[2] == "nominal"

        conn.close()

    def test_store_run_updates_cache(self, data_manager, sample_dashboard_data):
        """Test storing run updates L2 cache."""
        run_id = data_manager.store_run(sample_dashboard_data)

        cached_data = data_manager.cache.get(run_id)
        assert cached_data is not None
        assert cached_data.run_id == run_id

    def test_load_metadata_from_disk(self, data_manager, sample_dashboard_data):
        """Test loading metadata from disk."""
        run_id = data_manager.store_run(sample_dashboard_data)

        # Clear cache to force disk load
        data_manager.cache.clear()

        loaded_data = data_manager.load_metadata(run_id)

        assert loaded_data is not None
        assert loaded_data.run_id == run_id
        assert loaded_data.controller == "adaptive_smc"
        assert loaded_data.summary.settling_time_s == pytest.approx(2.34)

    def test_load_metadata_from_cache(self, data_manager, sample_dashboard_data):
        """Test loading metadata from cache (cache hit)."""
        run_id = data_manager.store_run(sample_dashboard_data)

        # First load (cache hit after store)
        loaded_data = data_manager.load_metadata(run_id)

        assert data_manager.cache.hits > 0
        assert loaded_data.run_id == run_id

    def test_load_metadata_nonexistent(self, data_manager):
        """Test loading non-existent metadata returns None."""
        result = data_manager.load_metadata("nonexistent_run")

        assert result is None

    def test_load_timeseries(self, data_manager, sample_dashboard_data):
        """Test loading time-series data."""
        run_id = data_manager.store_run(sample_dashboard_data, save_timeseries=True)

        df = data_manager.load_timeseries(run_id)

        assert df is not None
        assert len(df) == 10  # 10 snapshots
        assert 'time' in df.columns
        assert 'x1' in df.columns
        assert 'u' in df.columns

    def test_load_timeseries_nonexistent(self, data_manager):
        """Test loading non-existent time-series returns None."""
        df = data_manager.load_timeseries("nonexistent_run")

        assert df is None


# Test Query Functionality

class TestQueryFunctionality:
    """Test query operations with filters."""

    def test_query_runs_all(self, data_manager, sample_dashboard_data):
        """Test querying all runs."""
        # Store multiple runs
        for i in range(5):
            data = sample_dashboard_data
            data.run_id = f"2025-12-15_14{i:02d}00_adaptive_smc_nominal"
            data_manager.store_run(data)

        results = data_manager.query_runs(limit=10)

        assert len(results) == 5

    def test_query_runs_by_controller(self, data_manager, sample_dashboard_data):
        """Test filtering by controller type."""
        # Store runs with different controllers
        for ctrl in ["adaptive_smc", "classical_smc", "sta_smc"]:
            data = sample_dashboard_data
            data.run_id = f"2025-12-15_140000_{ctrl}_nominal"
            data.controller = ctrl
            data_manager.store_run(data)

        results = data_manager.query_runs(controller="adaptive_smc")

        assert len(results) == 1
        assert results[0].controller == "adaptive_smc"

    def test_query_runs_by_scenario(self, data_manager, sample_dashboard_data):
        """Test filtering by scenario."""
        # Store runs with different scenarios
        for scenario in ["nominal", "disturbance", "tracking"]:
            data = sample_dashboard_data
            data.run_id = f"2025-12-15_140000_adaptive_smc_{scenario}"
            data.scenario = scenario
            data_manager.store_run(data)

        results = data_manager.query_runs(scenario="disturbance")

        assert len(results) == 1
        assert results[0].scenario == "disturbance"

    def test_query_runs_pagination(self, data_manager, sample_dashboard_data):
        """Test pagination with limit and offset."""
        # Store 10 runs
        for i in range(10):
            data = sample_dashboard_data
            data.run_id = f"2025-12-15_14{i:02d}00_adaptive_smc_nominal"
            data_manager.store_run(data)

        # Get first page
        page1 = data_manager.query_runs(limit=3, offset=0)
        assert len(page1) == 3

        # Get second page
        page2 = data_manager.query_runs(limit=3, offset=3)
        assert len(page2) == 3

        # Ensure different runs
        assert page1[0].run_id != page2[0].run_id

    def test_query_runs_ordering(self, data_manager, sample_dashboard_data):
        """Test ordering by timestamp."""
        # Store runs in random order
        for i in [2, 0, 1]:
            data = sample_dashboard_data
            data.run_id = f"2025-12-15_14{i:02d}00_adaptive_smc_nominal"
            data_manager.store_run(data)

        results = data_manager.query_runs(order_by='timestamp', ascending=True)

        # Should be ordered chronologically
        assert "1400" in results[0].run_id
        assert "1401" in results[1].run_id
        assert "1402" in results[2].run_id


# Test Live Session Management

class TestLiveSessionManagement:
    """Test live monitoring session management."""

    def test_start_live_session(self, data_manager):
        """Test starting a live monitoring session."""
        session_id = data_manager.start_live_session("adaptive_smc", "nominal")

        assert session_id.startswith("live_")
        assert session_id in data_manager._live_sessions

        session = data_manager._live_sessions[session_id]
        assert session['controller'] == "adaptive_smc"
        assert session['scenario'] == "nominal"
        assert session['metrics_file'].exists()

    def test_get_live_metrics_empty(self, data_manager):
        """Test getting metrics from new live session."""
        session_id = data_manager.start_live_session("adaptive_smc")

        df = data_manager.get_live_metrics(session_id)

        # New session has header but no data yet
        assert df is not None
        assert len(df) == 0

    def test_get_live_metrics_nonexistent(self, data_manager):
        """Test getting metrics from non-existent session."""
        df = data_manager.get_live_metrics("nonexistent_session")

        assert df is None

    def test_stop_live_session(self, data_manager):
        """Test stopping a live session."""
        session_id = data_manager.start_live_session("adaptive_smc")

        result = data_manager.stop_live_session(session_id)

        assert session_id not in data_manager._live_sessions


# Test Cleanup Operations

class TestCleanupOperations:
    """Test cleanup and maintenance operations."""

    def test_cleanup_old_runs_dry_run(self, data_manager, sample_dashboard_data):
        """Test cleanup dry run returns list without deleting."""
        # Store run
        run_id = data_manager.store_run(sample_dashboard_data)

        # Dry run shouldn't delete
        old_runs = data_manager.cleanup_old_runs(days=0, dry_run=True)

        assert len(old_runs) > 0
        assert data_manager.load_metadata(run_id) is not None  # Still exists

    def test_cleanup_old_runs_actual(self, data_manager, sample_dashboard_data):
        """Test actual cleanup deletes old runs."""
        # Store old run
        run_id = data_manager.store_run(sample_dashboard_data)

        # Actually delete
        old_runs = data_manager.cleanup_old_runs(days=0, dry_run=False)

        assert len(old_runs) > 0
        assert data_manager.load_metadata(run_id) is None  # Deleted


# Test Error Handling

class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_load_corrupted_metadata(self, data_manager, sample_dashboard_data):
        """Test loading corrupted metadata file."""
        run_id = data_manager.store_run(sample_dashboard_data)

        # Corrupt metadata file
        metadata_path = data_manager.runs_path / run_id / "metadata.json"
        with open(metadata_path, 'w') as f:
            f.write("{ invalid json }")

        result = data_manager.load_metadata(run_id)

        assert result is None  # Should handle gracefully

    def test_get_cache_stats(self, data_manager, sample_dashboard_data):
        """Test getting cache statistics."""
        data_manager.store_run(sample_dashboard_data)

        stats = data_manager.get_cache_stats()

        assert 'size' in stats
        assert 'hit_rate_pct' in stats
        assert stats['max_size'] == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.utils.monitoring.data_manager", "--cov-report=term"])
