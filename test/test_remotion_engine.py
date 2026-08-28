import pytest
import subprocess
from unittest.mock import patch, MagicMock
from pathlib import Path
import json

from src.core.remotion_engine import RemotionEngine

@pytest.fixture
def engine():
    return RemotionEngine()

def test_export_props(engine, tmp_path):
    dest_path = tmp_path / "props.json"
    data = {"project": "test", "is_remotion": True}
    
    result_path = engine.export_props(data, str(dest_path))
    
    assert result_path == str(dest_path)
    assert dest_path.exists()
    
    with open(dest_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
        assert loaded["project"] == "test"
        assert loaded["is_remotion"] is True

@patch("src.core.remotion_engine.subprocess.run")
def test_render_video_success(mock_run, engine):
    # Mock subprocess.run to return success
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Render completed successfully"
    mock_run.return_value = mock_result
    
    props_path = "dummy/props.json"
    output_path = "dummy/output.mp4"
    project_dir = "./remotion"
    
    result = engine.render_video(props_path, output_path, project_dir)
    
    # Assert return value
    assert result["status"] == "success"
    assert result["path"] == str(Path(output_path))
    
    # Assert subprocess.run was called correctly
    expected_command = f'npx remotion render src/index.ts MiVideo "{output_path}" --props="{props_path}"'
    mock_run.assert_called_once_with(
        expected_command,
        cwd=project_dir,
        shell=True,
        capture_output=True,
        text=True
    )

@patch("src.core.remotion_engine.subprocess.run")
def test_render_video_failure(mock_run, engine):
    # Mock subprocess.run to return failure
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Command failed: node memory limit"
    mock_run.return_value = mock_result
    
    props_path = "dummy/props.json"
    output_path = "dummy/output.mp4"
    
    with pytest.raises(RuntimeError) as exc_info:
        engine.render_video(props_path, output_path)
        
    assert "Error al renderizar Remotion" in str(exc_info.value)
    assert "Command failed: node memory limit" in str(exc_info.value)
