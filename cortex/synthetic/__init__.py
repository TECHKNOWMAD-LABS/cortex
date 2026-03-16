"""Dataset Forge — Synthetic data generation, validation, and sharding.

Generates large-scale evaluation datasets for skill testing,
adversarial robustness, and continuous benchmarking.
"""

from cortex.synthetic.adversarial_generator import AdversarialGenerator
from cortex.synthetic.base_generator import BaseGenerator, GeneratedPrompt
from cortex.synthetic.domain_generator import DomainGenerator
from cortex.synthetic.reasoning_generator import ReasoningGenerator
from cortex.synthetic.research_generator import ResearchGenerator
from cortex.synthetic.shard_manager import ShardManager
from cortex.synthetic.strategy_generator import StrategyGenerator
from cortex.synthetic.validator import DatasetValidator

__all__ = [
    "BaseGenerator",
    "GeneratedPrompt",
    "ReasoningGenerator",
    "ResearchGenerator",
    "StrategyGenerator",
    "DomainGenerator",
    "AdversarialGenerator",
    "DatasetValidator",
    "ShardManager",
]
