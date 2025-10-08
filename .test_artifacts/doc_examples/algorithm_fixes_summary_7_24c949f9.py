# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 7
# Runnable: False
# Hash: 24c949f9

# example-metadata:
# runnable: false

   @given(
       gains=st.lists(st.floats(min_value=0.1, max_value=50.0), min_size=4, max_size=4),
       state=st.lists(st.floats(min_value=-10.0, max_value=10.0), min_size=6, max_size=6)
   )
   def test_sliding_surface_linearity_property(self, gains, state):
       """Test linearity property for all valid parameter combinations."""
       surface = LinearSlidingSurface(gains)

       state1 = np.array(state)
       state2 = np.random.uniform(-10, 10, 6)

       s1 = surface.compute(state1)
       s2 = surface.compute(state2)
       s_combined = surface.compute(state1 + state2)

       # Mathematical property: s(x1 + x2) = s(x1) + s(x2)
       assert abs(s_combined - (s1 + s2)) < 1e-10