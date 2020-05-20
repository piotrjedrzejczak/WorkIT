from datetime import datetime
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

    def timestamp(self):
        self.last_sent = datetime.now().__str__()

    def save(self):
        mongo.newsletters.insert(self.__dict__)

    def get_offers(self):
        return mongo.assemble_newsletter(
            self.locations,
            self.categories,
            self.keywords,
            self.max_results
        )

    def update_lastsent(self):
        mongo.newsletters.update_one(
            {"_id": self._id},
            {"$set": {"last_sent": self.last_sent}}
        )
