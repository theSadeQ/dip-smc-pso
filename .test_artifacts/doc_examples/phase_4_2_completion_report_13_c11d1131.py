# Example from: docs\api\phase_4_2_completion_report.md
# Index: 13
# Runnable: False
# Hash: c11d1131

# example-metadata:
# runnable: false

# Future API
from src.controllers.factory import register_controller

@register_controller('new_controller', default_gains=[...], gain_count=4)
class NewController:
    ...