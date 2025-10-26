import pandas as pd
import numpy as np

# Загрузка данных
print("Загрузка данных...")
df = pd.read_csv('survey_results_public.csv')
schema_df = pd.read_csv('survey_results_schema.csv')

# Основная информация о датасетах
print(f"Основной датасет: {df.shape}")
print(f"Датасет с описанием: {schema_df.shape}")

# Просмотрим структуру schema файла
print("\n=== СТРУКТУРА ФАЙЛА С ОПИСАНИЕМ ===")
print("Колонки в schema_df:", list(schema_df.columns))
print("\nПервые 5 строк schema_df:")
print(schema_df.head())

# Просмотрим структуру основного файла
print("\n=== СТРУКТУРА ОСНОВНОГО ФАЙЛА ===")
print("Первые 10 колонок основного файла:")
print(list(df.columns)[:10])

# Поиск колонок, связанных с технологиями в основном файле
print("\n=== ПОИСК ТЕХНОЛОГИЧЕСКИХ КОЛОНОК ===")
tech_columns = []
for col in df.columns:
    col_lower = col.lower()
    if any(keyword in col_lower for keyword in ['tech', 'tool', 'database', 'platform', 'cloud', 'language', 'framework', 'workflow']):
        tech_columns.append(col)

print(f"Найдено технологических колонок: {len(tech_columns)}")
for col in tech_columns:
    print(f"  - {col}")

# Анализ содержимого технологических колонок
print("\n=== АНАЛИЗ СОДЕРЖИМОГО ТЕХНОЛОГИЧЕСКИХ КОЛОНОК ===")
for col in tech_columns[:8]:  # Покажем первые 8
    if col in df.columns:
        sample_data = df[col].dropna().head(3)
        unique_count = df[col].nunique()
        print(f"\n{col}:")
        print(f"  Уникальных значений: {unique_count}")
        print(f"  Примеры: {list(sample_data)}")
        
        # Если это множественный выбор, покажем популярные технологии
        if unique_count > 1 and any(';' in str(x) for x in sample_data if pd.notna(x)):
            print(f"  Тип: Множественный выбор")
            # Проанализируем популярные технологии в этой колонке
            all_techs = []
            for tech_str in df[col].dropna():
                if ';' in str(tech_str):
                    techs = [t.strip() for t in str(tech_str).split(';')]
                    all_techs.extend(techs)
            if all_techs:
                from collections import Counter
                common_techs = Counter(all_techs).most_common(5)
                print(f"  Популярные технологии: {common_techs}")

# Поиск демографических колонок
print("\n=== ДЕМОГРАФИЧЕСКИЕ КОЛОНКИ ===")
demo_columns = []
for col in df.columns:
    col_lower = col.lower()
    if any(keyword in col_lower for keyword in ['country', 'age', 'year', 'experience', 'employment', 'size', 'education', 'salary']):
        demo_columns.append(col)

print(f"Найдено демографических колонок: {len(demo_columns)}")
for col in demo_columns[:10]:  # Покажем первые 10
    print(f"  - {col}")

# Сохраним список всех колонок для reference
print("\n=== ВСЕ КОЛОНКИ ДЛЯ СПРАВКИ ===")
print("Полный список колонок сохранен в файл: all_columns.txt")
with open('all_columns.txt', 'w') as f:
    for col in df.columns:
        f.write(f"{col}\n")

print("\n✅ Анализ завершен! Проверьте вывод выше чтобы определить нужные колонки.")