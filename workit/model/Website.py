class Website():

    def create_offers(self):
        raise NotImplementedError

    def serialize_offers(self):
        return [dict(offer) for offer in self.offers]
