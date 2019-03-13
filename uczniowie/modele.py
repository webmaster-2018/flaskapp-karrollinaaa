#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  modele.py
from peewee import *

baza_plik = 'uczniowie.db'
baza = SqliteDatabase(baza_plik)  # instancja bazy

### MODELE #
class BazaModel(Model):
    class Meta:
        database = baza


class Plec(BazaModel):
    nazwa_plci = CharField(null=False)

class Klasa(BazaModel):
    nazwa_klasy = CharField(null=False)
    rok_naboru = IntegerField(null=False)
    rok_matury = IntegerField(null=False)

class Uczen(BazaModel):
    imie_ucznia = CharField(null=False)
    nazwisko_ucznia = CharField(null=False)
    plec_ucznia = ForeignKeyField(Plec, related_name='plec_ucznia')
    klasa_ucznia = ForeignKeyField(Klasa, related_name='klasa_ucznia')
