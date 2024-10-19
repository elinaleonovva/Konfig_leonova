## Описание
Инструмент командной строки для учебного конфигурационного языка. 

Входной текст на языке yaml принимается из файла. Выходной текст на учебном конфигурационном языке попадает в стандартный вывод.

### Основные констуркции 

- Однострочные комментарии: || Это однострочный комментарий
- Массивы: list( значение, значение, значение, ... )
- Имена: [a-zA-Z][_a-zA-Z0-9]*
- Строки: "Это строка"
- Объявление константы на этапе трансляции: let имя = значение
- Вычисление константы на этапе трансляции: $имя$

## Клонирование репозитория
```
git clone <URL репозитория>
cd <директория проекта>
```

## Запуск программы
```
python converter.py
```

## Аргументы командной строки 
```
"C:\Users\elina\Konfig_leonova\ДЗ\DZ3\config1.yaml"
```
аргумент - путь к yaml файлу (пример пути указан)

## Пример работы

### Конфигурация веб-сервера

#### Входной yaml:
```
# Конфигурация веб-сервера
server_name: "Example.com"
port: "80"
root: "/var/www/html"

let:
  name: "max_connections"
  value: "100"

timeout: $max_connections$

file:
  - "config/nginx.conf"
  - "config/default.conf"
```

#### Конвертированный вывод:
```
|| Конфигурация веб-сервера              
server_name = "Example.com"
port = 80
root = "/var/www/html"
let max_connections = 100
timeout = 100
file = list("config/nginx.conf", "config/default.conf")
```

### Настройки базы данных

#### Входной yaml:
```
# Настройки базы данных
db_host: "localhost"
db_port: "5432"
db_name: "my_database"
db_password: "my_database"

let:
  name: "max_rows"
  value: "5000"

max_rows_per_table: $max_rows$

tables:
  - "users"
  - "orders"
  - "products"

```

#### Конвертированный вывод:
```
|| Настройки базы данных
db_host = "localhost"
db_port = 5432
db_name = "my_database"
db_password = "my_database"
let max_rows = 5000
max_rows_per_table = 5000
tables = list("users", "orders", "products")

```

## Запуск тестов 
```
pytest test_converter.py
```

## Результаты тестирования