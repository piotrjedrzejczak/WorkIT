from requests import get
from src.model.Offer import Offer
from src.model.Website import Website


class NoFluffJobs(Website):

    __get_offers_url = 'https://nofluffjobs.com/api/search/posting?'
    
    def __init__(self):
        self.offers = []
        self._raw_offers = []


    def create_offers(self):
        '''Converts raw JSON data to Offer objects'''
        self._get_raw_offers()
        for offer in self._raw_offers:
            self.offers.append(Offer(
                                title=offer['title'],
                                company=offer['name'],
                                city=offer['location']['places'][0]['city'],
                                techstack=offer.get('technology', []),
                                experience=offer.get('seniority', []),
                                offerurl='https://nofluffjobs.com/job/' + offer['url'],
                                logourl=offer.get('logo', '')
                                )
                        )

        return f'Created {len(self.offers)} offers.'

    
    def _get_raw_offers(self):
        '''Requests offers and returns them as JSON.'''
        response = get(self.__get_offers_url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            self._raw_offers = response.json()['postings']
            return f'{len(self._raw_offers)} offers found.'
        else:
            self._raw_offers = []
            return 'No offers found.'
