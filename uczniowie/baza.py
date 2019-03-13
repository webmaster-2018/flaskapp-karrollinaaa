#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
from modele import *
from peewee import chunked


def czy_jest(plik):
    """ Funkcja sprawdza istnienie pliku na dysku """
    if not os.path.isfile(plik):
        print("Plik {} nie istnieje!".format(plik))
        return False
    return True


def dane_z_pliku(nazwa_pliku, separator=';'):
    dane = []
    if not czy_jest(nazwa_pliku):
        return dane

    with open(nazwa_pliku, 'r', newline='\n', encoding='utf-8') as plik:
        tresc = csv.reader(plik, delimiter=separator)
        for rekord in tresc:
            rekord = [x.strip() for x in rekord]
            dane.append(rekord)
    return dane


def dodaj_dane(dane):
    for model, plik in dane.items():
        pola = [pole for pole in model._meta.fields]
        pola.pop(0)
        wpisy = dane_z_pliku(plik + '.txt', ';')
        print(wpisy)
        with baza.atomic():
            for batch in chunked(wpisy, 100):
                model.insert_many(batch, fields=pola).execute()
                baza.commit()


def main(args):
    if os.path.exists(baza_plik):
        os.remove(baza_plik)
    baza.connect()
    baza.create_tables([Plec, Klasa, Uczen])

    dane = {
        Plec: 'plec',
        Klasa: 'klasa',
        Uczen: 'uczen'
    }

    dodaj_dane(dane)
    baza.close()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
