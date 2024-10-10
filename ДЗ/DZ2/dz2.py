import requests
import subprocess
import argparse
from PIL import Image


def get_package_dependencies(package_name, version):
    '''
    Получение зависимостей пакета .NET из API NuGet
    Создание графа зависимостей в формате, который понимает Graphviz
    '''

    # Ссылка на каталог
    url = f"https://api.nuget.org/v3/registration5-gz-semver2/{package_name.lower()}/{version}.json"
    response = requests.get(url)
    dependencies = set()
    code = "digraph G {\n"

    if response.status_code != 200:
        return f"Ошибка: Не удалось получить информацию о пакете {package_name} версии {version}"

    data = response.json()

    # Получаем ссылку на метаданные пакета
    catalog_entry_url = data.get("catalogEntry")

    if not catalog_entry_url:
        return f"Ошибка: Не удалось найти catalogEntry для {package_name} версии {version}"

    # Шаг 2: Получаем данные из catalogEntry
    catalog_response = requests.get(catalog_entry_url)

    if catalog_response.status_code != 200:
        return f"Ошибка: Не удалось получить catalogEntry по адресу {catalog_entry_url}"

    catalog_data = catalog_response.json()
    for group in catalog_data['dependencyGroups']:
        group_name = group['targetFramework']
        if 'dependencies' in group:
            code += f'"{package_name}" -> "{group_name}";\n'
            for dependency in group['dependencies']:
                name, range = dependency['id'], dependency['range']
                dependencies.add((name, range))
                code += f'"{group_name}" -> "{name}";\n'

    code += "}"
    return code


def main():
    parser = argparse.ArgumentParser(description="Визуализатор зависимостей для пакетов .NET")
    parser.add_argument('--graphviz_path', type=str, required=True, help="Путь к программе Graphviz (dot.exe)")
    parser.add_argument('--package_info', type=str, required=True, help="Имя пакета и версия, разделённые пробелом")

    args = parser.parse_args()

    try:
        package_name, version = args.package_info.split(' ', 1)
    except ValueError:
        print("Ошибка: Пожалуйста, введите имя пакета и версию, разделённые пробелом.")
        return

    # Получаем зависимости пакета
    graph_code = get_package_dependencies(package_name, version)

    if isinstance(graph_code, str) and graph_code.startswith("Ошибка"):
        print(graph_code)
        return

    # Сохраняем сгенерированный код в файл dependencies.dot
    with open("dependencies.dot", "w") as f:
        f.write(graph_code)

    # Генерируем png из .dot файла с помощью Graphviz
    subprocess.run([args.graphviz_path, "-Tpng", "dependencies.dot", "-o", "dependencies.png"])

    img = Image.open("dependencies.png")
    img.show()


if __name__ == "__main__":
    main()