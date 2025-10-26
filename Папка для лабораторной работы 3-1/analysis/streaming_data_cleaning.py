import pandas as pd
import numpy as np
from collections import Counter
import re

def main():
    print("🚀 Очистка данных Stack Overflow Survey для анализа потоковой обработки")
    print("=" * 70)
    
    # Загрузка данных
    df = pd.read_csv('survey_results_public.csv')
    print(f"Загружено записей: {len(df):,}")
    
    # Ключевые колонки для анализа (только те, что есть в данных)
    target_columns = {
        'demographic': ['Country', 'Age', 'YearsCode', 'Employment', 'OrgSize'],
        'technologies': [
            'DatabaseHaveWorkedWith',      # Базы данных (содержат Kafka, Redis и др.)
            'PlatformHaveWorkedWith',      # Платформы (содержат облачные сервисы)
            'LanguageHaveWorkedWith',      # Языки программирования
            'CommPlatformHaveWorkedWith'   # Коммуникационные платформы
        ]
    }
    
    # Проверяем наличие колонок
    available_demo = [col for col in target_columns['demographic'] if col in df.columns]
    available_tech = [col for col in target_columns['technologies'] if col in df.columns]
    
    print(f"📊 Доступные демографические колонки: {available_demo}")
    print(f"🔧 Доступные технологические колонки: {available_tech}")
    
    # Инструменты потоковой обработки для поиска
    streaming_tools = {
        'Apache Kafka': ['kafka'],
        'Apache Flink': ['flink'],
        'Apache Spark': ['spark', 'pyspark'],
        'Apache Storm': ['storm'],
        'Apache Pulsar': ['pulsar'],
        'Amazon Kinesis': ['kinesis'],
        'Google Cloud Pub/Sub': ['pub/sub', 'pubsub'],
        'Azure Stream Analytics': ['azure stream', 'stream analytics'],
        'RabbitMQ': ['rabbitmq'],
        'Redis': ['redis'],
        'Apache NiFi': ['nifi'],
        'Apache Beam': ['beam'],
        'Confluent Cloud': ['confluent'],
        'AWS MSK': ['msk', 'managed streaming'],
        'Google Dataflow': ['dataflow'],
        'Apache Samza': ['samza'],
        'Amazon MSK': ['amazon msk'],
        'Azure Event Hubs': ['event hubs'],
        'AWS Lambda': ['aws lambda']  # Для serverless потоковой обработки
    }
    
    def extract_technologies_from_column(column_data):
        """Извлекает технологии из колонки с множественным выбором"""
        technologies = set()
        if pd.isna(column_data):
            return technologies
        
        tech_string = str(column_data)
        if ';' in tech_string:
            # Множественный выбор
            techs = [tech.strip() for tech in tech_string.split(';')]
            technologies.update(techs)
        else:
            # Одиночный выбор
            technologies.add(tech_string.strip())
        
        return technologies
    
    def find_streaming_tools(tech_set):
        """Находит инструменты потоковой обработки в наборе технологий"""
        found_tools = set()
        for tech in tech_set:
            tech_lower = tech.lower()
            for tool_name, keywords in streaming_tools.items():
                if any(keyword in tech_lower for keyword in keywords):
                    found_tools.add(tool_name)
        return found_tools
    
    print(f"\n🔍 Анализ использования инструментов потоковой обработки...")
    
    # Собираем данные для аналитического датасета
    analytical_data = []
    tool_usage_counter = Counter()
    
    for idx, row in df.iterrows():
        if idx % 5000 == 0:
            print(f"Обработано {idx:,} записей...")
        
        record = {}
        
        # Демографические данные
        for demo_col in available_demo:
            if demo_col in row and pd.notna(row[demo_col]):
                record[demo_col] = row[demo_col]
            else:
                record[demo_col] = 'Not specified'
        
        # Собираем все технологии из всех колонок
        all_technologies = set()
        for tech_col in available_tech:
            if tech_col in row:
                techs = extract_technologies_from_column(row[tech_col])
                all_technologies.update(techs)
        
        # Ищем инструменты потоковой обработки
        found_tools = find_streaming_tools(all_technologies)
        
        # Добавляем бинарные колонки для каждого инструмента
        for tool_name in streaming_tools.keys():
            record[tool_name] = 1 if tool_name in found_tools else 0
        
        # Считаем общее использование
        tool_usage_counter.update(found_tools)
        
        analytical_data.append(record)
    
    # Создаем финальный DataFrame
    analytical_df = pd.DataFrame(analytical_data)
    
    # Очистка и категоризация демографических данных
    print(f"\n🎯 Очистка демографических данных...")
    
    # Опыт работы (используем YearsCode вместо YearsCodePro)
    analytical_df['YearsCode'] = pd.to_numeric(analytical_df['YearsCode'], errors='coerce')
    
    def categorize_experience(years):
        if pd.isna(years):
            return 'Not specified'
        elif years < 3:
            return 'Junior (0-2 years)'
        elif years < 7:
            return 'Mid (3-6 years)'
        else:
            return 'Senior (7+ years)'
    
    analytical_df['ExperienceLevel'] = analytical_df['YearsCode'].apply(categorize_experience)
    
    # Очистка страны (оставляем только топ страны для анализа)
    country_counts = analytical_df['Country'].value_counts()
    top_countries = country_counts.head(15).index
    analytical_df['CountryGroup'] = analytical_df['Country'].apply(
        lambda x: x if x in top_countries else 'Other'
    )
    
    # Очистка размера организации
    analytical_df['OrgSize'] = analytical_df['OrgSize'].fillna('Not specified')
    
    # Сохраняем результаты
    print(f"\n💾 Сохранение данных...")
    
    # Основной аналитический датасет
    analytical_df.to_csv('streaming_tools_analysis.csv', index=False)
    
    # Агрегированные данные для визуализации
    tool_stats = []
    for tool, count in tool_usage_counter.most_common():
        percentage = (count / len(analytical_df)) * 100
        tool_stats.append({
            'Tool': tool,
            'Users': count,
            'Percentage': round(percentage, 2)
        })
    
    tool_stats_df = pd.DataFrame(tool_stats)
    tool_stats_df.to_csv('tool_popularity_stats.csv', index=False)
    
    # Данные по странам
    country_tool_usage = analytical_df.groupby('CountryGroup')[list(streaming_tools.keys())].sum()
    country_tool_usage.to_csv('country_tool_usage.csv')
    
    # Данные по опыту работы
    experience_tool_usage = analytical_df.groupby('ExperienceLevel')[list(streaming_tools.keys())].mean() * 100
    experience_tool_usage.to_csv('experience_tool_usage.csv')
    
    # Данные по размеру организации
    orgsize_tool_usage = analytical_df.groupby('OrgSize')[list(streaming_tools.keys())].mean() * 100
    orgsize_tool_usage.to_csv('orgsize_tool_usage.csv')
    
    # Статистика
    print(f"\n📊 РЕЗУЛЬТАТЫ АНАЛИЗА:")
    print(f"Всего обработано записей: {len(analytical_df):,}")
    print(f"Колонок в аналитическом датасете: {len(analytical_df.columns)}")
    
    print(f"\n🎯 ИСПОЛЬЗОВАНИЕ ИНСТРУМЕНТОВ ПОТОКОВОЙ ОБРАБОТКИ:")
    total_respondents = len(analytical_df)
    for tool, count in tool_usage_counter.most_common():
        if count > 0:
            percentage = (count / total_respondents) * 100
            print(f"  {tool}: {count:,} разработчиков ({percentage:.1f}%)")
    
    print(f"\n🌍 ГЕОГРАФИЧЕСКОЕ РАСПРЕДЕЛЕНИЕ:")
    print(f"Топ-5 стран: {list(top_countries[:5])}")
    
    print(f"\n👨‍💻 РАСПРЕДЕЛЕНИЕ ПО ОПЫТУ РАБОТЫ:")
    exp_distribution = analytical_df['ExperienceLevel'].value_counts()
    for level, count in exp_distribution.items():
        print(f"  {level}: {count:,} разработчиков")
    
    print(f"\n💾 СОХРАНЕННЫЕ ФАЙЛЫ:")
    print("  1. streaming_tools_analysis.csv - полный аналитический датасет")
    print("  2. tool_popularity_stats.csv - статистика популярности инструментов")
    print("  3. country_tool_usage.csv - использование по странам")
    print("  4. experience_tool_usage.csv - использование по опыту работы")
    print("  5. orgsize_tool_usage.csv - использование по размеру организации")
    
    print(f"\n✅ Очистка завершена! Данные готовы для Yandex DataLens.")

if __name__ == "__main__":
    main()