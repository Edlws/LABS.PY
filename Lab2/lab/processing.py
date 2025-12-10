from typing import List, Tuple, Dict, Any, Optional
from lab.models import Student
from lab.errors import DuplicateIdError, StudentNotFoundError, ValidationError

def get_student_by_id(students: List[Student], s_id: int) -> Optional[Student]:
    for s in students:
        if s.id == s_id:
            return s
    return None

def add_student(students: List[Student], s_id: int, name: str) -> None:
    if get_student_by_id(students, s_id):
        raise DuplicateIdError(f"Студент с ID {s_id} уже существует.")
    
    new_student = Student(id=s_id, name=name, grades=[])
    students.append(new_student)

def delete_student(students: List[Student], s_id: int) -> None:
    s = get_student_by_id(students, s_id)
    if not s:
        raise StudentNotFoundError(f"Студент с ID {s_id} не найден.")
    students.remove(s)

def update_grades(students: List[Student], s_id: int, new_grades: List[int]) -> None:
    s = get_student_by_id(students, s_id)
    if not s:
        raise StudentNotFoundError(f"Студент с ID {s_id} не найден.")
    
    temp_s = Student(id=s_id, name=s.name, grades=new_grades) 
    s.grades = new_grades

def calculate_stats(students: List[Student]) -> Dict[str, Any]:
    if not students:
        return {
            "count": 0,
            "overall_avg": 0.0,
            "best": None,
            "worst": None
        }

    all_grades = [g for s in students for g in s.grades]
    overall_avg = sum(all_grades) / len(all_grades) if all_grades else 0.0

    sorted_by_avg = sorted(students, key=lambda s: s.average)
    
    return {
        "count": len(students),
        "overall_avg": overall_avg,
        "best": sorted_by_avg[-1],
        "worst": sorted_by_avg[0]
    }

def sort_students(students: List[Student], key_type: str) -> List[Student]:

    if key_type == 'avg':
        return sorted(students, key=lambda s: (-s.average, s.name))
    elif key_type == 'name':
        return sorted(students, key=lambda s: s.name)
    elif key_type == 'id':
        return sorted(students, key=lambda s: s.id)
    else:
        return students

def get_top_n(students: List[Student], n: int) -> List[Student]:
    sorted_s = sort_students(students, 'avg')
    return sorted_s[:n]