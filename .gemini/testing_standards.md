# Testing & Coverage Standards

## Architecture of Tests

- Unit, integration, property‑based, benchmarks, and scientific validation.
- Example patterns:

```bash
pytest tests/test_controllers/ -k "not integration"
pytest tests/ -k "full_dynamics"
pytest --benchmark-only --benchmark-compare --benchmark-compare-fail=mean:5%
```

## Coverage Targets

- **Overall** ≥ 85%
- **Critical components** (controllers, plant models, simulation engines) ≥ 95%
- **Safety‑critical** mechanisms: **100%**

## Quality Gates (MANDATORY)

- Every new `.py` file has a `test_*.py` peer.
- Every public function/method has dedicated tests.
- Validate theoretical properties for critical algorithms.
- Include performance benchmarks for perf‑critical code.
