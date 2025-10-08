# Example from: docs\tools\ast_traversal_patterns.md
# Index: 11
# Runnable: False
# Hash: 909d6b2d

# example-metadata:
# runnable: false

class Outer:
    def method(self):
        def inner():
            """Inner implements X from Y"""  # ✅ Scope: ...Outer:method:inner