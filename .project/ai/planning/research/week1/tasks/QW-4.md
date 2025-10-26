# QW-4: Add Chattering Metrics

**Effort**: 2 hours | **Priority**: High | **Enables**: MT-6 (Week 4)

## Quick Summary
Create chattering analysis module with FFT analysis, frequency detection, amplitude measurement.

## Files to Create
- src/utils/analysis/chattering.py (~150 lines)
- tests/test_utils/test_chattering.py (~50 lines)

## Functions to Implement
1. `fft_analysis(control_signal, dt)` → (freqs, magnitudes)
2. `detect_chattering_frequency(freqs, mags, threshold=10.0)` → (peak_freq, peak_amp)
3. `measure_chattering_amplitude(control_signal, dt)` → chattering_index
4. `compute_chattering_metrics(control_signal, dt)` → dict

## Test Cases
- FFT detects 10 Hz sine wave
- Chattering detection above 10 Hz threshold
- RMS amplitude measurement
- Integration test (all metrics)

## Success Criteria
- [ ] Module created with 4 functions
- [ ] Unit tests pass (4 test cases)
- [ ] Can run on simulation output
- [ ] Returns quantitative metrics

See PLAN.md Task 3 for code examples.
