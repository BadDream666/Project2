import json
import os

from src.vacancy import Vacancy
from src.vacancy_container import VacancyContainer
from src.vacancy_saver import VacancySaver


class JSONSaver(VacancySaver):
    def __init__(self, filename: str):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        else:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list) or data != []:
                    with open(self.filename, 'w', encoding='utf-8') as f:
                        json.dump([], f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy):
        """ Adds vacancy to file """
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # using getattr
        vacancy_dict = {attr: getattr(vacancy, attr) for attr in vacancy.__slots__}
        data.append(vacancy_dict)

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_vacancies(self):
        """ Returns all data as a container """
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        vacancy_list = Vacancy.cast_to_object_list(data)

        return VacancyContainer(vacancy_list)

    def delete_vacancy(self, vacancy: Vacancy):
        """ Removes vacancy from .json file"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        vacancy_dict = {attr: getattr(vacancy, attr) for attr in vacancy.__slots__}

        data = [item for item in data if item != vacancy_dict]

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def container_extend(self, container: VacancyContainer):
        """ Allows to extend file with a whole container """
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for vacancy in container.get_list():
            vacancy_dict = {attr: getattr(vacancy, attr) for attr in vacancy.__slots__}

            data.append(vacancy_dict)

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def purge_all(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
