import json

from src.vacancy_container import VacancyContainer
from tests.conftest import temp_file


def test_add_vacancy(json_saver, vacancy, temp_file):
    json_saver.add_vacancy(vacancy)

    with open(temp_file.name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    vacancy_dict = {attr: getattr(vacancy, attr) for attr in vacancy.__slots__}
    assert vacancy_dict in data


def test_get_vacancies(vacancy_1, vacancy_2, json_saver):
    json_saver.add_vacancy(vacancy_1)
    json_saver.add_vacancy(vacancy_2)

    result_container = json_saver.get_vacancies()
    expected_container = VacancyContainer([vacancy_1, vacancy_2])

    # DEBUG PRINT
    # print("expected container:")
    # print(expected_container)
    # print("result container:")
    # print(result_container)

    assert result_container == expected_container


def test_delete_vacancy(vacancy_1, vacancy_2, vacancy_3, json_saver):
    json_saver.add_vacancy(vacancy_1)
    json_saver.add_vacancy(vacancy_2)
    json_saver.add_vacancy(vacancy_3)

    json_saver.delete_vacancy(vacancy_3)

    expected_container = VacancyContainer([vacancy_1, vacancy_2])

    result_container = json_saver.get_vacancies()

    assert result_container == expected_container


def test_container_extend(vacancy_1, vacancy_2, vacancy_3, json_saver):
    container = VacancyContainer([vacancy_1, vacancy_2, vacancy_3])
    json_saver.container_extend(container)

    result_container = json_saver.get_vacancies()
    expected_container = VacancyContainer([vacancy_1, vacancy_2, vacancy_3])

    assert result_container == expected_container


def test_purge_all(vacancy_1, vacancy_2, json_saver):
    json_saver.add_vacancy(vacancy_1)
    json_saver.add_vacancy(vacancy_2)

    json_saver.purge_all()

    result_container = json_saver.get_vacancies()
    expected_container = VacancyContainer([])

    assert result_container == expected_container
