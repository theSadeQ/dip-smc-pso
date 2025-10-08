#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/ai_query_generator.py
# ═══════════════════════════════════════════════════════════════════════════
"""
AI-Enhanced Query Generation for Academic Research.

Uses LLM to generate intelligent search queries from claims with minimal context.
Dramatically improves citation quality for CODE-IMPL and generic claims.

Usage:
    python ai_query_generator.py --input claims.json --output enhanced_claims.json
    python ai_query_generator.py --claim "Professional simulation framework" --interactive
"""

import json
import argparse
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
import anthropic
import os


class AIQueryGenerator:
    """
    Generate intelligent academic search queries using Claude.

    Transforms weak claims like "Professional simulation framework"
    into targeted queries like "numerical integration methods nonlinear
    dynamics control systems real-time simulation".
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI query generator.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY env var "
                "or pass api_key parameter."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def _build_query_prompt(self, claim: Dict) -> str:
        """
        Build prompt for AI query generation.

        Args:
            claim: Claim object with text, file_path, context, etc.

        Returns:
            Formatted prompt for Claude
        """
        claim_text = claim.get("claim_text") or claim.get("statement", "")
        file_path = claim.get("file_path", "")
        context = claim.get("context", "")
        category = claim.get("category", "")

        # Extract module from file path for domain context
        module = "control systems"
        if "optimization" in file_path.lower():
            module = "optimization algorithms"
        elif "controller" in file_path.lower():
            module = "control systems"
        elif "simulation" in file_path.lower():
            module = "numerical simulation"
        elif "plant" in file_path.lower() or "dynamics" in file_path.lower():
            module = "dynamics modeling"

        prompt = f"""You are an expert academic research assistant specializing in control systems, optimization, and robotics.

Your task: Generate 1-3 high-quality academic search queries for finding relevant papers.

CLAIM INFORMATION:
- Main claim: "{claim_text}"
- Module/Domain: {module}
- Category: {category}
- File: {file_path}
"""

        if context:
            prompt += f"- Context snippet: {context[:200]}...\n"

        prompt += """
REQUIREMENTS:
1. Generate queries that will find RELEVANT academic papers
2. Focus on the underlying ALGORITHM or THEORY, not generic terms
3. Include technical keywords that researchers actually use
4. Avoid overly generic terms like "professional" or "framework"
5. Return 1-3 queries, each on a new line
6. Keep queries concise (5-10 words each)

EXAMPLES:

Input: "Professional simulation framework for control engineering"
Output:
numerical integration methods nonlinear dynamics control systems
real-time simulation embedded control applications
Runge-Kutta methods state-space modeling

Input: "PSO optimization for controller gains"
Output:
particle swarm optimization PID tuning control systems
metaheuristic algorithms controller parameter optimization
swarm intelligence nonlinear control design

Input: "Lyapunov stability analysis for sliding mode control"
Output:
Lyapunov function sliding mode control stability proof
variable structure control systems Lyapunov theory
robust control Lyapunov stability analysis

NOW GENERATE QUERIES FOR THE CLAIM ABOVE:
"""
        return prompt

    def generate_queries(self, claim: Dict) -> List[str]:
        """
        Generate AI-enhanced queries for a single claim.

        Args:
            claim: Claim object

        Returns:
            List of 1-3 search queries
        """
        prompt = self._build_query_prompt(claim)

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # Parse queries (one per line)
            queries = [
                line.strip()
                for line in response_text.split('\n')
                if line.strip() and not line.startswith('#')
            ]

            # Limit to 3 queries max
            return queries[:3]

        except Exception as e:
            print(f"Error generating queries for {claim.get('id')}: {e}")
            # Fallback to claim text
            return [claim.get("claim_text", "")[:100]]

    async def generate_queries_batch(
        self,
        claims: List[Dict],
        max_concurrent: int = 5
    ) -> List[Dict]:
        """
        Generate queries for multiple claims with concurrency control.

        Args:
            claims: List of claim objects
            max_concurrent: Max concurrent API requests

        Returns:
            Claims with added 'ai_queries' field
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_claim(claim):
            async with semaphore:
                # Run synchronous API call in executor
                loop = asyncio.get_event_loop()
                queries = await loop.run_in_executor(
                    None,
                    self.generate_queries,
                    claim
                )
                claim['ai_queries'] = queries
                return claim

        tasks = [process_claim(claim) for claim in claims]
        return await asyncio.gather(*tasks)

    def enhance_claims_file(
        self,
        input_file: Path,
        output_file: Path,
        max_claims: Optional[int] = None
    ) -> Dict:
        """
        Enhance an entire claims file with AI-generated queries.

        Args:
            input_file: Input JSON file with claims
            output_file: Output JSON file with ai_queries added
            max_claims: Limit processing (for testing)

        Returns:
            Summary statistics
        """
        # Load claims
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        claims = data.get('claims', [])
        if max_claims:
            claims = claims[:max_claims]

        print(f"Enhancing {len(claims)} claims with AI queries...")

        # Generate queries
        enhanced = asyncio.run(self.generate_queries_batch(claims))

        # Update data
        data['claims'] = enhanced
        data['metadata'] = data.get('metadata', {})
        data['metadata']['ai_enhanced'] = True
        data['metadata']['ai_queries_generated'] = len(enhanced)

        # Save
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Statistics
        total_queries = sum(len(c.get('ai_queries', [])) for c in enhanced)
        avg_queries = total_queries / len(enhanced) if enhanced else 0

        stats = {
            'claims_processed': len(enhanced),
            'total_queries_generated': total_queries,
            'avg_queries_per_claim': avg_queries,
            'output_file': str(output_file)
        }

        print(f"\nAI Query Generation Complete:")
        print(f"  Claims processed: {stats['claims_processed']}")
        print(f"  Total queries: {stats['total_queries_generated']}")
        print(f"  Avg queries/claim: {stats['avg_queries_per_claim']:.2f}")
        print(f"  Output: {output_file}")

        return stats


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI-enhanced academic search queries from claims"
    )
    parser.add_argument(
        '--input',
        type=str,
        help='Input claims JSON file'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output enhanced claims JSON file'
    )
    parser.add_argument(
        '--claim',
        type=str,
        help='Single claim text for interactive mode'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode for single claim'
    )
    parser.add_argument(
        '--max-claims',
        type=int,
        help='Limit number of claims to process (for testing)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )

    args = parser.parse_args()

    # Initialize generator
    generator = AIQueryGenerator(api_key=args.api_key)

    # Interactive mode
    if args.interactive:
        claim_text = args.claim or input("Enter claim text: ")
        claim = {
            'claim_text': claim_text,
            'category': 'implementation',
            'file_path': 'unknown'
        }

        print("\nGenerating queries...")
        queries = generator.generate_queries(claim)

        print("\nAI-Generated Queries:")
        for i, query in enumerate(queries, 1):
            print(f"  {i}. {query}")

        return 0

    # Batch mode
    if not args.input or not args.output:
        print("Error: --input and --output required for batch mode")
        print("Use --interactive for single claim mode")
        return 1

    input_file = Path(args.input)
    output_file = Path(args.output)

    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        return 1

    # Enhance claims
    stats = generator.enhance_claims_file(
        input_file,
        output_file,
        max_claims=args.max_claims
    )

    return 0


if __name__ == '__main__':
    exit(main())
