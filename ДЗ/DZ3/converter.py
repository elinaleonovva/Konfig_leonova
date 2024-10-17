import yaml
import re

def convert_comments(line):
    """
    Преобразует комментарии из формата YAML (#) в конфигурационный формат (||).
    """
    comment_match = re.match(r'\s*#(.*)', line)
    if comment_match:
        comment = comment_match.group(1).strip()
        return f"|| {comment}"
    return None

def is_number(value):
    """Проверка, является ли строка числом."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def sanitize_name(name):
    """Очистка имени переменной или ключа от недопустимых символов."""
    return re.sub(r'\W|^(?=\d)', '_', name)


def convert_value(value, constants):
    """
    Преобразует значение в конфигурацию, включая подстановку констант.

    Параметры:
        value (str): Значение для преобразования.
        constants (dict): Словарь констант.

    Возвращает:
        str: Преобразованное значение.
    """
    value = value.strip()

    # Подстановка констант по шаблону $имя$
    value = re.sub(r'\$(\w+)\$', lambda match: constants.get(match.group(1), match.group(0)), value)

    if is_number(value):
        return value
    else:
        return f'"{value}"'


def process_yaml(yaml_data):
    """
    Обрабатывает YAML-данные и конвертирует их в конфигурационный формат.

    Параметры:
        yaml_data (dict): Данные из YAML.

    Возвращает:
        str: Преобразованная конфигурация.
    """
    result = []
    constants = {}

    # Обработка ключей и значений
    for key, value in yaml_data.items():
        if isinstance(value, str):
            if value.startswith("#"):
                continue  # Пропускаем однострочные комментарии
            result.append(f'{sanitize_name(key)} = {convert_value(value, constants)};')
        elif isinstance(value, (int, float)):
            result.append(f'{sanitize_name(key)} = {value};')
        elif isinstance(value, dict) and 'value' in value and 'name' in value:
            # Обработка объявления констант
            name = sanitize_name(value['name'])
            constants[name] = value['value']
            result.append(f'let {name} = {convert_value(value["value"], constants)};')
        elif isinstance(value, list):
            # Обработка массивов
            array_values = ', '.join(convert_value(str(item), constants) for item in value)
            result.append(f'{sanitize_name(key)} = list({array_values});')

    return "\n".join(result)


def main(yaml_file):
    """Главная функция для загрузки YAML-файла и его обработки."""
    with open(yaml_file, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)

    config_output = process_yaml(yaml_data)
    print(config_output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="YAML to custom config converter")
    parser.add_argument('-f', '--file', type=str, required=True, help="YAML file to process")
    args = parser.parse_args()

    main(args.file)