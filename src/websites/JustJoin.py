from requests import get
from src.model.Offer import Offer
from src.model.Website import Website


class JustJoinJobs(Website):

    __get_offers_url = 'https://justjoin.it/api/offers'
    
    def __init__(self):
        self.offers = []
        self._raw_offers = []


    def create_offers(self):
        '''Converts raw JSON data to Offer objects'''
        self._get_raw_offers()
        for offer in self._raw_offers:
            self.offers.append(Offer(
                                title=offer['title'],
                                company=offer['company_name'],
                                city=offer['city'],
                                salary=f'{offer["salary_from"]} - {offer["salary_to"]}',
                                techstack=[skill['name'] for skill in offer.get('skills', [])],
                                experience=offer.get('experience_level', []),
                                offerurl='https://justjoin.it/offers/' + offer['id'],
                                logourl=offer.get('company_logo_url', '')
                                )
                        )

        return f'Created {len(self.offers)} offers.'

    
    def _get_raw_offers(self):
        '''Requests offers and returns them as JSON.'''
        response = get(self.__get_offers_url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            self._raw_offers = response.json()
            return f'{len(self._raw_offers)} offers found.'
        else:
            self._raw_offers = []
            return 'No offers found.'

