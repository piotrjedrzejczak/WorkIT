from src.websites.BullDog import BullDogJobs
from src.websites.JustJoin import JustJoinJobs
from src.websites.NoFluff import NoFluffJobs
from src.storage.Metadata import Storage

def main():

    # Kontener na oferty
    database = []

    # Inicjalizacja obiektów stron
    websites = [JustJoinJobs(), BullDogJobs(), NoFluffJobs()]

    # Przejście przez wszystkie strony
    for website in websites:
        website.create_offers() # Wywołanie funkcji pobierających oferty na każdym obiekcie w liście
        database.extend(website.offers) # Pozyskiwanie gotowych ofert z obiektu

    #Tworzenie bazy
    db = Storage()
    db.Metadata(database)
    

if __name__ == '__main__':
    main()