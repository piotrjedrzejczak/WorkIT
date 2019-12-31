from requests import get
from src.model.Offer import Offer
from src.model.Website import Website
from logging import Formatter, FileHandler, getLogger, DEBUG

logger = getLogger('workit.justjoin')
logger.setLevel(DEBUG)
fhandler = FileHandler('src/logs/justjoin.log')
fhandler.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)


class JustJoinJobs(Website):

    __get_offers_url = 'https://justjoin.it/api/offers'

    def __init__(self):
        self.offers = []
        self._raw_offers = []

    def create_offers(self):
        '''Converts raw JSON data to Offer objects'''
        self._get_raw_offers()
        for offer in self._raw_offers:
            try:
                self.offers.append(
                    Offer(
                        title=offer['title'],
                        company=offer['company_name'],
                        city=offer['city'],
                        offerurl='https://justjoin.it/offers/' + offer['id'],
                        salary='{floor} - {ceiling}{currency}'.format(
                            floor=offer["salary_from"],
                            ceiling=offer["salary_to"],
                            currency=offer["salary_currency"]
                        ),
                        techstack=[
                            skill['name']
                            for skill in offer.get('skills', None)
                        ],
                        experience=offer.get('experience_level', None)
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
            self._raw_offers = response.json()
        else:
            self._raw_offers = []
        return self._raw_offers
