import pytest
import os
import shutil
from pathlib import Path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from organizer import FileOrganizerHandler, load_config

@pytest.fixture
def setup_test_env(tmp_path):
    # Setup source and dest directories
    src = tmp_path / "source"
    dest = tmp_path / "dest"
    src.mkdir()
    dest.mkdir()
    
    # Create a fake config
    config = {
        "watch_dir": str(src),
        "categories": {
            "Images": [".jpg", ".png"],
            "Documents": [".pdf", ".txt"]
        }
    }
    
    # Create handler
    handler = FileOrganizerHandler(config)
    
    yield handler, src, dest

def test_get_category(setup_test_env):
    handler, _, _ = setup_test_env
    
    assert handler._get_category(".jpg") == "Images"
    assert handler._get_category(".txt") == "Documents"
    assert handler._get_category(".unknown") == "Others"

def test_resolve_collision(setup_test_env):
    handler, _, dest = setup_test_env
    
    # Create a file in dest to simulate collision
    target_file = dest / "test.txt"
    target_file.touch()
    
    # Resolve collision for same name
    new_path = handler._resolve_collision(target_file)
    
    assert new_path.name == "test_1.txt"
    assert new_path.parent == dest
