# Example from: docs\configuration_integration_documentation.md
# Index: 18
# Runnable: True
# Hash: efc064e4

# ✅ Good: Use type-safe configuration classes
   @dataclass(frozen=True)
   class ControllerConfig:
       gains: List[float]
       max_force: float

   # ❌ Bad: Untyped dictionary configurations
   config = {'gains': 'should be list', 'max_force': 'not a number'}