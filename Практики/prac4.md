# Задача 1
На сайте https://onlywei.github.io/explain-git-with-d3 или http://git-school.github.io/visualizing-git/ (цвета могут отличаться, есть команды undo/redo) с помощью команд эмулятора git получить следующее состояние проекта (сливаем master с first, перебазируем second на master): см. картинку ниже. Прислать свою картинку.

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

## Решение 
```
elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1
$ git init
Initialized empty Git repository in C:/Users/elina/Desktop/МИРЭА/2 курс/konfig/prac41/coder1/.git/

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ git config user.name "Coder 1"

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ git config user.email "coder1@yandex.ru"

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ echo "# Программа для теста" > prog.py

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ git add prog.py
warning: in the working copy of 'prog.py', LF will be replaced by CRLF the next time Git touches it

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ git commit -m "first commit"
[master (root-commit) 42ba7db] first commit
 1 file changed, 1 insertion(+)
 create mode 100644 prog.py

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ cd ..

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41
$ git init --bare server.git
Initialized empty Git repository in C:/Users/elina/Desktop/МИРЭА/2 курс/konfig/prac41/server.git/

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41
$ cd coder1

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ git remote add server ../server.git

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ git remote -v
server  ../server.git (fetch)
server  ../server.git (push)

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ git push server master
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 242 bytes | 80.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To ../server.git
 * [new branch]      master -> master

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ cd ..

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41
$ git clone server.git coder2
Cloning into 'coder2'...
done.

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41
$ cd coder1

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ echo "INFO prog1" >> readme.md

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ git add readme.md
warning: in the working copy of 'readme.md', LF will be replaced by CRLF the next time Git touches it

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ git commit -m "coder1 info"
[master 3c554b1] coder1 info
 1 file changed, 1 insertion(+)
 create mode 100644 readme.md

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ git push server master
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 16 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 276 bytes | 92.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To ../server.git
   42ba7db..3c554b1  master -> master

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder1 (master)
$ cd ../coder2

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master)
$ echo "INFO prog2 data" >> readme.md

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master)
$ git add readme.md
warning: in the working copy of 'readme.md', LF will be replaced by CRLF the next time Git touches it

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master)
$ git config user.name "coder2"

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master)
$ git config user.email "coder2@gmail.com"

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master)
$ git commit -m "coder2 info"
[master e918880] coder2 info
 1 file changed, 1 insertion(+)
 create mode 100644 readme.md

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master)
$ git push origin master
To C:/Users/elina/Desktop/МИРЭА/2 курс/konfig/prac41/server.git
 ! [rejected]        master -> master (fetch first)
error: failed to push some refs to 'C:/Users/elina/Desktop/МИРЭА/2 курс/konfig/prac41/server.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master)
$ git pull --no-rebase origin master
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 256 bytes | 19.00 KiB/s, done.
From C:/Users/elina/Desktop/МИРЭА/2 курс/konfig/prac41/server
 * branch            master     -> FETCH_HEAD
   42ba7db..3c554b1  master     -> origin/master
Auto-merging readme.md
CONFLICT (add/add): Merge conflict in readme.md
Automatic merge failed; fix conflicts and then commit the result.

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master|MERGING)
$ git add readme.md

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master|MERGING)
$ git commit -m "fix readme"
[master 02400ff] fix readme

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master)
$ git push origin master
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 16 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (6/6), 616 bytes | 123.00 KiB/s, done.
Total 6 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To C:/Users/elina/Desktop/МИРЭА/2 курс/konfig/prac41/server.git
   3c554b1..02400ff  master -> master

elina@MEGABOOK_S1 MINGW64 ~/Desktop/МИРЭА/2 курс/konfig/prac41/coder2 (master)
$ git log --graph --all
*   commit 02400ffe119c6d3b7381f4cc9d59bf64d6502687 (HEAD -> master, origin/master, origin/HEAD)
|\  Merge: e918880 3c554b1
| | Author: coder2 <coder2@gmail.com>
| | Date:   Fri Nov 1 00:57:31 2024 +0300
| |
| |     fix readme
| |
| * commit 3c554b1668c097068676d0266773324172e9de5d
| | Author: Coder 1 <coder1@yandex.ru>
| | Date:   Fri Nov 1 00:55:38 2024 +0300
| |
| |     coder1 info
| |
* | commit e918880ff11916360afbf85396411aa91929fc0c
|/  Author: coder2 <coder2@gmail.com>
|   Date:   Fri Nov 1 00:56:44 2024 +0300
|
|       coder2 info
|
* commit 42ba7db1dc448ccf645bd8f9aa15ef22ebd36868
  Author: Coder 1 <coder1@yandex.ru>
  Date:   Fri Nov 1 00:53:45 2024 +0300

      first commit
```
![image](https://github.com/user-attachments/assets/05467aae-2999-4e47-a952-87e044345f5d)


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
