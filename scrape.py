import requests
import json
import sys

def justJoinITScrape():
    '''All offers from Just Join IT'''
    searchRequest = requests.get('https://justjoin.it/api/offers')
    offers = searchRequest.json()

    return offers

def noFluffJobsScrape():
    '''All offers from No Fluff Jobs'''
    searchRequest = requests.get('https://nofluffjobs.com/api/search/posting?')
    offers = searchRequest.json()
    ### https://nofluffjobs.com/job/ < - Use this to create links from json data

    return offers

noFluffOffers = noFluffJobsScrape()
justJoinOffers = justJoinITScrape()

with open("justJoinIt.json", "w", encoding='utf-8') as fp1:
    json.dump(justJoinOffers, fp1, ensure_ascii=False, indent=4)

with open("noFluffJobs.json", "w", encoding='utf-8') as fp2:
    json.dump(noFluffOffers, fp2, ensure_ascii=False, indent=4)

