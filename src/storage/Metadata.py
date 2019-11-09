import sqlite3
from os import remove

class Storage():

    def Metadata(self, offers):
        
        remove('./database.db')

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # utworzenie schemy kluczy
        columns = tuple(offers[0].__dict__.keys())
        cursor.execute(f"""CREATE TABLE Offers {columns}""")

        # insert
        queries = [
            tuple([str(field) for field in offer.__dict__.values()])
            for offer in offers
        ]
        
        template = """INSERT INTO Offers VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.executemany(template, queries)
        
        connection.commit()
        connection.close()
