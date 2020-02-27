import sqlite3
from datetime import datetime
from os import system, name, path, remove
import time
from random import randint

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def main():
    db = None
    c = None
    while True:
        clear()
        print("0 tulostaa kaikki toiminnot")
        print("Valitse toiminto (1-9):")
        cmd = input()
        if cmd == 'exit':
            break
        elif cmd == '0':
            print("1. Luo tietokanta")
            print("2. Lisää paikka")
            print("3. Lisää asiakas")
            print("4. Lisää paketti")
            print("5. Lisää tapahtuma")
            print("6. Tulosta paketin tapahtumat")
            print("7. Tulosta asiakkaan paketit")
            print("8. Hae paikan päivän tapahtumat")
            print("9. Tehokkuustesti")
            print(" 'exit' sulkee ohjelman")
        elif cmd == '1' and not db:
            file_exists = path.isfile('database.db')
            db = sqlite3.connect('database.db')
            db.execute('PRAGMA foreign_keys = 1')
            db.isolation_level = None
            c = db.cursor()
            if not file_exists:
                c.execute('CREATE TABLE Asiakkaat (id INTEGER PRIMARY KEY, nimi TEXT UNIQUE)')
                c.execute('CREATE TABLE Paketit (id INTEGER PRIMARY KEY, koodi TEXT UNIQUE, asiakas_id INTEGER REFERENCES Asiakkaat)')
                c.execute('CREATE TABLE Paikat (id INTEGER PRIMARY KEY, nimi TEXT UNIQUE)')
                c.execute('CREATE TABLE Tapahtumat '
                          '(id INTEGER PRIMARY KEY, paketti_id INTEGER REFERENCES Paketit,'
                          ' paikka_id INTEGER REFERENCES Paikat, päivämäärä TEXT, kuvaus TEXT)')
            print("Tietokanta luotu.")
        elif db:
            if cmd == '1':
                print("Tietokanta on jo olemassa.")
            elif cmd == '2':
                print("Anna paikan nimi:")
                nimi = input()
                c.execute('SELECT nimi FROM Paikat WHERE nimi=?', [nimi])
                tiedot = c.fetchone()
                if tiedot is None:
                    try:
                        c.execute('INSERT INTO Paikat (nimi) VALUES (?)', [nimi])
                        print("Paikka lisätty.")
                    except:
                        print("Jos näet tämän viestin, joku todennäköisesti onnistui lisäämään tietokantaan saman nimisen paikan noin mikrosekuntin sinua ennen. Huono tuuri :(")
                else:
                    print("Paikka on jo olemassa.")
                pass
            elif cmd == '3':
                print("Anna asiakkaan nimi:")
                nimi = input()
                c.execute('SELECT nimi FROM Asiakkaat WHERE nimi=?', [nimi])
                tiedot = c.fetchone()
                if tiedot is None:
                    try:
                        c.execute('INSERT INTO Asiakkaat (nimi) VALUES (?)', [nimi])
                        print("Asiakas lisätty.")
                    except:
                        print("Jos näet tämän viestin, joku todennäköisesti onnistui lisäämään tietokantaan saman nimisen käyttäjän noin mikrosekuntin sinua ennen. Huono tuuri :(")
                else:
                    print("Asiakas on jo olemassa.")
                pass
            elif cmd == '4':
                print("Anna paketin seurantakoodi:")
                koodi = input()
                c.execute('SELECT koodi FROM Paketit WHERE koodi=?', [koodi])
                tiedot = c.fetchone()
                if tiedot is None:
                    print("Anna asiakkaan nimi:")
                    nimi = input()
                    c.execute('SELECT id from Asiakkaat WHERE nimi=?', [nimi])
                    tiedot = c.fetchone()
                    if tiedot is None:
                        print("Asiakasta ei löydy.")
                    else:
                        try:
                            c.execute('INSERT INTO Paketit (koodi, asiakas_id) VALUES (?, ?)', [koodi, tiedot[0]])
                            print("Paketti lisätty.")
                        except:
                            print("Jos näet tämän viestin, joku todennäköisesti onnistui lisäämään tietokantaan paketin samalla seurantakoodilla noin mikrosekuntin sinua ennen. Huono tuuri :(")
                    pass
                else:
                    print("Seurantakoodi on jo olemassa.")
                pass
            elif cmd == '5':
                print("Anna paketin seurantakoodi:")
                koodi = input()
                c.execute('SELECT id FROM Paketit WHERE koodi=?', [koodi])
                tiedot = c.fetchone()
                if tiedot is not None:
                    paketti_id = tiedot[0]
                    print("Anna tapahtuman paikka:")
                    paikka = input()
                    c.execute('SELECT id FROM Paikat WHERE nimi=?', [paikka])
                    tiedot = c.fetchone()
                    if tiedot is not None:
                        paikka_id = tiedot[0]
                        print("Anna tapahtuman kuvaus:")
                        kuvaus = input()
                        päivämäärä = datetime.now()
                        c.execute('INSERT INTO Tapahtumat (paketti_id, paikka_id, päivämäärä, kuvaus) VALUES (?, ?, ?, ?)',
                                  [paketti_id, paikka_id, päivämäärä, kuvaus])
                        print("Tapahtuma lisätty.")
                    else:
                        print("Paikkaa ei löydy.")
                else:
                    print("Seurantakoodia ei löydy.")
                pass
            elif cmd == '6':
                print("Anna paketin seurantakoodi:")
                koodi = input()
                c.execute('SELECT id FROM Paketit WHERE koodi=?', [koodi])
                tiedot = c.fetchone()
                if tiedot is not None:
                    paketti_id = tiedot[0]
                    c.execute('SELECT päivämäärä, nimi, kuvaus FROM Tapahtumat LEFT JOIN Paikat ON Paikat.id=paikka_id')
                    tiedot = c.fetchall()
                    if tiedot is not None:
                        for tapahtuma in tiedot:
                            print('{}, {}, {}'.format(tapahtuma[0], tapahtuma[1], tapahtuma[2]))
                    else:
                        print("Seurantakoodilla ei löytynyt tapahtumia.")
                else:
                    print("Seurantakoodia ei löydy.")
                pass
            elif cmd == '7':
                print("Anna asiakkaan nimi:")
                nimi = input()
                c.execute('SELECT id FROM Asiakkaat WHERE nimi=?', [nimi])
                tiedot = c.fetchone()
                if tiedot is not None:
                    id = tiedot[0]
                    c.execute('SELECT koodi, COUNT(paketti_id) FROM Paketit LEFT JOIN Tapahtumat on Paketit.id = Tapahtumat.paketti_id WHERE Paketit.asiakas_id=? GROUP BY koodi', [id])
                    tiedot = c.fetchall()
                    if tiedot is not None:
                        for paketti in tiedot:
                            print('{}, {} tapahtumaa'.format(paketti[0], paketti[1]))
                    else:
                        print("Asiakkaalle ei löydy paketteja.")
                else:
                    print("Asiakasta ei löydy.")
                pass
            elif cmd == '8':
                print("Anna paikan nimi:")
                nimi = input()
                c.execute('SELECT id FROM Paikat WHERE nimi=?', [nimi])
                tiedot = c.fetchone()
                if tiedot is not None:
                    id = tiedot[0]
                    print("Anna päivämäärä (vvvv-kk-pp):")
                    päivä = input()
                    formatted = ''
                    if '.' in päivä:
                        splitted = päivä.split('.')
                        formatted = '-'.join(splitted)
                        pass
                    elif ' ' in päivä:
                        splitted = '-'.join(splitted)
                        pass
                    elif '_' in päivä:
                        splitted = päivä.split('_')
                        formatted = '-'.join(splitted)
                        pass
                    else:
                        formatted = päivä
                    formatted = '{}{}{}'.format('%', formatted, '%')
                    c.execute("SELECT COUNT(*) FROM Tapahtumat WHERE päivämäärä LIKE ? AND paikka_id=?", [formatted, id])
                    tiedot = c.fetchall()
                    if tiedot is not None:
                        lkm = str(tiedot[0]).replace('(', '').replace(')', '').replace(',', '')
                        print("Tapahtumien määrä: {}".format(lkm))
                    else:
                        print("Paikalle ei löytynyt tapahtumia.")
                else:
                    print("Paikkaa ei löydy.")
                pass
        elif cmd == '9':
            if path.exists('tehokkuustesti.db'):
                remove('tehokkuustesti.db')
            db = sqlite3.connect('tehokkuustesti.db')
            db.execute('PRAGMA foreign_keys = 1')
            db.isolation_level = None
            c = db.cursor()
            c.execute('CREATE TABLE Asiakkaat (id INTEGER PRIMARY KEY, nimi TEXT)')
            c.execute(
                'CREATE TABLE Paketit (id INTEGER PRIMARY KEY, koodi TEXT, asiakas_id INTEGER REFERENCES Asiakkaat)')
            c.execute('CREATE TABLE Paikat (id INTEGER PRIMARY KEY, nimi TEXT)')
            c.execute('CREATE TABLE Tapahtumat '
                      '(id INTEGER PRIMARY KEY, paketti_id INTEGER REFERENCES Paketit,'
                      ' paikka_id INTEGER REFERENCES Paikat, päivämäärä TEXT, kuvaus TEXT)')
            print("Käytetäänkö indeksejä? (Y/n, default:n)")
            v = input()
            if v.lower() == 'y':
                c.execute('CREATE INDEX idx_paketti ON Tapahtumat (paketti_id)')
            c.execute('BEGIN')
            start_time = time.time()
            for i in range(1000):
                nimi = 'P{}'.format(i+1)
                c.execute('INSERT INTO Paikat (nimi) VALUES (?)', [nimi])
            print("Lisättiin 1000 paikkaa, aikaa kului: {} sekunttia".format(str(time.time() - start_time)[:8]))
            start_time = time.time()
            for i in range(1000):
                nimi = 'A{}'.format(i+1)
                c.execute('INSERT INTO Asiakkaat (nimi) VALUES (?)', [nimi])
            print("Lisättiin 1000 asiakasta, aikaa kului: {} sekunttia".format(str(time.time() - start_time)[:8]))
            start_time = time.time()
            for i in range(1000):
                koodi = 'K000{}'.format(i+1)
                asiakas_id = randint(1, 1000)
                c.execute('INSERT INTO Paketit (koodi, asiakas_id) VALUES (?, ?)', [koodi, asiakas_id])
            print("Lisättiin 1000 pakettia, aikaa kului: {} sekunttia".format(str(time.time() - start_time)[:8]))
            values = []
            start_time = time.time()
            for i in range(1000000):
                kuvaus = 'Kuvaus {}'.format(i+1)
                päivämäärä = datetime.now()
                paikka_id = randint(1, 1000)
                paketti_id = randint(1, 1000)
                values.append((paketti_id, paikka_id, päivämäärä, kuvaus))
            c.executemany('INSERT INTO Tapahtumat (paketti_id, paikka_id, päivämäärä, kuvaus) VALUES (?, ?, ?, ?)', values)
            print("Lisättiin 1 000 000 tapahtumaa, aikaa kului: {} sekunttia".format(str(time.time() - start_time)[:8]))
            c.execute('COMMIT')
            start_time = time.time()
            for i in range(1000):
                asiakas_id = randint(1, 1000)
                c.execute('SELECT COUNT(*) FROM Paketit WHERE asiakas_id=?', [asiakas_id])
            print("Suoritettiin 1000 kyselyä satunnaisen asiakkaan pakettien määrästä\n\tAikaa kului: {} sekunttia".format(str(time.time() - start_time)[:8]))
            start_time = time.time()
            for i in range(1000):
                paketti_id = randint(1, 1000)
                c.execute('SELECT COUNT(*) FROM Tapahtumat WHERE paketti_id=?', [paketti_id])
            print("Suoritettiin 1000 kyselyä satunnaisen paketin tapahtumien määrästä\n\tAikaa kului: {} sekunttia".format(
                str(time.time() - start_time)[:8]))
            pass
        else:
            print("Tämä komento vaatii olemassa olevan tietokannan.")
            print("Luo tietokanta komennolla 1.")
        print("Paina enter jatkaaksesi. . .")
        input()
    pass

if __name__ == '__main__':
    main()