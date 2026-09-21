"""Services layer.

Each service is a pure or near-pure module that orchestrates one piece of
domain logic. They depend on connectors (for data), agents (for LLM), and
models (for persistence) but never the other way around.
"""

from .embedder import Embedder, cosine_similarity
from .submission_validator import SubmissionIntegrityValidator, ValidationIssue, ValidationReport

__all__ = [
    "Embedder",
    "cosine_similarity",
    "SubmissionIntegrityValidator",
    "ValidationReport",
    "ValidationIssue",
]
