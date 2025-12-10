import csv
import os
from typing import List, Optional
from lab.models import Student
from lab.errors import DataSourceError, ValidationError

def load_students_from_csv(filename: str) -> List[Student]:
    """
    Загружает список студентов из CSV файла.
    Поддерживает файлы с заголовком и без.
    """
    if not os.path.exists(filename):
        raise DataSourceError(f"Файл не найден: {filename}")

    students = []
    
    try:
        with open(filename, mode='r', encoding='utf-8', newline='') as f:
            # Читаем первую строку, чтобы понять, есть ли заголовок
            sample = f.read(1024)
            has_header = csv.Sniffer().has_header(sample)
            f.seek(0)
            
            reader = csv.reader(f)
            if has_header:
                next(reader)  # Пропускаем заголовок

            for row_idx, row in enumerate(reader, start=1):
                if not row:
                    continue
                
                # Минимально должны быть id и name
                if len(row) < 2:
                    continue  # Или можно кинуть предупреждение

                try:
                    s_id = int(row[0])
                    name = row[1].strip()
                    grades = []
                    
                    # Парсинг оценок (начиная с 3-й колонки)
                    for val in row[2:]:
                        val = val.strip()
                        if val:  # Если ячейка не пустая
                            grades.append(int(val))
                    
                    students.append(Student(id=s_id, name=name, grades=grades))
                except ValueError as e:
                    # Логируем ошибку, но не роняем всё приложение, если одна строка битая
                    print(f"[Warning] Ошибка парсинга строки {row_idx}: {e}")
                    
    except (IOError, csv.Error) as e:
        raise DataSourceError(f"Ошибка чтения CSV: {e}")

    return students

def save_students_to_csv(filename: str, students: List[Student]):
    """
    Сохраняет список студентов в CSV.
    Выравнивает количество колонок оценок по максимуму.
    """
    if not students:
        max_grades = 0
    else:
        max_grades = max(len(s.grades) for s in students)

    header = ["id", "name"] + [f"grade{i+1}" for i in range(max_grades)]

    try:
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for s in students:
                # Дополняем список оценок пустыми строками для выравнивания
                grades_row = list(map(str, s.grades)) + [""] * (max_grades - len(s.grades))
                writer.writerow([s.id, s.name] + grades_row)
                
    except IOError as e:
        raise DataSourceError(f"Ошибка записи в файл: {e}")

def export_top_students(filename: str, students: List[Student]):
    """
    Экспорт ТОП-N студентов в специальном формате:
    id, name, average, grades (строкой через пробел)
    """
    header = ["id", "name", "average", "grades"]
    try:
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for s in students:
                grades_str = " ".join(map(str, s.grades))
                writer.writerow([s.id, s.name, f"{s.average:.2f}", grades_str])
    except IOError as e:
        raise DataSourceError(f"Ошибка экспорта: {e}")