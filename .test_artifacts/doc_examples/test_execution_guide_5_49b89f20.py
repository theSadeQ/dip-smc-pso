# Example from: docs\test_execution_guide.md
# Index: 5
# Runnable: True
# Hash: 49b89f20

import tempfile
import pytest

@pytest.fixture
def temp_config_file():
    """Create temporary configuration file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(test_config, f)
        yield f.name
    os.unlink(f.name)