import glob
import json
from tabulate import tabulate
import base64

def generate_mermaid_chart(data):
    chart = "```mermaid\npie\n    title Технологии по категориям\n"
    for category, tools in data['categories'].items():
        chart += f'    "{category}" : {len(tools)}\n'
    return chart + "```"

def main():
    tech_data = {'categories': {'Анализ': [], 'Интеграции': [], 'Данные': [], 'Документирование': []}}
    table_data = []

    for file in glob.glob("Cases/**/_techstack.md", recursive=True):
        with open(file) as f:
            raw_content = f.read().split('```json')[1].split('```')[0].strip()
            case_data = json.loads(raw_content)
            
            # Добавляем в таблицу
            row = {
                'Кейс': f"[{file.split('/')[1]}]({file.replace('_techstack.md', '')})",
                'Анализ': ', '.join(case_data['analysis']),
                'Интеграции': ', '.join(case_data['integration']),
                'Данные': ', '.join(case_data['data']),
                'Документирование': ', '.join(case_data['docs'])
            }
            table_data.append(row)
            
            # Агрегируем для диаграммы
            for category in tech_data['categories']:
                tech_data['categories'][category].extend(case_data[category.lower()])

    # Генерация файла
    with open("techstack.md", "w") as f:
        f.write("# 🛠 Технологический стек\n\n")
        f.write(tabulate(table_data, headers="keys", tablefmt="github"))
        f.write("\n\n" + generate_mermaid_chart(tech_data))

if __name__ == "__main__":
    main()