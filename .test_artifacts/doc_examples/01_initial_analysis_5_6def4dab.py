# Example from: docs\plans\citation_system\01_initial_analysis.md
# Index: 5
# Runnable: False
# Hash: 6def4dab

class AgentSelectionStrategy:
    """
    Decision framework for optimal agent configuration.
    """

    EXISTING_AGENTS = {
        'integration_coordinator': {
            'skills': ['cross-domain orchestration', 'system health',
                      'config validation', 'debugging across components'],
            'match_score': 0.25  # For citation system
        },
        'documentation_expert': {
            'skills': ['LaTeX math', 'Sphinx docs', 'scientific writing',
                      'citation systems', 'mathematical notation'],
            'match_score': 0.35  # For citation system
        },
        'pso_optimization_engineer': {
            'skills': ['PSO tuning', 'convergence analysis'],
            'match_score': 0.10  # Low relevance
        },
        'control_systems_specialist': {
            'skills': ['SMC design', 'stability analysis'],
            'match_score': 0.15  # Domain knowledge only
        }
    }

    def should_create_new(self, requirements: Set[str]) -> bool:
        """
        Create new agent if:
        1. Skill gap > 30% (best match < 0.7)
        2. Workload > 40 hours AND parallelizable
        3. CLAUDE.md mandates specialist
        """

        best_match = max(agent['match_score']
                        for agent in self.EXISTING_AGENTS.values())

        skill_gap = 1.0 - best_match

        # Citation system: best_match = 0.35 (Doc Expert)
        # skill_gap = 0.65 (65% of requirements not covered)

        if skill_gap > 0.30:
            return True, "SKILL_GAP"

        return False, "REUSE_SUFFICIENT"