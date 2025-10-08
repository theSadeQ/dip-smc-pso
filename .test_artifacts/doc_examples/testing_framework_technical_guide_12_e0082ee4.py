# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 12
# Runnable: True
# Hash: e0082ee4

@pytest.fixture
def mock_psutil(monkeypatch):
    """Mock psutil for systems where it's unavailable."""
    try:
        import psutil
        yield psutil
    except ImportError:
        # Provide fallback mock
        class MockProcess:
            def memory_info(self):
                return type('obj', (object,), {'rss': 1024 * 1024 * 100})()  # 100 MB

        mock_psutil_module = type('obj', (object,), {
            'Process': lambda pid: MockProcess()
        })()

        monkeypatch.setitem(__import__('sys').modules, 'psutil', mock_psutil_module)
        yield mock_psutil_module