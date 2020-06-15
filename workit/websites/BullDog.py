from logging import Formatter, FileHandler, getLogger, DEBUG
from bs4 import BeautifulSoup as BSoup
from workit.model.Website import Website
from workit.model.Offer import Offer
from datetime import datetime
from requests import get
from re import compile


logger = getLogger('workit.bulldog')
logger.setLevel(DEBUG)
fhandler = FileHandler('workit/logs/bulldog.log')
fhandler.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)


class BullDogJobs(Website):

    __get_offers_url = 'https://bulldogjob.pl/companies/jobs?mode=plain&page='
    __fetch_time = datetime(1, 1, 1)

    def __init__(self):
        self.offers = []

    def create_offers(self):
        '''This method creates Offers from BullDogJobs'''
        self.__fetch_time = datetime.now()
        last_page = 1
        response = get(
            self.__get_offers_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        if response.status_code == 200:
            html = BSoup(response.text, 'html.parser')
            last_page += int(self._get_html_text(
                html,
                classname='pagination',
                by_attr=True,
                attr='data-total'
                )
            )
            for page in range(1, last_page):
                response = get(
                    f'{self.__get_offers_url}{str(page)}',
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                html = BSoup(response.text, 'html.parser')
                for listing in html.find_all(
                    class_=compile(r'job-item')
                ):
                    try:
                        offer = self._parse_offer(listing)
                        self.offers.append(Offer(*offer))
                    except ValueError:
                        logger.info(' '.join((
                            f'Failed to create offer, values passed: {offer}',
                            f'Listing Text: {repr(listing.text)}'
                        )))
                        continue
        return self.offers

    def _parse_offer(self, offer):
        ''' This method extracts all the necessary information
            from the HTML element to create a Offer object.
            It returns a tuple, sorted according to the Offer Class API. '''

        title = self._get_html_text(offer, classname='title')
        company = self._get_html_text(offer, classname='company')
        city = self._get_html_text(offer, classname='location')
        salary = self._get_html_text(offer, classname='salary')
        techstack = self._get_html_text(
            offer,
            classname='btn btn-sm btn-default',
            multiple=True
        )
        url = offer['href']
        exp = None

        return title, company, city, url, salary, techstack, exp

    def _get_html_text(self, html, classname, by_attr=False, multiple=False, attr=''):
        '''Extracts text from Tag objects.

        Given a bs4.element.Tag object, extracts raw text or specified HTML attribute.
        In case of collections of Tag objects, set multiple=True and it will return
        list of strings from that collection. If the specified Tag does not exist
        empty string will be returned. If the HTML object is not a Tag element
        None will be returned.

        Args:
            html: bs4.element.Tag object.
            classname: Name of the HTML class the text is extracted from.
            by_attr: True if a specific HTML attribute has to be extracted (Default=False).
            multiple: True if html parameter is a collection of Tag objects (Default=False).
            attr: Name of the HTML attribute to extract, used only when by_attr=True.

        Returns:
            Single String from the InnerText HTML attribute.
            List of Strings in case of multiple Tags, each from the InnerText HTML attribute.
            Empty String when the InnerText attribute of Tag is empty.
            None in case of AttributeError or TypeError
        '''
        try:
            if by_attr:
                return html.find(class_=classname)[attr]
            if multiple:
                return [
                    elem.text.strip()
                    for elem in html.find_all(class_=classname)
                ]
            return html.find(class_=classname).text.strip()
        except (AttributeError, TypeError):
            return None
