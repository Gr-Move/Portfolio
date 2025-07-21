import json
import glob
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
        
        > ⚠️ **Этот файл автоматически обновляется. Ручные правки будут перезаписаны!**
        
        ## Общие принципы
        - Используем только проверенные технологии
        - Стек обновляется ежеквартально
        - Критерии выбора: производительность, документация, сообщество
        
        ### Технологический стек (Тестовые данные):
        - Нотации: BPMN 2.0, UML (Use Case, Sequence), C4 Model
        - Документация: ГОСТ 34, Техническое задание, Архитектурное решение
        - REST API: Swagger/OpenAPI, curl/requests тесты
        - Язык: Markdown + HTML + CSS
        
        ## Автоматически генерируемые данные:\n\n"""

    # Ищем файл TechStack.json в папке Portfolio/Cases/**/
    file_paths = glob.glob('Cases/**/TechStack.json')

    if not file_paths:
        print("Файл TechStack.json не найден.")
        return

    # Читаем данные из первого найденного файла TechStack.json
    try:
        with open(file_paths[0], 'r', encoding='utf-8') as f:
            case_data = json.load(f)
    except FileNotFoundError:
        print("Файл TechStack.json не найден.")
        return
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        return

    # Формируем таблицу данных
    row = {
        'Кейс': 'TechStack',
        'Анализ': ', '.join(case_data.get('analysis', [])),
        'Интеграции': ', '.join(case_data.get('integration', [])),
        'Данные': ', '.join(case_data.get('data', [])),
        'Документирование': ', '.join(case_data.get('docs', []))
    }
    table_data.append(row)

    for category in tech_data['categories']:
        tools = case_data.get(category.lower(), [])
        tech_data['categories'][category].extend(tools)

    with open("techstack.md", "w", encoding="utf-8") as f:
        f.write(header_content)
        f.write(tabulate(table_data, headers="keys", tablefmt="github"))
        f.write("\n\n" + generate_mermaid_chart(tech_data))

if __name__ == "__main__":
    main()
