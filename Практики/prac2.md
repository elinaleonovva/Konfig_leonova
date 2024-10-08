# Задача 1
Вывести служебную информацию о пакете matplotlib (Python). Разобрать основные элементы содержимого файла со служебной информацией из пакета. 

![image](https://github.com/user-attachments/assets/b0351d97-4a57-4d80-8112-6378b943bf21)
![image](https://github.com/user-attachments/assets/5ff3fda0-ceb2-4401-a4e6-d6b5e4859697)

# Задача 2
Вывести служебную информацию о пакете express (JavaScript). Разобрать основные элементы содержимого файла со служебной информацией из пакета. 

![image](https://github.com/user-attachments/assets/aac8ab1d-3757-4814-b6c6-4b62de7a0a1c)
![image](https://github.com/user-attachments/assets/83992569-fdb0-48d4-bf81-7e6572e22ec6)
![image](https://github.com/user-attachments/assets/e8c73f4b-9b98-43a9-a290-8b3338eb10a3)

# Задача 3
Сформировать graphviz-код и получить изображения зависимостей matplotlib и express.
```
import requests
def clear_name(s: str):
    s2 = ""
    for c in s:
        if c.isalpha():
            s2 = s2 + c
    return s2

def main():
    package_name = input()
    print("digraph G {")

    try:
        main_dependencies = [clear_name(x.split()[0]) for x in
                             requests.get(f"https://pypi.org/pypi/{package_name}/json").json()["info"]["requires_dist"]]
    except Exception:
        print("Неизвестная библиотека")
        return

    for dependency in main_dependencies:
        print(f"{package_name} -> {dependency}")
        try:
            child_dependencies = [clear_name(x.split()[0]) for x in
                                  requests.get(f"https://pypi.org/pypi/{dependency}/json").json()["info"][
                                      "requires_dist"]]
        except Exception:
            child_dependencies = []

        for dependency2 in child_dependencies:
            if dependency2 != package_name:
                print(f"{dependency} -> {dependency2}")

    print("}")

if __name__ == "__main__":
    main()
```

![image](https://github.com/user-attachments/assets/b88dc37c-3e73-44f7-934e-f7c4f81c9b70)
![image](https://github.com/user-attachments/assets/c6a3e9b6-29cd-493f-9879-caf01b0f9621)
![image](https://github.com/user-attachments/assets/b76e02d2-ee35-43e3-ad57-40e7f2f9369a)
![image](https://github.com/user-attachments/assets/4e313f59-35c7-41bb-b7e7-030cee09a055)
![image](https://github.com/user-attachments/assets/d9374f9d-e9ac-4bb3-9699-920f7db83ffa)
![image](https://github.com/user-attachments/assets/89c9c611-ee71-4412-8b39-d4c9e27be612)

# Задача 4
Изучить основы программирования в ограничениях. Установить MiniZinc, разобраться с основами его синтаксиса и работы в IDE.
Решить на MiniZinc задачу о счастливых билетах. Добавить ограничение на то, что все цифры билета должны быть различными (подсказка: используйте all_different). Найти минимальное решение для суммы 3 цифр.

![image](https://github.com/user-attachments/assets/5d814dfd-b5a4-4bb3-a7e7-45f2944e3eec)

# Задача 5
Решить на MiniZinc задачу о зависимостях пакетов для рисунка, приведенного ниже.
![image_2024-10-07_17-39-41](https://github.com/user-attachments/assets/0f143a54-8f04-47af-aea3-f8a379bf3026)


# Задача 6
Решить на MiniZinc задачу о зависимостях пакетов для следующих данных.
``` 
root 1.0.0 зависит от foo ^1.0.0 и target ^2.0.0.
foo 1.1.0 зависит от left ^1.0.0 и right ^1.0.0.
foo 1.0.0 не имеет зависимостей.
left 1.0.0 зависит от shared >=1.0.0.
right 1.0.0 зависит от shared <2.0.0.
shared 2.0.0 не имеет зависимостей.
shared 1.0.0 зависит от target ^1.0.0.
target 2.0.0 и 1.0.0 не имеют зависимостей.
```

![image](https://github.com/user-attachments/assets/f3f024d3-7ff1-4e5d-84f3-c4e260186d8c)











