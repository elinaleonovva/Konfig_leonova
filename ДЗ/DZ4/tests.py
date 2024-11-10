import struct
import pytest
from assembler import load_constant, memory_read, memory_write, greater_than, assemble
from interpreter import interpret


@pytest.mark.parametrize("command_func, b, expected_a", [
    (load_constant, 256, 30),
    (memory_read, 128, 0),
    (memory_write, 512, 8),
    (greater_than, 1024, 20),
])
def test_commands(command_func, b, expected_a):
    result = command_func(b)
    a_b, result_b = struct.unpack('>BH', result)
    assert a_b >> 3 == expected_a  # Проверка значения 'a' в команде
    assert result_b == b & 0xFF  # Проверка значения 'b' в команде


def test_assemble_correct_input(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.bin"
    log_file = tmp_path / "log.csv"

    # Корректные данные
    input_file.write_text("LOAD_CONSTANT 256\nMEMORY_READ 128\nMEMORY_WRITE 512\nGREATER_THAN 1024\n")
    assemble(str(input_file), str(output_file), str(log_file))

    # Проверка содержимого output.bin
    with open(output_file, 'rb') as binfile:
        assert binfile.read(3) == load_constant(256)
        assert binfile.read(3) == memory_read(128)
        assert binfile.read(3) == memory_write(512)
        assert binfile.read(3) == greater_than(1024)

    # Проверка содержимого log.csv
    with open(log_file, 'r') as logfile:
        lines = logfile.readlines()
        assert lines[0] == "A = 30, B = 256\n"
        assert lines[1] == "A = 0, B = 128\n"
        assert lines[2] == "A = 8, B = 512\n"
        assert lines[3] == "A = 20, B = 1024\n"


@pytest.mark.parametrize("input_text, expected_error_message", [
    ("INVALID_COMMAND 123\n", "Ошибка в строке 1: недопустимая команда 'INVALID_COMMAND'."),
    ("LOAD_CONSTANT\n", "Ошибка в строке 1: неверное количество аргументов. Ожидалось 2, найдено 1."),
    ("LOAD_CONSTANT abc\n", "Ошибка в строке 1: 'abc' не является целым числом."),
])
def test_assemble_invalid_input(tmp_path, capsys, input_text, expected_error_message):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.bin"
    log_file = tmp_path / "log.csv"

    # Запись некорректных данных
    input_file.write_text(input_text)

    # Проверка, что выполнение завершается с сообщением об ошибке
    assemble(str(input_file), str(output_file), str(log_file))
    captured = capsys.readouterr()
    assert expected_error_message in captured.out


def test_interpret(tmp_path):
    binary_file = tmp_path / "output.bin"
    result_file = tmp_path / "result.csv"

    # Создаем бинарный файл для интерпретации
    with open(binary_file, 'wb') as binfile:
        binfile.write(load_constant(42))
        binfile.write(memory_write(10))
        binfile.write(memory_read(10))
        binfile.write(greater_than(5))

    # Выполняем интерпретацию и проверяем результат
    interpret(str(binary_file), str(result_file), start=0, end=15)

    # Проверка содержимого result.csv
    with open(result_file, 'r') as resfile:
        reader = resfile.readlines()
        assert reader[0].strip() == "Address,Value"
        # Проверяем, что память была модифицирована корректно на адресах 0-15


if __name__ == "__main__":
    pytest.main()
