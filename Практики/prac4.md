# Задача 1
На сайте https://onlywei.github.io/explain-git-with-d3 или http://git-school.github.io/visualizing-git/ (цвета могут отличаться, есть команды undo/redo) с помощью команд эмулятора git получить следующее состояние проекта (сливаем master с first, перебазируем second на master): см. картинку ниже. Прислать свою картинку.
![image](https://github.com/user-attachments/assets/e7aa033c-a880-4b38-9151-ca59681e7457)

## Решение
![image](https://github.com/user-attachments/assets/1dc98ae4-bab7-4df7-b991-eb68880a5b2a)


# Задача 2
Создать локальный git-репозиторий. Задать свои имя и почту (далее – coder1). Разместить файл prog.py с какими-нибудь данными. Прислать в текстовом виде диалог с git.

## Решение
![image](https://github.com/user-attachments/assets/0c429850-6e87-4fa2-a3bb-8905bc6a5e11)

# Задача 3
Создать рядом с локальным репозиторием bare-репозиторий с именем server. Загрузить туда содержимое локального репозитория. Команда git remote -v должна выдать информацию о server! Синхронизировать coder1 с server.

Клонировать репозиторий server в отдельной папке. Задать для работы с ним произвольные данные пользователя и почты (далее – coder2). Добавить файл readme.md с описанием программы. Обновить сервер.

Coder1 получает актуальные данные с сервера. Добавляет в readme в раздел об авторах свою информацию и обновляет сервер.

Coder2 добавляет в readme в раздел об авторах свою информацию и решает вопрос с конфликтами.

Прислать список набранных команд и содержимое git log.

# Задача 4
Написать программу на Питоне (или другом ЯП), которая выводит список содержимого всех объектов репозитория. Воспользоваться командой "git cat-file -p". Идеальное решение – не использовать иных сторонних команд и библиотек для работы с git.

```
import os
import subprocess

def main():
    os.chdir("C:/Users/elina/Desktop/МИРЭА/2 курс/konfig/prac4")

    file_list = subprocess.check_output("dir /b", shell=True).decode("cp866").split()
    print(f"List of files: {file_list}")

    for file_name in file_list:
        file_hash = subprocess.check_output(f"git hash-object {file_name}", shell=True).decode("cp866").strip()
        print(f'{file_name}:\n{subprocess.check_output(f"git cat-file -p {file_hash}", shell=True).decode("cp866")}')


if __name__ == "__main__":
    main()
```
![image](https://github.com/user-attachments/assets/ddb2c1a7-a8b5-4616-bdb9-165ecb1a949b)
