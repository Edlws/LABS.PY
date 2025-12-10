import pytest
from lab.models import Student

@pytest.fixture
def sample_students():
    return [
        Student(1, "Иванов", [80, 90]),
        Student(2, "Петров", [60, 50]),
        Student(3, "Сидоров", [])
    ]