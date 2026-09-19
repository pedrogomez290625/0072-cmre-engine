"""Tests for the embedder service."""

from cmre.agents.base import MockLLMClient
from cmre.schemas import ProblemDNA
from cmre.services.embedder import Embedder, cosine_similarity


def test_embed_problem_dna_returns_vector_of_correct_dim():
    llm = MockLLMClient()
    embedder = Embedder(llm)
    dna = ProblemDNA(
        title="Test",
        platform="kaggle",
        task_type="binary_classification",
        modality="tabular",
        metric="roc_auc",
        metric_family="auc",
    )
    vec = embedder.embed_problem_dna(dna)
    assert isinstance(vec, list)
    assert len(vec) == embedder.dim


def test_embed_problem_dna_caches_results():
    llm = MockLLMClient()
    embedder = Embedder(llm)
    dna = ProblemDNA(
        title="Test",
        platform="kaggle",
        task_type="binary_classification",
        modality="tabular",
        metric="roc_auc",
        metric_family="auc",
    )
    v1 = embedder.embed_problem_dna(dna)
    v2 = embedder.embed_problem_dna(dna)
    assert v1 == v2  # cached


def test_embed_claim_handles_empty_inputs():
    llm = MockLLMClient()
    embedder = Embedder(llm)
    vec = embedder.embed_claim("")
    assert len(vec) == embedder.dim


def test_cosine_similarity_identical_vectors():
    a = [1.0, 2.0, 3.0]
    b = [1.0, 2.0, 3.0]
    assert abs(cosine_similarity(a, b) - 1.0) < 1e-9


def test_cosine_similarity_orthogonal():
    a = [1.0, 0.0, 0.0]
    b = [0.0, 1.0, 0.0]
    assert abs(cosine_similarity(a, b) - 0.0) < 1e-9


def test_cosine_similarity_handles_zero_vectors():
    a = [0.0, 0.0]
    b = [1.0, 2.0]
    assert cosine_similarity(a, b) == 0.0
    assert cosine_similarity([], b) == 0.0
