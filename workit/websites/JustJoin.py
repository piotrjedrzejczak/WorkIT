from logging import Formatter, FileHandler, getLogger, DEBUG
from workit.model.Website import Website
from workit.model.Offer import Offer
from datetime import datetime
from requests import get


logger = getLogger('workit.justjoin')
logger.setLevel(DEBUG)
fhandler = FileHandler('workit/logs/justjoin.log')
fhandler.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)


class JustJoinJobs(Website):

    __get_offers_url = 'https://justjoin.it/api/offers'
    __fetch_time = datetime(1, 1, 1)

    def __init__(self):
        self.offers = []
        self._raw_offers = []

    def create_offers(self):
        '''Converts raw JSON data to Offer objects'''
        self.__fetch_time = datetime.now()
        self._get_raw_offers()
        for offer in self._raw_offers:
            new_offer = {
                'title': offer.get('title'),
                'company': offer.get('company_name'),
                'city': offer.get('city'),
                'experience': offer.get('experience_level'),
                'url': 'https://justjoin.it/offers/' + offer.get('id'),
                'techstack': [skill['name'] for skill in offer.get('skills')],
            }
            try:
                salary = offer.get('employment_types')[0].get('salary')
                new_offer['salary'] = {
                    'floor': salary.get('from'),
                    'ceiling': salary.get('to'),
                    'currency': salary.get('currency'),
                }
            except (IndexError, AttributeError):
                new_offer['salary'] = None
            try:
                self.offers.append(Offer(**new_offer))
            except ValueError:
                logger.info(f'Failed to create offer from object: {new_offer}')
                continue
        return self.offers

    def _get_raw_offers(self):
        '''Requests offers and returns them as JSON.'''
        response = get(
            self.__get_offers_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        if response.status_code == 200:
            self._raw_offers = response.json()
        else:
            self._raw_offers = []
        return self._raw_offers
