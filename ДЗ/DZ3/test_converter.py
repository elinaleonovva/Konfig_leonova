import pytest
import yaml
from converter import (
    convert_comments_in_line,
    is_number,
    sanitize_name,
    convert_value,
    process_yaml,
    process_yaml_with_comments
)


# Тест для convert_comments_in_line
def test_convert_comments_in_line():
    assert convert_comments_in_line('some_code # comment') == ('some_code', '|| comment')
    assert convert_comments_in_line('code_without_comment') == ('code_without_comment', None)
    assert convert_comments_in_line('# comment_only') == ('', '|| comment_only')
    assert convert_comments_in_line('') == ('', None)


# Тест для is_number
def test_is_number():
    assert is_number("123") is True
    assert is_number("123.456") is True
    assert is_number("not_a_number") is False
    assert is_number("12abc") is False


# Тест для sanitize_name
def test_sanitize_name():
    assert sanitize_name("valid_name") == "valid_name"
    assert sanitize_name("123name") == "_123name"
    assert sanitize_name("invalid name!") == "invalid_name_"


# Тест для convert_value
def test_convert_value():
    constants = {"SOME_CONSTANT": "42"}
    assert convert_value("$SOME_CONSTANT$", constants) == '42'
    assert convert_value("123", constants) == "123"
    assert convert_value("hello world", constants) == '"hello world"'


# Тест для process_yaml
def test_process_yaml():
    yaml_data = {
        "key1": "value1",
        "key2": 123,
        "array": [1, 2, 3],
        "constant": {"name": "CONST", "value": "constant_value"}
    }
    expected_output = (
        'key1 = "value1";\n'
        'key2 = 123;\n'
        'let CONST = "constant_value";\n'
        'array = list(1, 2, 3);'
    )

    actual_output = process_yaml(yaml_data)

    # Сравниваем строки как множества, чтобы порядок строк не был важен
    assert set(actual_output.splitlines()) == set(expected_output.splitlines())


# Тест для process_yaml_with_comments
def test_process_yaml_with_comments(tmp_path):
    # Создаем временный YAML файл для теста
    yaml_content = """
    # Comment
    key1: value1  
    key2: 123  
    array:  
      - 1
      - 2
      - 3
    constant:
      name: CONST
      value: constant_value
    """
    yaml_file = tmp_path / "test.yaml"
    yaml_file.write_text(yaml_content)

    expected_output = (
        '|| Comment\n'
        'key1 = "value1";\n'
        'key2 = 123;\n'
        'array = list(1, 2, 3);\n'
        'let CONST = "constant_value";'
    )

    actual_output = process_yaml_with_comments(str(yaml_file))

    assert actual_output == expected_output