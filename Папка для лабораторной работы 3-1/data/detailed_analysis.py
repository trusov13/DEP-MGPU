import pandas as pd
import numpy as np

print("📊 ДЕТАЛЬНЫЙ АНАЛИЗ ДАННЫХ")
print("=" * 50)

# Загрузка очищенных данных
df = pd.read_csv('streaming_tools_analysis.csv')
tool_stats = pd.read_csv('tool_popularity_stats.csv')

print(f"Размер датасета: {df.shape}")
print(f"\nКолонки: {list(df.columns)}")

print(f"\n🎯 СТАТИСТИКА ИНСТРУМЕНТОВ:")
print(tool_stats)

print(f"\n🌍 РАСПРЕДЕЛЕНИЕ ПО СТРАНАМ:")
country_dist = df['CountryGroup'].value_counts()
print(country_dist.head(10))

print(f"\n👨‍💻 РАСПРЕДЕЛЕНИЕ ПО ОПЫТУ:")
print(df['ExperienceLevel'].value_counts())

print(f"\n🏢 РАСПРЕДЕЛЕНИЕ ПО РАЗМЕРУ КОМПАНИИ:")
print(df['OrgSize'].value_counts())

# Проверим исходные данные для поиска других инструментов
print(f"\n🔍 ПОИСК ДРУГИХ ИНСТРУМЕНТОВ В ИСХОДНЫХ ДАННЫХ:")
original_df = pd.read_csv('survey_results_public.csv')

# Анализируем колонку с базами данных
if 'DatabaseHaveWorkedWith' in original_df.columns:
    db_data = original_df['DatabaseHaveWorkedWith'].dropna()
    all_dbs = []
    for item in db_data:
        if ';' in str(item):
            dbs = [db.strip() for db in str(item).split(';')]
            all_dbs.extend(dbs)
    
    from collections import Counter
    db_counter = Counter(all_dbs).most_common(20)
    print(f"\n📊 ТОП-20 БАЗ ДАННЫХ:")
    for db, count in db_counter:
        print(f"  {db}: {count}")

# Анализируем колонку с платформами
if 'PlatformHaveWorkedWith' in original_df.columns:
    platform_data = original_df['PlatformHaveWorkedWith'].dropna()
    all_platforms = []
    for item in platform_data:
        if ';' in str(item):
            platforms = [p.strip() for p in str(item).split(';')]
            all_platforms.extend(platforms)
    
    platform_counter = Counter(all_platforms).most_common(15)
    print(f"\n🖥️ ТОП-15 ПЛАТФОРМ:")
    for platform, count in platform_counter:
        print(f"  {platform}: {count}")