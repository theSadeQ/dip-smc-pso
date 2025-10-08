# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 11
# Runnable: True
# Hash: ae68b95f

@pytest.fixture
def temp_output_dir(tmp_path):
    """Provide temporary directory for test outputs."""
    output_dir = tmp_path / "test_outputs"
    output_dir.mkdir()
    yield output_dir
    # Cleanup handled automatically by pytest tmp_path