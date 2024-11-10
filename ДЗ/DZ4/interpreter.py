import struct
import csv
import argparse

# Инициализация памяти и аккумулятора для хранения временных данных
MEMORY_SIZE = 1024
memory = [0] * MEMORY_SIZE
accumulator = 0


def format_byte(byte):
    """
    Форматирует байт в шестнадцатеричную строку с префиксом '0x'.
    """
    return f"0x{byte:02X}"


def interpret(binary_file, result_file, start, end):
    """
    Функция интерпретации команд из бинарного файла.

    Читает команды из файла, выполняет их, и сохраняет значения из заданного диапазона памяти в CSV-файл.
    """
    with open(binary_file, 'rb') as binfile, open(result_file, 'w', newline='') as resfile:
        result_writer = csv.writer(resfile)
        result_writer.writerow(['Address', 'Value'])

        # Построчное чтение команды из бинарного файла
        while True:
            command = binfile.read(3)  # Чтение одной команды (3 байта)
            if not command:
                break

            # Распаковка команд
            a_b, b = struct.unpack('>BH', command)
            a = a_b >> 3
            b = ((a_b & 0x07) << 8) | b

            global accumulator

            # Выполнение команды в зависимости от значения 'a'
            if a == 30:  # LOAD_CONSTANT
                accumulator = b
            elif a == 0:  # MEMORY_READ
                if b < len(memory):
                    accumulator = memory[b]
            elif a == 8:  # MEMORY_WRITE
                if b < len(memory):
                    memory[b] = accumulator
            elif a == 20:  # GREATER_THAN
                if b < len(memory):
                    memory[b] = 1 if memory[b] > accumulator else 0
        # Запись диапазона памяти [start, end] в result.csv
        for i in range(start, end + 1):
            if i < len(memory):
                result_writer.writerow([i, memory[i]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter for virtual machine.")
    parser.add_argument("binary_file", help="Path to the binary input file")
    parser.add_argument("result_file", help="Path to the result CSV file")
    parser.add_argument("start", type=int, help="Starting memory address to output")
    parser.add_argument("end", type=int, help="Ending memory address to output")

    args = parser.parse_args()
    interpret(args.binary_file, args.result_file, args.start, args.end)
