from workit import users_collection
from datetime import date
from workit import newsletters_collection


class Newsletter:

    __MAX_RESULTS = 30
    __MIN_RESULTS = 1
    __MAX_FREQUENCY = 7
    __MIN_FREQUENCY = 1

    def __init__(
        self,
        user_id,
        locations,
        categories,
        keywords,
        max_results,
        frequency,
        last_sent
    ):
        self.user_id = user_id
        self.locations = locations
        self.categories = categories
        self.keywords = keywords
        self.max_results = max_results
        self.frequency = frequency
        self.last_sent = None

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, uid):
        user = users_collection.find({'_id': uid})
        if user:
            self._user_id = uid
        else:
            raise ValueError('No such user.')

    @property
    def locations(self):
        return self._locations

    @locations.setter
    def locations(self, cities):
        if type(cities) is list:
            self._locations = cities
        else:
            raise TypeError(
                f'Locations have to be of type list, not {type(cities)}'
            )

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, choises):
        if type(choises):
            self._categories = choises
        else:
            raise TypeError(
                f'Categories have to be of type list, not {type(choises)}'
            )

    @property
    def max_results(self):
        return self._max_results

    @max_results.setter
    def max_results(self, value):
        if value > self.__MAX_RESULTS:
            self._max_results = self.__MAX_RESULTS
        if value < self.__MIN_RESULTS:
            self._max_results = self.__MIN_RESULTS

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, days):
        if days > self.__MAX_FREQUENCY:
            self.frequency = self.__MAX_FREQUENCY
        if days < self.__MIN_FREQUENCY:
            self.frequency = self.__MIN_FREQUENCY

    def timestamp(self):
        self.last_sent = date.today()

    def find_offers(self):
        query = {}
        if self.locations:
            query['city'] = {'$in': self.locations}
        if self.categories:
            query['category'] = {"$in": self.categories}
        if self.keywords:
            query['$text'] = {'$search': self.keywords}
        return newsletters_collection.find(query).limit(self.max_results)
