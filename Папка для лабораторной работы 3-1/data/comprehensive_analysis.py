import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

print("📊 КОМПЛЕКСНЫЙ АНАЛИЗ ИНСТРУМЕНТОВ ПОТОКОВОЙ ОБРАБОТКИ")
print("=" * 60)

# Загрузка данных
df = pd.read_csv('streaming_tools_analysis.csv')
original_df = pd.read_csv('survey_results_public.csv')

# Анализ всех инструментов из нашего датасета
tool_columns = ['Apache Kafka', 'Apache Flink', 'Apache Spark', 'Apache Storm', 
                'Apache Pulsar', 'Amazon Kinesis', 'Google Cloud Pub/Sub', 
                'Azure Stream Analytics', 'RabbitMQ', 'Redis', 'Apache NiFi', 
                'Apache Beam', 'Confluent Cloud', 'AWS MSK', 'Google Dataflow', 
                'Apache Samza', 'Amazon MSK', 'Azure Event Hubs', 'AWS Lambda']

print("🎯 ИСПОЛЬЗОВАНИЕ ИНСТРУМЕНТОВ ПОТОКОВОЙ ОБРАБОТКИ:")
tool_usage = {}
for tool in tool_columns:
    users = df[tool].sum()
    if users > 0:
        percentage = (users / len(df)) * 100
        tool_usage[tool] = {'users': users, 'percentage': percentage}
        print(f"  {tool}: {users:,} разработчиков ({percentage:.2f}%)")

# Анализ по опыту работы
print(f"\n👨‍💻 ИСПОЛЬЗОВАНИЕ ПО ОПЫТУ РАБОТЫ:")
experience_analysis = df.groupby('ExperienceLevel')[tool_columns].sum()
for level in df['ExperienceLevel'].unique():
    level_data = experience_analysis.loc[level]
    total_respondents = len(df[df['ExperienceLevel'] == level])
    print(f"\n{level}:")
    for tool in tool_columns:
        users = level_data[tool]
        if users > 0:
            pct = (users / total_respondents) * 100
            print(f"  {tool}: {users} ({pct:.1f}%)")

# Анализ по странам
print(f"\n🌍 ИСПОЛЬЗОВАНИЕ ПО СТРАНАМ (ТОП-5):")
top_countries = ['United States of America', 'Germany', 'India', 
                 'United Kingdom of Great Britain and Northern Ireland', 'France']

for country in top_countries:
    country_data = df[df['CountryGroup'] == country]
    if len(country_data) > 0:
        print(f"\n{country}:")
        for tool in ['Redis', 'Apache Kafka', 'RabbitMQ', 'AWS Lambda']:
            users = country_data[tool].sum()
            if users > 0:
                pct = (users / len(country_data)) * 100
                print(f"  {tool}: {users} ({pct:.1f}%)")

# Анализ по размеру компании
print(f"\n🏢 ИСПОЛЬЗОВАНИЕ ПО РАЗМЕРУ КОМПАНИИ:")
orgsize_analysis = df.groupby('OrgSize')[tool_columns].sum()
for orgsize in df['OrgSize'].unique():
    if orgsize != 'Not specified':
        org_data = orgsize_analysis.loc[orgsize]
        total_in_org = len(df[df['OrgSize'] == orgsize])
        print(f"\n{orgsize}:")
        redis_users = org_data['Redis']
        if redis_users > 0:
            pct = (redis_users / total_in_org) * 100
            print(f"  Redis: {redis_users} ({pct:.1f}%)")

# Создаем агрегированные данные для DataLens
print(f"\n💾 СОЗДАНИЕ АГРЕГИРОВАННЫХ ДАННЫХ ДЛЯ DATALENS...")

# 1. Данные по инструментам
tools_summary = []
for tool in tool_columns:
    users = df[tool].sum()
    if users > 0:
        tools_summary.append({
            'Tool': tool,
            'Users': users,
            'Percentage': (users / len(df)) * 100
        })
tools_df = pd.DataFrame(tools_summary)
tools_df.to_csv('datalens_tools_summary.csv', index=False)

# 2. Данные по странам и инструментам
country_tools = df.groupby('CountryGroup')[tool_columns].sum()
country_tools['Total_Respondents'] = df.groupby('CountryGroup').size()
country_tools.reset_index(inplace=True)
country_tools.to_csv('datalens_country_tools.csv', index=False)

# 3. Данные по опыту и инструментам
experience_tools = df.groupby('ExperienceLevel')[tool_columns].sum()
experience_tools['Total_Respondents'] = df.groupby('ExperienceLevel').size()
experience_tools.reset_index(inplace=True)
experience_tools.to_csv('datalens_experience_tools.csv', index=False)

# 4. Данные по размеру компании
orgsize_tools = df.groupby('OrgSize')[tool_columns].sum()
orgsize_tools['Total_Respondents'] = df.groupby('OrgSize').size()
orgsize_tools.reset_index(inplace=True)
orgsize_tools.to_csv('datalens_orgsize_tools.csv', index=False)

print(f"\n✅ СОЗДАНЫ ФАЙЛЫ ДЛЯ DATALENS:")
print("  - datalens_tools_summary.csv")
print("  - datalens_country_tools.csv") 
print("  - datalens_experience_tools.csv")
print("  - datalens_orgsize_tools.csv")