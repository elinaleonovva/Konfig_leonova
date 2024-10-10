import pytest
from unittest.mock import patch, mock_open
import requests
import subprocess
from PIL import Image
from dz2 import get_package_dependencies, main


# Тестирование функции get_package_dependencies
@patch('requests.get')
def test_get_package_dependencies_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = [
        {"catalogEntry": "https://example.com/catalog"},
        {
            "dependencyGroups": [
                {
                    "targetFramework": ".NETFramework4.6.2",
                    "dependencies": [
                        {"id": "Dependency1", "range": "[1.0.0]"}
                    ]
                }
            ]
        }
    ]

    expected_output = '''digraph G {
"test_package" -> ".NETFramework4.6.2";
".NETFramework4.6.2" -> "Dependency1";
}'''

    result = get_package_dependencies("test_package", "1.0.0")
    assert result == expected_output


# Имитация случая, когда API возвращает пустой ответ
@patch('requests.get')
def test_get_package_dependencies_no_catalog_entry(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}

    result = get_package_dependencies("test_package", "1.0.0")
    assert result == "Ошибка: Не удалось найти catalogEntry для test_package версии 1.0.0"


# Проверка на возникновение HTTP-ошибки (404)
@patch('requests.get')
def test_get_package_dependencies_http_error(mock_get):
    mock_get.return_value.status_code = 404

    result = get_package_dependencies("test_package", "1.0.0")
    assert result == "Ошибка: Не удалось получить информацию о пакете test_package версии 1.0.0"


# Тестирование ошибок при запуске через терминал
@patch('argparse.ArgumentParser.parse_args')
@patch('subprocess.run')
@patch('builtins.open', new_callable=mock_open)
@patch('PIL.Image.open')
@patch('dz2.get_package_dependencies')
def test_main_success(mock_get_deps, mock_image_open, mock_open_file, mock_subprocess_run, mock_parse_args):
    mock_parse_args.return_value.graphviz_path = '/path/to/dot'
    mock_parse_args.return_value.package_info = 'Microsoft.Extensions.Logging 9.0.0'

    mock_get_deps.return_value = '''digraph G {
"Microsoft.Extensions.Logging" -> ".NETFramework4.6.2";
".NETFramework4.6.2" -> "Dependency1";
}'''

    main()

    # Проверяем, что файл .dot был записан
    mock_open_file.assert_called_once_with("dependencies.dot", "w")
    mock_open_file().write.assert_called_once_with(mock_get_deps.return_value)

    # Проверяем, что Graphviz был вызван правильно
    mock_subprocess_run.assert_called_once_with(['/path/to/dot', '-Tpng', 'dependencies.dot', '-o', 'dependencies.png'])

    # Проверяем, что изображение было открыто
    mock_image_open.assert_called_once_with('dependencies.png')


# Обработка неверного формата аргументов командной строки
@patch('argparse.ArgumentParser.parse_args')
def test_main_package_info_error(mock_parse_args):
    mock_parse_args.return_value.graphviz_path = '/path/to/dot'
    mock_parse_args.return_value.package_info = 'InvalidFormat'

    with patch('builtins.print') as mock_print:
        main()
        mock_print.assert_called_once_with("Ошибка: Пожалуйста, введите имя пакета и версию, разделённые пробелом.")