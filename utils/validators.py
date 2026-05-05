import os

def validate_path(path_str):
    """Validate if a given path exists"""
    return os.path.exists(path_str)
