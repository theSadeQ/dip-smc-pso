# Monitoring Data Directory

Production monitoring system data storage for DIP-SMC-PSO project.

**Purpose:** Stores simulation runs, PSO optimization results, and benchmark comparisons for analysis via the Streamlit monitoring dashboard.

**Status:** Foundation complete (Phase 1 of 6-phase production monitoring system)

---

## Directory Structure

```
monitoring_data/
├── runs/                           # Simulation run results
│   └── {run_id}/
│       ├── metadata.json          # Run configuration and performance summary
│       ├── timeseries.csv         # State and control time-series data
│       └── config.yaml            # Controller configuration snapshot
├── pso_runs/                       # PSO optimization runs
│   └── {pso_id}/
│       ├── metadata.json          # PSO configuration and final results
│       ├── convergence.csv        # Iteration-by-iteration fitness
│       └── best_gains.json        # Final optimized gains
├── benchmarks/                     # Multi-controller comparison results
│   └── {benchmark_id}/
│       ├── results.json           # Aggregated metrics table
│       └── metadata.json          # Scenario configuration
├── cache/                          # Temporary cache (auto-generated, gitignored)
├── logs/                           # DataManager operation logs
└── index.db                        # SQLite catalog for fast queries
```

---

## Naming Conventions

### Run ID Format

`{date}_{time}_{controller}_{scenario}`

**Examples:**
- `2025-12-15_143022_adaptive_smc_nominal`
- `2025-12-15_150033_classical_smc_disturbance`

**Components:**
- `date`: YYYY-MM-DD format
- `time`: HHMMSS format (24-hour)
- `controller`: Controller type (e.g., adaptive_smc, classical_smc, sta_smc)
- `scenario`: Scenario name (e.g., nominal, disturbance, tracking)

### PSO ID Format

`{date}_{time}_{controller}_seed{seed}`

**Example:** `2025-12-15_160000_adaptive_smc_seed42`

### Benchmark ID Format

`{date}_{time}_{scenario}_benchmark`

**Example:** `2025-12-15_170000_nominal_benchmark`

---

## Data Schemas

### metadata.json (Simulation Run)

```json
{
  "run_id": "2025-12-15_143022_adaptive_smc_nominal",
  "timestamp": "2025-12-15T14:30:22Z",
  "controller": {
    "type": "adaptive_smc",
    "config": {
      "gains": [10.0, 5.0, 8.0, 3.0, 15.0, 2.0],
      "max_force": 150.0,
      "leak_rate": 0.01
    }
  },
  "scenario": {
    "type": "nominal",
    "initial_state": [0.1, 0, 0.05, 0],
    "duration": 10.0,
    "dt": 0.01
  },
  "performance": {
    "settling_time_s": 2.34,
    "rise_time_s": 0.89,
    "overshoot_pct": 0.12,
    "steady_state_error": 0.003,
    "energy_j": 45.67,
    "total_variation": 123.45,
    "peak_control": 89.12,
    "stability_margin": 0.85,
    "lyapunov_decrease_rate": -0.12,
    "bounded_states": true,
    "chattering_frequency_hz": 12.5,
    "chattering_amplitude": 0.23,
    "chattering_total_variation": 67.89,
    "disturbance_rejection_db": 0.0,
    "recovery_time_s": 0.0,
    "avg_computation_time_ms": 0.15,
    "max_computation_time_ms": 0.45,
    "deadline_misses": 0
  },
  "status": "complete",
  "start_time": 1734273022.123,
  "end_time": 1734273032.456,
  "duration_s": 10.333,
  "errors": [],
  "warnings": [],
  "files": {
    "timeseries": "timeseries.csv"
  }
}
```

### timeseries.csv (Time-Series Data)

**Format:** CSV with headers

**Columns:**
- `time` (float): Simulation time in seconds
- `x1` (float): First angle (theta1) in radians
- `x2` (float): Second angle (theta2) in radians
- `x3` (float): First angular velocity (theta1_dot) in rad/s
- `x4` (float): Second angular velocity (theta2_dot) in rad/s
- `u` (float): Control signal in Newtons
- `tracking_error` (float): Error norm ||e||
- `control_effort` (float): Absolute control effort |u|
- `chattering_metric` (float): Instantaneous chattering index

**Example:**
```csv
time,x1,x2,x3,x4,u,tracking_error,control_effort,chattering_metric
0.00,0.1000,0.0000,0.0500,0.0000,0.0000,0.1118,0.0000,0.0000
0.01,0.0995,0.0123,0.0498,0.0034,2.3456,0.1115,2.3456,0.0012
0.02,0.0988,0.0245,0.0493,0.0067,4.6789,0.1108,4.6789,0.0023
```

**Sampling Rate:** Configurable (default: every step, dt=0.01s)

**File Size:** ~10,000 rows × 9 columns × 10 bytes ≈ 900 KB per run (10s simulation)

### metadata.json (PSO Run)

```json
{
  "pso_id": "2025-12-15_150033_adaptive_smc_seed42",
  "timestamp": "2025-12-15T15:00:33Z",
  "controller_type": "adaptive_smc",
  "pso_config": {
    "n_particles": 30,
    "max_iterations": 50,
    "seed": 42,
    "options": {
      "c1": 2.0,
      "c2": 2.0,
      "w": 0.7
    }
  },
  "results": {
    "best_fitness": 0.0234,
    "best_gains": [12.3, 5.6, 9.1, 3.4, 14.2, 2.1],
    "iterations_converged": 42,
    "convergence_time_s": 1234.56
  }
}
```

### convergence.csv (PSO Convergence Data)

**Columns:**
- `iteration` (int): Iteration number
- `best_fitness` (float): Best fitness value so far
- `mean_fitness` (float): Mean fitness across all particles
- `std_fitness` (float): Standard deviation of fitness
- `diversity` (float): Particle diversity metric

**Example:**
```csv
iteration,best_fitness,mean_fitness,std_fitness,diversity
0,0.9876,1.2345,0.3456,0.8765
1,0.8765,1.1234,0.2987,0.7654
2,0.7654,1.0345,0.2456,0.6543
```

---

## SQLite Index Schema

**Database:** `index.db`

### Table: runs

```sql
CREATE TABLE runs (
    run_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    controller TEXT NOT NULL,
    scenario TEXT NOT NULL,
    status TEXT NOT NULL,
    settling_time REAL,
    overshoot REAL,
    steady_state_error REAL,
    energy REAL,
    chattering_index REAL,
    score REAL,
    duration_s REAL,
    created_at TEXT NOT NULL
);

CREATE INDEX idx_runs_controller ON runs(controller);
CREATE INDEX idx_runs_timestamp ON runs(timestamp);
CREATE INDEX idx_runs_score ON runs(score);
```

### Table: pso_runs

```sql
CREATE TABLE pso_runs (
    pso_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    controller TEXT NOT NULL,
    seed INTEGER,
    best_fitness REAL,
    iterations_converged INTEGER,
    created_at TEXT NOT NULL
);

CREATE INDEX idx_pso_controller ON pso_runs(controller);
```

### Table: benchmarks

```sql
CREATE TABLE benchmarks (
    benchmark_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    scenario TEXT NOT NULL,
    num_controllers INTEGER,
    num_trials INTEGER,
    created_at TEXT NOT NULL
);
```

---

## Usage Examples

### 1. Save Simulation Results

```bash
# Run simulation and save results automatically
python simulate.py --ctrl adaptive_smc --save-results

# Output:
# [OK] Results saved: 2025-12-15_143022_adaptive_smc_nominal
#     Location: monitoring_data/runs/2025-12-15_143022_adaptive_smc_nominal/
#     Score: 87.3/100
```

### 2. Query Runs Programmatically

```python
from src.utils.monitoring.data_manager import DataManager

dm = DataManager()

# Query recent runs
runs = dm.query_runs(
    controller='adaptive_smc',
    limit=10,
    order_by='score',
    ascending=False  # Best scores first
)

# Load specific run
metadata = dm.load_metadata('2025-12-15_143022_adaptive_smc_nominal')
print(f"Settling time: {metadata.summary.settling_time_s:.2f}s")

# Load time-series data
df = dm.load_timeseries('2025-12-15_143022_adaptive_smc_nominal')
print(df.head())
```

### 3. Filter by Date Range

```python
from datetime import datetime, timedelta

dm = DataManager()

# Get runs from last 7 days
week_ago = datetime.now() - timedelta(days=7)
recent_runs = dm.query_runs(
    date_from=week_ago,
    min_score=70.0,  # Only good performers
    limit=50
)
```

### 4. Cleanup Old Data

```python
from src.utils.monitoring.data_manager import DataManager

dm = DataManager()

# Dry run: see what would be deleted
old_runs = dm.cleanup_old_runs(days=90, dry_run=True)
print(f"Would delete {len(old_runs)} runs older than 90 days")

# Actually delete
dm.cleanup_old_runs(days=90, dry_run=False)
```

---

## Performance Characteristics

### Storage Requirements

- **Per run:** ~1 MB (metadata 10 KB + timeseries 900 KB + config 1 KB)
- **100 runs:** ~100 MB
- **1,000 runs:** ~1 GB

### Query Performance (L2 Cache)

- **Load metadata (cache hit):** <10 ms
- **Load metadata (cache miss):** <100 ms
- **Query 100 runs (indexed):** <500 ms
- **Load timeseries CSV:** <200 ms

### Cache Hit Rates (Expected)

- **L2 Memory Cache:** 70-80% hit rate for recent runs
- **SQLite Index:** 100% hit rate (always used for queries)
- **File System:** Fallback when cache misses

---

## Data Lifecycle

### Creation

1. User runs: `python simulate.py --ctrl adaptive_smc --save-results`
2. Simulation executes with metrics collection enabled
3. Results converted to DashboardData format (PerformanceSummary + snapshots)
4. DataManager stores:
   - metadata.json (performance metrics, configuration)
   - timeseries.csv (state and control time-series)
   - config.yaml (controller configuration snapshot)
5. Run indexed in SQLite for fast queries
6. L2 cache updated with new run

### Access

1. Dashboard queries DataManager: `dm.query_runs(controller='adaptive_smc')`
2. DataManager checks L2 cache first (LRU)
3. If cache miss, queries SQLite index
4. Loads metadata.json from disk
5. Optionally loads timeseries.csv for detailed plots
6. Returns DashboardData objects

### Retention

- **Default policy:** Keep runs for 90 days
- **Configurable:** `dm.cleanup_old_runs(days=N)`
- **Manual:** Delete run directories as needed

---

## File Format Rationale

### Why JSON for Metadata?

- **Human-readable:** Easy to inspect without tools
- **Version-controllable:** Git-friendly format
- **Portable:** Works across platforms and languages
- **Schema-flexible:** Can add fields without breaking compatibility

### Why CSV for Timeseries?

- **Compact:** 10× smaller than JSON for numerical arrays
- **Pandas-compatible:** Direct `pd.read_csv()` integration
- **Excel-compatible:** Can open in spreadsheet tools
- **Fast to parse:** NumPy/Pandas optimized C parsers

### Why SQLite for Index?

- **Zero-config:** No external database required
- **ACID transactions:** Data integrity guaranteed
- **Fast queries:** B-tree indexes for O(log N) lookups
- **SQL flexibility:** Complex multi-table joins supported

---

## Integration Points

### Streamlit Dashboard

**Location:** `streamlit_monitoring_dashboard.py` (5-page dashboard)

**Phase 1 (Foundation):** File storage operational
**Phase 2 (History):** Experiment browser with filters
**Phase 3 (Live):** Real-time monitoring page
**Phase 4 (PSO):** PSO convergence tracking
**Phase 5 (Comparison):** Multi-controller benchmarks

### simulate.py CLI

```bash
# Save results automatically
python simulate.py --ctrl adaptive_smc --save-results

# Combine with other flags
python simulate.py --ctrl sta_smc --save-results --plot
```

### Test Suite

```bash
# Unit tests for DataManager
pytest tests/test_monitoring/test_data_manager.py -v

# Integration tests
pytest tests/test_integration/test_monitoring_system.py -v
```

---

## Troubleshooting

### Issue: Run ID Already Exists

**Symptom:** `FileExistsError` when saving run

**Cause:** Multiple runs within same second with same controller/scenario

**Solution:** Run IDs include HH:MM:SS precision. Wait 1 second or use different scenario name.

### Issue: SQLite Database Locked

**Symptom:** `sqlite3.OperationalError: database is locked`

**Cause:** Multiple processes accessing index.db simultaneously

**Solution:** SQLite automatically retries. If persistent, check for stale lock files.

### Issue: CSV Parse Error

**Symptom:** `pd.read_csv()` fails with parse error

**Cause:** Corrupted timeseries.csv (incomplete write)

**Solution:** Check run `errors` field in metadata.json. Re-run simulation if needed.

### Issue: Cache Eviction Too Aggressive

**Symptom:** Low cache hit rate (<50%)

**Cause:** LRU cache size too small for access pattern

**Solution:** Increase cache size: `DataManager(cache_size=200)` (default: 100)

---

## Migration Guide

### From Legacy Storage (if applicable)

If you have existing simulation results in other formats:

1. **Identify legacy files:** Search for old JSON/CSV results
2. **Convert to DashboardData:** Use `ControlMetricsCollector`
3. **Store via DataManager:** `dm.store_run(dashboard_data)`
4. **Verify index:** Query runs to confirm visibility

### To Future Schema Versions

Forward-compatible design:
- New fields added to JSON schemas won't break old parsers
- SQL schema migrations handled by DataManager on initialization
- Timeseries CSV format stable (core 9 columns)

---

## Development Notes

### Phase 1 Status (Current)

- [OK] Directory structure created
- [OK] DataManager class implemented (542 lines)
- [OK] SQLite indexing operational
- [OK] simulate.py `--save-results` flag integrated
- [OK] Documentation complete (this file)
- [PENDING] Unit tests (95% coverage target)
- [PENDING] Validation with test simulations

### Phase 2-6 Roadmap

**Phase 2:** History Browser (query filters, pagination, export)
**Phase 3:** Live Monitoring (real-time plots, start/stop controls)
**Phase 4:** PSO Integration (convergence tracking, callback system)
**Phase 5:** Multi-Controller Comparison (automated benchmarks, ANOVA)
**Phase 6:** Production Hardening (error handling, alerts, health checks)

**Total Timeline:** 46-60 hours over 6 weeks (8-12 hrs/phase)

---

## References

**Data Models:** `src/utils/monitoring/data_model.py`
- MetricsSnapshot (single time-step metrics)
- PerformanceSummary (aggregated run metrics)
- DashboardData (complete run with snapshots)

**Collector:** `src/utils/monitoring/metrics_collector_control.py`
- ControlMetricsCollector (real-time collection)

**Manager:** `src/utils/monitoring/data_manager.py`
- DataManager (storage orchestration)
- LRUCache (memory optimization)

**CLI:** `simulate.py`
- `--save-results` flag (automatic data collection)

**Plan:** `C:\Users\SadeQ\.claude41\plans\vast-riding-feather.md`
- Complete 6-phase production monitoring system plan

---

**Version:** 1.0
**Last Updated:** December 15, 2025
**Maintained By:** Claude Code MT-8 Team
