"""Batch fix F401 unused import errors"""
import re
from pathlib import Path

# Define fixes for each file
fixes = [
    # production_readiness.py - remove unused imports
    {
        'file': 'src/integration/production_readiness.py',
        'old': '    from src.utils.coverage.monitoring import CoverageMonitor, CoverageMetrics\n    from src.integration.compatibility_matrix import CompatibilityMatrix, CompatibilityLevel',
        'new': '    from src.utils.coverage.monitoring import CoverageMonitor\n    from src.integration.compatibility_matrix import CompatibilityMatrix'
    },
    # daq_systems.py - remove unused constants
    {
        'file': 'src/interfaces/hardware/daq_systems.py',
        'old': '    import nidaqmx\n    from nidaqmx.constants import AcquisitionType, TerminalConfiguration',
        'new': '    import nidaqmx'
    },
    # real_time_sync.py - remove unused ctypes.util
    {
        'file': 'src/interfaces/hil/real_time_sync.py',
        'old': '    import ctypes\n    import ctypes.util',
        'new': '    import ctypes'
    },
    # udp_interface_deadlock_free.py - remove unused imports
    {
        'file': 'src/interfaces/network/udp_interface_deadlock_free.py',
        'old': '    from ..core.protocols import CommunicationProtocol, MessageMetadata, ConnectionState, MessageType, Priority\n    from ..core.data_types import Message, ConnectionInfo, InterfaceConfig, InterfaceType, TransportType',
        'new': '    from ..core.protocols import MessageMetadata, ConnectionState, MessageType, Priority\n    from ..core.data_types import Message, InterfaceConfig'
    },
    # stability.py - remove unused scipy imports
    {
        'file': 'src/optimization/objectives/control/stability.py',
        'old': '    from scipy import signal\n    from scipy.linalg import eigvals',
        'new': '    pass  # scipy signal and eigvals not currently used'
    },
]

# Add __all__ exports for __init__.py files
init_fixes = [
    {
        'file': 'src/optimization/__init__.py',
        'search': '^(__all__ = \\[)',
        'additions': ['BFGSOptimizer', 'RobustnessObjective', 'WeightedSumObjective', 'ParetoObjective']
    },
    {
        'file': 'src/simulation/__init__.py',
        'search': '^(__all__ = \\[)',
        'additions': ['_guard_no_nan', '_guard_energy', '_guard_bounds']
    }
]

# Apply simple string replacements
fixed_count = 0
for fix in fixes:
    filepath = Path(fix['file'])
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if fix['old'] in content:
            new_content = content.replace(fix['old'], fix['new'])
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {filepath}")
            fixed_count += 1
        else:
            print(f"Pattern not found in {filepath}")
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

# Handle __all__ additions
for init_fix in init_fixes:
    filepath = Path(init_fix['file'])
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find __all__ or add it after imports
        found_all = False
        modified = False

        for i, line in enumerate(lines):
            if '__all__' in line:
                found_all = True
                # Add items to __all__ if not present
                for item in init_fix['additions']:
                    if item not in line:
                        # Find the closing bracket and add before it
                        if i+1 < len(lines) and ']' in lines[i+1]:
                            lines[i] = lines[i].rstrip() + ',\n'
                            lines.insert(i+1, f'    "{item}",\n')
                            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Updated __all__ in {filepath}")
            fixed_count += 1
        elif not found_all:
            print(f"No __all__ found in {filepath}, may need manual addition")

    except Exception as e:
        print(f"Error updating {filepath}: {e}")

print(f"\nFixed {fixed_count} files")
