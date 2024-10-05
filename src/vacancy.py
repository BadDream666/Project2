from src.vacancy_base import VacancyBase


class Vacancy(VacancyBase):
    """ Represents a vacancy """
    __slots__ = ('name', 'url', 'salary_from', 'salary_to', 'salary_currency')

    def __init__(self,
                 name: str,
                 url: str,
                 salary_from: float,
                 salary_to: float,
                 salary_currency: str,
                 ):
        self.name = name
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency

    # MAGIC METHODS
    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            raise TypeError('Incorrect type for comparison')
        return (self.name == other.name and
                self.url == other.url and
                self.salary_currency == other.salary_currency and
                self.salary_from == other.salary_from and
                self.salary_to == other.salary_to)

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            raise TypeError('Incorrect type for comparison')
        else:
            if self.salary_currency == other.salary_currency:
                return self.salary_from < other.salary_from
            raise ValueError('Comparison of vacancies with salaries in different currencies is not yet provided')

    def __le__(self, other):
        if not isinstance(other, Vacancy):
            raise TypeError('Incorrect type for comparison')
        else:
            if self.salary_currency == other.salary_currency:
                return self.salary_from <= other.salary_from
            raise ValueError('Comparison of vacancies with salaries in different currencies is not yet provided')

    def __gt__(self, other):
        if not isinstance(other, Vacancy):
            raise TypeError('Incorrect type for comparison')
        else:
            if self.salary_currency == other.salary_currency:
                return self.salary_from > other.salary_from
            raise ValueError('Comparison of vacancies with salaries in different currencies is not yet provided')

    def __ge__(self, other):
        if not isinstance(other, Vacancy):
            raise TypeError('Incorrect type for comparison')
        else:
            if self.salary_currency == other.salary_currency:
                return self.salary_from >= other.salary_from
            raise ValueError('Comparison of vacancies with salaries in different currencies is not yet provided')

    def __str__(self):
        # return f'{self.__class__.__name__} ({self.salary_from}-{self.salary_to} {self.salary_currency}) url: {
        # self.url}'
        return (f"Name: {self.name}\nURL: {self.url}\nSalary: {self.salary_from} - {self.salary_to} "
                f"{self.salary_currency}")

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.salary_from}-{self.salary_to} {self.salary_currency}) url: {self.url}'

    @classmethod
    def cast_to_object_list(cls, vacancies: list[dict]) -> list:
        """
        Return list of Vacancy objects from list of JSON vacancy info
        :param vacancies: data in JSONFormat
        :return: list of Vacancy objects
        :param vacancies:
        :return: list of Vacancy objects
        """
        result = []
        for vacancy in vacancies:
            # GET NAME AND URL
            name = vacancy.get('name', 'Untitled')
            url = vacancy.get('url', 'URL not found')

            # GET SALARY
            if vacancy.get('salary'):
                salary_from = cls.valid_value(vacancy.get('salary', {'from': 0}).get('from'))
                salary_to = cls.valid_value(vacancy.get('salary', {'to': 0}).get('to'))
                salary_currency = cls.valid_str(vacancy.get('salary', {'currency': 'USD'}).get('currency'))
            else:
                salary_from = cls.valid_value(vacancy.get('salary_from', 0))
                salary_to = cls.valid_value(vacancy.get('salary_to', 0))
                salary_currency = cls.valid_str(vacancy.get('salary_currency', 'Unknown'))

            vacancy_obj = cls(name, url, salary_from, salary_to, salary_currency)
            result.append(vacancy_obj)
        return result

    @staticmethod
    def valid_str(data):
        if isinstance(data, str) and data:
            return data
        else:
            return 'Data not found'

    @staticmethod
    def valid_value(data):
        """ Util that returns data if it is value, 0 """
        if isinstance(data, (float, int)) and data:
            return data
        else:
            return 0
