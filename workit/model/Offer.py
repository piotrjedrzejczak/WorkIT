from workit.const import CATEGORIES, CURRENCIES, POLISH_CHARS
from uuid import uuid4
from re import sub


class Offer:

    def __init__(
        self,
        title,
        company,
        city,
        url,
        salary,
        techstack,
        experience
    ):

        self.title = title
        self.company = company
        self.city = city
        self.url = url
        self.salary = salary
        self.techstack = techstack
        self.experience = experience
        self.category = self._classify()
        self._id = self._generate_id()

    def __repr__(self):
        return str(self.__dict__)

    def __iter__(self):
        yield 'title', self.title
        yield 'company', self.company
        yield 'city', self.city
        yield 'url', self.url
        yield 'salary', self.salary
        yield 'techstack', self.techstack
        yield 'experience', self.experience
        yield 'category', self.category

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, name):
        if type(name) is str:
            cleaned_city_name = name.split(',')[0] \
                                    .replace('-', ' ') \
                                    .lower() \
                                    .strip()
            for char in POLISH_CHARS.keys():
                if char in cleaned_city_name:
                    cleaned_city_name = cleaned_city_name.replace(
                        char, POLISH_CHARS[char]
                    )
            self._city = cleaned_city_name.title()
        else:
            raise ValueError(
                'City field has to be of type str. ' +
                f'You passed {type(name)}'
            )

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        self._experience = []
        if type(value) is list:
            self._experience = [exp.title() for exp in value]
        if type(value) is str:
            if value.find(',') == -1:
                self._experience = value.split(',')
            self._experience = [value.title()]

    @property
    def techstack(self):
        return self._techstack

    @techstack.setter
    def techstack(self, value):
        self._techstack = []
        if type(value) is list:
            self._techstack = [tech.title() for tech in value]
        if type(value) is str and value != '':
            if value.find(',') == -1:
                self._techstack = value.split(',')
            self._techstack = [value.title()]

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if url is not None and url != '':
            self._url = url
        else:
            raise ValueError(f'Offer URL {url} cannot be empty or None.')

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        self._salary = {'floor': None, 'ceiling': None, 'currency': None}
        if value is not None and value != '':
            currency = sub(r'[^a-zA-Z]', '', value)
            split = value.split('-')
            if currency.lower() in CURRENCIES:
                self._salary['currency'] = currency.upper()
            if len(split) == 2:
                floor = sub(r'[^0-9]', '', split[0])
                ceiling = sub(r'[^0-9]', '', split[1])
                if floor.isdecimal() and ceiling.isdecimal():
                    self._salary['floor'] = floor
                    self._salary['ceiling'] = ceiling

    def _classify(self):
        description = sub(r'-', '', self.title).lower()
        description = sub(r'[^a-zA-Z.+# ]', ' ', description).lower()
        for keyword in description.split():
            for category, tags in CATEGORIES.items():
                if keyword in tags:
                    return category
        for tech in self.techstack:
            for category, tags in CATEGORIES.items():
                if tech.lower() in tags:
                    return category
        return 'Other'

    def _generate_id(self):
        return str(uuid4())