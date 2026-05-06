import pytest
import os
import logging
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from organizer import FileOrganizerHandler

@pytest.fixture
def setup_test_env(tmp_path):
    src = tmp_path / "source"
    dest = tmp_path / "dest"
    src.mkdir()
    dest.mkdir()
    
    # Mock logger
    logger = logging.getLogger("TestLogger")
    
    # Create config matching organizer.py expectations
    config = {
        "watch_directory": str(src),
        "organize_by": {
            "Images": [".jpg", ".png"],
            "Documents": [".pdf", ".txt"]
        },
        "ignore_files": [".DS_Store", "desktop.ini"]
    }
    
    handler = FileOrganizerHandler(config, logger)
    yield handler, src, dest

def test_get_destination_folder(setup_test_env):
    handler, _, _ = setup_test_env
    
    assert handler.get_destination_folder(".jpg") == "Images"
    assert handler.get_destination_folder(".txt") == "Documents"
    assert handler.get_destination_folder(".unknown") == "Others"

def test_organize_file_ignore(setup_test_env):
    handler, src, _ = setup_test_env
    
    ignore_file = src / ".DS_Store"
    ignore_file.touch()
    
    # Shouldn't raise any errors or move anything
    handler.organize_file(ignore_file)
    assert ignore_file.exists() # Remains in source

def test_organize_file_move(setup_test_env):
    handler, src, _ = setup_test_env
    
    test_file = src / "test.jpg"
    test_file.touch()
    
    handler.organize_file(test_file)
    
    # Should be moved to Images folder
    moved_file = handler.watch_dir / "Images" / "test.jpg"
    assert moved_file.exists()
    assert not test_file.exists()
