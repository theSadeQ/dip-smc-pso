# Example from: docs\memory_management_quick_reference.md
# Index: 7
# Runnable: True
# Hash: b34410fa

if i % 100 == 99:
    controller.cleanup()
    del controller
    gc.collect()