import requests
import subprocess
from PIL import Image


def get_package_dependencies(package_name, version):
    # Шаг 1: Получаем ссылку на каталог (catalogEntry)
    url = f"https://api.nuget.org/v3/registration5-gz-semver2/{package_name.lower()}/{version}.json"
    response = requests.get(url)
    dependencies = set()
    code = "digraph G {\n"

    if response.status_code != 200:
        print(f"Ошибка: Не удалось получить информацию о пакете {package_name} версии {version}")
        return

    data = response.json()

    # Получаем ссылку на метаданные пакета
    catalog_entry_url = data.get("catalogEntry")

    if not catalog_entry_url:
        print(f"Ошибка: Не удалось найти catalogEntry для {package_name} версии {version}")
        return

    # Шаг 2: Получаем данные из catalogEntry
    catalog_response = requests.get(catalog_entry_url)

    if catalog_response.status_code != 200:
        print(f"Ошибка: Не удалось получить catalogEntry по адресу {catalog_entry_url}")
        return

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

    package_name = input("Введите имя пакета\n")
    version = input("Введите версию\n")
    graph_code = get_package_dependencies(package_name, version)

    # Сохраняем сгенерированный код в файл dependencies.dot
    with open("dependencies.dot", "w") as f:
        f.write(graph_code)

    # Генерируем png из .dot файла с помощью Graphviz
    # subprocess.run(["dot", "-Tpng", "dependencies.dot", "-o", "dependencies.png"])
    subprocess.run([r"C:\Program Files\Graphviz\bin\dot.exe", "-Tpng", "dependencies.dot", "-o", "dependencies.png"])

    # Открываем сгенерированное изображение
    img = Image.open("dependencies.png")
    img.show()


if __name__ == "__main__":
    main()
