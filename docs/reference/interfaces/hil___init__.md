# interfaces.hil.__init__

**Source:** `src\interfaces\hil\__init__.py`

## Module Overview

Enhanced Hardware-in-the-Loop (HIL) system for control engineering.
This module provides advanced HIL capabilities including real-time simulation,
hardware integration, fault injection, and comprehensive testing frameworks
for control system validation and verification.

## Complete Source Code

```{literalinclude} ../../../src/interfaces/hil/__init__.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from .enhanced_hil import EnhancedHILSystem, HILConfig, HILMode, TestScenario`
- `from .real_time_sync import RealTimeScheduler, TimingConstraints, DeadlineMissHandler`
- `from .fault_injection import FaultInjector, FaultType, FaultScenario`
- `from .test_automation import HILTestFramework, TestSuite, TestCase`
- `from .data_logging import HILDataLogger, LoggingConfig`
- `from .simulation_bridge import SimulationBridge, ModelInterface`
- `from .controller_client import HILControllerClient, run_client`
- `from .plant_server import PlantServer`
