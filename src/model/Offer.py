from src.model.Const import CATEGORIES, CURRENCIES
from re import sub


class Offer:

    def __init__(
        self,
        title,
        company,
        city,
        offerurl,
        salary,
        techstack,
        experience
    ):

        self.title = title
        self.company = company
        self.city = city
        self.offerurl = offerurl
        self.salary = salary
        self.techstack = techstack
        self.experience = experience
        self.category = self._classify()

    def __repr__(self):
        return str(self.__dict__)

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        self._experience = []
        if type(value) is list:
            self._experience = value
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
            self._techstack = value
        if type(value) is str and value != '':
            if value.find(',') == -1:
                self._techstack = value.split(',')
            self._techstack = [value]

    @property
    def offerurl(self):
        return self._offerurl

    @offerurl.setter
    def offerurl(self, url):
        if url is not None and url != '':
            self._offerurl = url
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
