"""Unit tests for seeder_claims service."""

import pytest
from sqlmodel import Session, select

from cmre.db import get_session, init_db
from cmre.models import Claim, Mechanism
from cmre.services.seeder_claims import seed_forensic_and_hpc_claims


def test_seed_forensic_and_hpc_claims():
    init_db()
    with get_session() as session:
        count = seed_forensic_and_hpc_claims(session)
        assert count == 54

        # Verify claims presence
        claims = session.exec(select(Claim)).all()
        assert len(claims) >= 54

        # Verify specific key claims
        fc03 = session.exec(select(Claim).where(Claim.summary.like("%FC03%"))).first()
        assert fc03 is not None
        assert "image" in fc03.modality_tags
        assert fc03.evidence_level >= 4
        assert len(fc03.citations) > 0

        c01 = session.exec(select(Claim).where(Claim.summary.like("%C01%"))).first()
        assert c01 is not None
        assert c01.evidence_level == 6

        hpc01 = session.exec(select(Claim).where(Claim.summary.like("%HPC01%"))).first()
        assert hpc01 is not None
        assert hpc01.claim_type == "hpc_microkernel"

        # Verify idempotency
        count_repeat = seed_forensic_and_hpc_claims(session)
        assert count_repeat == 54
        claims_after = session.exec(select(Claim)).all()
        assert len(claims_after) == len(claims)
