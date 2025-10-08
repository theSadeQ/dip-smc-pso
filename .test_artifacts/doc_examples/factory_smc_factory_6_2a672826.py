# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 6
# Runnable: True
# Hash: 2a672826

@dataclass
class GainSpecification:
    n_gains: int
    bounds: List[Tuple[float, float]]
    gain_names: List[str]
    description: str