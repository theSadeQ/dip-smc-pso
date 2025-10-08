# Example from: docs\versioning_guide.md
# Index: 1
# Runnable: True
# Hash: 9696780c

# Version information
import subprocess

# Get version from git tags
try:
    version = subprocess.check_output(
        ['git', 'describe', '--tags', '--abbrev=0'],
        stderr=subprocess.DEVNULL
    ).decode('utf-8').strip()
    release = version
except:
    version = '1.0.0'
    release = '1.0.0'

# Version selector
html_context = {
    'display_github': True,
    'github_user': 'theSadeQ',
    'github_repo': 'dip-smc-pso',
    'github_version': 'main',
    'conf_py_path': '/docs/',
    'versions': [
        ('latest', '/en/latest/'),
        ('stable', '/en/stable/'),
        ('v1.0', '/en/v1.0/'),
    ]
}