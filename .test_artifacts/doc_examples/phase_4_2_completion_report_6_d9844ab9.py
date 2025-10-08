# Example from: docs\api\phase_4_2_completion_report.md
# Index: 6
# Runnable: True
# Hash: d9844ab9

controller = create_controller('classical_smc', config, gains=[10,10,10,1,1,1])
# Always uses [10,10,10,1,1,1] regardless of config or defaults