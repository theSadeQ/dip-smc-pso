# Example from: docs\tools\ast_traversal_patterns.md
# Index: 11
# Runnable: False
# Hash: d8747f1a

class Outer:
    def method(self):
        def inner():
            """Inner implements X from Y"""  # ✅ Scope: ...Outer:method:inner