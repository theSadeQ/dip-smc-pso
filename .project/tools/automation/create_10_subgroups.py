#!/usr/bin/env python3
"""
Split 91 claims into 10 logical subgroups for ChatGPT processing
"""
import json
from pathlib import Path
from collections import defaultdict

# Load remaining claims
remaining_path = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/remaining_91_claims.json')
with open(remaining_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    all_claims = data['full_claims']

# Create 10 logical subgroups based on functionality and module
subgroups = {
    'group_01_smc_adaptive_hybrid': {
        'name': 'SMC Algorithms - Adaptive & Hybrid',
        'description': 'Adaptive parameter estimation (RLS), hybrid switching logic',
        'claim_ids': [
            'CODE-IMPL-132',  # Online estimation module
            'CODE-IMPL-135',  # RLS algorithm
            'CODE-IMPL-150',  # Initialize hybrid controllers
            'CODE-IMPL-152',  # Hybrid switching logic
            'CODE-IMPL-155',  # Switching based on control effort
            'CODE-IMPL-157',  # Switching based on adaptation rate
            'CODE-IMPL-159',  # Switching based on time
            'CODE-IMPL-121',  # Named tuples for adaptive SMC
            'CODE-IMPL-122',  # Set dynamics model
        ]
    },

    'group_02_smc_core': {
        'name': 'SMC Core - Equivalent Control & Switching',
        'description': 'Equivalent control computation, switching functions, chattering mitigation',
        'claim_ids': [
            'CODE-IMPL-181',  # Equivalent control module
            'CODE-IMPL-182',  # Initialize equivalent control
            'CODE-IMPL-183',  # Gain validation
            'CODE-IMPL-192',  # Chattering in practice
            'CODE-IMPL-193',  # Switching function derivative
            'CODE-IMPL-194',  # Hyperbolic tangent switching
            'CODE-IMPL-195',  # Chattering in real systems
        ]
    },

    'group_03_smc_controllers': {
        'name': 'SMC Controllers - Classical & Super-Twisting',
        'description': 'Classical SMC and Super-Twisting controller implementations',
        'claim_ids': [
            'CODE-IMPL-178',  # Six gains in order
            'CODE-IMPL-180',  # Reset classical SMC
            'CODE-IMPL-201',  # Numba-accelerated STA core
            'CODE-IMPL-204',  # Initialize Super-Twisting SMC
            'CODE-IMPL-167',  # Feasibility check for STA gains
            'CODE-IMPL-517',  # Super-twisting state variables
        ]
    },

    'group_04_optimization_core': {
        'name': 'Optimization Core & Interfaces',
        'description': 'Optimization interfaces, factory methods, algorithm properties',
        'claim_ids': [
            'CODE-IMPL-321',  # Factory to create optimizers
            'CODE-IMPL-322',  # Get available algorithms
            'CODE-IMPL-323',  # Quick optimization function
            'CODE-IMPL-325',  # Parameter space interface
            'CODE-IMPL-326',  # Optimization problem interface
            'CODE-IMPL-327',  # Algorithm name property
            'CODE-IMPL-328',  # Supports constraints
            'CODE-IMPL-329',  # Supports parameter bounds
            'CODE-IMPL-330',  # Population-based property
            'CODE-IMPL-331',  # Update population
        ]
    },

    'group_05_optimization_multi': {
        'name': 'Multi-Objective Optimization',
        'description': 'Pareto dominance, weighted sum scalarization, robustness objectives',
        'claim_ids': [
            'CODE-IMPL-332',  # Initialize multi-objective problem
            'CODE-IMPL-334',  # Initialize composite objective
            'CODE-IMPL-335',  # Combine objectives
            'CODE-IMPL-336',  # Robustness objective
            'CODE-IMPL-339',  # Frequency response objective
            'CODE-IMPL-340',  # Pareto multi-objective
            'CODE-IMPL-341',  # Initialize Pareto
            'CODE-IMPL-342',  # Weighted sum scalarization
            'CODE-IMPL-343',  # Initialize weighted sum
            'CODE-IMPL-344',  # Normalize objectives
        ]
    },

    'group_06_plant_full_lowrank': {
        'name': 'Plant Models - Full & Low-Rank',
        'description': 'Full fidelity and low-rank DIP dynamics models',
        'claim_ids': [
            'CODE-IMPL-382',  # Full fidelity DIP dynamics
            'CODE-IMPL-384',  # Compatibility for legacy _rhs_core
            'CODE-IMPL-386',  # Full-fidelity physics computation
            'CODE-IMPL-387',  # Compute RHS of dynamics
            'CODE-IMPL-390',  # Low-rank DIP dynamics
            'CODE-IMPL-393',  # Low-rank physics computer
        ]
    },

    'group_07_plant_simplified': {
        'name': 'Plant Models - Simplified & Interfaces',
        'description': 'Simplified dynamics, physics matrices, base interfaces',
        'claim_ids': [
            'CODE-IMPL-370',  # Plant core dynamics compatibility
            'CODE-IMPL-375',  # Simplified physics matrices
            'CODE-IMPL-378',  # Available integration methods
            'CODE-IMPL-379',  # Compute dynamics interface
            'CODE-IMPL-397',  # Simplified DIP dynamics
            'CODE-IMPL-399',  # Dynamics using modular approach
            'CODE-IMPL-400',  # Dynamics using JIT approach
            'CODE-IMPL-402',  # Simplified physics module
            'CODE-IMPL-403',  # Simplified physics computation
            'CODE-IMPL-404',  # JIT-compiled simplified dynamics
        ]
    },

    'group_08_integrators': {
        'name': 'Simulation Integrators - Euler & Runge-Kutta',
        'description': 'Euler methods (explicit, implicit, modified), RK45 adaptive integration',
        'claim_ids': [
            'CODE-IMPL-437',  # Legacy Dormand-Prince
            'CODE-IMPL-438',  # Original RK45 fallback
            'CODE-IMPL-451',  # Euler integration module
            'CODE-IMPL-452',  # Forward Euler method
            'CODE-IMPL-454',  # Integrate using forward Euler
            'CODE-IMPL-455',  # Backward Euler method
            'CODE-IMPL-457',  # Integrate using backward Euler
            'CODE-IMPL-458',  # Modified Euler (Heun's)
            'CODE-IMPL-460',  # Integrate using Heun's method
            'CODE-IMPL-440',  # Initialize base integrator
            'CODE-IMPL-443',  # Initialize integration result
        ]
    },

    'group_09_simulation_core': {
        'name': 'Simulation Core & Orchestrators',
        'description': 'Simulation context, orchestrators, time domain, safety recovery',
        'claim_ids': [
            'CODE-IMPL-406',  # Initialize simulation context
            'CODE-IMPL-410',  # Integration method order
            'CODE-IMPL-411',  # Execute simulation strategy
            'CODE-IMPL-415',  # Advance by one time step
            'CODE-IMPL-420',  # Simulation step router
            'CODE-IMPL-422',  # Unified simulation entry point
            'CODE-IMPL-423',  # Simulate using Euler method
            'CODE-IMPL-473',  # Execute orchestrator strategy
            'CODE-IMPL-474',  # Run single simulation
            'CODE-IMPL-476',  # Legacy simulation runner
        ]
    },

    'group_10_misc_utilities': {
        'name': 'Miscellaneous & Utilities',
        'description': 'Benchmarks, MPC, compatibility, safety, result containers, ZOH integration',
        'claim_ids': [
            'CODE-IMPL-085',  # Benchmark default simulator
            'CODE-IMPL-115',  # MPC continuous-time dynamics call
            'CODE-IMPL-117',  # MPC compatibility import
            'CODE-IMPL-446',  # Safely integrate with fallback
            'CODE-IMPL-448',  # ZOH integration order
            'CODE-IMPL-449',  # ZOH nonlinear integration
            'CODE-IMPL-477',  # Result containers
            'CODE-IMPL-478',  # Recovery strategy interface
            'CODE-IMPL-479',  # Emergency stop recovery
            'CODE-IMPL-480',  # State limiting recovery
            'CODE-IMPL-481',  # Register recovery strategy
            'CODE-IMPL-482',  # Apply recovery strategy
        ]
    }
}

# Verify all 91 claims are covered
all_grouped_ids = []
for group_key, group_info in subgroups.items():
    all_grouped_ids.extend(group_info['claim_ids'])

missing_ids = set(c['id'] for c in all_claims) - set(all_grouped_ids)
duplicate_ids = [id for id in all_grouped_ids if all_grouped_ids.count(id) > 1]

print(f"SUBGROUP VERIFICATION")
print(f"=" * 80)
print(f"Total claims: {len(all_claims)}")
print(f"Grouped claims: {len(all_grouped_ids)}")
print(f"Missing: {len(missing_ids)}")
print(f"Duplicates: {len(duplicate_ids)}")
print()

if missing_ids:
    print(f"WARNING: Missing claim IDs: {sorted(missing_ids)}")
    print()

if duplicate_ids:
    print(f"WARNING: Duplicate claim IDs: {sorted(set(duplicate_ids))}")
    print()

# Print subgroup summary
print(f"SUBGROUP SUMMARY")
print(f"=" * 80)
for group_key, group_info in subgroups.items():
    print(f"{group_key}: {len(group_info['claim_ids'])} claims")
    print(f"  Name: {group_info['name']}")
    print(f"  Description: {group_info['description']}")
    print()

# Create claim lookup
claims_by_id = {c['id']: c for c in all_claims}

# Save each subgroup
output_dir = Path('D:/Projects/main/artifacts/research_batches/08_HIGH_implementation_general/subgroups')
output_dir.mkdir(exist_ok=True)

for group_key, group_info in subgroups.items():
    # Get full claim data
    group_claims = [claims_by_id[cid] for cid in group_info['claim_ids'] if cid in claims_by_id]

    # Create input JSON for this subgroup
    claims_for_chatgpt = []
    for claim in group_claims:
        claims_for_chatgpt.append({
            'claim_id': claim['id'],
            'code_summary': claim.get('context', ''),
            'file_path': claim.get('file_path', ''),
            'line_number': claim.get('line_number', ''),
            'description': claim.get('description', '')
        })

    # Save subgroup JSON
    subgroup_file = output_dir / f'{group_key}_input.json'
    with open(subgroup_file, 'w', encoding='utf-8') as f:
        json.dump({
            'group_name': group_info['name'],
            'description': group_info['description'],
            'total_claims': len(claims_for_chatgpt),
            'claims': claims_for_chatgpt
        }, f, indent=2)

    print(f"Saved: {subgroup_file.name} ({len(claims_for_chatgpt)} claims)")

print()
print(f"All subgroups saved to: {output_dir}")
