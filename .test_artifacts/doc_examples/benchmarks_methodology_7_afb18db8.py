# Example from: docs\benchmarks_methodology.md
# Index: 7
# Runnable: False
# Hash: afb18db8

# example-metadata:
# runnable: false

benchmark_metadata = {
    'timestamp': datetime.now().isoformat(),
    'config_hash': hashlib.md5(config_content).hexdigest(),
    'random_seed': 1234,
    'n_trials': 30,
    'environment': {
        'python_version': sys.version,
        'numpy_version': np.__version__,
        'platform': platform.platform()
    }
}