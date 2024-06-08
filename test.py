from main import Scanner, compare_files
from unittest.mock import patch, call
import os
import shutil
import pytest

@pytest.fixture
def scanner():
    scanner = Scanner()
    scanner.scan("test_assets")
    return scanner

def test_compare_files():
    assert compare_files("./test_assets/a/821125_1716301429.jpg",
                        "./test_assets/b/821125_1716301429.jpg") == True
    assert compare_files("./test_assets/a/a",
                        "./test_assets/b/a") == False


def test_find_dup(scanner):
    assert len(scanner.duplicates.keys()) == 4
    assert len(scanner.duplicates["test_assets/a/VID_20240508_134739_00_063_20240607223804_clip23.mp4"]) == 2
    assert len(scanner.duplicates["test_assets/a/821125_1716301429.jpg"]) == 1
    assert "a" not in scanner.duplicates


@patch('os.makedirs')
@patch('shutil.move')
def test_delete_dup(mock_move, mock_mkdir, scanner):
    scanner.remove_duplicate_files("recycle")
    assert mock_mkdir.call_count == 1
    assert mock_move.call_count == 4+1 # there's a file was duplicated twice


@patch('os.path.exists', return_value=True)
@patch('os.makedirs')
@patch('shutil.move')
def test_delete_dup2(mock_move, mock_mkdir, mock_exist, scanner):
    scanner.remove_duplicate_files("recycle")
    assert mock_mkdir.call_count == 0
    assert mock_move.call_count == 4+1 # there's a file was duplicated twice

