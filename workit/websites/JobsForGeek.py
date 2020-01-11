from logging import Formatter, FileHandler, getLogger, DEBUG
from workit.model.Website import Website
from workit.model.Offer import Offer
from datetime import datetime
from requests import get


logger = getLogger('workit.jobsforgeek')
logger.setLevel(DEBUG)
fhandler = FileHandler('workit/logs/jobsforgeek.log')
fhandler.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)


class JobsForGeek(Website):

    __get_offers_url = 'https://jobsforgeek.com/api/public/job-offer/'
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
                        title=offer['jobTitle'],
                        company=offer['companyName'],
                        city=offer.get('city', 'Remote'),
                        url='https://jobsforgeek.com/job-offers/details/' +
                            str(offer['id']),
                        salary=self._determine_salary({
                            'emp_floor': offer.get('employmentSalaryFrom', None), # noqa E501
                            'emp_ceil': offer.get('employmentSalaryTo', None),
                            'emp_freq': offer.get('employmentFrequency', None),
                            'b2b_floor': offer.get('b2bSalaryFrom', None),
                            'b2b_ceil': offer.get('b2bSalaryFrom', None),
                            'b2b_freq': offer.get('b2bFrequency', None)
                        }),
                        techstack=offer["skills"],
                        experience=None
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

    def _determine_salary(self, info):
        if info['emp_floor'] is not None and info['emp_ceil'] is not None:
            if info['emp_freq'] == 'MONTH':
                return '{} - {} PLN'.format(
                    info['emp_floor'],
                    info['emp_ceil']
                )
            if info['emp_freq'] == 'HOUR':
                return '{} - {} PLN'.format(
                    info['emp_floor'] * 160,
                    info['emp_ceil'] * 160
                )
        if info['b2b_floor'] is not None and info['b2b_ceil'] is not None:
            if info['b2b_freq'] == 'MONTH':
                return '{} - {} PLN'.format(
                    info['b2b_floor'],
                    info['b2b_ceil']
                )
            if info['b2b_freq'] == 'HOUR':
                return '{} - {} PLN'.format(
                    info['b2b_floor'] * 160,
                    info['b2b_ceil'] * 160
                )
        return 'Undefined'
