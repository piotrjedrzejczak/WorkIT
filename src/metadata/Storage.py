import sqlite3
import os
from mysql.connector import Error

class Storage(object):

    def Metadata():
        
        f = open("database.txt")
        text_db = f.read()
        type(text_db)

        lists = text_db.split("\n\n")

        #Konwesja pliku na listę dictów
        tab1 = []
        for l in lists:
            a = l.split("\n")
            tab1.append(a)

        d_list = []
        for i, var_tab in enumerate(tab1):
            d_name = f"Offer_{i}"
            ddd = {}
            for d in var_tab:
                if d == "Offer:":
                    content = [""]
                    pass
                else:
                    content = d.split(": ")
                if len(content[0]) != 0:
                    d1 = {content[0]: content[1]}
                    ddd.update(d1)  
            d_list.append(ddd)

        #Lista kluczy dla kazdego dicta
        tk = []
        for key, value in d_list[0].items() :
            tk.append(key)
        values = ", ".join(tk)
        
        #Stworzenie wartości do zapytania
        query_raw = []
        for i, d in enumerate(d_list):
            val = (tuple([d[tk[0]], d[tk[1]], d[tk[2]], d[tk[3]], d[tk[4]], d[tk[5]], d[tk[6]], d[tk[7]]]))
            query_raw.append(val)

        columns = tuple(tk)

        os.remove('./database.db')

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # utworzenie schemy kluczy
        cursor.execute("""CREATE TABLE offers {0}""".format(columns))

        # insert
        q = """INSERT INTO offers VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.executemany(q, query_raw)

        

        # all records
        # print("\n###\nALL\n###")
        # cursor.execute('SELECT * FROM offers')
        # print(cursor.fetchall())

        # zapytanie dla konkretnego rekordu
        # print("\n###\nWROCŁAW\n###")
        # cursor.execute('SELECT * FROM offers WHERE City = "Wrocław" limit 1')
        # print(cursor.fetchall())

        # zapytanie o techstacks 
        # print("\n###\nTECHSTACK JAKO STRING OGARNIĘCIE\n###")
        # cursor.execute('SELECT TechStack FROM offers WHERE City = "Wrocław" limit 1')
        # ts = cursor.fetchall()
        # print(ts)