# proteinphonics/utils.py
import os

def ensure_directory_exists(directory):
    """
    Ensure that the specified directory exists.
    If it does not, create it.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
