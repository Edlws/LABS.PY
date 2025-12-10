import pytest
from lab import processing as proc
from lab.errors import DuplicateIdError, StudentNotFoundError

def test_sort_by_avg(sample_students):
    # Иванов: 85, Петров: 55, Сидоров: 0
    sorted_s = proc.sort_students(sample_students, 'avg')
    assert sorted_s[0].id == 1
    assert sorted_s[-1].id == 3

def test_add_duplicate(sample_students):
    with pytest.raises(DuplicateIdError):
        proc.add_student(sample_students, 1, "Clone")

def test_delete_nonexistent(sample_students):
    with pytest.raises(StudentNotFoundError):
        proc.delete_student(sample_students, 999)

def test_group_stats(sample_students):
    stats = proc.calculate_stats(sample_students)
    assert stats['count'] == 3
    # (80+90+60+50)/4 = 280/4 = 70
    assert stats['overall_avg'] == 70.0