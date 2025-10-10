# Streamlit Testing Workflow with Playwright MCP

**Browser Automation for Streamlit Dashboard Validation**

This workflow uses Playwright MCP server to automate testing of the Streamlit web interface for DIP-SMC-PSO simulations.

## Prerequisites

```bash
# Install Playwright browsers
npm run playwright:install

# Or directly
npx playwright install chromium

# Start Streamlit dashboard
streamlit run streamlit_app.py
# Dashboard available at: http://localhost:8501
```

## Workflow Overview

| Phase | Duration | Tests | Expected Output |
|-------|----------|-------|-----------------|
| 1. Visual Testing | 10 min | Screenshots, rendering | UI screenshots saved |
| 2. Functional Testing | 20 min | Interactions, workflows | Simulation completed |
| 3. Performance Testing | 15 min | Load time, rendering speed | Performance metrics |
| 4. Integration Testing | 20 min | End-to-end workflows | Full workflow validated |

**Total Time:** ~65 minutes

## Phase 1: Visual Testing (10 min)

### Goal
Verify all UI elements render correctly without visual errors.

### Test Cases

#### 1.1 Screenshot Dashboard Home
```plaintext
Request: "Screenshot Streamlit dashboard at localhost:8501"

Expected:
- Full page screenshot saved
- All UI elements visible
- No rendering errors
- Plots properly displayed
```

#### 1.2 Capture Simulation Results
```plaintext
Request: "Screenshot simulation results page with classical SMC"

Steps:
1. Select "Classical SMC" controller
2. Click "Run Simulation"
3. Wait for completion
4. Screenshot results page

Expected:
- State trajectory plots visible
- Control input plots rendered
- Sliding surface plot displayed
- Performance metrics shown
```

#### 1.3 Verify Plot Rendering
```plaintext
Request: "Capture all plots on the dashboard"

Expected:
- Time-domain plots (states, controls)
- Phase-plane plots
- Lyapunov function plots
- PSO convergence plots (if applicable)
```

### Validation Criteria
- ✅ All screenshots captured successfully
- ✅ No blank or error placeholders
- ✅ Plots render with correct data
- ✅ UI elements properly aligned

## Phase 2: Functional Testing (20 min)

### Goal
Test user interactions and workflow execution.

### Test Cases

#### 2.1 Controller Selection
```plaintext
Request: "Test controller selection dropdown"

Steps:
1. Click controller dropdown
2. Verify options: Classical SMC, STA SMC, Adaptive SMC, Hybrid SMC
3. Select each controller
4. Verify parameter form updates

Expected:
- All 4 controllers available
- Parameter forms change per controller
- Gain inputs match controller requirements
```

#### 2.2 Parameter Input Forms
```plaintext
Request: "Test parameter input validation"

Steps:
1. Enter invalid gains (e.g., negative)
2. Enter valid gains
3. Click "Run Simulation"

Expected:
- Invalid inputs rejected with error message
- Valid inputs accepted
- Simulation starts successfully
```

#### 2.3 PSO Optimization Trigger
```plaintext
Request: "Test PSO optimization workflow"

Steps:
1. Select controller (e.g., Classical SMC)
2. Click "Optimize with PSO"
3. Configure PSO parameters (swarm size, iterations)
4. Click "Start Optimization"
5. Monitor progress
6. View optimized gains

Expected:
- PSO configuration UI appears
- Optimization runs with progress bar
- Convergence plot updates in real-time
- Optimized gains displayed
```

#### 2.4 Configuration Loading
```plaintext
Request: "Test configuration file upload"

Steps:
1. Prepare test config YAML
2. Use file uploader
3. Click "Load Configuration"
4. Verify parameters loaded

Expected:
- File upload successful
- Configuration parsed correctly
- All parameters populated
- Ready for simulation
```

### Validation Criteria
- ✅ All interactive elements functional
- ✅ Form validation working correctly
- ✅ Simulations execute without errors
- ✅ Results displayed properly

## Phase 3: Performance Testing (15 min)

### Goal
Measure dashboard performance and identify bottlenecks.

### Metrics to Collect

#### 3.1 Dashboard Load Time
```plaintext
Request: "Measure dashboard load time at localhost:8501"

Metrics:
- Initial page load: <3 seconds
- Time to interactive: <5 seconds
- Resource loading: <2 seconds

Expected:
- Load time within acceptable range
- No timeout errors
- All assets loaded successfully
```

#### 3.2 Simulation Execution Speed
```plaintext
Request: "Measure classical SMC simulation execution time"

Steps:
1. Start timer
2. Click "Run Simulation"
3. Wait for completion
4. Record duration

Expected:
- 10-second simulation: <5 seconds execution
- 30-second simulation: <15 seconds execution
- Progress updates smooth (no freezing)
```

#### 3.3 Plot Rendering Performance
```plaintext
Request: "Monitor plot rendering time"

Test:
1. Generate simulation with many data points
2. Measure time to render plots
3. Check for lag/freezing

Expected:
- Plots render in <2 seconds
- No UI freezing during render
- Smooth animations (if applicable)
```

### Validation Criteria
- ✅ Load time <5 seconds
- ✅ Simulation time within 2x real-time
- ✅ Plot rendering <2 seconds
- ✅ No performance degradation over time

## Phase 4: Integration Testing (20 min)

### Goal
Validate complete end-to-end workflows.

### Test Scenarios

#### 4.1 Classical SMC Simulation Workflow
```plaintext
Request: "Test complete classical SMC workflow"

Steps:
1. Open dashboard
2. Select "Classical SMC"
3. Enter default gains: [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
4. Set simulation time: 10 seconds
5. Click "Run Simulation"
6. Wait for completion
7. Verify results
8. Download results (if available)

Expected:
- Simulation completes successfully
- Pendulum stabilized (final state near zero)
- Control inputs within bounds
- Results downloadable
```

#### 4.2 PSO Optimization → Simulation Workflow
```plaintext
Request: "Test PSO optimization followed by simulation"

Steps:
1. Select "Classical SMC"
2. Click "Optimize with PSO"
3. Configure: 30 particles, 50 iterations
4. Run optimization
5. Wait for convergence
6. Load optimized gains
7. Run simulation with optimized gains
8. Compare performance

Expected:
- PSO converges successfully
- Optimized gains improve performance
- Simulation stable with optimized gains
- Performance metrics better than default
```

#### 4.3 Controller Comparison Workflow
```plaintext
Request: "Test controller comparison feature"

Steps:
1. Select multiple controllers
2. Configure identical simulation conditions
3. Run comparison
4. View side-by-side results

Expected:
- Multiple controllers selectable
- Simulations run in parallel or sequence
- Results displayed side-by-side
- Performance comparison table shown
```

#### 4.4 Configuration → Simulation → Analysis
```plaintext
Request: "Test complete workflow from config to analysis"

Steps:
1. Upload configuration YAML
2. Verify parameters loaded
3. Run simulation
4. Generate performance report
5. Download results
6. Verify output files

Expected:
- Config loaded correctly
- Simulation executes
- Report generated with metrics
- Files downloadable (CSV, JSON, plots)
```

### Validation Criteria
- ✅ All workflows complete end-to-end
- ✅ No errors or exceptions
- ✅ Results match expectations
- ✅ Data export functional

## Playwright MCP Usage Examples

### Basic Screenshot
```plaintext
You: Screenshot Streamlit dashboard at localhost:8501

Claude (via Playwright MCP):
1. Navigates to http://localhost:8501
2. Waits for page load
3. Captures full-page screenshot
4. Saves to: streamlit_dashboard_YYYYMMDD_HHMMSS.png
```

### Interactive Testing
```plaintext
You: Test classical SMC simulation
1. Navigate to localhost:8501
2. Click controller dropdown
3. Select "Classical SMC"
4. Enter gains: [10, 5, 8, 3, 15, 2]
5. Click "Run Simulation"
6. Wait for completion (check for "Simulation Complete" text)
7. Screenshot results page

Claude (via Playwright MCP):
[Executes steps]
✅ Simulation completed successfully
✅ Screenshot saved: classical_smc_results.png
✅ Final state: [0.001, 0.002, 0.001, 0.003, 0.002, 0.001]
```

### Performance Monitoring
```plaintext
You: Measure dashboard load time

Claude (via Playwright MCP):
- Initial load: 2.3 seconds
- Time to interactive: 4.1 seconds
- Largest contentful paint: 1.8 seconds
- First input delay: 120ms
✅ Performance within acceptable range
```

## Report Template

```markdown
# Streamlit Dashboard Test Report
**Date:** YYYY-MM-DD
**Dashboard:** http://localhost:8501
**Playwright Version:** X.XX.X

## Visual Testing Results

| Test Case | Status | Screenshot | Notes |
|-----------|--------|------------|-------|
| Homepage render | ✅ Pass | home.png | All elements visible |
| Simulation results | ✅ Pass | results.png | Plots rendered correctly |
| PSO convergence | ⚠️ Warn | pso.png | Minor axis label overlap |

## Functional Testing Results

| Feature | Status | Details |
|---------|--------|---------|
| Controller selection | ✅ Pass | All 4 controllers available |
| Parameter validation | ✅ Pass | Invalid inputs rejected |
| Simulation execution | ✅ Pass | Completes in 4.2s |
| PSO optimization | ✅ Pass | Converges after 35 iterations |

## Performance Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Load time | 2.3s | <5s | ✅ Pass |
| Simulation time (10s) | 4.1s | <10s | ✅ Pass |
| Plot rendering | 1.8s | <2s | ✅ Pass |
| Memory usage | 450MB | <1GB | ✅ Pass |

## Integration Test Results

| Workflow | Status | Duration | Issues |
|----------|--------|----------|--------|
| Classical SMC | ✅ Pass | 15s | None |
| PSO → Simulation | ✅ Pass | 3m 20s | None |
| Controller comparison | ⚠️ Warn | 45s | Slight UI lag with 4 controllers |
| Config → Analysis | ✅ Pass | 25s | None |

## Issues Found

1. **Minor:** Axis labels overlap on PSO convergence plot with long titles
   - Severity: Low
   - Workaround: Shorten plot titles
   - Fix: Adjust plot layout in `streamlit_app.py`

2. **Performance:** UI lag when comparing 4 controllers simultaneously
   - Severity: Medium
   - Workaround: Compare 2 at a time
   - Fix: Implement async rendering or pagination

## Recommendations

1. ✅ Overall dashboard stable and functional
2. ⚠️ Consider adding loading spinners for long operations
3. ⚠️ Implement result caching for repeated simulations
4. ✅ Add export functionality for all plots
5. ⚠️ Improve mobile responsiveness (optional)

## Next Steps

- [ ] Fix axis label overlap in PSO plots
- [ ] Optimize controller comparison rendering
- [ ] Add more visual regression tests
- [ ] Implement automated test suite with Playwright
```

## Automation Script Example

```python
# tests/test_streamlit_dashboard.py
"""
Automated Streamlit testing with Playwright.
Run via Playwright MCP or directly with pytest-playwright.
"""

def test_dashboard_loads(page):
    """Test dashboard loads successfully."""
    page.goto("http://localhost:8501")
    page.wait_for_selector("h1")  # Wait for title
    assert "DIP SMC PSO" in page.title()

def test_classical_smc_simulation(page):
    """Test classical SMC simulation workflow."""
    page.goto("http://localhost:8501")

    # Select controller
    page.select_option("#controller-dropdown", "Classical SMC")

    # Enter gains
    gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
    for i, gain in enumerate(gains):
        page.fill(f"#gain-{i}", str(gain))

    # Run simulation
    page.click("button:has-text('Run Simulation')")

    # Wait for completion
    page.wait_for_selector("text=Simulation Complete", timeout=30000)

    # Verify results
    assert page.is_visible("#results-plots")
    assert page.is_visible("#performance-metrics")

def test_pso_optimization(page):
    """Test PSO optimization workflow."""
    page.goto("http://localhost:8501")

    page.select_option("#controller-dropdown", "Classical SMC")
    page.click("button:has-text('Optimize with PSO')")

    # Configure PSO
    page.fill("#swarm-size", "30")
    page.fill("#iterations", "50")

    # Run optimization
    page.click("button:has-text('Start Optimization')")

    # Wait for convergence (may take a few minutes)
    page.wait_for_selector("text=Optimization Complete", timeout=300000)

    # Verify optimized gains loaded
    assert page.is_visible("#optimized-gains")
```

## Troubleshooting

### Issue: Playwright Cannot Connect

```bash
# Check Streamlit is running
curl http://localhost:8501  # Should return HTML

# Check Playwright installation
npx playwright --version

# Reinstall browsers if needed
npx playwright install --force
```

### Issue: Screenshots Blank

```bash
# Increase wait time
page.wait_for_load_state("networkidle")  # Wait for all network requests

# Check console errors
page.on("console", lambda msg: print(f"Console: {msg.text}"))
```

### Issue: Timeout Errors

```bash
# Increase timeout for slow operations
page.wait_for_selector("selector", timeout=60000)  # 60 seconds

# Use polling for dynamic content
page.wait_for_function("() => document.querySelector('.plot').complete")
```

---

**Version:** 1.0.0
**Last Updated:** 2025-10-10
**Estimated Duration:** 65 minutes
**Playwright MCP:** @modelcontextprotocol/server-playwright v0.6.2
