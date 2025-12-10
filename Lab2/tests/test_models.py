import pytest
from lab.models import Student
from lab.errors import ValidationError

def test_student_creation():
    s = Student(1, "Test", [10, 20])
    assert s.average == 15.0

def test_empty_grades_average():
    s = Student(1, "Test", [])
    assert s.average == 0.0

def test_validation_error_negative_grade():
    with pytest.raises(ValidationError):
        Student(1, "Test", [101])

def test_validation_error_empty_name():
    with pytest.raises(ValidationError):
        Student(1, "", [50])