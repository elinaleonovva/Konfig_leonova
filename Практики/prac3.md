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
    student(19, group_temp % [4, 20], "Иванов И.И."),
    student(18, group_temp % [5, 20], "Петров П.П."),
    student(18, group_temp % [5, 20], "Сидоров С.С."),
    student(19, group_temp % [20, 22], "Леонова Э.Р."),
  ],
  subject: "Конфигурационное управление",
}
```

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
	"ИКБО-${Natural/show (num + 1)}-2
let makeStudent : Natural -> Text -> Text -> Student =
	\(age : Natural) ->
	\(group : Text) ->
	\(name : Text) ->

let age : Natural = age
let group : Text = group
let name : Text = name
let student : Student = { age, group, name }

in student

let students : List Student = [ 
	makeStudent 19 (groupTemp 4 20) "Иванов И.И.",
	makeStudent 18 (groupTemp 5 20) "Петров П.П.",
	makeStudent 18 (groupTemp 5 20) "Сидоров С.С.",
	makeStudent 19 (groupTemp 20 22) "Леонова Э.Р."
]

let subject = "Конфигурационное управление"
let out = < groups : List Text | students : List Student | subject : Text>

in { 
	subject,
	students,
	groups = generate 23 Text anotherGroupTemp
}
```

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

![image](https://github.com/user-attachments/assets/7b19fd7e-507d-4a18-af5e-b3b9aa3386fd)
