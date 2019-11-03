from src.websites.BullDog import BullDogJobs
from src.websites.JustJoin import JustJoinJobs
from src.websites.NoFluff import NoFluffJobs

def main():

    # Symulator naszej bazy danych
    database = []

    # Inicjalizacja obiektów stron
    websites = [JustJoinJobs(), BullDogJobs(), NoFluffJobs()]

    # Przejście przez wszystkie strony
    for website in websites:
        website.create_offers() # Wywołanie funkcji pobierających oferty na każdym obiekcie w liście
        database.extend(website.offers) # Pozyskiwanie gotowych ofert z obiektu

    # Zapis danych do pliku symulującego baze danych
    with open("database.txt", "w", encoding='utf-8') as db:
        for offer in database:
            db.write(str(offer))
            db.write('\n')

if __name__ == '__main__':
    main()