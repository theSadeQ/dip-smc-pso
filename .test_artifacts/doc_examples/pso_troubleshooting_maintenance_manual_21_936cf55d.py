# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 21
# Runnable: True
# Hash: 936cf55d

class OptimizationResultsRecovery:
    """Recover and validate optimization results."""

    def __init__(self, results_dir='./results'):
        self.results_dir = Path(results_dir)

    def scan_for_results(self):
        """Scan for all optimization result files."""
        result_files = list(self.results_dir.glob('*.json'))
        print(f"📊 Found {len(result_files)} result files")

        valid_results = []
        corrupted_results = []

        for result_file in result_files:
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)

                # Validate result structure
                required_fields = ['controller_type', 'best_gains', 'best_cost']
                if all(field in data for field in required_fields):
                    valid_results.append(result_file)
                    print(f"✅ {result_file.name} - Valid")
                else:
                    corrupted_results.append(result_file)
                    print(f"⚠️  {result_file.name} - Missing required fields")

            except json.JSONDecodeError:
                corrupted_results.append(result_file)
                print(f"❌ {result_file.name} - JSON corruption")
            except Exception as e:
                corrupted_results.append(result_file)
                print(f"❌ {result_file.name} - Error: {e}")

        return valid_results, corrupted_results

    def recover_partial_results(self, corrupted_file):
        """Attempt to recover partial data from corrupted files."""
        print(f"🔧 Attempting recovery of {corrupted_file.name}")

        try:
            with open(corrupted_file, 'r') as f:
                content = f.read()

            # Try to extract partial JSON
            # Look for gains array pattern
            import re
            gains_pattern = r'"best_gains"\s*:\s*\[([\d.,\s]+)\]'
            gains_match = re.search(gains_pattern, content)

            if gains_match:
                gains_str = gains_match.group(1)
                gains = [float(x.strip()) for x in gains_str.split(',')]
                print(f"✅ Recovered gains: {gains}")

                # Try to extract controller type
                ctrl_pattern = r'"controller_type"\s*:\s*"([^"]+)"'
                ctrl_match = re.search(ctrl_pattern, content)

                if ctrl_match:
                    controller_type = ctrl_match.group(1)
                    print(f"✅ Recovered controller type: {controller_type}")

                    # Create minimal valid result
                    recovered_result = {
                        'controller_type': controller_type,
                        'best_gains': gains,
                        'best_cost': 'unknown',
                        'recovery_note': f"Partial recovery from {corrupted_file.name}",
                        'recovery_timestamp': datetime.now().isoformat()
                    }

                    # Save recovered result
                    recovery_file = corrupted_file.parent / f"recovered_{corrupted_file.name}"
                    with open(recovery_file, 'w') as f:
                        json.dump(recovered_result, f, indent=2)

                    print(f"✅ Recovered result saved to: {recovery_file.name}")
                    return recovery_file

        except Exception as e:
            print(f"❌ Recovery failed: {e}")

        return None

# Usage
recovery = OptimizationResultsRecovery()
valid, corrupted = recovery.scan_for_results()

# Attempt recovery of corrupted files
for corrupted_file in corrupted:
    recovery.recover_partial_results(corrupted_file)