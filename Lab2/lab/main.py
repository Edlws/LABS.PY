import sys
import argparse
from typing import List
from lab.models import Student
from lab.errors import AppError
import lab.io_utils as io
import lab.processing as proc

def input_int(prompt: str) -> int:
    while True:
        try:
            val = input(prompt)
            return int(val)
        except ValueError:
            print("Ошибка: введите целое число.")

def input_grades() -> List[int]:
    raw = input("Введите оценки через пробел (Enter для пустого списка): ")
    if not raw.strip():
        return []
    try:
        return [int(x) for x in raw.split()]
    except ValueError:
        print("Ошибка: оценки должны быть числами.")
        return []

def print_menu():
    print("\n=== Меню Управления Студентами ===")
    print("1. Загрузить из CSV")
    print("2. Сохранить в CSV")
    print("3. Показать всех студентов")
    print("4. Добавить студента")
    print("5. Удалить студента по ID")
    print("6. Обновить оценки по ID")
    print("7. Показать статистику группы")
    print("8. Экспорт ТОП-N студентов")
    print("9. Сортировка списка")
    print("0. Выход")

def main():
    students: List[Student] = []
    
    parser = argparse.ArgumentParser(description="Student Manager CLI")
    parser.add_argument("--load", help="Путь к файлу для автозагрузки")
    args = parser.parse_args()

    if args.load:
        try:
            students = io.load_students_from_csv(args.load)
            print(f"Загружено {len(students)} студентов из {args.load}")
        except AppError as e:
            print(f"Ошибка при загрузке: {e}")

    while True:
        print_menu()
        choice = input("Выберите пункт: ")

        try:
            if choice == '1':
                fname = input("Введите имя файла (data/students.csv): ") or "data/students.csv"
                students = io.load_students_from_csv(fname)
                print(f"Успешно загружено {len(students)} записей.")

            elif choice == '2':
                fname = input("Введите имя файла для сохранения: ")
                io.save_students_to_csv(fname, students)
                print("Сохранено.")

            elif choice == '3':
                if not students:
                    print("Список пуст.")
                for s in students:
                    print(s)

            elif choice == '4':
                s_id = input_int("Введите ID: ")
                name = input("Введите ФИО: ")
                proc.add_student(students, s_id, name)
                print("Студент добавлен.")

            elif choice == '5':
                s_id = input_int("Введите ID для удаления: ")
                proc.delete_student(students, s_id)
                print("Студент удален.")

            elif choice == '6':
                s_id = input_int("Введите ID студента: ")
                grades = input_grades()
                proc.update_grades(students, s_id, grades)
                print("Оценки обновлены.")

            elif choice == '7':
                stats = proc.calculate_stats(students)
                print(f"Всего студентов: {stats['count']}")
                print(f"Средний балл по группе: {stats['overall_avg']:.2f}")
                if stats['best']:
                    print(f"Лучший: {stats['best'].name} ({stats['best'].average:.2f})")
                if stats['worst']:
                    print(f"Худший: {stats['worst'].name} ({stats['worst'].average:.2f})")

            elif choice == '8':
                n = input_int("Количество студентов (N): ")
                fname = input("Имя файла для экспорта: ")
                top_s = proc.get_top_n(students, n)
                io.export_top_students(fname, top_s)
                print(f"ТОП-{n} сохранен в {fname}.")

            elif choice == '9':
                key = input("Критерий (avg, name, id): ").lower()
                if key not in ['avg', 'name', 'id']:
                    print("Неверный критерий.")
                else:
                    students = proc.sort_students(students, key)
                    print("Список отсортирован.")

            elif choice == '0':
                print("Выход...")
                break
            else:
                print("Неверный выбор.")

        except AppError as e:
            print(f"Ошибка приложения: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()