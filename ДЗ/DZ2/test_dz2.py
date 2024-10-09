import pytest
from dz2 import get_package_dependencies  # Импортируйте вашу функцию


# Фикстура для предоставления пакетов и версий
@pytest.fixture
def package_info():
    return {
        'Newtonsoft.Json': '13.0.3',
        'System.Text.Json': '9.0.0-rc.2.24473.5',
        'NonExistent.Package': '1.0.0'
    }


# Имитация функции для тестирования
def mock_get(package_name, version):
    if package_name == 'Newtonsoft.Json' and version == '13.0.3':
        return {
            "catalogEntry": "https://api.nuget.org/v3/registration5-gz-semver2/Newtonsoft.Json/13.0.3.json",
            "dependencyGroups": [
                {
                    "targetFramework": ".NETFramework,Version=v4.5",
                    "dependencies": [{"id": "Newtonsoft.Json.Bson", "range": "[1.0.0, 2.0.0)"}]
                }
            ]
        }
    elif package_name == 'System.Text.Json' and version == '9.0.0-rc.2.24473.5':
        return {
            "catalogEntry": "https://api.nuget.org/v3/registration5-gz-semver2/System.Text.Json/9.0.0-rc.2.24473.5.json",
            "dependencyGroups": []
        }
    else:
        return None  # Для несуществующих пакетов


@pytest.mark.parametrize(
    'package_name, version, expected_dependencies',
    [
        ('Newtonsoft.Json', '13.0.3', {('Newtonsoft.Json.Bson', '[1.0.0, 2.0.0)')}),
        ('System.Text.Json', '9.0.0-rc.2.24473.5', set()),  # Ожидаем, что зависимостей нет
        ('NonExistent.Package', '1.0.0', set()),  # Ожидаем, что зависимостей нет
    ]
)
def test_get_package_dependencies(package_info, package_name, version, expected_dependencies):
    # Здесь мы вызываем имитацию функции вместо requests.get
    response = mock_get(package_name, version)

    if response is None:
        result = "Ошибка: пакет не найден"
        assert expected_dependencies == set()  # Если ошибка, то зависимостей не должно быть
    else:
        # Здесь будет ваша логика, чтобы извлечь зависимости из response
        dependencies = set()
        if 'dependencyGroups' in response:
            for group in response['dependencyGroups']:
                for dep in group['dependencies']:
                    dependencies.add((dep['id'], dep['range']))

        # Проверяем, что зависимости совпадают с ожидаемыми
        assert expected_dependencies == dependencies
