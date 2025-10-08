# Example from: docs\plans\orchestration\ci_agent_framework.md
# Index: 1
# Runnable: False
# Hash: 3c60b9b7

class AgentSelectionStrategy:
    """
    Decision framework for optimal agent configuration.
    """

    def should_reuse(self, issue_requirements: Set[str]) -> Dict[str, float]:
        """
        Calculate skill match scores for existing agents.

        Returns: {agent_name: match_score (0.0-1.0)}
        """
        scores = {}

        for agent_name, agent_spec in self.EXISTING_AGENTS.items():
            agent_skills = set(agent_spec['skills'])

            # Jaccard similarity
            intersection = issue_requirements & agent_skills
            union = issue_requirements | agent_skills

            scores[agent_name] = len(intersection) / len(union) if union else 0.0

        return scores

    def should_create_new(self, best_match_score: float,
                         workload_estimate: int) -> Dict[str, Any]:
        """
        Create new agent if:
        1. Skill gap > 30% (best_match < 0.7)
        2. Throughput gap: workload > 4 hours AND parallelizable
        3. Policy gap: CLAUDE.md mandates specialist
        """

        if best_match_score < 0.7:
            return {
                'create': True,
                'reason': 'SKILL_GAP',
                'blocking': True,
                'justification': f'No existing agent covers >70% of required skills'
            }

        if workload_estimate > 240:  # 4 hours
            return {
                'create': True,
                'reason': 'THROUGHPUT_GAP',
                'blocking': False,  # Can proceed slower
                'justification': f'{workload_estimate}min workload benefits from parallelization'
            }

        return {'create': False}