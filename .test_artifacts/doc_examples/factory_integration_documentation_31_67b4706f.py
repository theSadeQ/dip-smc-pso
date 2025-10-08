# Example from: docs\factory_integration_documentation.md
# Index: 31
# Runnable: True
# Hash: 67b4706f

try:
       controller = create_controller('classical_smc')
   except RuntimeError as e:
       if "timeout" in str(e).lower():
           # Retry with exponential backoff
           time.sleep(random.uniform(0.1, 0.5))
           controller = create_controller('classical_smc')
       else:
           raise