# Example from: docs\guides\api\utilities.md
# Index: 5
# Runnable: True
# Hash: 3216e76b

from src.utils.validation import sanitize_input

# Clean and validate user input
user_input = "  10.5, 8.0, 15.2, 12.1, 50.0, 5.5  "
gains = sanitize_input(user_input, expected_length=6)

# Returns: [10.5, 8.0, 15.2, 12.1, 50.0, 5.5]