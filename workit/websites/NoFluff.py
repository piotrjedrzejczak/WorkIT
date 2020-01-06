from logging import Formatter, FileHandler, getLogger, DEBUG
from workit.model.Website import Website
from workit.model.Offer import Offer
from datetime import datetime
from requests import get


logger = getLogger('workit.nofluff')
logger.setLevel(DEBUG)
fhandler = FileHandler('workit/logs/nofluff.log')
fhandler.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)


class NoFluffJobs(Website):

    __get_offers_url = 'https://nofluffjobs.com/api/search/posting?'
    __fetch_time = datetime(1, 1, 1)

    def __init__(self):
        self.offers = []
        self._raw_offers = []

    def create_offers(self):
        '''Converts raw JSON data to Offer objects'''
        self.__fetch_time = datetime.now()
        self._get_raw_offers()
        for offer in self._raw_offers:
            try:
                self.offers.append(
                    Offer(
                        title=offer['title'],
                        company=offer['name'],
                        city=offer['location']['places'][0]['city'],
                        url='https://nofluffjobs.com/job/' + offer['url'],
                        salary=None,
                        techstack=offer.get('technology', None),
                        experience=offer.get('seniority', None)
                    )
                )
            except ValueError:
                logger.info(f'Failed to create offer, values passed: {offer}')
                continue
        return self.offers

    def _get_raw_offers(self):
        '''Requests offers and returns them as JSON.'''
        response = get(
            self.__get_offers_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        if response.status_code == 200:
            self._raw_offers = response.json()['postings']
        else:
            self._raw_offers = []
        return self._raw_offers
