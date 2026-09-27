import json
from pathlib import Path
from cmre.services.problem_profiler import load_active_competitions
from cmre.schemas import ProblemDNA, ExperimentPlan

def test_load_active_competitions_success(tmp_path: Path):
    # Crear un JSON válido de prueba
    test_json = {
        "competitions": [
            {
                "id": "test-comp-01",
                "name": "Test Competition 01",
                "platform": "kaggle",
                "target_type": "multilabel_classification",
                "modalities": ["image_2.5d_mri"],
                "target_metric": "macro_averaged_roc_auc",
                "key_challenges": ["severe_class_imbalance"]
            }
        ]
    }

    json_path = tmp_path / "ACTIVE_COMPETITIONS_TEST.json"
    json_path.write_text(json.dumps(test_json), encoding="utf-8")

    results = load_active_competitions(str(json_path))

    assert "test-comp-01" in results
    dna, plan = results["test-comp-01"]

    assert isinstance(dna, ProblemDNA)
    assert isinstance(plan, ExperimentPlan)

    assert dna.title == "Test Competition 01"
    assert dna.platform == "kaggle"
    assert dna.task_type == "multiclass_classification"  # mapped
    assert dna.modality == "image"  # mapped
    assert dna.metric == "macro_averaged_roc_auc"
    assert plan.competition_title == "Test Competition 01"


def test_load_active_competitions_file_not_found():
    results = load_active_competitions("ARCHIVO_INEXISTENTE_XYZ.json")
    assert results == {}


def test_load_active_competitions_invalid_json(tmp_path: Path):
    json_path = tmp_path / "INVALID.json"
    json_path.write_text("ESTO NO ES JSON", encoding="utf-8")

    results = load_active_competitions(str(json_path))
    assert results == {}
