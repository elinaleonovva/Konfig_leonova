# Задача 1
Реализовать на Jsonnet приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.
```
local student(age, group, name) = {
  age: age,
  group: group,
  name: name,
};

local group_temp = "ИКБО-%g-%g";
{
  groups: [
  (group_temp % [x, 20]) for x in std.range(1, 24)
  ],

  students: [
    student(19, group_temp % [4, 20], "Маркаданов А.А."),
    student(18, group_temp % [5, 20], "Землянская М.М."),
    student(18, group_temp % [5, 20], "Барташевский Д.Д."),
    student(19, group_temp % [20, 22], "Леонова Э.Р."),
  ],
  subject: "Конфигурационное управление",
}
```

![image](https://github.com/user-attachments/assets/1db4721f-c04d-43da-b2dc-56b5e730acc4)
![image](https://github.com/user-attachments/assets/e1a71156-86a6-4655-b62a-a736964db071)
![image](https://github.com/user-attachments/assets/843d4d89-554a-4902-a0b8-36e7078967aa)


# Задача 2
Реализовать на Dhall приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.
```
let generate = https://prelude.dhall-lang.org/List/generate

let Student : Type = { 
  age : Natural,
  group : Text,
  name : Text
}

let groupTemp : Natural -> Natural -> Text =
  \(num : Natural) ->
  \(year : Natural) ->
  "ИКБО-${Natural/show num}-${Natural/show year}"

let anotherGroupTemp : Natural -> Text =
  \(num : Natural) ->
  "ИКБО-${Natural/show (num + 1)}-20"  

let makeStudent : Natural -> Text -> Text -> Student =
  \(age : Natural) ->
  \(group : Text) ->
  \(name : Text) ->
  { age = age, group = group, name = name }

let students : List Student = 
  [ makeStudent 19 (groupTemp 4 20) "Иванов И"
  , makeStudent 18 (groupTemp 5 20) "Петров П.П."
  , makeStudent 18 (groupTemp 5 20) "Леонова Э.Р."
  , makeStudent 19 (groupTemp 20 22) "Барташевский Д.Д."
  ]

let subject = "Конфигурационное управление"

let out = { groups : List Text, students : List Student, subject : Text }

in { 
  subject = subject,
  students = students,
  groups = generate 24 Text anotherGroupTemp  
}
```

![image](https://github.com/user-attachments/assets/0739c25a-4955-4d6b-9d7c-6885b7ba1b3b)


# Задача 3-5
Реализовать грамматики, описывающие следующие языки (для каждого решения привести БНФ). Код решения должен содержаться в переменной BNF
```
import random

def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar

def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)

# Задача 3:
BNF_3 = '''
E = 0 | 1
S = E S | E
'''

# Задача 4:
BNF_4 = '''
OG = (
ZG = )
OF = {
ZF = }
S = OG ZG | OG S ZG | OF ZF | OF S ZF
'''

# Задача 5:
BNF_5 = '''
P = x | y
O = &
E = ( E ) | ~ E | P O P | ( E O E )
'''

# Генерация для задачи 3
print("Задача 3:")
for i in range(10):
    print(generate_phrase(parse_bnf(BNF_3), 'S'))

# Генерация для задачи 4
print("\nЗадача 4:")
for i in range(10):
    print(generate_phrase(parse_bnf(BNF_4), 'S'))

# Генерация для задачи 5
print("\nЗадача 5:")
for i in range(10):
    print(generate_phrase(parse_bnf(BNF_5), 'E'))

```

![image](https://github.com/user-attachments/assets/b9404cec-65c3-40cd-aabe-8906cdda92eb)
![image](https://github.com/user-attachments/assets/8df3a334-3049-43d5-8938-2ae3a898b931)
