import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
import json

# Añadir la raíz del proyecto para que se pueda importar scripts.gdrive_hub
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.gdrive_hub import report_status, upload_file_to_drive, sync_claims_and_postmortems

@patch('scripts.gdrive_hub.requests.post')
def test_report_status_success(mock_post, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": "Telemetría enviada"}
    mock_post.return_value = mock_response

    result = report_status(estado="Activo", progreso="50%", tarea="TASK-11", notas="Prueba")

    mock_post.assert_called_once()
    assert result is True
    assert "Telemetría enviada" in capsys.readouterr().out

@patch('scripts.gdrive_hub.requests.post')
def test_upload_file_to_drive_success(mock_post, tmp_path):
    test_file = tmp_path / "test.json"
    test_file.write_text(json.dumps({"test": "data"}))

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "file_name": "test.json",
        "file_url": "http://gdrive/test"
    }
    mock_post.return_value = mock_response

    result = upload_file_to_drive(str(test_file))

    assert result is True
    mock_post.assert_called_once()

@patch('scripts.gdrive_hub.upload_file_to_drive')
def test_sync_claims_and_postmortems(mock_upload, tmp_path, monkeypatch):
    # Mock REPO_ROOT para que use tmp_path
    monkeypatch.setattr('scripts.gdrive_hub.REPO_ROOT', tmp_path)

    # Crear los archivos para que existan
    knowledge_dir = tmp_path / "data" / "knowledge"
    knowledge_dir.mkdir(parents=True)

    claims_file = knowledge_dir / "claims_cmre.json"
    claims_file.write_text('{}')

    postmortems_file = knowledge_dir / "postmortems_failures_catalog.json"
    postmortems_file.write_text('{}')

    mock_upload.return_value = True

    result = sync_claims_and_postmortems()

    assert result is True
    assert mock_upload.call_count == 2
