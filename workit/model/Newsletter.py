from datetime import date
from workit import mongo
from uuid import uuid4


class Newsletter:

    def __init__(
        self,
        user_id,
        locations,
        categories,
        keywords,
        max_results,
        frequency,
        last_sent=None,
        _id=None
    ):
        self.user_id = user_id
        self.locations = locations
        self.categories = categories
        self.keywords = keywords
        self.max_results = max_results
        self.frequency = frequency
        self.last_sent = last_sent
        self._id = uuid4().hex if _id is None else _id

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, uid):
        user = mongo.users.find({'_id': uid})
        if user:
            self._user_id = uid
        else:
            raise ValueError('No such user.')

    def timestamp(self):
        self.last_sent = date.today().__str__()

    def save(self):
        mongo.newsletters.insert(self.__dict__)
