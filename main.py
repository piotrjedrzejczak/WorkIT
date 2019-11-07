from src.websites.BullDog import BullDogJobs
from src.websites.JustJoin import JustJoinJobs
from src.websites.NoFluff import NoFluffJobs
from src.metadata.Storage import Storage

def main():

    # Symulator naszej bazy danych
    database = []

    # Inicjalizacja obiektów stron
    websites = [JustJoinJobs(), BullDogJobs(), NoFluffJobs()]

    # Przejście przez wszystkie strony
    for website in websites:
        website.create_offers() # Wywołanie funkcji pobierających oferty na każdym obiekcie w liście
        database.extend(website.offers) # Pozyskiwanie gotowych ofert z obiektu

        # for offer in website.offers:
            # insert into (offer)

    # Zapis danych do pliku symulującego baze danych
    with open("database.txt", "w", encoding='utf-8') as db:
        for offer in database:
            db.write(str(offer))
            db.write('\n')

    # By storage działał należy usunąć dwie ostatnie puste linie w pliku database.txt
    # Jako że za każdym pobraniem ofert dwie linie są dodawane, sugeruję na przetestowanie zakomentować powyższe metody.
    # Jakiś pomysł żeby zautomatyzować to?
    Storage.Metadata()
    

if __name__ == '__main__':
    main()