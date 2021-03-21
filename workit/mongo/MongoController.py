from pymongo import MongoClient


class MongoController:

    _SESSION = MongoClient('mongodb://db:27017/')

    def __init__(self):
        self.users = self._SESSION.db.users
        self.offers = self._SESSION.db.offers
        self.newsletters = self._SESSION.db.newsletters
        self.offers.create_index(
            [("title", "text"), ("techstack", "text")], default_language="english"
        )

    def search_offers(self, keyword, category, city, exp):
        query = {}
        if keyword:
            query.update({"$text": {"$search": keyword}})
        if category:
            query.update({"category": category})
        if city:
            query.update({"city": city})
        if exp:
            query.update({"experience": exp})
        return self.offers.find(query)

    def offers_sample(self, size):
        return self.offers.aggregate([{"$sample": {"size": size}}])

    def edit_user_field(self, id, field, value):
        payload = {'$set': {}}
        if value:
            payload['$set'] = {field: value}
            self.users.update_one({'_id': id}, payload)
            return True
        else:
            return False

    def insert_multiple_offers(self, offers):
        if offers:
            self.offers.insert_many(offers)
        else:
            raise ValueError("Cannot insert empty list.")

    def aggregate_single_field(self, field, sort, size):
        pipe = []
        if field:
            pipe.append({"$group": {"_id": {field: "$"+field}, "count": {"$sum": 1}}})
        if size > 0:
            pipe.append({"$limit": size})
        if sort == 1 or sort == -1:
            pipe.append({"$sort": {"count": sort}})
        else:
            raise ValueError(f'Sort takes only two values 1 or -1, you passed {sort}')
        return list(self.offers.aggregate(pipe))

    def assemble_newsletter(self, locations, categories, keywords, size):
        query = {}
        if locations:
            query['city'] = {'$in': locations}
        if categories:
            query['category'] = {"$in": categories}
        if keywords:
            query['$text'] = {'$search': keywords}
        return list(self.offers.find(query).limit(size))

    def refresh_offers(self, new_offers):
        if new_offers:
            self.offers.delete_many({})
            self.insert_multiple_offers(new_offers)
            return True
        raise ValueError('New set of offers is empty.')
