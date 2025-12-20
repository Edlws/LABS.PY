import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np
from sklearn.preprocessing import LabelEncoder

print("--- Этап 1: Загрузка данных ---")

# URL
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"

# Названия столбцов
columns = [
    'checking_status', 'duration', 'credit_history', 'purpose', 'credit_amount',
    'savings', 'employment', 'installment_rate', 'personal_status', 'other_debtors',
    'residence_since', 'property', 'age', 'other_installment_plans', 'housing',
    'existing_credits', 'job', 'people_liable', 'telephone', 'foreign_worker', 'credit_risk'
]

# Загрузка данных
try:
    df = pd.read_csv(url, sep=' ', header=None, names=columns)
    print("Данные успешно загружены.")
except Exception as e:
    print(f"Ошибка загрузки: {e}")
    exit()

# Проверка на пропущенные значения
print("\nПропущенные значения в столбцах:")
print(df.isnull().sum())

# Интерпретация целевой переменной
df['credit_risk_label'] = df['credit_risk'].map({1: 'Good', 2: 'Bad'})

print(f"\nРазмер датасета: {df.shape}")
print(df.head())


print("\n--- Этап 2: Анализ переменных ---")

# Описательная статистика для числовых признаков
numerical_cols = ['duration', 'credit_amount', 'installment_rate', 'residence_since', 'age', 'existing_credits', 'people_liable']
print("\nСтатистика числовых признаков:")
print(df[numerical_cols].describe())

# Анализ категориальных признаков
categorical_cols = ['checking_status', 'credit_history', 'purpose', 'savings', 'employment', 'personal_status', 
                    'other_debtors', 'property', 'other_installment_plans', 'housing', 'job', 'telephone', 'foreign_worker']

print("\nУникальные значения категориальных признаков (топ-3):")
for col in categorical_cols:
    print(f"{col}: {df[col].unique()[:3]}... (Всего уникальных: {df[col].nunique()})")

# Кодирование категориальных признаков для анализа корреляций
df_encoded = df.copy()
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    label_encoders[col] = le

print("\nКатегориальные признаки закодированы в числовой формат.")

print("\n--- Этап 3: Взаимосвязи и группировка ---")

# Корреляционная матрица
cols_for_corr = numerical_cols + categorical_cols + ['credit_risk']
correlation_matrix = df_encoded[cols_for_corr].corr()

# Группировка: Средняя сумма кредита и возраст в зависимости от статуса риска
grouped_risk = df.groupby('credit_risk_label')[['credit_amount', 'age']].mean()
print("\nСредние показатели по статусу кредита:")
print(grouped_risk)

# Группировка: Средняя сумма кредита по целям (Purpose)
grouped_purpose = df.groupby('purpose')['credit_amount'].mean().sort_values(ascending=False)
print("\nСредний кредит по целям (топ-5 категорий):")
print(grouped_purpose.head())

print("\n--- Этап 4: Построение графиков ---")

# Настройка стиля
sns.set_style("whitegrid")
plt.figure(figsize=(18, 12))

# График 1: Гистограмма распределения возраста
plt.subplot(2, 2, 1)
sns.histplot(data=df, x='age', bins=20, kde=True, color='skyblue')
plt.title('Распределение возраста клиентов')
plt.xlabel('Возраст')
plt.ylabel('Количество')

# График 2: Boxplot суммы кредита в зависимости от риска
plt.subplot(2, 2, 2)
sns.boxplot(x='credit_risk_label', y='credit_amount', data=df, palette="Set2")
plt.title('Распределение суммы кредита по статусу риска')
plt.xlabel('Статус кредита (Good/Bad)')
plt.ylabel('Сумма кредита (DM)')

# График 3: Тепловая карта корреляции
plt.subplot(2, 2, 3)
subset_corr = df_encoded[numerical_cols + ['credit_risk']].corr()
sns.heatmap(subset_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Корреляция числовых признаков')

# График 4: Столбчатая диаграмма целей кредита
plt.subplot(2, 2, 4)
sns.countplot(x='purpose', data=df, order=df['purpose'].value_counts().index, palette='viridis')
plt.title('Количество кредитов по целям')
plt.xticks(rotation=45)
plt.xlabel('Код цели (A40-A410)')

plt.tight_layout()
plt.savefig('german_credit_analysis.png') # Сохранение графиков
print("Графики сохранены в файл 'german_credit_analysis.png'")
plt.show()

print("\n--- Этап 5: Работа с SQL ---")

# Создание соединения с БД
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Создание таблицы
create_table_query = """
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    gender_status TEXT,
    job_type TEXT,
    housing TEXT,
    saving_accounts TEXT,
    checking_account TEXT,
    credit_amount INTEGER,
    duration INTEGER,
    purpose TEXT,
    risk INTEGER
);
"""
cursor.execute(create_table_query)

# Подготовка данных
# 1. Берем нужные столбцы из исходного DataFrame
data_to_insert = df[['age', 'personal_status', 'job', 'housing', 'savings', 
                     'checking_status', 'credit_amount', 'duration', 'purpose', 'credit_risk']].copy()

# 2. Переименовываем столбцы
data_to_insert.rename(columns={
    'personal_status': 'gender_status',
    'job': 'job_type',
    'savings': 'saving_accounts',
    'checking_status': 'checking_account',
    'credit_risk': 'risk'
}, inplace=True)

# Вставка данных
data_to_insert.to_sql('clients', conn, if_exists='append', index=False)
print("Данные успешно экспортированы в SQLite.")

# SQL Запрос 1: Выборка топ-5 самых больших кредитов
print("\nSQL 1: Топ-5 самых больших кредитов:")
query1 = """
SELECT age, purpose, credit_amount, risk 
FROM clients 
ORDER BY credit_amount DESC 
LIMIT 5;
"""
for row in cursor.execute(query1):
    print(row)

# SQL Запрос 2: Агрегация - Средний кредит по типу жилья
print("\nSQL 2: Средний кредит по типу жилья:")
query2 = """
SELECT housing, AVG(credit_amount) as avg_credit, COUNT(*) as count
FROM clients 
GROUP BY housing;
"""
for row in cursor.execute(query2):
    print(f"Жилье: {row[0]}, Средний кредит: {row[1]:.2f}, Кол-во: {row[2]}")

# SQL Запрос 3: Выборка "Плохих" заемщиков старше 50 лет
print("\nSQL 3: Рискованные заемщики старше 50 лет (примеры):")
query3 = """
SELECT age, credit_amount, purpose 
FROM clients 
WHERE risk = 2 AND age > 50 
LIMIT 3;
"""
for row in cursor.execute(query3):
    print(row)

# Закрытие соединения
conn.close()
print("\nРабота завершена.")