import struct
import argparse


# Определяем функции для каждой команды
def load_constant(b):
    a = 30
    return struct.pack('>BH', (a << 3) | (b >> 8), b & 0xFF)


def memory_read(b):
    a = 0
    return struct.pack('>BH', (a << 3) | (b >> 8), b & 0xFF)


def memory_write(b):
    a = 8
    return struct.pack('>BH', (a << 3) | (b >> 8), b & 0xFF)


def greater_than(b):
    a = 20
    return struct.pack('>BH', (a << 3) | (b >> 8), b & 0xFF)


# Ассемблерная обработка
def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as infile, open(output_file, 'wb') as binfile, open(log_file, 'w') as logfile:
        for line in infile:
            line = line.strip()  # Удаление пробелов в начале и конце строки
            if not line:  # Пропуск пустых строк
                continue
            parts = line.split()
            command = parts[0]
            if command == "LOAD_CONSTANT":
                b = int(parts[1])
                code = load_constant(b)
                logfile.write(f"A = 30, B = {b}\n")
            elif command == "MEMORY_READ":
                b = int(parts[1])
                code = memory_read(b)
                logfile.write(f"A = 0, B = {b}\n")
            elif command == "MEMORY_WRITE":
                b = int(parts[1])
                code = memory_write(b)
                logfile.write(f"A = 8, B = {b}\n")
            elif command == "GREATER_THAN":
                b = int(parts[1])
                code = greater_than(b)
                logfile.write(f"A = 20, B = {b}\n")
            else:
                continue
            binfile.write(code)


# Настраиваем аргументы командной строки
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler for virtual machine.")
    parser.add_argument("input_file", help="Path to the input file with text program")
    parser.add_argument("output_file", help="Path to the output binary file")
    parser.add_argument("log_file", help="Path to the log CSV file")

    args = parser.parse_args()
    assemble(args.input_file, args.output_file, args.log_file)