import csv
import re
import pytest
from assembler import assemble, load_constant, memory_read, memory_write, greater_than
from interpreter import interpret

# Тестовые значения для проверки на шестнадцатеричные коды
test_commands = [
    ("LOAD_CONSTANT 684", b'\x9E\x55\x00'),
    ("MEMORY_READ 327", b'\xE0\x28\x00'),
    ("MEMORY_WRITE 168", b'\x08\x15\x00'),
    ("GREATER_THAN 679", b'\xF4\x54\x00')
]

# Путь к файлам
input_file = 'input.txt'
output_file = 'output.bin'
log_file = 'log.csv'
result_file = 'result.csv'


@pytest.fixture
def prepare_input_file(tmp_path):
    """Создает временный файл с тестовыми командами"""
    temp_input = tmp_path / input_file
    with open(temp_input, 'w') as f:
        for command, _ in test_commands:
            f.write(command + '\n')
    return temp_input


@pytest.fixture
def prepare_output_log_files(tmp_path):
    """Создает временные файлы для бинарного и лог файлов"""
    temp_output = tmp_path / output_file
    temp_log = tmp_path / log_file
    return temp_output, temp_log


@pytest.fixture
def prepare_binary_file(tmp_path):
    """Создает временный бинарный файл для интерпретатора"""
    temp_binary = tmp_path / output_file
    with open(temp_binary, 'wb') as f:
        for _, expected_code in test_commands:
            f.write(expected_code)
    return temp_binary


def test_assemble_commands(prepare_input_file, prepare_output_log_files):
    """Тестирует выполнение assemble с проверкой правильного кода команд"""
    temp_input, temp_output, temp_log = prepare_input_file, *prepare_output_log_files

    # Выполнение ассемблера
    assemble(temp_input, temp_output, temp_log)

    # Проверка бинарного файла
    with open(temp_output, 'rb') as f:
        for _, expected_code in test_commands:
            assert f.read(3) == expected_code


def test_log_file_format():
    """Тестирует формат и содержание лог файла"""
    log_data = [
        "A = 30, B = 684 (0x9E, 0x55, 0x00)",
        "A = 0, B = 327 (0xE0, 0x28, 0x00)",
        "A = 8, B = 168 (0x08, 0x15, 0x00)",
        "A = 20, B = 679 (0xF4, 0x54, 0x00)"
    ]

    # Регулярное выражение для проверки формата строки
    log_pattern = re.compile(r"A = (\d+), B = (\d+) \((0x[0-9A-Fa-f]+, 0x[0-9A-Fa-f]+, 0x[0-9A-Fa-f]+)\)")

    for line in log_data:
        match = log_pattern.match(line.strip())
        assert match, f"Неверный формат строки: {line.strip()}"

        a_value = int(match.group(1))
        b_value = int(match.group(2))
        hex_values = match.group(3)

        if a_value == 30:
            assert b_value == 684
            assert hex_values == "0x9E, 0x55, 0x00"
        elif a_value == 0:
            assert b_value == 327
            assert hex_values == "0xE0, 0x28, 0x00"
        elif a_value == 8:
            assert b_value == 168
            assert hex_values == "0x08, 0x15, 0x00"
        elif a_value == 20:
            assert b_value == 679
            assert hex_values == "0xF4, 0x54, 0x00"
        else:
            assert False, f"Неизвестное значение A = {a_value}"


def test_interpreter_output_format(prepare_binary_file, tmp_path):
    """Тестирует интерпретацию и форматирование выводимого CSV файла"""
    temp_binary = prepare_binary_file
    temp_result = tmp_path / result_file

    # Выполнение интерпретатора
    interpret(temp_binary, temp_result, start=0, end=5)

    # Проверка содержимого CSV файла
    with open(temp_result, 'r') as res:
        reader = csv.reader(res)
        header = next(reader)
        assert header == ['Address', 'Value']
        rows = list(reader)
        assert len(rows) >= 6


@pytest.mark.parametrize("command, expected_code", test_commands)
def test_hex_code_formatting(command, expected_code):
    """Тестирует корректность шестнадцатеричного кода для каждой команды"""
    command_name, b_value = command.split()
    b = int(b_value)

    if command_name == "LOAD_CONSTANT":
        assert load_constant(b) == expected_code
    elif command_name == "MEMORY_READ":
        assert memory_read(b) == expected_code
    elif command_name == "MEMORY_WRITE":
        assert memory_write(b) == expected_code
    elif command_name == "GREATER_THAN":
        assert greater_than(b) == expected_code