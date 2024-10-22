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

![image](https://github.com/user-attachments/assets/c63cfa47-0167-4911-ba09-5ea4c4003ab5)


# Задача 2
Реализовать вариант трансляции, при котором повторный запуск make не выводит для civgraph на экран уже выполненные "задачи".
```
import json
import os

def get_dependencies(graph, target_technology):
    dependencies = set(graph.get(target_technology, []))
    for dependency in graph.get(target_technology, []):
        dependencies.update(get_dependencies(graph, dependency))
    return dependencies

def update_makefile(graph, target_technology):
    completed_tasks = read_completed_tasks()
    dependencies = get_dependencies(graph, target_technology)
    completed_tasks.add(target_technology)
    
    with open('Makefile', 'a') as makefile:
        for dependency in dependencies:
            if dependency not in completed_tasks:
                completed_tasks.add(dependency)
                makefile.write(f'\t@echo "{dependency} done"\n')

    write_completed_tasks(completed_tasks)

def read_completed_tasks():
    if os.path.exists("task_done.txt"):
        with open("task_done.txt", 'r') as file:
            return set(file.read().splitlines())
    return set()

def write_completed_tasks(tasks):
    with open("task_done.txt", 'w') as file:
        file.write('\n'.join(tasks))

if __name__ == '__main__':
    with open('civgraph.json') as json_file:
        dependency_graph = json.load(json_file)
    target_input = input('Введите цель: ')
    update_makefile(dependency_graph, target_input)
```

![image](https://github.com/user-attachments/assets/e05a6fe2-6171-4cda-881d-2f2ba25a0131)


# Задача 3
Добавить цель clean, не забыв и про "животное".
```
import json
import os

def read_tasks():
    tasks = []
    if os.path.isfile("task_done.txt"):
        with open("task_done.txt", 'r') as file:
            tasks = file.read().splitlines()
    return set(tasks)


def write_tasks(tasks):
    with open("task_done.txt", 'w') as file:
        file.write('\n'.join(sorted(tasks)))


def clear_tasks():
    if os.path.isfile("task_done.txt"):
        os.remove("task_done.txt")
        print("Cleaned completed tasks.")
    else:
        print("No tasks to clean.")


def read_civgraph():
    try:
        with open("civgraph.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File civgraph.json not found.")
        return {}


def process_dependencies(graph, start_node):
    seen = set()
    ordered_tasks = []
    done_tasks = read_tasks()

    def traverse(node):
        if node not in seen and node not in done_tasks:
            seen.add(node)
            dependencies = graph.get(node, [])
            for dep in dependencies:
                traverse(dep)
            ordered_tasks.append(node)

    traverse(start_node)

    for task in ordered_tasks:
        if task not in done_tasks:
            print(task)
            done_tasks.add(task)

    write_tasks(done_tasks)


if __name__ == '__main__':
    graph = read_civgraph()
    user_action = input("Enter action: ").strip().lower()

    if user_action == 'clean':
        clear_tasks()
    elif user_action == 'make':
        target = input("Enter the target technology: ").strip()
        if target in graph:
            process_dependencies(graph, target)
        else:
            print(f"Target '{target}' not found in the graph.")
    else:
        print("Invalid action. Please enter 'make' or 'clean'.")
```
![image](https://github.com/user-attachments/assets/00f86098-0c08-432f-8df6-1cf73c132cd9)
![image](https://github.com/user-attachments/assets/749986a8-4b1c-4bf1-b2b8-a89321d752a9)


# Задача 4
Написать makefile для следующего скрипта сборки:
```
gcc prog.c data.c -o prog
dir /B > files.lst
7z a distr.zip *.*
```Вместо gcc можно использовать другой компилятор командной строки, но на вход ему должны подаваться два модуля: prog и data. Если используете не Windows, то исправьте вызовы команд на их эквиваленты из вашей ОС. В makefile должны быть, как минимум, следующие задачи: all, clean, archive. Обязательно покажите на примере, что уже сделанные подзадачи у вас не перестраиваются.
```

Решение

```
CC = gcc 
SRC = prog.c data.c  
EXEC = prog  
ARCHIVE = distr.zip 

ifeq ($(OS),Windows_NT)
    LIST_CMD = dir /B > files.lst  # Команда для создания списка файлов в Windows
else
    LIST_CMD = ls > files.lst  # Команда для создания списка файлов в Linux/macOS
endif

.PHONY: all clean archive

all: $(EXEC)

$(EXEC): $(SRC)
	$(CC) $(SRC) -o $(EXEC)

archive: $(EXEC)
	$(LIST_CMD) 
	7z a $(ARCHIVE) *.* 

clean:
	rm -f $(EXEC) files.lst $(ARCHIVE)
```
![image](https://github.com/user-attachments/assets/8c22421d-9634-4ecb-b37d-3f69ba11e8b1)
![image](https://github.com/user-attachments/assets/9dbf7205-088d-4218-8204-db2b5476b723)
![image](https://github.com/user-attachments/assets/9eba6ebd-779b-4226-b107-6d67f24ec4d2)
