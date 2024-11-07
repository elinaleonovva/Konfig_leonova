import csv
import struct
import sys

# Размеры памяти и регистра
MEMORY_SIZE = 1024
ACCUMULATOR = 0


# Функции команд
def load_const(value):
    global ACCUMULATOR
    ACCUMULATOR = value


def load_mem(memory, address):
    global ACCUMULATOR
    ACCUMULATOR = memory[address]


def store_mem(memory, address):
    global ACCUMULATOR
    memory[address] = ACCUMULATOR


def compare_gt(memory, address):
    global ACCUMULATOR
    if memory[address] > ACCUMULATOR:
        memory[address] = 1
    else:
        memory[address] = 0


# Интерпретатор для бинарного файла
def interpret(binary_file, result_file, memory_range):
    memory = [0] * MEMORY_SIZE

    with open(binary_file, 'rb') as f:
        while chunk := f.read(3):
            instruction = struct.unpack('>I', b'\x00' + chunk)[0]
            a = (instruction >> 17) & 0x1F
            b = instruction & 0x1FFFF

            if a == 30:  # LOAD_CONST
                load_const(b)
            elif a == 0:  # LOAD_MEM
                load_mem(memory, b)
            elif a == 8:  # STORE_MEM
                store_mem(memory, b)
            elif a == 20:  # COMPARE_GT
                compare_gt(memory, b)

    # Записываем память в файл результата
    with open(result_file, 'w', newline='') as result_csv:
        writer = csv.writer(result_csv)
        writer.writerow(['address', 'value'])

        start, end = map(int, memory_range.split(':'))
        for i in range(start, end + 1):
            writer.writerow([i, memory[i]])


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python interpreter.py <output.bin> <result.csv> <memory_range>")
        sys.exit(1)

    interpret(sys.argv[1], sys.argv[2], sys.argv[3])
