"""Centralized settings for CMRE.

All knobs that vary between local, dev, prod live here.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CMRE"
    version: str = "0.2.0"

    # --- Database ---------------------------------------------------------
    database_url: str = "postgresql+psycopg://cmre:cmre@localhost:5432/cmre"
    database_echo: bool = False

    # --- Cloud LLMs (optional, used only when explicitly enabled) --------
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-3-flash"
    deep_research_model: str = "gemini-3-pro"

    # --- Local LLM (default path) ----------------------------------------
    # Antigravity CLI exposes a local endpoint; we talk to it via HTTP.
    antigravity_base_url: str = "http://127.0.0.1:4317"
    antigravity_model: str = "antigravity-local"
    antigravity_timeout_seconds: float = 60.0
    antigravity_fallback_to_gemini: bool = False

    # --- Jules cloud coding agent ----------------------------------------
    jules_api_base: str = "https://jules.googleapis.com/v1alpha"
    jules_api_key: Optional[str] = None
    jules_free_tier_daily_limit: int = 15
    jules_concurrent_limit: int = 3

    # --- Connectors (any of these can be disabled) ------------------------
    connector_huggingface_enabled: bool = True
    connector_semantic_scholar_enabled: bool = True
    connector_arxiv_enabled: bool = True
    connector_github_enabled: bool = True
    connector_kaggle_enabled: bool = True

    # --- GitHub / repo integration ---------------------------------------
    github_token: Optional[str] = None
    github_repo: str = "your-org/cmre-engine"
    create_github_issues: bool = False

    # --- Gemini Spark (manual / Drive-backed) ----------------------------
    spark_drive_folder_id: Optional[str] = None
    spark_docs_export_format: str = "markdown"

    # --- Policies ---------------------------------------------------------
    allow_unknown_license_in_reports: bool = False
    max_artifacts_per_run: int = 25
    max_claims_per_report: int = 20

    # --- Embeddings -------------------------------------------------------
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dim: int = 384

    # --- Recency decay for evidence --------------------------------------
    evidence_half_life_days: int = 365

    model_config = SettingsConfigDict(env_file=".env", env_prefix="CMRE_", extra="ignore")


def get_settings() -> Settings:
    return Settings()
