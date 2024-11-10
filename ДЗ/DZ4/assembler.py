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


# Допустимые команды
VALID_COMMANDS = {
    "LOAD_CONSTANT": load_constant,
    "MEMORY_READ": memory_read,
    "MEMORY_WRITE": memory_write,
    "GREATER_THAN": greater_than,
}


# Ассемблерная обработка
def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as infile, open(output_file, 'wb') as binfile, open(log_file, 'w') as logfile:
        for line_num, line in enumerate(infile, 1):
            line = line.strip()  # Удаление пробелов в начале и конце строки

            if not line:  # Пропуск пустых строк
                continue

            parts = line.split()

            # Проверка количества аргументов
            if len(parts) != 2:
                print(f"Ошибка в строке {line_num}: неверное количество аргументов. "
                      f"Ожидалось 2, найдено {len(parts)}.")
                print("Пожалуйста, перезапишите данные в файле на корректные.")
                return

            command = parts[0]
            b_value = parts[1]

            # Проверка допустимости команды
            if command not in VALID_COMMANDS:
                print(f"Ошибка в строке {line_num}: недопустимая команда '{command}'.")
                print("Пожалуйста, используйте одну из следующих команд:", ", ".join(VALID_COMMANDS.keys()))
                print("Перезапишите данные в файле корректно.")
                return

            # Проверка, является ли b числом
            try:
                b = int(b_value)
            except ValueError:
                print(f"Ошибка в строке {line_num}: '{b_value}' не является целым числом.")
                print("Пожалуйста, перезапишите данные в файле на корректные.")
                return

            # Получаем функцию команды и формируем код
            command_func = VALID_COMMANDS[command]
            code = command_func(b)

            # Запись данных в лог и бинарный файл
            a_value = (code[0] >> 3)  # Извлекаем значение 'a' из кода команды
            logfile.write(f"A = {a_value}, B = {b}\n")
            binfile.write(code)


# Настраиваем аргументы командной строки
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler for virtual machine.")
    parser.add_argument("input_file", help="Path to the input file with text program")
    parser.add_argument("output_file", help="Path to the output binary file")
    parser.add_argument("log_file", help="Path to the log CSV file")

    args = parser.parse_args()
    assemble(args.input_file, args.output_file, args.log_file)
