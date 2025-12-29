# QW-3: Visualize PSO Convergence

**Effort**: 2 hours | **Priority**: Medium | **Purpose**: Visual feedback + publication plots

## Quick Summary
Create PSO visualization module with convergence and diversity plots.

## Files to Create
- src/utils/visualization/pso_plots.py (~100 lines)
- Modify simulate.py (PSO plot integration)

## Functions to Implement
1. `plot_convergence(fitness_history, save_path, show, title)` - Best fitness vs generation
2. `plot_diversity(position_history, save_path, show, title)` - Particle diversity over time
3. `plot_pso_summary(fitness_history, position_history, save_path, show)` - Combined 2-panel plot

## Integration
```python
# In simulate.py after PSO optimization
from src.utils.visualization.pso_plots import plot_pso_summary

fitness_history = result['history']['cost']
position_history = result['history']['pos']

plot_pso_summary(
    fitness_history=fitness_history,
    position_history=position_history,
    save_path="pso_convergence_summary.png",
    show=True
)
```

## Test
```bash
python simulate.py --ctrl classical_smc --run-pso --plot
# Verify: pso_convergence_summary.png generated
```

## Success Criteria
- [ ] Module created with 3 functions
- [ ] Integration with simulate.py complete
- [ ] Plots generated (300 DPI, proper labels)
- [ ] Visual feedback available

See PLAN.md Task 5 for code examples.
