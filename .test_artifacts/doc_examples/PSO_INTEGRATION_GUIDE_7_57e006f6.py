# Example from: docs\PSO_INTEGRATION_GUIDE.md
# Index: 7
# Runnable: True
# Hash: 57e006f6

# Run PSO integration tests
python -m pytest tests/test_controllers/factory/test_controller_factory.py::TestPSOIntegration -v

# Run end-to-end validation
python test_pso_integration_workflow.py