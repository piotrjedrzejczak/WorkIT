from logging import Formatter, FileHandler, getLogger, DEBUG
from workit.model.Website import Website
from workit.model.Offer import Offer
from datetime import datetime
from requests import get
from unicodedata import normalize

logger = getLogger('workit.pracuj')
logger.setLevel(DEBUG)
fhandler = FileHandler('workit/logs/pracuj.log')
fhandler.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)


class PracujJobs(Website):

    __get_offers_url = 'https://massachusetts.pracuj.pl/api/offers'
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
                        title=normalize('NFKD', offer['jobTitle']),
                        company=normalize('NFKD', offer['employer']),
                        city=normalize('NFKD', offer['location']),
                        url=normalize('NFKD', offer['offerUrl']),
                        salary=self._parse_salary(offer['salary']),
                        experience=normalize('NFKD', offer['employmentLevel']),
                        techstack=[]
                    )
                )
            except ValueError:
                logger.info(f'Failed to create offer, values passed: {offer}')
                continue
        return self.offers

    def _get_raw_offers(self):
        '''Requests offers and returns them as JSON.'''
        for page in range(1, 21):
            response = get(
                self.__get_offers_url,
                headers={'User-Agent': 'Mozilla/5.0'},
                params={'pn': page}
            )
            if response.status_code == 200 and response.json()['offers'] != []:
                self._raw_offers.extend(response.json()['offers'])
            else:
                break
        return self._raw_offers

    def _parse_salary(self, raw_salary):
        if raw_salary:
            raw_salary = normalize('NFKD', raw_salary)
            salary_details = raw_salary.split(' ')
            if len(salary_details) == 5:
                # Splitting on DASH, do not mistake with HYPHEN.
                stake = salary_details[0].split('–')
                try:
                    if salary_details[-1] == 'godz.':
                        return '{floor}-{ceil} {currency}'.format(
                            floor=str(int(stake[0])*160),
                            ceil=str(int(stake[1])*160),
                            currency=salary_details[1]
                        )
                    elif salary_details[-1] == 'mies.':
                        return '{floor}-{ceil} {currency}'.format(
                            floor=stake[0],
                            ceil=stake[1],
                            currency=salary_details[1]
                        )
                    else:
                        return None
                except IndexError:
                    logger.info(
                        f'Index Out Of Range. \
                        Raw Salary {raw_salary}, \
                        After Split {salary_details}, \
                        After Last Split {stake}')
            return None
        return None
