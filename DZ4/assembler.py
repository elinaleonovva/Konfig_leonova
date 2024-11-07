import csv
import struct
import sys

# Таблица команд с кодами операций
COMMANDS = {
    'LOAD_CONST': 30,  # Загрузка константы
    'LOAD_MEM': 0,  # Чтение из памяти
    'STORE_MEM': 8,  # Запись в память
    'COMPARE_GT': 20  # Бинарная операция ">"
}


def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as f, open(output_file, 'wb') as out, open(log_file, 'w', newline='') as log_csv:
        writer = csv.writer(log_csv)
        writer.writerow(['command', 'A', 'B', 'binary'])

        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                print("Неправильный формат команды:", line)
                continue

            command, a_str, b_str = parts
            a = COMMANDS.get(command, None)
            b = int(b_str)

            if a is None:
                print(f"Неизвестная команда: {command}")
                continue

            # Записываем в бинарный файл и файл лога
            binary_instruction = (a << 5) | (b & 0x1FFFF)
            out.write(struct.pack('>I', binary_instruction)[1:])  # Записываем 3 байта
            writer.writerow([command, a, b, f"0x{binary_instruction:06X}"])


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python assembler.py <input.asm> <output.bin> <log.csv>")
        sys.exit(1)

    assemble(sys.argv[1], sys.argv[2], sys.argv[3])
