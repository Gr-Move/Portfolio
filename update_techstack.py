import glob
import json
from tabulate import tabulate


def generate_mermaid_chart(data):
    """Генерирует Mermaid-диаграмму в формате Markdown"""
    chart = "```mermaid\npie\n    title Технологии по категориям\n"
    for category, tools in data['categories'].items():
        chart += f'    "{category}" : {len(tools)}\n'
    return chart + "```"


def main():
    tech_data = {
        'categories': {
            'Анализ': [],
            'Интеграции': [],
            'Данные': [],
            'Документирование': []
        }
    }
    table_data = []

    # Статичная часть (запишем это один раз в итоговый файл)
    header_content = """# 🛠 Технологический стек

> Этот файл автоматически обновляется. Ручные правки будут перезаписаны!

## Общие принципы
- Используем только проверенные технологии
- Стек обновляется ежеквартально
- Критерии выбора: производительность, документация, сообщество
<br><br>
### Технологический стек (Тестовые данные):
- Нотации: BPMN 2.0, UML (Use Case, Sequence), C4 Model
- Документация: ГОСТ 34, Техническое задание, Архитектурное решение
- REST API: Swagger/OpenAPI, curl/requests тесты
- Язык: Markdown + HTML + CSS

## Автоматически генерируемые данные:\n\n"""

    # Поиск всех файлов _techstack.md в подпапках Cases
    for file in glob.glob("Portfolio/Cases/**/_techstack.md", recursive=True):
        with open(file) as f:
            content = f.read()
            # Предполагаем, что JSON начинается с "json: "
            try:
                raw_content = content.split('json: ')[1].strip()
                case_data = json.loads(raw_content)
            except (IndexError, json.JSONDecodeError):
                print(f"Ошибка при обработке файла: {file}")
                continue

            # Формирование строки для таблицы
            row = {
                'Кейс': f"[{file.split('/')[-2]}]({file.replace('_techstack.md', '')})",
                'Анализ': ', '.join(case_data.get('analysis', [])),
                'Интеграции': ', '.join(case_data.get('integration', [])),
                'Данные': ', '.join(case_data.get('data', [])),
                'Документирование': ', '.join(case_data.get('docs', []))
            }
            table_data.append(row)

            # Агрегация данных для диаграммы
            for category in tech_data['categories']:
                tech_data['categories'][category].extend(case_data.get(category.lower(), []))

    # Генерация итогового файла
    with open("techstack.md", "w") as f:
        f.write(header_content)
        f.write(tabulate(table_data, headers="keys", tablefmt="github"))
        f.write("\n\n" + generate_mermaid_chart(tech_data))


if __name__ == "__main__":
    main()
