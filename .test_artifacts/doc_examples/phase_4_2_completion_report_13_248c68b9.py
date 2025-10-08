# Example from: docs\api\phase_4_2_completion_report.md
# Index: 13
# Runnable: False
# Hash: 248c68b9

# Future API
from src.controllers.factory import register_controller

@register_controller('new_controller', default_gains=[...], gain_count=4)
class NewController:
    ...