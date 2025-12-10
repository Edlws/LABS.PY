import pytest
from lab import io_utils
from lab.models import Student

def test_save_load_roundtrip(tmp_path, sample_students):
    f = tmp_path / "test.csv"
    str_path = str(f)
    
    io_utils.save_students_to_csv(str_path, sample_students)
    loaded = io_utils.load_students_from_csv(str_path)
    
    assert len(loaded) == 3
    assert loaded[0].name == "Иванов"
    assert len(loaded[0].grades) == 2

def test_load_bad_file():
    with pytest.raises(Exception):
        io_utils.load_students_from_csv("non_existent.csv")