# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 20
# Runnable: True
# Hash: bff8a052

import shutil
import json
from pathlib import Path
from datetime import datetime

class ConfigurationRecovery:
    """Handle configuration file recovery and restoration."""

    def __init__(self, config_dir='.', backup_dir='./config_backups'):
        self.config_dir = Path(config_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def create_emergency_backup(self, description="emergency"):
        """Create emergency backup of current configuration."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"config_emergency_{description}_{timestamp}.yaml"
        backup_path = self.backup_dir / backup_name

        try:
            shutil.copy2(self.config_dir / 'config.yaml', backup_path)
            print(f"✅ Emergency backup created: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"❌ Failed to create emergency backup: {e}")
            return None

    def list_available_backups(self):
        """List all available configuration backups."""
        backups = sorted(self.backup_dir.glob('config_*.yaml'))

        print("📋 Available Configuration Backups:")
        print("=" * 50)

        for i, backup in enumerate(backups, 1):
            # Extract timestamp from filename
            parts = backup.stem.split('_')
            if len(parts) >= 3:
                timestamp = f"{parts[-2]}_{parts[-1]}"
                try:
                    dt = datetime.strptime(timestamp, '%Y%m%d_%H%M%S')
                    formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_date = timestamp

                print(f"  {i:2d}. {backup.name}")
                print(f"      Date: {formatted_date}")
                print(f"      Size: {backup.stat().st_size} bytes")
                print()

        return backups

    def restore_from_backup(self, backup_index=None, backup_name=None):
        """Restore configuration from backup."""
        backups = sorted(self.backup_dir.glob('config_*.yaml'))

        if backup_index is not None:
            if 1 <= backup_index <= len(backups):
                selected_backup = backups[backup_index - 1]
            else:
                print(f"❌ Invalid backup index: {backup_index}")
                return False

        elif backup_name is not None:
            selected_backup = self.backup_dir / backup_name
            if not selected_backup.exists():
                print(f"❌ Backup not found: {backup_name}")
                return False

        else:
            print("❌ Must specify either backup_index or backup_name")
            return False

        try:
            # Create backup of current config before restoration
            self.create_emergency_backup("pre_restore")

            # Restore from backup
            shutil.copy2(selected_backup, self.config_dir / 'config.yaml')
            print(f"✅ Configuration restored from: {selected_backup.name}")

            # Validate restored configuration
            from src.config import load_config
            try:
                config = load_config('config.yaml')
                print("✅ Restored configuration is valid")
                return True
            except Exception as e:
                print(f"❌ Restored configuration is invalid: {e}")
                return False

        except Exception as e:
            print(f"❌ Failed to restore configuration: {e}")
            return False

    def restore_factory_defaults(self):
        """Restore factory default configuration."""
        default_config = {
            'global_seed': 42,
            'pso': {
                'n_particles': 50,
                'n_iterations': 100,
                'cognitive_weight': 1.49445,
                'social_weight': 1.49445,
                'inertia_weight': 0.729,
                'bounds': {
                    'classical_smc': {
                        'lower': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                        'upper': [20.0, 20.0, 20.0, 20.0, 100.0, 10.0]
                    }
                }
            },
            'cost_function': {
                'weights': {
                    'state_error': 1.0,
                    'control_effort': 0.01,
                    'control_rate': 0.001,
                    'stability': 10.0
                }
            },
            'simulation': {
                'duration': 10.0,
                'dt': 0.001
            },
            'controllers': {
                'classical_smc': {
                    'max_force': 150.0,
                    'boundary_layer': 0.02
                }
            }
        }

        try:
            # Backup current config
            self.create_emergency_backup("pre_factory_reset")

            # Write factory defaults
            import yaml
            with open(self.config_dir / 'config.yaml', 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False, indent=2)

            print("✅ Factory default configuration restored")
            return True

        except Exception as e:
            print(f"❌ Failed to restore factory defaults: {e}")
            return False

# Usage example
recovery = ConfigurationRecovery()

# List backups and restore
recovery.list_available_backups()
# recovery.restore_from_backup(backup_index=1)
# recovery.restore_factory_defaults()