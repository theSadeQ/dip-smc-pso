# Example from: docs\guides\how-to\testing-validation.md
# Index: 8
# Runnable: False
# Hash: 5138e254

# 1. Write failing test
def test_new_feature():
    controller = MyController(...)
    result = controller.new_feature()
    assert result == expected_value

# 2. Implement to pass test
class MyController:
    def new_feature(self):
        # Implementation
        return expected_value

# 3. Refactor if needed