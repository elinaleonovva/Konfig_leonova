# Задача 1
Написать программу на Питоне, которая транслирует граф зависимостей civgraph в makefile в духе примера выше. Для мало знакомых с Питоном используется упрощенный вариант civgraph: civgraph.json.
```
import json

def print_all_dependences(target, graph, added, makefile):
    # Рекурсивная запись зависимостей в Makefile
    for dep in graph.get(target, []):
        print_all_dependences(dep, graph, added, makefile)
    if target not in added:
        makefile.write(f"{target}: {' '.join(graph.get(target, []))}\n")
        makefile.write(f"\t@echo \"{target} done.\"\n")
        added.add(target)

def main():
    with open("civgraph.json", "r") as file:
        graph = json.load(file)

    last_target = input("Enter the last target: ")

    with open("Makefile", "w") as makefile:
        added = set()
        print_all_dependences(last_target, graph, added, makefile)

if __name__ == "__main__":
    main()
```

![image](https://github.com/user-attachments/assets/6b91fc88-7d55-457d-948f-89ccb793e63a)
![image](https://github.com/user-attachments/assets/1269f3c3-1735-4436-bac7-6b3acda6fd94)
![image](https://github.com/user-attachments/assets/b55087f6-0e27-46ef-b7e8-4192d92669c7)

# Задача 2
Реализовать вариант трансляции, при котором повторный запуск make не выводит для civgraph на экран уже выполненные "задачи".
```
import json

def print_all_dependences(x, graph, added, makefile):
    for i in graph[x]:
        print_all_dependences(i, graph, added, makefile)
    if x not in added:
        # Генерация правила для каждой задачи с проверкой файла-флага
        makefile.write(f"{x}: .{x}_done\n")
        makefile.write(f".{x}_done:\n")
        makefile.write(f"\t@echo \"{x} done.\"\n")
        makefile.write(f"\ttouch .{x}_done\n")
    added.add(x)

def main():
    graph = json.loads(open("civgraph.json").read())
    last = input("Enter the last target: ")

    with open("Makefile", "w") as makefile:
        makefile.write(f"{last}: ")
        for dep in graph[last]:
            makefile.write(f"{dep} ")
        makefile.write("\n\t@echo \"{last} done.\"\n")

        added = set()
        print_all_dependences(last, graph, added, makefile)


if __name__ == "__main__":
    main()
```

![Без имени](https://github.com/user-attachments/assets/7d746e29-bb9c-4590-bc84-7f595dad2e46)

# Задача 3
Добавить цель clean, не забыв и про "животное".
```
import json

def print_all_dependences(x, graph, added, makefile):
    for i in graph[x]:
        print_all_dependences(i, graph, added, makefile)
    if x not in added:
        # Генерация правила для каждой задачи без точки в имени файла-флага
        makefile.write(f"{x}: {x}_done\n")
        makefile.write(f"{x}_done:\n")
        makefile.write(f"\t@echo \"{x} done.\"\n")
        makefile.write(f"\ttouch {x}_done\n") 
    added.add(x)

def main():
    graph = json.loads(open("civgraph.json").read())
    last = input("Enter the last target: ")

    with open("Makefile", "w") as makefile:
        makefile.write(f"{last}: ")
        for dep in graph[last]:
            makefile.write(f"{dep} ")
        makefile.write("\n\t@echo \"{last} done.\"\n")

        added = set()
        print_all_dependences(last, graph, added, makefile)

        makefile.write("clean:\n")
        makefile.write("\t@echo \"Cleaning up...\"\n")
        for i in added:
            makefile.write(f"\trm -f {i}_done\n")


if __name__ == "__main__":
    main()
```
![Без имени](https://github.com/user-attachments/assets/043039ac-3628-424d-88d4-035621e2cc5d)

# Задача 4
Написать makefile для следующего скрипта сборки:
```
gcc prog.c data.c -o prog
dir /B > files.lst
7z a distr.zip *.*
```Вместо gcc можно использовать другой компилятор командной строки, но на вход ему должны подаваться два модуля: prog и data. Если используете не Windows, то исправьте вызовы команд на их эквиваленты из вашей ОС. В makefile должны быть, как минимум, следующие задачи: all, clean, archive. Обязательно покажите на примере, что уже сделанные подзадачи у вас не перестраиваются.

Решение

```
all: prog files.lst distr.zip

prog: prog.c data.c
    gcc prog.c data.c -o prog

files.lst: 
    dir /B > files.lst

distr.zip: *
    7z a distr.zip $^
clean:
    rm -f prog files.lst distr.zip
```

