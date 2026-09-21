"""Database connection layer.

Supports Postgres + pgvector when available; gracefully falls back to local
SQLite (sqlite:///data/cmre.db) when Postgres is not running or unreachable,
ensuring offline portability and zero-friction execution.
"""

from pathlib import Path
import structlog
from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings

log = structlog.get_logger("cmre.db")
settings = get_settings()


def _create_engine_with_fallback():
    target_url = settings.database_url
    if target_url.startswith("sqlite"):
        return create_engine(target_url, echo=settings.database_echo)

    # If Postgres, attempt quick connection check with short timeout
    try:
        eng = create_engine(
            target_url,
            echo=settings.database_echo,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 1},
        )
        with eng.connect():
            pass
        return eng
    except Exception as e:
        fallback_path = Path(__file__).resolve().parent.parent.parent / "data" / "cmre.db"
        fallback_path.parent.mkdir(parents=True, exist_ok=True)
        fallback_url = f"sqlite:///{fallback_path.as_posix()}"
        log.warning(
            "PostgreSQL unreachable; activating standalone SQLite fallback",
            error=str(e),
            fallback=fallback_url,
        )
        return create_engine(
            fallback_url,
            echo=settings.database_echo,
            connect_args={"check_same_thread": False},
        )


engine = _create_engine_with_fallback()


def init_db() -> None:
    global engine
    from . import models  # noqa: F401

    if engine.dialect.name == "postgresql":
        try:
            with engine.begin() as conn:
                conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS vector")
        except Exception as e:
            log.warning("Could not create vector extension", error=str(e))

    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
