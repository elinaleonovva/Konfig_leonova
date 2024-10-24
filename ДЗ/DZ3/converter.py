import yaml
import re
import argparse


def convert_comments_in_line(line):
    """
    Преобразует комментарии в строке YAML (#) в конфигурационный формат (||).
    """
    comment_split = line.split('#', 1)
    if len(comment_split) > 1:
        comment = comment_split[1].strip()
        line_without_comment = comment_split[0].strip()
        return line_without_comment, f"|| {comment}"
    return line, None


def is_number(value):
    """
    Проверка, является ли строка числом.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def sanitize_name(name):
    """
    Очистка имени переменной или ключа от недопустимых символов.
    """
    return re.sub(r'\W|^(?=\d)', '_', name)


def convert_value(value, constants):
    """
    Преобразует значение в конфигурацию, включая подстановку констант.
    """
    if isinstance(value, int):
        return str(value)
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
    """
    result = []
    constants = {}

    for key, value in yaml_data.items():
        if isinstance(value, str):
            result.append(f'{sanitize_name(key)} = {convert_value(value, constants)}')
        elif isinstance(value, (int, float)):
            result.append(f'{sanitize_name(key)} = {value}')
        elif isinstance(value, dict) and 'value' in value and 'name' in value:
            # Обработка объявления констант
            name = sanitize_name(value['name'])
            constants[name] = str(value['value'])
            result.append(f'let {name} = {convert_value(value["value"], constants)}')
        elif isinstance(value, list):
            # Обработка массивов
            array_values = ', '.join(convert_value(str(item), constants) for item in value)
            result.append(f'{sanitize_name(key)} = list({array_values})')
    return "\n".join(result)


def process_yaml_with_comments(yaml_file):
    """
    Обрабатывает YAML-файл и конвертирует его в конфигурацию с комментариями.
    """
    result = []
    constants = {}

    with open(yaml_file, 'r', encoding='utf-8') as file:
        yaml_lines = []
        for line in file:
            # Обрабатываем строку для поиска комментариев
            line_without_comment, comment = convert_comments_in_line(line)

            # Добавляем основную строку (без комментария)
            if line_without_comment.strip():
                yaml_lines.append(line_without_comment)

            # Добавляем комментарий, если он есть
            if comment:
                result.append(comment)

        # Обработка синтаксических ошибок
        try:
            yaml_data = yaml.safe_load("\n".join(yaml_lines))
        except yaml.YAMLError as exc:
            raise SyntaxError(f"Ошибка синтаксиса в YAML: {exc}")

    config_output = process_yaml(yaml_data)
    result.append(config_output)

    return "\n".join(result)


def main(yaml_file):
    try:
        config_output = process_yaml_with_comments(yaml_file)
        print(config_output)
    except SyntaxError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YAML to custom config converter")
    parser.add_argument('file', type=str, help="YAML file to process")
    args = parser.parse_args()

    main(args.file)