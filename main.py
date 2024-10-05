import os.path

from src.hh_api_client import HHAPIClient
from src.json_saver import JSONSaver
from src.paths import get_project_root
from src.vacancy import Vacancy
from src.vacancy_container import VacancyContainer


def user_interaction() -> None:
    # PRIMARY INPUT
    print('Greetings!')
    search_query = input('Enter your query:\n')
    top_n = int(input('Enter the number of vacancies to display:\n'))

    # Creating client
    hh_client = HHAPIClient()

    # Casting Vacancies
    hh_client.load_vacancies(search_query)
    hh_vacancies = hh_client.get_info()
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    # Creating container
    vac_container = VacancyContainer(vacancies_list)

    # Using some features
    # FILTERING
    keyword = input('Enter keyword for filtering or skip (leave it blank):\n')
    keyword = keyword.strip()
    if not keyword:
        print('You decided to skip')
        filtered = vac_container
    else:
        filtered = vac_container.filtered_by(keyword)

    # RANGING / SORTING
    ranging = input("Enter 'Y' to sort vacancies or skip by entering anything else:\n")
    if not 'y' in ranging:
        ranged = filtered
    else:
        ranged = filtered.ranged()

    # Creating JSON Connector with a path to file
    file_name = input('Enter name of a new file:\n')
    path = os.path.join(get_project_root(), 'data', file_name)
    json_saver = JSONSaver(path)
    json_saver.container_extend(ranged)

    top_vacancies = json_saver.get_vacancies().get_top_n(top_n)
    print(top_vacancies)


if __name__ == '__main__':
    user_interaction()
