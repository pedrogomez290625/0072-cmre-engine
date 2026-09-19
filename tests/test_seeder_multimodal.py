"""Tests for the multi-modal seeder."""

from datetime import datetime
from typing import List

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from cmre.config import get_settings
from cmre.models import Claim
from cmre.services.seeder_multimodal import seed


@pytest.fixture()
def session():
    # Use in-memory SQLite for tests so we don't need Postgres.
    # Note: pgvector features are mocked by SQLModel.
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    # Add minimal pgvector support: just store embedding as JSON, not a vector column.
    with Session(engine) as s:
        yield s


def test_seed_inserts_at_least_30_claims(session: Session):
    n = seed(session)
    assert n >= 30
    session.commit()
    rows = session.exec(select(Claim)).all()
    assert len(rows) >= 30


def test_seed_covers_all_modalities(session: Session):
    seed(session)
    session.commit()
    rows = session.exec(select(Claim)).all()
    modalities_seen = set()
    for c in rows:
        for m in c.modality_tags:
            modalities_seen.add(m)
    assert "tabular" in modalities_seen
    assert "text" in modalities_seen
    assert "image" in modalities_seen
    assert "time_series" in modalities_seen
    assert "multimodal" in modalities_seen


def test_seed_is_idempotent(session: Session):
    n1 = seed(session)
    session.commit()
    n2 = seed(session)
    session.commit()
    assert n1 >= 30
    assert n2 == 0


def test_approved_claims_are_flagged(session: Session):
    seed(session)
    session.commit()
    rows = session.exec(select(Claim).where(Claim.approved == True)).all()  # noqa: E712
    assert len(rows) >= 30
