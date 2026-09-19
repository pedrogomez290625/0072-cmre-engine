Perfecto. Vamos a convertir el diseño en un **esqueleto de repo ejecutable** con esta división de trabajo:

- **DeepResearch / Gemini Research Agent**: investiga fuentes públicas, extrae candidatos, lee write-ups/notebooks/papers y produce borradores estructurados.
- **Jules**: agente de código que recibe tareas programadas desde el repo, implementa conectores, tests, migraciones, fixes y abre PRs.
- **GitHub Actions**: scheduler para ingesta, extracción, sincronización de tareas y CI.
- **Knowledge Base**: base relacional con proveniencia, licencias, claims condicionales, fracasos, experimentos y perfiles de problema.
- **Reasoning Engine**: puntúa técnicas según Problem DNA, evidencia, riesgo, costo y licencia.
- **Human-in-the-loop**: nada entra como “verdad” sin aprobación o evidencia suficiente.

Abajo te dejo un **esqueleto copy-paste** del repo `cmre-engine`.

---

# 1. Nombre y propósito del repo

```text
cmre-engine
```

**CMRE = Competitive ML Reasoning Engine**

Objetivo del repo:

> Construir una base de conocimiento evidencial y un motor de razonamiento para competencias de ML, automatizado con agentes de investigación y coding agents, respetando licencias, proveniencia y validación humana.

---

# 2. Arquitectura operativa con agentes

```text
┌──────────────────────────────────────────────────────────────┐
│                    GitHub Repo: cmre-engine                  │
│                                                              │
│  ┌────────────────┐       ┌──────────────────────────────┐  │
│  │ DeepResearch   │──────▶│ Ingestion / Extraction Jobs  │  │
│  │ Agent          │       │ GitHub Actions scheduled     │  │
│  └────────────────       └─────────────────────────────┘  │
│                                          │                  │
│                                          ▼                  │
│                         ┌────────────────────────────┐      │
│                         │ Knowledge Base             │      │
│                         │ Artifacts, Claims,         │      │
│                         │ Failures, Profiles,        │      │
│                         │ Experiments, Reviews       │      │
│                         └──────────────┬─────────────┘      │
│                                        │                    │
│                                        ▼                    │
│                         ┌────────────────────────────┐      │
│                         │ Reasoning Engine           │      │
│                         │ Problem DNA → ranked claims│      │
│                         └──────────────┬─────────────┘      │
│                                        │                    │
│                                        ▼                    │
│                         ┌────────────────────────────┐      │
│                         │ Experiment Planner         │      │
│                         │ Markdown / JSON report     │      │
│                         └────────────────────────────┘      │
│                                                              │
│  ┌────────────────┐       ┌──────────────────────────────┐  │
│  │ Jules Agent    │◀──────│ .jules/tasks.yaml            │  │
│  │ coding tasks   │       │ scheduled backlog sync       │  │
│  └────────────────┘       └──────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

Regla importante:

> DeepResearch no “decide” solo. Produce borradores estructurados con citas, licencia y evidencia.  
> Jules no “inventa” arquitectura libre. Ejecuta tareas acotadas desde `.jules/tasks.yaml`.  
> La KB solo usa automáticamente artefactos con `license_status = allowed`.

---

# 3. Estructura del repo

```text
cmre-engine/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── nightly-discovery.yml
│       ├── nightly-extraction.yml
│       ├── weekly-report.yml
│       └── jules-backlog-sync.yml
├── .jules/
│   ├── config.yaml
│   ├── tasks.yaml
│   └── outbox.jsonl
├── data/
│   ├── examples/
│   │   └── competition_fraud.json
│   └── outcomes/
│       └── example_outcome.json
├── prompts/
│   ├── deep_research_discovery.md
│   ├── deep_research_extraction.md
│   └── jules_task.md
├── reports/
│   └── .gitkeep
├── src/
│   └── cmre/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── db.py
│       ├── models.py
│       ├── schemas.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── gemini_client.py
│       │   ├── deep_research.py
│       │   └── jules.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── knowledge_base.py
│       │   ├── problem_profiler.py
│       │   ├── reasoner.py
│       │   ├── planner.py
│       │   └── reporter.py
│       └── workflows/
│           ├── __init__.py
│           ├── ingest_public_artifacts.py
│           ├── extract_claims.py
│           ├── generate_competition_report.py
│           └── register_outcome.py
├── tests/
│   └── test_reasoner.py
├── .env.example
├── .gitignore
├── Makefile
├── README.md
└── pyproject.toml
```

---

# 4. `pyproject.toml`

```toml
[project]
name = "cmre-engine"
version = "0.1.0"
description = "Competitive ML Reasoning Engine: knowledge base + reasoning engine for ML competitions."
requires-python = ">=3.11"
dependencies = [
  "pydantic>=2.8",
  "pydantic-settings>=2.3",
  "sqlmodel>=0.0.21",
  "typer>=0.12",
  "rich>=13.7",
  "python-dotenv>=1.0",
  "httpx>=0.27",
  "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.2",
  "ruff>=0.5",
]
postgres = [
  "psycopg[binary]>=3.2",
]

[project.scripts]
cmre = "cmre.cli:app"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py311"
```

---

# 5. `.env.example`

```env
# Database
# Local MVP:
DATABASE_URL=sqlite:///./cmre.db

# Production / shared:
# DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/cmre

# Agentes
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.0-flash-exp

# GitHub / Jules
GITHUB_TOKEN=
GITHUB_REPO=your-org/cmre-engine
CREATE_GITHUB_ISSUES=false

# Políticas
ALLOW_UNKNOWN_LICENSE_IN_REPORTS=false
MAX_ARTIFACTS_PER_RUN=25
MAX_CLAIMS_PER_REPORT=20
```

---

# 6. `.gitignore`

```gitignore
__pycache__/
*.py[cod]
.venv/
.env
*.db
reports/*.md
!reports/.gitkeep
.jules/outbox.jsonl
.pytest_cache/
.ruff_cache/
dist/
build/
*.egg-info/
```

---

# 7. `Makefile`

```makefile
.PHONY: install dev init-db seed report test lint ingest extract jules-sync

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

init-db:
	cmre init-db

seed:
	cmre seed

report:
	cmre report --input data/examples/competition_fraud.json --output reports/demo.md

test:
	pytest

lint:
	ruff check .
	ruff format --check .

ingest:
	cmre ingest --query "public Kaggle DrivenData tabular competition writeups notebooks" --platforms kaggle,drivendata

extract:
	cmre extract --limit 10

jules-sync:
	cmre jules-sync
```

---

# 8. `README.md`

```markdown
# CMRE Engine

Competitive ML Reasoning Engine.

This repository implements a knowledge base and reasoning engine for ML competitions.

## Core idea

CMRE is not just a catalog of winning notebooks.

It converts public artifacts, papers, repos, models, write-ups and failures into:

- Problem DNA
- conditional claims
- failure records
- ranked technique recommendations
- experiment plans
- feedback loop

## Main components

- `agents/deep_research.py`: research/extraction agent.
- `agents/jules.py`: coding task dispatcher.
- `services/problem_profiler.py`: builds Problem DNA.
- `services/reasoner.py`: scores claims against Problem DNA.
- `services/planner.py`: generates experiment plan.
- `workflows/`: scheduled automations.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
cmre init-db
cmre seed
cmre report --input data/examples/competition_fraud.json --output reports/demo.md
pytest
```

## Important policy

Only artifacts with `license_status=allowed` are automatically usable.

Unknown or restricted artifacts require human review.
```

---

# 9. `src/cmre/__init__.py`

```python
__version__ = "0.1.0"
```

---

# 10. `src/cmre/config.py`

```python
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CMRE"

    database_url: str = "sqlite:///./cmre.db"

    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-2.0-flash-exp"

    github_token: Optional[str] = None
    github_repo: str = "your-org/cmre-engine"
    create_github_issues: bool = False

    allow_unknown_license_in_reports: bool = False
    max_artifacts_per_run: int = 25
    max_claims_per_report: int = 20

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    return Settings()
```

---

# 11. `src/cmre/db.py`

```python
from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings

settings = get_settings()

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args=connect_args,
)


def init_db() -> None:
    # Import models so SQLModel metadata is populated.
    from . import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
```

---

# 12. `src/cmre/models.py`

```python
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Artifact(SQLModel, table=True):
    __tablename__ = "artifacts"

    id: Optional[int] = Field(default=None, primary_key=True)

    source_type: str = Field(index=True)
    platform: str = Field(index=True)
    url: str = Field(index=True, unique=True)

    title: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    competition_external_id: Optional[str] = Field(default=None, index=True)

    license: Optional[str] = None
    license_status: str = Field(default="unknown", index=True)

    content_hash: Optional[str] = None
    raw_path: Optional[str] = None

    processing_state: str = Field(default="new", index=True)

    metadata_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class Competition(SQLModel, table=True):
    __tablename__ = "competitions"

    id: Optional[int] = Field(default=None, primary_key=True)

    platform: str = Field(index=True)
    external_id: Optional[str] = Field(default=None, index=True)
    title: str
    url: Optional[str] = None

    task_type: Optional[str] = Field(default=None, index=True)
    modality: Optional[str] = Field(default=None, index=True)
    metric: Optional[str] = Field(default=None, index=True)

    rules_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    data_profile_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    status: str = Field(default="active", index=True)

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class ProblemProfile(SQLModel, table=True):
    __tablename__ = "problem_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)

    competition_id: Optional[int] = Field(default=None, foreign_key="competitions.id", index=True)

    dna_json: Dict[str, Any] = Field(sa_column=Column(JSON))
    embedding_json: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=utcnow)


class Mechanism(SQLModel, table=True):
    __tablename__ = "mechanisms"

    id: Optional[int] = Field(default=None, primary_key=True)

    slug: str = Field(index=True, unique=True)
    name: str
    description: Optional[str] = None
    parent_slug: Optional[str] = Field(default=None, index=True)


class Technique(SQLModel, table=True):
    __tablename__ = "techniques"

    id: Optional[int] = Field(default=None, primary_key=True)

    slug: str = Field(index=True, unique=True)
    name: str
    category: Optional[str] = Field(default=None, index=True)
    mechanism_slug: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = None

    paper_refs: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    code_refs: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    model_refs: List[str] = Field(default_factory=list, sa_column=Column(JSON))


class Claim(SQLModel, table=True):
    """
    Conditional statement:
    technique/mechanism works/fails under conditions.
    """

    __tablename__ = "claims"

    id: Optional[int] = Field(default=None, primary_key=True)

    technique_slug: Optional[str] = Field(default=None, index=True)
    mechanism_slug: Optional[str] = Field(default=None, index=True)
    problem_profile_id: Optional[int] = Field(default=None, foreign_key="problem_profiles.id", index=True)

    statement: str
    summary: Optional[str] = None

    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    applicable_when: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    not_recommended_when: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    expected_effect: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    cost: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    risk: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    evidence_level: int = Field(default=1, index=True)
    license_status: str = Field(default="unknown", index=True)

    approved: bool = Field(default=False, index=True)

    source_artifact_ids: List[int] = Field(default_factory=list, sa_column=Column(JSON))
    citations: List[Dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class Failure(SQLModel, table=True):
    __tablename__ = "failures"

    id: Optional[int] = Field(default=None, primary_key=True)

    technique_slug: Optional[str] = Field(default=None, index=True)
    mechanism_slug: Optional[str] = Field(default=None, index=True)
    problem_profile_id: Optional[int] = Field(default=None, foreign_key="problem_profiles.id", index=True)

    statement: str
    symptoms: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    root_cause_hypothesis: Optional[str] = None
    lesson: Optional[str] = None
    condition_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    evidence_level: int = Field(default=1, index=True)
    source_artifact_ids: List[int] = Field(default_factory=list, sa_column=Column(JSON))

    approved: bool = Field(default=False, index=True)

    created_at: datetime = Field(default_factory=utcnow)


class Experiment(SQLModel, table=True):
    __tablename__ = "experiments"

    id: Optional[int] = Field(default=None, primary_key=True)

    competition_id: Optional[int] = Field(default=None, foreign_key="competitions.id", index=True)

    hypothesis: str
    techniques_used: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    config_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    result_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    decision: str = Field(default="investigate", index=True)
    notes: Optional[str] = None
    run_id: Optional[str] = None

    created_at: datetime = Field(default_factory=utcnow)


class ReviewTask(SQLModel, table=True):
    __tablename__ = "review_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)

    entity_type: str = Field(index=True)
    entity_id: int = Field(index=True)

    status: str = Field(default="pending", index=True)
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    payload_json: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=utcnow)
```

---

# 13. `src/cmre/schemas.py`

```python
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class SourceType(str, Enum):
    notebook = "notebook"
    writeup = "writeup"
    paper = "paper"
    repo = "repo"
    model = "model"
    dataset = "dataset"
    forum = "forum"
    other = "other"


class Platform(str, Enum):
    kaggle = "kaggle"
    drivendata = "drivendata"
    zindi = "zindi"
    aicrowd = "aicrowd"
    codalab = "codalab"
    github = "github"
    arxiv = "arxiv"
    huggingface = "huggingface"
    semantic_scholar = "semantic_scholar"
    other = "other"


class LicenseStatus(str, Enum):
    allowed = "allowed"
    restricted = "restricted"
    forbidden = "forbidden"
    unknown = "unknown"


class EvidenceLevel(IntEnum):
    rumor = 0
    mentioned = 1
    code_visible = 2
    partially_reproduced = 3
    internal_ablation = 4
    multiple_problems = 5
    theoretical_strong = 6


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class EffectDirection(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    mixed = "mixed"


class ArtifactCandidate(BaseModel):
    model_config = ConfigDict(extra="allow")

    source_type: str
    platform: str
    url: str
    title: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[str] = None
    competition_external_id: Optional[str] = None

    license: Optional[str] = None
    license_status: str = LicenseStatus.unknown.value

    metadata: Dict[str, Any] = Field(default_factory=dict)


class ClaimDraft(BaseModel):
    model_config = ConfigDict(extra="allow")

    statement: str
    summary: Optional[str] = None

    technique_slug: Optional[str] = None
    mechanism_slug: Optional[str] = None

    tags: List[str] = Field(default_factory=list)

    applicable_when: List[str] = Field(default_factory=list)
    not_recommended_when: List[str] = Field(default_factory=list)

    expected_effect: Dict[str, Any] = Field(default_factory=dict)
    cost: Dict[str, Any] = Field(default_factory=dict)
    risk: Dict[str, Any] = Field(default_factory=dict)

    evidence_level: int = EvidenceLevel.mentioned.value
    license_status: str = LicenseStatus.unknown.value

    source_artifact_ids: List[int] = Field(default_factory=list)
    citations: List[Dict[str, Any]] = Field(default_factory=list)


class CompetitionInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str
    platform: str
    task_type: str
    modality: str
    metric: str

    description: Optional[str] = None
    data_summary: Optional[str] = None

    has_temporal_component: bool = False
    has_group_structure: bool = False

    class_imbalance: str = "unknown"
    label_noise_risk: str = "unknown"
    distribution_shift_risk: str = "unknown"

    leak_risks: List[str] = Field(default_factory=list)

    external_data_allowed: Optional[bool] = None
    pretrained_models_allowed: Optional[bool] = None

    compute_constraint: str = "unknown"
    interpretability_required: bool = False


class ProblemDNA(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str
    platform: str
    task_type: str
    modality: str
    metric: str

    has_temporal_component: bool = False
    has_group_structure: bool = False

    class_imbalance: str = "unknown"
    label_noise_risk: str = "unknown"
    distribution_shift_risk: str = "unknown"

    leak_risks: List[str] = Field(default_factory=list)

    external_data_allowed: Optional[bool] = None
    pretrained_models_allowed: Optional[bool] = None

    compute_constraint: str = "unknown"
    interpretability_required: bool = False

    risk_flags: List[str] = Field(default_factory=list)
    validation_recommendations: List[str] = Field(default_factory=list)
    anti_patterns: List[str] = Field(default_factory=list)

    raw: Dict[str, Any] = Field(default_factory=dict)


class RankedClaim(BaseModel):
    claim_id: Optional[int] = None
    statement: str
    mechanism_slug: Optional[str] = None
    technique_slug: Optional[str] = None

    score: float
    reasons: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    evidence_level: int = 0
    license_status: str = "unknown"


class ExperimentPhase(BaseModel):
    name: str
    objective: str
    actions: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)


class ExperimentPlan(BaseModel):
    competition_title: str
    dna_summary: str

    phases: List[ExperimentPhase] = Field(default_factory=list)
    top_techniques: List[RankedClaim] = Field(default_factory=list)
    avoid: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)


class JulesTask(BaseModel):
    id: str
    title: str
    description: str
    acceptance_criteria: List[str] = Field(default_factory=list)
    labels: List[str] = Field(default_factory=lambda: ["jules"])
    files: List[str] = Field(default_factory=list)
    priority: str = "medium"
```

---

# 14. `src/cmre/services/__init__.py`

```python
```

---

# 15. `src/cmre/services/knowledge_base.py`

```python
from typing import List, Optional

from sqlmodel import Session, select

from ..models import Artifact, Claim, ReviewTask
from ..schemas import ArtifactCandidate, ClaimDraft


def upsert_artifact(session: Session, candidate: ArtifactCandidate) -> Artifact:
    stmt = select(Artifact).where(Artifact.url == candidate.url)
    artifact = session.exec(stmt).first()

    if artifact:
        artifact.title = candidate.title or artifact.title
        artifact.author = candidate.author or artifact.author
        artifact.license = candidate.license or artifact.license
        artifact.license_status = candidate.license_status or artifact.license_status
        artifact.metadata_json = candidate.metadata or artifact.metadata_json
        session.add(artifact)
        session.commit()
        session.refresh(artifact)
        return artifact

    artifact = Artifact(
        source_type=candidate.source_type,
        platform=candidate.platform,
        url=candidate.url,
        title=candidate.title,
        author=candidate.author,
        competition_external_id=candidate.competition_external_id,
        license=candidate.license,
        license_status=candidate.license_status,
        metadata_json=candidate.metadata or {},
        processing_state="new",
    )
    session.add(artifact)
    session.commit()
    session.refresh(artifact)
    return artifact


def get_artifacts_for_extraction(session: Session, limit: int = 10) -> List[Artifact]:
    stmt = (
        select(Artifact)
        .where(Artifact.license_status == "allowed")
        .where(Artifact.processing_state == "new")
        .limit(limit)
    )
    return list(session.exec(stmt).all())


def mark_artifact_processed(session: Session, artifact_id: int, state: str = "extracted") -> None:
    artifact = session.get(Artifact, artifact_id)
    if not artifact:
        return
    artifact.processing_state = state
    session.add(artifact)
    session.commit()


def create_claim_draft(session: Session, draft: ClaimDraft) -> Claim:
    claim = Claim(
        technique_slug=draft.technique_slug,
        mechanism_slug=draft.mechanism_slug,
        statement=draft.statement,
        summary=draft.summary,
        tags=draft.tags,
        applicable_when=draft.applicable_when,
        not_recommended_when=draft.not_recommended_when,
        expected_effect=draft.expected_effect,
        cost=draft.cost,
        risk=draft.risk,
        evidence_level=draft.evidence_level,
        license_status=draft.license_status,
        approved=False,
        source_artifact_ids=draft.source_artifact_ids,
        citations=draft.citations,
    )
    session.add(claim)
    session.commit()
    session.refresh(claim)
    return claim


def approve_claim(session: Session, claim_id: int) -> Optional[Claim]:
    claim = session.get(Claim, claim_id)
    if not claim:
        return None
    claim.approved = True
    session.add(claim)
    session.commit()
    session.refresh(claim)
    return claim


def get_approved_claims(session: Session) -> List[Claim]:
    stmt = select(Claim).where(Claim.approved == True)  # noqa: E712
    return list(session.exec(stmt).all())


def create_review_task(
    session: Session,
    entity_type: str,
    entity_id: int,
    status: str = "pending",
    notes: Optional[str] = None,
    payload: Optional[dict] = None,
) -> ReviewTask:
    task = ReviewTask(
        entity_type=entity_type,
        entity_id=entity_id,
        status=status,
        notes=notes,
        payload_json=payload or {},
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

---

# 16. `src/cmre/services/problem_profiler.py`

```python
from ..schemas import CompetitionInput, ProblemDNA


def build_dna(inp: CompetitionInput) -> ProblemDNA:
    risk_flags = []
    validation_recommendations = []
    anti_patterns = []

    if inp.has_temporal_component:
        risk_flags.extend(["temporal_drift", "public_private_gap"])
        validation_recommendations.extend(
            ["temporal_validation", "rolling_origin", "adversarial_validation"]
        )
        anti_patterns.append("random_kfold_as_primary_validation")

    if inp.has_group_structure:
        risk_flags.append("group_dependence")
        validation_recommendations.append("group_cv")
        anti_patterns.append("iid_assumption_without_group_check")

    if inp.class_imbalance in {"high", "extreme"}:
        risk_flags.append("class_imbalance")
        validation_recommendations.extend(
            ["class_imbalance_handling", "sample_weighting", "threshold_optimization"]
        )

    if inp.label_noise_risk in {"medium", "high"}:
        risk_flags.append("label_noise")
        validation_recommendations.extend(["noise_robust_loss", "confident_learning"])

    if inp.distribution_shift_risk in {"medium", "high"}:
        risk_flags.append("distribution_shift")
        validation_recommendations.extend(["adversarial_validation", "feature_stability"])
        anti_patterns.append("train_only_validation")

    for leak in inp.leak_risks:
        risk_flags.append(f"leak_{leak}")
        validation_recommendations.append("leak_detection")

    if inp.metric.lower() in {"auc", "average_precision", "pr_auc", "ndcg", "map"}:
        risk_flags.append("ranking_metric")
        validation_recommendations.append("metric_alignment")

    if inp.compute_constraint in {"low", "moderate"}:
        anti_patterns.append("architecture_before_validation")

    if inp.interpretability_required:
        risk_flags.append("interpretability_constraint")
        validation_recommendations.append("interpretable_model_or_posthoc_explanation")

    dna = ProblemDNA(
        title=inp.title,
        platform=inp.platform,
        task_type=inp.task_type,
        modality=inp.modality,
        metric=inp.metric,
        has_temporal_component=inp.has_temporal_component,
        has_group_structure=inp.has_group_structure,
        class_imbalance=inp.class_imbalance,
        label_noise_risk=inp.label_noise_risk,
        distribution_shift_risk=inp.distribution_shift_risk,
        leak_risks=inp.leak_risks,
        external_data_allowed=inp.external_data_allowed,
        pretrained_models_allowed=inp.pretrained_models_allowed,
        compute_constraint=inp.compute_constraint,
        interpretability_required=inp.interpretability_required,
        risk_flags=risk_flags,
        validation_recommendations=validation_recommendations,
        anti_patterns=anti_patterns,
        raw=inp.model_dump(),
    )

    return dna
```

---

# 17. `src/cmre/services/reasoner.py`

```python
from typing import List, Tuple

from sqlmodel import Session

from ..models import Claim
from ..schemas import ProblemDNA, RankedClaim
from .knowledge_base import get_approved_claims


def _dna_text(dna: ProblemDNA) -> str:
    parts = [
        dna.title,
        dna.platform,
        dna.task_type,
        dna.modality,
        dna.metric,
        dna.class_imbalance,
        dna.label_noise_risk,
        dna.distribution_shift_risk,
        dna.compute_constraint,
    ]

    parts.extend(dna.leak_risks)
    parts.extend(dna.risk_flags)
    parts.extend(dna.validation_recommendations)
    parts.extend(dna.anti_patterns)

    if dna.has_temporal_component:
        parts.append("has_temporal_component temporal time_series future_test")
    if dna.has_group_structure:
        parts.append("has_group_structure group dependence")
    if dna.interpretability_required:
        parts.append("interpretability required")
    if dna.external_data_allowed is True:
        parts.append("external_data_allowed")
    if dna.external_data_allowed is False:
        parts.append("external_data_forbidden")
    if dna.pretrained_models_allowed is True:
        parts.append("pretrained_models_allowed")
    if dna.pretrained_models_allowed is False:
        parts.append("pretrained_models_forbidden")

    return " ".join(str(p).lower() for p in parts if p)


def score_claim(claim: Claim, dna: ProblemDNA) -> Tuple[float, List[str], List[str]]:
    reasons: List[str] = []
    warnings: List[str] = []
    score = 0.0

    if claim.license_status == "forbidden":
        return -100.0, reasons, ["Forbidden license"]

    if claim.license_status == "unknown":
        score -= 50.0
        warnings.append("Unknown license status")
    elif claim.license_status == "restricted":
        score -= 20.0
        warnings.append("Restricted license: human review required")
    elif claim.license_status == "allowed":
        score += 5.0
        reasons.append("License allowed")

    score += float(claim.evidence_level) * 2.0
    reasons.append(f"Evidence level {claim.evidence_level}")

    dna_text = _dna_text(dna)
    dna_flags = set(dna.risk_flags + dna.validation_recommendations + dna.leak_risks)

    if claim.mechanism_slug and claim.mechanism_slug in dna_flags:
        score += 12.0
        reasons.append(f"Mechanism matches DNA flag: {claim.mechanism_slug}")

    for tag in claim.tags or []:
        if tag in dna_flags:
            score += 4.0
            reasons.append(f"Tag matches DNA: {tag}")

    for term in claim.applicable_when or []:
        if term.lower() in dna_text:
            score += 3.0
            reasons.append(f"Applicable condition matched: {term}")

    for term in claim.not_recommended_when or []:
        if term.lower() in dna_text:
            score -= 18.0
            warnings.append(f"Contraindication matched: {term}")

    cost = claim.cost or {}
    for key in ("implementation", "tuning", "compute"):
        if str(cost.get(key, "")).lower() == "high":
            score -= 3.0
            warnings.append(f"High {key} cost")

    risk = claim.risk or {}
    for key in ("overfit_public_lb", "instability_seed", "license_issue"):
        value = str(risk.get(key, "")).lower()
        if value == "high":
            score -= 5.0
            warnings.append(f"High risk: {key}")
        elif value == "medium":
            score -= 2.0
            warnings.append(f"Medium risk: {key}")

    return round(score, 2), reasons, warnings


def retrieve_and_rank(
    session: Session,
    dna: ProblemDNA,
    limit: int = 20,
    allow_unknown_license: bool = False,
) -> List[RankedClaim]:
    claims = get_approved_claims(session)
    ranked: List[RankedClaim] = []

    for claim in claims:
        if claim.license_status == "forbidden":
            continue
        if claim.license_status == "unknown" and not allow_unknown_license:
            continue

        score, reasons, warnings = score_claim(claim, dna)

        ranked.append(
            RankedClaim(
                claim_id=claim.id,
                statement=claim.statement,
                mechanism_slug=claim.mechanism_slug,
                technique_slug=claim.technique_slug,
                score=score,
                reasons=reasons,
                warnings=warnings,
                evidence_level=claim.evidence_level,
                license_status=claim.license_status,
            )
        )

    ranked.sort(key=lambda x: x.score, reverse=True)
    return ranked[:limit]
```

---

# 18. `src/cmre/services/planner.py`

```python
from typing import List

from ..schemas import ExperimentPhase, ExperimentPlan, ProblemDNA, RankedClaim


def _baseline_actions(dna: ProblemDNA) -> List[str]:
    modality = dna.modality.lower()
    task = dna.task_type.lower()

    if "tabular" in modality:
        return [
            "Correr LightGBM baseline con validación recomendada",
            "Correr CatBoost baseline si hay categoricales relevantes",
            "Correr LogisticRegression / Ridge como sanity check",
        ]

    if "image" in modality:
        return [
            "Correr baseline con backbone preentrenado pequeño",
            "Probar progressive resizing si el dataset es grande",
            "Validar por paciente/dispositivo/domain si aplica",
        ]

    if "text" in modality or "nlp" in modality:
        return [
            "Correr baseline con transformer preentrenado permitido",
            "Revisar longitud, truncamiento y tokenizer",
            "Validar por fuente/annotator si hay ruido de etiquetas",
        ]

    if "time" in modality or "series" in modality or "forecast" in task:
        return [
            "Correr seasonal naive / historical mean baseline",
            "Probar global time-series model si hay muchas series",
            "Usar rolling origin validation",
        ]

    return [
        "Construir baseline simple y reproducible",
        "Medir overhead de preprocessing",
        "Fijar seeds y versiones",
    ]


def generate_plan(
    dna: ProblemDNA,
    ranked_claims: List[RankedClaim],
    max_techniques: int = 10,
) -> ExperimentPlan:
    top_techniques = ranked_claims[:max_techniques]

    validation_actions = list(dna.validation_recommendations) or ["Definir validación creíble"]
    anti_patterns = list(dna.anti_patterns) or ["Evitar overfitting al leaderboard público"]

    phase_1 = ExperimentPhase(
        name="Fase 1: Validación creíble",
        objective="Construir una validación que simule el test y exponga riesgos.",
        actions=validation_actions + [
            "Fijar seeds",
            "Registrar CV score por fold/segmento",
            "Comparar distribución train/test si es posible",
        ],
        success_criteria=[
            "La validación explica razonablemente el leaderboard público",
            "No hay fuga obvia de información futura o de ID",
            "El baseline es reproducible",
        ],
        risks=[
            "Usar KFold aleatorio en datos temporales",
            "Confiar solo en leaderboard público",
            "Ignorar group structure",
        ],
    )

    phase_2 = ExperimentPhase(
        name="Fase 2: Baseline fuerte",
        objective="Capturar la mayor señal con el menor costo.",
        actions=_baseline_actions(dna),
        success_criteria=[
            "Mejora clara sobre dummy/random baseline",
            "Tiempo de entrenamiento razonable",
            "Resultados estables entre seeds",
        ],
        risks=[
            "Overfitting temprano por tuning excesivo",
            "Elegir modelo complejo sin necesidad",
        ],
    )

    phase_3 = ExperimentPhase(
        name="Fase 3: Diagnóstico",
        objective="Identificar la restricción dominante del problema.",
        actions=[
            "Error analysis por segmento",
            "Feature importance / attribution básica",
            "Chequeo de leakage",
            "Chequeo de drift train/test",
            "Revisar colas de la métrica",
        ],
        success_criteria=[
            "Saber qué tipo de errores dominan",
            "Detectar si el problema es validación, datos, métrica o modelo",
        ],
        risks=[
            "Mirar solo promedio global",
            "Confundir correlación con causalidad",
        ],
    )

    phase_4 = ExperimentPhase(
        name="Fase 4: Mejoras de alto ROI",
        objective="Probar técnicas condicionales al Problem DNA.",
        actions=[c.statement for c in top_techniques],
        success_criteria=[
            "Cada experimento tiene hipótesis explícita",
            "Se mide lift real sobre validación creíble",
            "Se descarta rápido lo que no funciona",
        ],
        risks=[
            "Adoptar trucos de write-ups sin reproducir condiciones",
            "Aumentar complejidad sin ganancia",
        ],
    )

    phase_5 = ExperimentPhase(
        name="Fase 5: Robustez",
        objective="Reducir varianza y riesgo de submission final.",
        actions=[
            "Multi-seed evaluation",
            "Stress test con subperíodos o segmentos",
            "Verificar consistencia público/privado si hay señal",
            "Revisar licencias y reglas antes de usar artefactos externos",
        ],
        success_criteria=[
            "El modelo no depende de una seed afortunada",
            "No hay riesgo legal/reglamentario",
        ],
        risks=[
            "Ensemble ciego",
            "Overfitting al leaderboard público",
        ],
    )

    phase_6 = ExperimentPhase(
        name="Fase 6: Submission final",
        objective="Enviar la solución con menor riesgo esperado.",
        actions=[
            "Ensemble conservador solo si hay diversidad medida",
            "Postprocessing alineado a métrica",
            "Documentar supuestos y riesgos",
            "Guardar plan B si el privado se comporta distinto",
        ],
        success_criteria=[
            "Submission reproducible",
            "Riesgos conocidos documentados",
        ],
        risks=anti_patterns,
    )

    dna_summary = (
        f"Tarea: {dna.task_type}; modalidad: {dna.modality}; métrica: {dna.metric}; "
        f"riesgos: {', '.join(dna.risk_flags) or 'ninguno detectado'}"
    )

    return ExperimentPlan(
        competition_title=dna.title,
        dna_summary=dna_summary,
        phases=[phase_1, phase_2, phase_3, phase_4, phase_5, phase_6],
        top_techniques=top_techniques,
        avoid=anti_patterns,
        next_steps=[
            "Revisar claims de baja confianza antes de ejecutar",
            "Registrar cada experimento con hipótesis y resultado",
            "Al finalizar, hacer post-mortem y actualizar KB",
        ],
    )
```

---

# 19. `src/cmre/services/reporter.py`

```python
from ..schemas import ExperimentPlan, ProblemDNA, RankedClaim


def render_markdown(dna: ProblemDNA, plan: ExperimentPlan, ranked_claims: list[RankedClaim]) -> str:
    lines = []

    lines.append(f"# CMRE Report: {dna.title}")
    lines.append("")
    lines.append("## Problem DNA")
    lines.append("")
    lines.append(f"- Plataforma: `{dna.platform}`")
    lines.append(f"- Tarea: `{dna.task_type}`")
    lines.append(f"- Modalidad: `{dna.modality}`")
    lines.append(f"- Métrica: `{dna.metric}`")
    lines.append(f"- Componente temporal: `{dna.has_temporal_component}`")
    lines.append(f"- Estructura de grupos: `{dna.has_group_structure}`")
    lines.append(f"- Desbalance: `{dna.class_imbalance}`")
    lines.append(f"- Ruido de etiquetas: `{dna.label_noise_risk}`")
    lines.append(f"- Distribution shift: `{dna.distribution_shift_risk}`")
    lines.append(f"- Leak risks: `{', '.join(dna.leak_risks) or 'none'}`")
    lines.append(f"- Compute constraint: `{dna.compute_constraint}`")
    lines.append(f"- Interpretabilidad requerida: `{dna.interpretability_required}`")
    lines.append("")

    lines.append("## Risk Flags")
    lines.append("")
    if dna.risk_flags:
        for flag in dna.risk_flags:
            lines.append(f"- `{flag}`")
    else:
        lines.append("- Ninguno detectado en profiler determinístico.")
    lines.append("")

    lines.append("## Validation Recommendations")
    lines.append("")
    if dna.validation_recommendations:
        for rec in dna.validation_recommendations:
            lines.append(f"- `{rec}`")
    else:
        lines.append("- Definir validación creíble antes de modelar.")
    lines.append("")

    lines.append("## Anti-patterns")
    lines.append("")
    if dna.anti_patterns:
        for ap in dna.anti_patterns:
            lines.append(f"- `{ap}`")
    else:
        lines.append("- Ninguno marcado.")
    lines.append("")

    lines.append("## Ranked Techniques")
    lines.append("")
    if ranked_claims:
        for i, claim in enumerate(ranked_claims, start=1):
            lines.append(f"### {i}. Score: `{claim.score}`")
            lines.append("")
            lines.append(claim.statement)
            lines.append("")
            if claim.mechanism_slug:
                lines.append(f"- Mechanism: `{claim.mechanism_slug}`")
            if claim.technique_slug:
                lines.append(f"- Technique: `{claim.technique_slug}`")
            lines.append(f"- Evidence level: `{claim.evidence_level}`")
            lines.append(f"- License: `{claim.license_status}`")
            if claim.reasons:
                lines.append("- Reasons:")
                for r in claim.reasons:
                    lines.append(f"  - {r}")
            if claim.warnings:
                lines.append("- Warnings:")
                for w in claim.warnings:
                    lines.append(f"  - {w}")
            lines.append("")
    else:
        lines.append("No hay claims aprobados disponibles. Corre `cmre seed` o revisa la KB.")
        lines.append("")

    lines.append("## Experiment Plan")
    lines.append("")
    for phase in plan.phases:
        lines.append(f"### {phase.name}")
        lines.append("")
        lines.append(f"**Objective:** {phase.objective}")
        lines.append("")
        lines.append("**Actions:**")
        for action in phase.actions:
            lines.append(f"- {action}")
        lines.append("")
        lines.append("**Success criteria:**")
        for criterion in phase.success_criteria:
            lines.append(f"- {criterion}")
        lines.append("")
        if phase.risks:
            lines.append("**Risks:**")
            for risk in phase.risks:
                lines.append(f"- {risk}")
            lines.append("")

    lines.append("## Avoid")
    lines.append("")
    for item in plan.avoid:
        lines.append(f"- `{item}`")
    lines.append("")

    lines.append("## Next Steps")
    lines.append("")
    for step in plan.next_steps:
        lines.append(f"- {step}")

    return "\n".join(lines)
```

---

# 20. `src/cmre/agents/__init__.py`

```python
```

---

# 21. `src/cmre/agents/base.py`

```python
from typing import Protocol


class LLMClient(Protocol):
    def complete_json(self, system_prompt: str, user_prompt: str, schema_name: str) -> dict:
        ...


class MockLLMClient:
    """
    Used when no API key is configured.
    Returns empty structures so workflows can run locally.
    """

    def complete_json(self, system_prompt: str, user_prompt: str, schema_name: str) -> dict:
        if schema_name == "ArtifactCandidateList":
            return {"artifacts": []}
        if schema_name == "ClaimDraftList":
            return {"claims": []}
        return {}
```

---

# 22. `src/cmre/agents/gemini_client.py`

```python
import json
from typing import Optional

from ..config import Settings


class GeminiClient:
    """
    Adapter placeholder for Gemini / Deep Research style JSON completion.

    Replace this with the official Google SDK integration you use:
    - Gemini API
    - Vertex AI
    - Google Agentspace / Deep Research
    - Internal research agent endpoint

    The important contract is:
    complete_json(system_prompt, user_prompt, schema_name) -> dict
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self._client = None

        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required for GeminiClient")

        try:
            from google import genai  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "Google GenAI SDK not installed. Add the official dependency "
                "or replace this adapter with your internal DeepResearch client."
            ) from exc

        self._client = genai.Client(api_key=settings.gemini_api_key)

    def complete_json(self, system_prompt: str, user_prompt: str, schema_name: str) -> dict:
        prompt = (
            f"{system_prompt}\n\n"
            f"{user_prompt}\n\n"
            "Return only valid JSON. Do not include markdown. "
            f"The JSON must follow schema hint: {schema_name}."
        )

        # NOTE: Adjust config/API to the official SDK version you use.
        response = self._client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.1,
            },
        )

        text: Optional[str] = getattr(response, "text", None)
        if not text:
            return {}

        return json.loads(text)
```

---

# 23. `src/cmre/agents/deep_research.py`

```python
import json
from pathlib import Path
from typing import List, Optional

from pydantic import TypeAdapter

from ..config import Settings, get_settings
from ..models import Artifact
from ..schemas import ArtifactCandidate, ClaimDraft
from .base import LLMClient, MockLLMClient

PROMPT_DIR = Path(__file__).resolve().parents[2] / "prompts"


def _load_prompt(filename: str, default: str) -> str:
    path = PROMPT_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return default


def get_llm_client(settings: Optional[Settings] = None) -> LLMClient:
    settings = settings or get_settings()
    if settings.gemini_api_key:
        try:
            from .gemini_client import GeminiClient

            return GeminiClient(settings)
        except Exception:
            # Fallback to mock so local development does not break.
            return MockLLMClient()
    return MockLLMClient()


class DeepResearchAgent:
    def __init__(self, llm_client: Optional[LLMClient] = None, settings: Optional[Settings] = None):
        self.llm = llm_client or get_llm_client(settings)
        self.settings = settings or get_settings()

    def discover_artifacts(
        self,
        query: str,
        platforms: List[str],
        limit: int = 20,
    ) -> List[ArtifactCandidate]:
        system_prompt = _load_prompt(
            "deep_research_discovery.md",
            "You are a research agent for ML competitions. Return only public, licensable artifacts.",
        )

        user_prompt = json.dumps(
            {
                "query": query,
                "platforms": platforms,
                "limit": limit,
                "policy": {
                    "only_public_sources": True,
                    "respect_terms_of_service": True,
                    "require_license_or_public_permission": True,
                    "forbidden": [
                        "private notebooks",
                        "leaked solutions",
                        "paid content",
                        "copyrighted material without permission",
                    ],
                },
            },
            indent=2,
        )

        payload = self.llm.complete_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            schema_name="ArtifactCandidateList",
        )

        if isinstance(payload, list):
            items = payload
        else:
            items = payload.get("artifacts", payload.get("items", []))

        adapter = TypeAdapter(List[ArtifactCandidate])
        candidates = adapter.validate_python(items)

        # Hard policy filter.
        filtered = []
        for c in candidates:
            if c.license_status == "forbidden":
                continue
            filtered.append(c)

        return filtered[:limit]

    def extract_claims_from_artifact(self, artifact: Artifact) -> List[ClaimDraft]:
        if artifact.license_status != "allowed":
            return []

        system_prompt = _load_prompt(
            "deep_research_extraction.md",
            "Extract conditional ML competition claims with citations. Do not hallucinate.",
        )

        user_prompt = json.dumps(
            {
                "artifact": {
                    "id": artifact.id,
                    "source_type": artifact.source_type,
                    "platform": artifact.platform,
                    "url": artifact.url,
                    "title": artifact.title,
                    "license_status": artifact.license_status,
                    "metadata": artifact.metadata_json,
                },
                "instruction": (
                    "Read the permitted artifact content and extract claims/failures. "
                    "Each claim must include applicable conditions, contraindications, "
                    "evidence level, citations and license status. "
                    "If content is unavailable, return empty claims."
                ),
                "raw_content_available": False,
            },
            indent=2,
        )

        payload = self.llm.complete_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            schema_name="ClaimDraftList",
        )

        if isinstance(payload, list):
            items = payload
        else:
            items = payload.get("claims", payload.get("items", []))

        adapter = TypeAdapter(List[ClaimDraft])
        drafts = adapter.validate_python(items)

        cleaned = []
        for draft in drafts:
            draft.source_artifact_ids = [artifact.id] if artifact.id else []
            draft.license_status = artifact.license_status
            cleaned.append(draft)

        return cleaned
```

---

# 24. `src/cmre/agents/jules.py`

```python
import json
import os
import subprocess
from pathlib import Path
from typing import List

from ..config import Settings, get_settings
from ..schemas import JulesTask


class JulesAgent:
    """
    Dispatches bounded coding tasks to Jules.

    In this skeleton, tasks are written to .jules/outbox.jsonl.
    If CREATE_GITHUB_ISSUES=true and gh CLI is available, it can also open issues.
    """

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.outbox_path = Path(".jules/outbox.jsonl")
        self.outbox_path.parent.mkdir(parents=True, exist_ok=True)

    def queue_task(self, task: JulesTask) -> None:
        record = task.model_dump()
        with self.outbox_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        if self.settings.create_github_issues and os.getenv("GITHUB_TOKEN"):
            self._create_github_issue(task)

    def queue_tasks(self, tasks: List[JulesTask]) -> None:
        for task in tasks:
            self.queue_task(task)

    def _create_github_issue(self, task: JulesTask) -> None:
        body_lines = [
            task.description,
            "",
            "## Acceptance criteria",
        ]
        for criterion in task.acceptance_criteria:
            body_lines.append(f"- {criterion}")

        if task.files:
            body_lines.append("")
            body_lines.append("## Relevant files")
            for file in task.files:
                body_lines.append(f"- `{file}`")

        body = "\n".join(body_lines)
        labels = ",".join(task.labels) if task.labels else "jules"

        cmd = [
            "gh",
            "issue",
            "create",
            "--repo",
            self.settings.github_repo,
            "--title",
            task.title,
            "--body",
            body,
            "--label",
            labels,
        ]

        try:
            subprocess.run(cmd, check=True)
        except Exception:
            # Issue creation is optional in skeleton mode.
            pass
```

---

# 25. `src/cmre/workflows/__init__.py`

```python
```

---

# 26. `src/cmre/workflows/ingest_public_artifacts.py`

```python
from typing import List

from sqlmodel import Session

from ..agents.deep_research import DeepResearchAgent
from ..config import get_settings
from ..db import engine, init_db
from ..services.knowledge_base import create_review_task, upsert_artifact


def run(query: str, platforms: List[str], limit: int | None = None) -> int:
    settings = get_settings()
    init_db()

    agent = DeepResearchAgent(settings=settings)
    candidates = agent.discover_artifacts(
        query=query,
        platforms=platforms,
        limit=limit or settings.max_artifacts_per_run,
    )

    imported = 0

    with Session(engine) as session:
        for candidate in candidates:
            artifact = upsert_artifact(session, candidate)
            create_review_task(
                session,
                entity_type="artifact",
                entity_id=artifact.id or 0,
                status="pending",
                notes="Verify license, provenance and usability before extraction.",
                payload={"url": artifact.url, "license_status": artifact.license_status},
            )
            imported += 1

    return imported
```

---

# 27. `src/cmre/workflows/extract_claims.py`

```python
from sqlmodel import Session

from ..agents.deep_research import DeepResearchAgent
from ..config import get_settings
from ..db import engine, init_db
from ..services.knowledge_base import (
    create_claim_draft,
    create_review_task,
    get_artifacts_for_extraction,
    mark_artifact_processed,
)


def run(limit: int = 10) -> int:
    settings = get_settings()
    init_db()

    agent = DeepResearchAgent(settings=settings)
    created = 0

    with Session(engine) as session:
        artifacts = get_artifacts_for_extraction(session, limit=limit)

        for artifact in artifacts:
            drafts = agent.extract_claims_from_artifact(artifact)

            for draft in drafts:
                claim = create_claim_draft(session, draft)
                create_review_task(
                    session,
                    entity_type="claim",
                    entity_id=claim.id or 0,
                    status="pending",
                    notes="Review extracted claim before approval.",
                    payload={"statement": claim.statement, "license_status": claim.license_status},
                )
                created += 1

            mark_artifact_processed(session, artifact.id or 0, state="extracted")

    return created
```

---

# 28. `src/cmre/workflows/generate_competition_report.py`

```python
import json
from pathlib import Path

from sqlmodel import Session

from ..config import get_settings
from ..db import engine, init_db
from ..schemas import CompetitionInput
from ..services.planner import generate_plan
from ..services.problem_profiler import build_dna
from ..services.reasoner import retrieve_and_rank
from ..services.reporter import render_markdown


def run(input_path: str, output_path: str | None = None) -> str:
    settings = get_settings()
    init_db()

    path = Path(input_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    inp = CompetitionInput.model_validate(data)

    dna = build_dna(inp)

    with Session(engine) as session:
        ranked_claims = retrieve_and_rank(
            session,
            dna,
            limit=settings.max_claims_per_report,
            allow_unknown_license=settings.allow_unknown_license_in_reports,
        )

    plan = generate_plan(dna, ranked_claims, max_techniques=settings.max_claims_per_report)
    report = render_markdown(dna, plan, ranked_claims)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")

    return report
```

---

# 29. `src/cmre/workflows/register_outcome.py`

```python
import json
from pathlib import Path
from typing import Any, Dict

from sqlmodel import Session

from ..db import engine, init_db
from ..models import Experiment, Failure


def run(outcome_path: str) -> Dict[str, Any]:
    init_db()

    path = Path(outcome_path)
    data = json.loads(path.read_text(encoding="utf-8"))

    result: Dict[str, Any] = {"experiment_created": False, "failure_created": False}

    with Session(engine) as session:
        experiment = Experiment(
            competition_id=data.get("competition_id"),
            hypothesis=data.get("hypothesis", "Unnamed hypothesis"),
            techniques_used=data.get("techniques_used", []),
            config_json=data.get("config", {}),
            result_json=data.get("result", {}),
            decision=data.get("decision", "investigate"),
            notes=data.get("notes"),
            run_id=data.get("run_id"),
        )
        session.add(experiment)
        session.commit()
        session.refresh(experiment)
        result["experiment_created"] = True
        result["experiment_id"] = experiment.id

        if experiment.decision in {"discard", "failed", "negative"} and data.get("lesson"):
            failure = Failure(
                technique_slug=data.get("technique_slug"),
                mechanism_slug=data.get("mechanism_slug"),
                statement=data.get("lesson"),
                symptoms=data.get("symptoms", []),
                root_cause_hypothesis=data.get("root_cause_hypothesis"),
                lesson=data.get("lesson"),
                condition_json=data.get("condition", {}),
                evidence_level=data.get("evidence_level", 3),
                source_artifact_ids=data.get("source_artifact_ids", []),
                approved=False,
            )
            session.add(failure)
            session.commit()
            result["failure_created"] = True

    return result
```

---

# 30. `src/cmre/cli.py`

```python
import json
from pathlib import Path
from typing import List, Optional

import typer
import yaml
from rich.console import Console
from sqlmodel import Session, select

from .agents.jules import JulesAgent
from .config import get_settings
from .db import engine, init_db
from .models import Claim, Mechanism
from .schemas import ClaimDraft, JulesTask
from .services.knowledge_base import approve_claim
from .workflows.extract_claims import run as run_extract
from .workflows.generate_competition_report import run as run_report
from .workflows.ingest_public_artifacts import run as run_ingest
from .workflows.register_outcome import run as run_register_outcome

app = typer.Typer(add_completion=False)
console = Console()


@app.command("init-db")
def cmd_init_db() -> None:
    init_db()
    console.print("[green]Database initialized.[/green]")


@app.command("seed")
def cmd_seed() -> None:
    init_db()

    with Session(engine) as session:
        existing = session.exec(select(Mechanism)).first()
        if existing:
            console.print("[yellow]Seed already exists.[/yellow]")
            return

        mechanisms = [
            Mechanism(slug="temporal_validation", name="Temporal validation"),
            Mechanism(slug="adversarial_validation", name="Adversarial validation"),
            Mechanism(slug="tree_baseline", name="Tree-based baseline"),
            Mechanism(slug="class_imbalance_handling", name="Class imbalance handling"),
            Mechanism(slug="metric_alignment", name="Metric alignment"),
        ]
        session.add_all(mechanisms)

        claims = [
            ClaimDraft(
                statement=(
                    "Si el dataset tiene timestamp y el test parece futuro, usar validación temporal "
                    "o rolling origin antes que KFold aleatorio como validación primaria."
                ),
                mechanism_slug="temporal_validation",
                tags=["temporal_drift", "public_private_gap", "tabular"],
                applicable_when=["has_temporal_component", "test_is_future"],
                not_recommended_when=["confirmed_iid", "timestamp_is_noise"],
                expected_effect={
                    "metric": "public_private_consistency",
                    "direction": "positive",
                    "confidence": 0.85,
                },
                cost={"implementation": "low", "tuning": "low", "compute": "low"},
                risk={"overfit_public_lb": "low", "instability_seed": "low"},
                evidence_level=5,
                license_status="allowed",
            ),
            ClaimDraft(
                statement=(
                    "Cuando hay riesgo de distribution shift entre train y test, adversarial validation "
                    "ayuda a detectar features inestables y a diseñar validación más realista."
                ),
                mechanism_slug="adversarial_validation",
                tags=["distribution_shift", "feature_stability"],
                applicable_when=["distribution_shift_risk_high", "has_temporal_component"],
                not_recommended_when=["train_test_confirmed_identical_distribution"],
                expected_effect={
                    "metric": "robustness",
                    "direction": "positive",
                    "confidence": 0.75,
                },
                cost={"implementation": "medium", "tuning": "low", "compute": "low"},
                risk={"overfit_public_lb": "low", "instability_seed": "low"},
                evidence_level=4,
                license_status="allowed",
            ),
            ClaimDraft(
                statement=(
                    "En problemas tabulares con compute limitado, LightGBM/CatBoost suelen ser baselines "
                    "fuertes antes de explorar arquitecturas neuronales complejas."
                ),
                mechanism_slug="tree_baseline",
                tags=["tabular", "baseline", "compute_efficient"],
                applicable_when=["modality_tabular", "compute_limited", "structured_features"],
                not_recommended_when=["strong_sequence_structure", "graph_structure_required"],
                expected_effect={
                    "metric": "quick_signal_capture",
                    "direction": "positive",
                    "confidence": 0.9,
                },
                cost={"implementation": "low", "tuning": "medium", "compute": "low"},
                risk={"overfit_public_lb": "medium", "instability_seed": "low"},
                evidence_level=5,
                license_status="allowed",
            ),
            ClaimDraft(
                statement=(
                    "Focal loss puede ayudar en clasificación binaria muy desbalanceada con red neuronal "
                    "cuando la métrica premia la clase minoritaria, pero requiere tuning y puede ser inestable."
                ),
                mechanism_slug="class_imbalance_handling",
                tags=["class_imbalance", "neural_network", "ranking"],
                applicable_when=["class_imbalance_extreme", "model_neural_network", "metric_minority_sensitive"],
                not_recommended_when=["metric_log_loss", "labels_noisy", "small_dataset"],
                expected_effect={
                    "metric": "average_precision",
                    "direction": "positive",
                    "magnitude_range": "+0.001 to +0.010",
                    "confidence": 0.62,
                },
                cost={"implementation": "low", "tuning": "medium", "compute": "low"},
                risk={"overfit_public_lb": "medium", "instability_seed": "medium"},
                evidence_level=3,
                license_status="allowed",
            ),
            ClaimDraft(
                statement=(
                    "Cuando la métrica es de ranking, optimizar el orden relativo y hacer postprocessing "
                    "alineado a la métrica suele tener mejor ROI que cambiar arquitectura sin necesidad."
                ),
                mechanism_slug="metric_alignment",
                tags=["ranking", "postprocessing", "metric_alignment"],
                applicable_when=["metric_ranking", "auc", "average_precision", "ndcg"],
                not_recommended_when=["metric_requires_calibration_only"],
                expected_effect={
                    "metric": "ranking_metric",
                    "direction": "positive",
                    "confidence": 0.8,
                },
                cost={"implementation": "low", "tuning": "low", "compute": "low"},
                risk={"overfit_public_lb": "low", "instability_seed": "low"},
                evidence_level=4,
                license_status="allowed",
            ),
        ]

        for draft in claims:
            claim = Claim(
                technique_slug=draft.technique_slug,
                mechanism_slug=draft.mechanism_slug,
                statement=draft.statement,
                summary=draft.summary,
                tags=draft.tags,
                applicable_when=draft.applicable_when,
                not_recommended_when=draft.not_recommended_when,
                expected_effect=draft.expected_effect,
                cost=draft.cost,
                risk=draft.risk,
                evidence_level=draft.evidence_level,
                license_status=draft.license_status,
                approved=True,
                source_artifact_ids=[],
                citations=[
                    {
                        "type": "seed",
                        "note": "Initial curated claim for CMRE skeleton.",
                    }
                ],
            )
            session.add(claim)

        session.commit()

    console.print("[green]Demo KB seeded with curated claims.[/green]")


@app.command("report")
def cmd_report(
    input: str = typer.Option(..., help="Path to competition input JSON."),
    output: Optional[str] = typer.Option(None, help="Optional path to save markdown report."),
) -> None:
    report = run_report(input_path=input, output_path=output)
    console.print(report)
    if output:
        console.print(f"\n[green]Report saved to {output}[/green]")


@app.command("ingest")
def cmd_ingest(
    query: str = typer.Option(..., help="Research query for public artifacts."),
    platforms: str = typer.Option("kaggle,drivendata,zindi,aicrowd", help="Comma-separated platforms."),
    limit: Optional[int] = typer.Option(None, help="Max artifacts to import."),
) -> None:
    platform_list = [p.strip() for p in platforms.split(",") if p.strip()]
    count = run_ingest(query=query, platforms=platform_list, limit=limit)
    console.print(f"[green]Imported {count} artifact candidates.[/green]")


@app.command("extract")
def cmd_extract(limit: int = typer.Option(10, help="Max artifacts to process.")) -> None:
    count = run_extract(limit=limit)
    console.print(f"[green]Created {count} claim drafts.[/green]")


@app.command("approve-claim")
def cmd_approve_claim(claim_id: int = typer.Argument(...)) -> None:
    init_db()
    with Session(engine) as session:
        claim = approve_claim(session, claim_id)
        if claim:
            console.print(f"[green]Approved claim {claim.id}.[/green]")
        else:
            console.print("[red]Claim not found.[/red]")


@app.command("register-outcome")
def cmd_register_outcome(outcome_path: str = typer.Argument(...)) -> None:
    result = run_register_outcome(outcome_path)
    console.print(json.dumps(result, indent=2))


@app.command("jules-sync")
def cmd_jules_sync(
    tasks_file: str = typer.Option(".jules/tasks.yaml", help="Path to Jules tasks YAML."),
) -> None:
    settings = get_settings()
    path = Path(tasks_file)

    if not path.exists():
        console.print(f"[yellow]No tasks file found at {path}[/yellow]")
        return

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw_tasks = data.get("tasks", [])

    agent = JulesAgent(settings=settings)
    queued = 0

    for raw in raw_tasks:
        task = JulesTask.model_validate(raw)
        agent.queue_task(task)
        queued += 1

    console.print(f"[green]Queued {queued} Jules tasks to .jules/outbox.jsonl[/green]")


if __name__ == "__main__":
    app()
```

---

# 31. `tests/test_reasoner.py`

```python
from cmre.models import Claim
from cmre.schemas import ProblemDNA
from cmre.services.reasoner import score_claim


def test_temporal_validation_claim_scores_high_for_temporal_problem():
    claim = Claim(
        statement="Use temporal validation when test is future.",
        mechanism_slug="temporal_validation",
        tags=["temporal_drift", "public_private_gap"],
        applicable_when=["has_temporal_component"],
        not_recommended_when=["confirmed_iid"],
        expected_effect={},
        cost={},
        risk={},
        evidence_level=5,
        license_status="allowed",
        approved=True,
    )

    dna = ProblemDNA(
        title="Fraud Detection",
        platform="Kaggle",
        task_type="binary_classification",
        modality="tabular",
        metric="auc",
        has_temporal_component=True,
        risk_flags=["temporal_drift", "public_private_gap"],
        validation_recommendations=["temporal_validation"],
        anti_patterns=["random_kfold_as_primary_validation"],
    )

    score, reasons, warnings = score_claim(claim, dna)

    assert score > 20
    assert any("Mechanism matches DNA flag" in r for r in reasons)
    assert "Unknown license status" not in warnings


def test_contraindication_reduces_score():
    claim = Claim(
        statement="Random KFold is acceptable.",
        mechanism_slug="random_validation",
        tags=["validation"],
        applicable_when=["iid_data"],
        not_recommended_when=["has_temporal_component"],
        expected_effect={},
        cost={},
        risk={},
        evidence_level=3,
        license_status="allowed",
        approved=True,
    )

    dna = ProblemDNA(
        title="Fraud Detection",
        platform="Kaggle",
        task_type="binary_classification",
        modality="tabular",
        metric="auc",
        has_temporal_component=True,
        risk_flags=["temporal_drift"],
        validation_recommendations=["temporal_validation"],
        anti_patterns=["random_kfold_as_primary_validation"],
    )

    score, reasons, warnings = score_claim(claim, dna)

    assert any("Contraindication matched" in w for w in warnings)
```

---

# 32. `data/examples/competition_fraud.json`

```json
{
  "title": "Payment Fraud Detection",
  "platform": "Kaggle",
  "task_type": "binary_classification",
  "modality": "tabular",
  "metric": "auc",
  "description": "Detect fraudulent transactions. Train contains past months, test contains future period.",
  "data_summary": "2M rows, 180 features, timestamps, customer IDs, extreme class imbalance.",
  "has_temporal_component": true,
  "has_group_structure": false,
  "class_imbalance": "extreme",
  "label_noise_risk": "medium",
  "distribution_shift_risk": "high",
  "leak_risks": ["temporal", "id"],
  "external_data_allowed": true,
  "pretrained_models_allowed": false,
  "compute_constraint": "moderate",
  "interpretability_required": false
}
```

---

# 33. `data/outcomes/example_outcome.json`

```json
{
  "competition_id": null,
  "hypothesis": "Temporal CV reduces public/private gap compared to random KFold.",
  "techniques_used": ["time_series_split", "lightgbm", "adversarial_validation"],
  "config": {
    "folds": 5,
    "seed": 42
  },
  "result": {
    "cv_score": 0.72,
    "public_lb": 0.74,
    "private_lb": 0.69,
    "gap": -0.03
  },
  "decision": "keep",
  "notes": "Random KFold overestimated performance by 0.05.",
  "run_id": "demo-run-001",
  "lesson": "If transaction data has timestamps and test is future, never use random KFold as primary validation.",
  "mechanism_slug": "temporal_validation",
  "symptoms": ["public_private_gap", "unstable_segment_scores"],
  "condition": {
    "has_temporal_component": true,
    "test_is_future": true
  },
  "evidence_level": 4
}
```

---

# 34. `prompts/deep_research_discovery.md`

```markdown
You are DeepResearch, a bounded research agent for Competitive ML Reasoning Engine.

Your job is to find ONLY public, legally usable artifacts related to ML competitions:
- Kaggle public notebooks
- DrivenData public solutions
- Zindi public notebooks
- AIcrowd public discussions
- GitHub repos with clear licenses
- arXiv papers
- Hugging Face models with clear licenses
- public write-ups with permission or clear public license

Hard rules:
1. Do not propose private notebooks.
2. Do not propose leaked solutions.
3. Do not propose paid/copyrighted content without permission.
4. Respect platform Terms of Service.
5. Prefer official APIs and public pages.
6. Every artifact must include license_status:
   - allowed
   - restricted
   - forbidden
   - unknown
7. If license is unclear, mark unknown.
8. Return only valid JSON.

Output schema:
{
  "artifacts": [
    {
      "source_type": "notebook|writeup|paper|repo|model|dataset|forum|other",
      "platform": "kaggle|drivendata|zindi|aicrowd|github|arxiv|huggingface|semantic_scholar|other",
      "url": "https://...",
      "title": "...",
      "author": "...",
      "published_at": "YYYY-MM-DD or null",
      "competition_external_id": "... or null",
      "license": "MIT|Apache-2.0|CC-BY|Kaggle-public|unknown|...",
      "license_status": "allowed|restricted|forbidden|unknown",
      "metadata": {
        "why_relevant": "...",
        "placement_if_known": "gold|silver|bronze|top10|unknown",
        "task_type": "...",
        "modality": "..."
      }
    }
  ]
}
```

---

# 35. `prompts/deep_research_extraction.md`

```markdown
You are DeepResearch extraction agent for CMRE.

Your job is to convert a permitted public artifact into conditional claims.

A claim is not just "technique X won".
A claim must specify:
- what mechanism is being used
- when it applies
- when it is not recommended
- expected effect
- cost
- risk
- evidence level
- citations

Hard rules:
1. Do not hallucinate.
2. If the artifact content is unavailable, return empty claims.
3. Only use artifacts with license_status = allowed.
4. Every claim must cite source artifact.
5. Distinguish:
   - architectural choice
   - validation choice
   - data discovery
   - leakage trick
   - postprocessing
   - ensemble strategy
   - metric alignment
6. Capture failures too.
7. Return only valid JSON.

Evidence levels:
0 = rumor
1 = mentioned in write-up
2 = code visible but not reproduced
3 = partially reproduced
4 = internal ablation
5 = validated across multiple problems
6 = strong theoretical backing

Output schema:
{
  "claims": [
    {
      "statement": "...",
      "summary": "...",
      "technique_slug": "... or null",
      "mechanism_slug": "temporal_validation|adversarial_validation|class_imbalance_handling|metric_alignment|tree_baseline|...",
      "tags": ["..."],
      "applicable_when": ["..."],
      "not_recommended_when": ["..."],
      "expected_effect": {
        "metric": "...",
        "direction": "positive|negative|neutral|mixed",
        "magnitude_range": "...",
        "confidence": 0.0
      },
      "cost": {
        "implementation": "low|medium|high",
        "tuning": "low|medium|high",
        "compute": "low|medium|high"
      },
      "risk": {
        "overfit_public_lb": "low|medium|high",
        "instability_seed": "low|medium|high",
        "license_issue": "none|low|medium|high"
      },
      "evidence_level": 0,
      "license_status": "allowed",
      "citations": [
        {
          "source_artifact_id": 1,
          "quote": "...",
          "url": "..."
        }
      ]
    }
  ]
}
```

---

# 36. `prompts/jules_task.md`

```markdown
You are Jules, a coding agent for the CMRE repository.

Your job is to implement bounded tasks from .jules/tasks.yaml or GitHub issues labeled `jules`.

Rules:
1. Do not redesign the whole architecture unless explicitly asked.
2. Keep changes minimal and tested.
3. Preserve license/provenance guardrails.
4. Do not add scraping of private or ToS-violating sources.
5. Run tests before proposing completion.
6. Update README/docs when adding commands.
7. Prefer simple, maintainable code over speculative abstraction.

Typical commands:
- pip install -e ".[dev]"
- pytest
- ruff check .
- cmre init-db
- cmre seed
- cmre report --input data/examples/competition_fraud.json

When finishing:
- summarize changed files
- list tests run
- list remaining risks
```

---

# 37. `.jules/config.yaml`

```yaml
version: 1
repo: your-org/cmre-engine
default_branch: main

task_source: .jules/tasks.yaml
prompt_file: prompts/jules_task.md

labels:
  - jules
  - automation

guardrails:
  - "Do not violate platform Terms of Service."
  - "Do not ingest private or leaked competition solutions."
  - "Preserve license_status enforcement."
  - "All automated claims require citations and review status."

commands:
  install: "pip install -e \".[dev]\""
  test: "pytest"
  lint: "ruff check ."
  format: "ruff format ."
```

---

# 38. `.jules/tasks.yaml`

```yaml
tasks:
  - id: kb-license-guard
    title: "Strengthen license guard in reasoner and ingestion"
    description: |
      Ensure no artifact or claim with license_status unknown/restricted/forbidden
      is automatically used in reports unless explicitly allowed by config.
      Add tests for policy enforcement.
    acceptance_criteria:
      - "Reasoner rejects forbidden claims."
      - "Unknown license claims are excluded by default."
      - "Restricted license claims produce warning."
      - "Tests cover all license statuses."
    labels:
      - jules
      - security
      - kb
    files:
      - src/cmre/services/reasoner.py
      - src/cmre/workflows/ingest_public_artifacts.py
      - tests/test_reasoner.py
    priority: high

  - id: deep-research-adapter
    title: "Replace GeminiClient placeholder with official DeepResearch/Gemini adapter"
    description: |
      Implement a robust JSON client for the chosen Google research agent.
      Include retries, timeout, schema validation and logging.
    acceptance_criteria:
      - "Client returns validated JSON."
      - "Failures degrade to MockLLMClient safely."
      - "No secrets logged."
    labels:
      - jules
      - agents
    files:
      - src/cmre/agents/gemini_client.py
      - src/cmre/agents/deep_research.py
    priority: high

  - id: notebook-parser
    title: "Implement notebook structural parser"
    description: |
      Build parser for .ipynb files that extracts cells, imports, functions,
      hyperparameters, seeds, metrics and possible leakage signals.
    acceptance_criteria:
      - "Parser handles malformed notebooks gracefully."
      - "Outputs structured JSON."
      - "Unit tests included."
    labels:
      - jules
      - extraction
    files:
      - src/cmre/services/
      - tests/
    priority: medium

  - id: pgvector-index
    title: "Add vector index for claims and problem profiles"
    description: |
      Introduce embedding storage and similarity search for claims/profiles.
      Start with pgvector or LanceDB depending on deployment.
    acceptance_criteria:
      - "Claims can be embedded."
      - "Problem DNA can be embedded."
      - "Hybrid retrieval combines filters and vector search."
    labels:
      - jules
      - search
    files:
      - src/cmre/models.py
      - src/cmre/services/reasoner.py
    priority: medium

  - id: review-ui
    title: "Create minimal human review UI"
    description: |
      Build a simple Streamlit/FastAPI page to approve/reject artifact and claim drafts.
    acceptance_criteria:
      - "Can list pending review tasks."
      - "Can approve claim."
      - "Can reject with note."
    labels:
      - jules
      - ui
    files:
      - src/cmre/
    priority: medium

  - id: experiment-tracker-integration
    title: "Integrate MLflow or W&B for experiment registration"
    description: |
      Connect Experiment model to an experiment tracker so outcomes can be registered automatically.
    acceptance_criteria:
      - "Register outcome creates tracker run link."
      - "Metrics are stored in KB."
    labels:
      - jules
      - experiments
    files:
      - src/cmre/workflows/register_outcome.py
    priority: low
```

---

# 39. GitHub Actions: CI

`.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint
        run: ruff check .

      - name: Test
        run: pytest
```

---

# 40. GitHub Actions: Nightly Discovery

`.github/workflows/nightly-discovery.yml`

```yaml
name: Nightly Discovery

on:
  schedule:
    - cron: "0 3 * * *"
  workflow_dispatch:

permissions:
  contents: read
  issues: write

jobs:
  discovery:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: ${{ secrets.CMRE_DATABASE_URL || 'sqlite:///./cmre-nightly.db' }}
      GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      GEMINI_MODEL: ${{ vars.GEMINI_MODEL || 'gemini-2.0-flash-exp' }}
      ALLOW_UNKNOWN_LICENSE_IN_REPORTS: "false"
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: Init DB
        run: cmre init-db

      - name: Run discovery
        run: |
          cmre ingest \
            --query "public Kaggle DrivenData Zindi AIcrowd ML competition writeups notebooks papers" \
            --platforms kaggle,drivendata,zindi,aicrowd,github,arxiv,huggingface \
            --limit 25

      - name: Upload fallback DB artifact
        if: always() && env.DATABASE_URL == 'sqlite:///./cmre-nightly.db'
        uses: actions/upload-artifact@v4
        with:
          name: cmre-nightly-db
          path: cmre-nightly.db
```

---

# 41. GitHub Actions: Nightly Extraction

`.github/workflows/nightly-extraction.yml`

```yaml
name: Nightly Extraction

on:
  schedule:
    - cron: "30 4 * * *"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  extraction:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: ${{ secrets.CMRE_DATABASE_URL || 'sqlite:///./cmre-extract.db' }}
      GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      GEMINI_MODEL: ${{ vars.GEMINI_MODEL || 'gemini-2.0-flash-exp' }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: Init DB
        run: cmre init-db

      - name: Extract claims
        run: cmre extract --limit 10

      - name: Upload fallback DB artifact
        if: always() && env.DATABASE_URL == 'sqlite:///./cmre-extract.db'
        uses: actions/upload-artifact@v4
        with:
          name: cmre-extract-db
          path: cmre-extract.db
```

---

# 42. GitHub Actions: Weekly Report

`.github/workflows/weekly-report.yml`

```yaml
name: Weekly Report

on:
  schedule:
    - cron: "0 6 * * 1"
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  report:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: ${{ secrets.CMRE_DATABASE_URL || 'sqlite:///./cmre-report.db' }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: Init DB
        run: cmre init-db

      - name: Seed if empty
        run: cmre seed || true

      - name: Generate demo report
        run: |
          mkdir -p reports
          cmre report \
            --input data/examples/competition_fraud.json \
            --output reports/weekly-demo.md

      - name: Commit report
        run: |
          git config user.name "cmre-bot"
          git config user.email "cmre-bot@users.noreply.github.com"
          git add reports/weekly-demo.md || true
          git diff --staged --quiet || git commit -m "chore: update weekly demo report"
          git push || true
```

---

# 43. GitHub Actions: Jules Backlog Sync

`.github/workflows/jules-backlog-sync.yml`

```yaml
name: Jules Backlog Sync

on:
  schedule:
    - cron: "0 5 * * 1"
  workflow_dispatch:
  push:
    paths:
      - ".jules/tasks.yaml"

permissions:
  contents: read
  issues: write

jobs:
  sync:
    runs-on: ubuntu-latest
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      GITHUB_REPO: ${{ github.repository }}
      CREATE_GITHUB_ISSUES: "false"
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: Queue Jules tasks
        run: cmre jules-sync --tasks-file .jules/tasks.yaml

      - name: Upload Jules outbox
        uses: actions/upload-artifact@v4
        with:
          name: jules-outbox
          path: .jules/outbox.jsonl
```

Nota: si tu integración real de Jules consume GitHub Issues, cambiá `CREATE_GITHUB_ISSUES` a `"true"` y asegurate de que los labels existan. Si no, el esqueleto deja las tareas en `.jules/outbox.jsonl`.

---

# 44. Docker Compose opcional para Postgres

`docker-compose.yml`

```yaml
version: "3.9"

services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: cmre
      POSTGRES_PASSWORD: cmre
      POSTGRES_DB: cmre
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  app:
    build: .
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql+psycopg://cmre:cmre@db:5432/cmre
    profiles:
      - app

volumes:
  pgdata:
```

Si usás Postgres, instalá también:

```bash
pip install -e ".[postgres]"
```

---

# 45. Cómo correr el esqueleto local

```bash
git init cmre-engine
cd cmre-engine

# crea la estructura de carpetas y archivos de arriba

python -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"

cp .env.example .env

cmre init-db
cmre seed

cmre report \
  --input data/examples/competition_fraud.json \
  --output reports/demo.md

pytest
```

Sin `GEMINI_API_KEY`, los agentes de investigación usan `MockLLMClient`, así que `ingest` y `extract` no crearán mucho contenido externo. Pero `seed` te deja una KB demo funcional para probar el reasoning engine.

---

# 46. Qué hace cada automatización inicial

## `cmre ingest`

Flow:

```text
DeepResearchAgent.discover_artifacts()
→ ArtifactCandidate[]
→ policy filter
→ upsert_artifact()
→ ReviewTask pending
```

No usa automáticamente artefactos con licencia dudosa.

---

## `cmre extract`

Flow:

```text
get_artifacts_for_extraction(license_status=allowed)
→ DeepResearchAgent.extract_claims_from_artifact()
→ ClaimDraft[]
→ create_claim_draft(approved=False)
→ ReviewTask pending
```

Los claims extraídos no son “verdad” hasta aprobación humana o validación experimental.

---

## `cmre report`

Flow:

```text
CompetitionInput JSON
→ build_dna()
→ retrieve_and_rank(approved claims)
→ generate_plan()
→ render_markdown()
```

Este es el primer output verdaderamente accionable.

---

## `cmre register-outcome`

Flow:

```text
Outcome JSON
→ Experiment row
→ optional Failure row
```

Esto alimenta el feedback loop.

---

## `cmre jules-sync`

Flow:

```text
.jules/tasks.yaml
→ JulesTask[]
→ .jules/outbox.jsonl
→ optional GitHub issue
```

Esto es el puente para que Jules trabaje por tareas acotadas.

---

# 47. Primer sprint recomendado sobre este esqueleto

## Sprint 1: hacer útil el reasoning local

Objetivo: que el reporte sea accionable sin depender de scraping real.

Tareas:

1. Mejorar `problem_profiler.py` con más heurísticas:
   - metric family parser;
   - leak risk normalizer;
   - compute constraint scorer;
   - modality-specific validation recommendations.

2. Ampliar seed claims:
   - 30 claims tabulares;
   - 10 failures;
   - 10 anti-patterns.

3. Mejorar `reasoner.py`:
   - agregar peso por recencia;
   - agregar penalización por contradicción;
   - agregar boost si claim viene de ablation propia.

4. Agregar tests:
   - temporal problem;
   - noisy labels;
   - few-shot vision;
   - time series forecasting.

Entregable:

```text
Un informe demo que identifique correctamente:
- validación temporal;
- riesgo de leak;
- baseline tree-based;
- postprocessing por métrica;
- anti-patterns.
```

---

## Sprint 2: conectar DeepResearch real

Objetivo: reemplazar `MockLLMClient` por un adapter confiable.

Tareas:

1. Definir cliente oficial de Gemini/DeepResearch/Vertex.
2. Agregar retries y validación JSON.
3. Crear connector para:
   - Kaggle public API si está permitida;
   - arXiv API;
   - Semantic Scholar API;
   - Hugging Face Hub API;
   - GitHub public search API.
4. No scraping agresivo.
5. Guardar raw response para auditoría.

Entregable:

```text
cmre ingest produce candidatos reales con metadata y license_status.
```

---

## Sprint 3: extracción de notebooks/write-ups

Objetivo: convertir artefactos permitidos en claims condicionales.

Tareas:

1. Parser de `.ipynb`.
2. AST para funciones clave.
3. Detector de:
   - seeds;
   - CV type;
   - external data usage;
   - pretrained model usage;
   - leakage suspicious patterns;
   - ensemble logic;
   - postprocessing.
4. LLM extractor para narrativa de write-ups.
5. Review UI mínima.

Entregable:

```text
100 claims candidatos extraídos, con al menos 30 aprobados por humano.
```

---

## Sprint 4: Jules como motor de mantenimiento

Objetivo: que Jules implemente tareas técnicas repetitivas.

Tareas:

1. Conectar `.jules/tasks.yaml` con tu runner real.
2. Agregar tareas:
   - fix failing tests;
   - add connector;
   - improve schema validation;
   - generate migration;
   - write docs.
3. Proteger main branch.
4. Requerir PR + tests verdes.

Entregable:

```text
Jules abre PRs acotados y testeables sobre el repo.
```

---

# 48. Lo más importante de este esqueleto

Este repo ya no es “un Drive con código ganador”.

Es un sistema con:

1. **Proveniencia**
   - cada artefacto tiene URL, licencia, hash, estado.

2. **Evidencia condicional**
   - cada claim tiene cuándo aplica y cuándo no.

3. **Problem DNA**
   - cada competencia se perfila por restricciones.

4. **Reasoning score**
   - no recomienda por popularidad, sino por fit + evidencia + riesgo + costo.

5. **Experiment plan**
   - traduce recomendaciones en fases ejecutables.

6. **Feedback loop**
   - registra experimentos y fracasos.

7. **Agentes acotados**
   - DeepResearch investiga; Jules programa código; humanos aprueban.

---

# 49. Frase para definir el repo

> `cmre-engine` es un monorepo de reasoning competitivo: knowledge base evidencial, profiler de problemas, ranked technique engine, experiment planner y automatizaciones con agentes de investigación y coding agents.

---

# 50. Siguiente paso concreto

Si querés, en el próximo mensaje puedo hacer una de estas tres cosas sobre este mismo esqueleto:

1. **Completar la KB seed tabular** con 50 claims condicionales listos para cargar.
2. **Escribir el parser real de notebooks `.ipynb` + AST** para extraer CV, seeds, models, losses y leakage signals.
3. **Armar la integración concreta con Jules/DeepResearch** usando un formato de task JSON y prompts listos para ejecutar en GitHub Actions.

Mi recomendación: empezar por **1 + 2**, porque sin claims buenos y parser de notebooks, el reasoning engine no tiene carne real para razonar.