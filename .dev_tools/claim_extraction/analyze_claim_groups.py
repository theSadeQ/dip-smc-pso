"""
Analyze claims and group by topic/algorithm for efficient batch research.

Outputs:
- Claim groups by topic (SMC, PSO, Adaptive, etc.)
- Research batch recommendations
- Suggested ChatGPT prompts per group
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict, Counter


class ClaimGroupAnalyzer:
    """Analyze and group claims by research topic for efficient batch processing."""

    # Topic detection keywords
    TOPIC_PATTERNS = {
        'sliding_mode_classical': [
            'classical smc', 'classical sliding mode', 'boundary layer',
            'chattering reduction', 'sliding surface', 'reaching law'
        ],
        'sliding_mode_super_twisting': [
            'super-twisting', 'super twisting', 'sta-smc', 'sta smc',
            'higher-order sliding', 'second-order sliding', 'twisting algorithm',
            'finite-time convergence'
        ],
        'sliding_mode_adaptive': [
            'adaptive smc', 'adaptive sliding mode', 'adaptation law',
            'online gain', 'uncertainty estimation', 'adaptive gain'
        ],
        'sliding_mode_hybrid': [
            'hybrid smc', 'hybrid adaptive', 'hybrid sliding mode',
            'mode switching', 'combined adaptive'
        ],
        'pso_optimization': [
            'pso', 'particle swarm', 'swarm optimization', 'gain tuning',
            'parameter optimization', 'pso-optimized', 'swarm intelligence'
        ],
        'lyapunov_stability': [
            'lyapunov', 'stability analysis', 'asymptotic stability',
            'global stability', 'stability proof', 'lyapunov function'
        ],
        'control_theory_general': [
            'control theory', 'feedback control', 'closed-loop',
            'controller design', 'control system'
        ],
        'inverted_pendulum': [
            'inverted pendulum', 'double pendulum', 'dip system',
            'pendulum dynamics', 'cart-pole'
        ],
        'numerical_methods': [
            'numerical stability', 'matrix regularization', 'condition number',
            'ill-conditioned', 'numerical integration', 'runge-kutta'
        ],
        'benchmarking_performance': [
            'benchmark', 'performance metric', 'ise', 'itae', 'rms error',
            'statistical analysis', 'monte carlo'
        ],
        'fault_detection': [
            'fault detection', 'fdi', 'residual', 'threshold',
            'diagnosis', 'anomaly detection'
        ],
        'hardware_in_loop': [
            'hil', 'hardware-in-the-loop', 'real-time',
            'latency', 'communication protocol'
        ]
    }

    def __init__(self, inventory_path: Path):
        """Initialize analyzer with claims inventory."""
        self.inventory_path = inventory_path
        with open(inventory_path, 'r', encoding='utf-8') as f:
            self.inventory = json.load(f)
        self.claims = self.inventory['claims']

    def detect_topics(self, claim: Dict) -> Set[str]:
        """Detect topics for a claim based on text content."""
        # Get text from claim (handle None values)
        text = ' '.join(filter(None, [
            claim.get('statement'),
            claim.get('claim_text'),
            claim.get('research_description'),
            claim.get('algorithm_name'),
            claim.get('source_attribution')
        ])).lower()

        topics = set()
        for topic, keywords in self.TOPIC_PATTERNS.items():
            if any(keyword in text for keyword in keywords):
                topics.add(topic)

        # If no specific topic, mark as general
        if not topics:
            if claim.get('category') == 'theoretical':
                topics.add('control_theory_general')
            else:
                topics.add('implementation_general')

        return topics

    def group_claims_by_topic(self) -> Dict[str, List[Dict]]:
        """Group claims by detected topics."""
        topic_groups = defaultdict(list)

        for claim in self.claims:
            topics = self.detect_topics(claim)
            for topic in topics:
                topic_groups[topic].append(claim)

        return dict(topic_groups)

    def group_claims_by_priority_and_topic(self) -> Dict[str, Dict[str, List[Dict]]]:
        """Group claims by priority, then by topic."""
        priority_topic_groups = {
            'CRITICAL': defaultdict(list),
            'HIGH': defaultdict(list),
            'MEDIUM': defaultdict(list)
        }

        for claim in self.claims:
            priority = claim.get('priority', 'UNKNOWN')
            if priority not in priority_topic_groups:
                continue

            topics = self.detect_topics(claim)
            for topic in topics:
                priority_topic_groups[priority][topic].append(claim)

        # Convert defaultdicts to regular dicts
        return {
            priority: dict(topics)
            for priority, topics in priority_topic_groups.items()
        }

    def generate_batch_recommendations(self) -> List[Dict]:
        """Generate recommended research batches with claim counts."""
        groups = self.group_claims_by_priority_and_topic()

        batches = []

        # CRITICAL batches (research first)
        for topic, claims in sorted(groups['CRITICAL'].items(), key=lambda x: -len(x[1])):
            batches.append({
                'priority': 'CRITICAL',
                'topic': topic,
                'claim_count': len(claims),
                'estimated_time_hours': len(claims) * 0.25,  # 15 min per claim
                'claim_ids': [c['id'] for c in claims],
                'research_order': 1
            })

        # HIGH batches (group by topic for efficiency)
        high_topics = sorted(groups['HIGH'].items(), key=lambda x: -len(x[1]))
        for topic, claims in high_topics:
            batches.append({
                'priority': 'HIGH',
                'topic': topic,
                'claim_count': len(claims),
                'estimated_time_hours': len(claims) * 0.2,  # 12 min per claim (faster with batching)
                'claim_ids': [c['id'] for c in claims],
                'research_order': 2
            })

        # MEDIUM batches (validation)
        for topic, claims in sorted(groups['MEDIUM'].items(), key=lambda x: -len(x[1])):
            batches.append({
                'priority': 'MEDIUM',
                'topic': topic,
                'claim_count': len(claims),
                'estimated_time_hours': len(claims) * 0.05,  # 3 min per claim (just validation)
                'claim_ids': [c['id'] for c in claims],
                'research_order': 3
            })

        return batches

    def print_summary(self):
        """Print grouping analysis summary."""
        topic_groups = self.group_claims_by_topic()
        priority_topic_groups = self.group_claims_by_priority_and_topic()

        print("="*80)
        print("CLAIM GROUPING ANALYSIS")
        print("="*80)

        print(f"\nTotal claims: {len(self.claims)}")

        # Topic distribution
        print("\nTopic Distribution (claims may have multiple topics):")
        for topic, claims in sorted(topic_groups.items(), key=lambda x: -len(x[1])):
            print(f"  {topic:35s}: {len(claims):3d} claims")

        # Priority breakdown
        print("\nPriority + Topic Breakdown:")
        for priority in ['CRITICAL', 'HIGH', 'MEDIUM']:
            topics = priority_topic_groups[priority]
            if topics:
                print(f"\n  {priority}:")
                for topic, claims in sorted(topics.items(), key=lambda x: -len(x[1])):
                    print(f"    {topic:33s}: {len(claims):3d} claims")

        # Batch recommendations
        batches = self.generate_batch_recommendations()
        print("\n" + "="*80)
        print("RECOMMENDED RESEARCH BATCHES")
        print("="*80)

        total_time = 0
        for i, batch in enumerate(batches, 1):
            if i == 1 or batch['priority'] != batches[i-2]['priority']:
                print(f"\n{batch['priority']} Priority Batches:")

            print(f"  {i:2d}. {batch['topic']:30s} | "
                  f"{batch['claim_count']:3d} claims | "
                  f"~{batch['estimated_time_hours']:.1f}h")
            total_time += batch['estimated_time_hours']

        print(f"\nTotal estimated time: {total_time:.1f} hours")
        print("="*80)

    def save_batch_plan(self, output_path: Path):
        """Save batch research plan to JSON."""
        batches = self.generate_batch_recommendations()
        priority_topic_groups = self.group_claims_by_priority_and_topic()

        # Build detailed batch plan
        batch_plan = {
            'summary': {
                'total_claims': len(self.claims),
                'total_batches': len(batches),
                'estimated_total_hours': sum(b['estimated_time_hours'] for b in batches),
                'by_priority': {
                    'CRITICAL': len([b for b in batches if b['priority'] == 'CRITICAL']),
                    'HIGH': len([b for b in batches if b['priority'] == 'HIGH']),
                    'MEDIUM': len([b for b in batches if b['priority'] == 'MEDIUM'])
                }
            },
            'batches': batches,
            'claim_details_by_batch': {}
        }

        # Add claim details for each batch
        for batch in batches:
            batch_key = f"{batch['priority']}_{batch['topic']}"
            claims_in_batch = [
                c for c in self.claims
                if c['id'] in batch['claim_ids']
            ]
            batch_plan['claim_details_by_batch'][batch_key] = claims_in_batch

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(batch_plan, f, indent=2, ensure_ascii=False)

        print(f"\nBatch plan saved to: {output_path}")


def main():
    """Main execution."""
    project_root = Path(__file__).parent.parent.parent
    inventory_path = project_root / "artifacts" / "claims_inventory.json"
    output_path = project_root / "artifacts" / "research_batch_plan.json"

    analyzer = ClaimGroupAnalyzer(inventory_path)
    analyzer.print_summary()
    analyzer.save_batch_plan(output_path)


if __name__ == "__main__":
    main()
