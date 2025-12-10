from dataclasses import dataclass, field
from typing import List
from lab.errors import ValidationError

@dataclass
class Student:
    """
    Класс, представляющий студента.
    """
    id: int
    name: str
    grades: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.validate()

    @property
    def average(self) -> float:
        """Расчет среднего балла. Если оценок нет, возвращает 0.0."""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def validate(self):
        """Проверка корректности данных студента."""
        if not self.name or not self.name.strip():
            raise ValidationError("Имя студента не может быть пустым.")
        if self.id < 0:
            raise ValidationError(f"ID должен быть положительным числом (получено: {self.id}).")
        for g in self.grades:
            if not (0 <= g <= 100):
                raise ValidationError(f"Оценка должна быть от 0 до 100 (получено: {g}).")

    def __str__(self):
        return (f"ID: {self.id} | {self.name:<20} | "
                f"Ср. балл: {self.average:.2f} | Оценки: {self.grades}")