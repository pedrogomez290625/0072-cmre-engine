"""Postgres + pgvector connection layer.

No SQLite fallback. SQLite + JSON columns don't scale to multi-modal KB with
embedding search. The docker-compose brings up pgvector; for local dev you
can `docker compose up -d db`.
"""

from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
)


def init_db() -> None:
    # pgvector extension must exist; create_engine handles postgres-specific
    # DDL via SQLModel metadata.
    from . import models  # noqa: F401  (populate metadata)

    # Ensure pgvector extension is available before creating vector columns.
    with engine.begin() as conn:
        conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS vector")

    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
