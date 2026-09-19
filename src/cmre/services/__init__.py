"""Services layer.

Each service is a pure or near-pure module that orchestrates one piece of
domain logic. They depend on connectors (for data), agents (for LLM), and
models (for persistence) but never the other way around.
"""

from .embedder import Embedder, cosine_similarity

__all__ = [
    "Embedder",
    "cosine_similarity",
    # filled in by the reasoner/profiler/planner/knowledge_base/reporter modules
]
