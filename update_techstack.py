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
    with open("techstack.md", "w") as f:
        # Статичная часть
        f.write("""# 🛠 Технологический стек

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

    ## Автоматически генерируемые данные:\n\n""")

    # Автоматическая часть:
    # Инициализация структур данных
    tech_data = {
        'categories': {
            'Анализ': [],
            'Интеграции': [],
            'Данные': [],
            'Документирование': []
        }
    }
    table_data = []

    # Шаг 1: Поиск всех файлов _techstack.md в подпапках Cases
    for file in glob.glob("Cases/**/_techstack.md", recursive=True):
        with open(file) as f:
            # Шаг 2: Извлечение JSON-данных из файла
            raw_content = f.read().split('```json')[1].split('```')[0].strip()
            case_data = json.loads(raw_content)

            # Шаг 3: Формирование строки для таблицы
            row = {
                'Кейс': f"[{file.split('/')[1]}]({file.replace('_techstack.md', '')})",
                'Анализ': ', '.join(case_data['analysis']),
                'Интеграции': ', '.join(case_data['integration']),
                'Данные': ', '.join(case_data['data']),
                'Документирование': ', '.join(case_data['docs'])
            }
            table_data.append(row)

            # Шаг 4: Агрегация данных для диаграммы
            for category in tech_data['categories']:
                tech_data['categories'][category].extend(case_data[category.lower()])

    # Шаг 5: Генерация итогового файла
    with open("techstack.md", "w") as f:
        # Заголовок
        f.write("# 🛠 Технологический стек\n\n")

        # Таблица данных (используем формат GitHub Markdown)
        f.write(tabulate(table_data, headers="keys", tablefmt="github"))

        # Добавляем Mermaid-диаграмму
        f.write("\n\n" + generate_mermaid_chart(tech_data))


if __name__ == "__main__":
    main()