# -*- coding: utf-8 -*-
# quiz-orm/views.py

from flask import Flask
from flask import render_template, request, flash, redirect, url_for, abort
from modele import *
from forms import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/lista_uczniow")
def lista_uczniow():
    uczen = (Uczen
             .select(Uczen.id, Uczen.imie_ucznia, Uczen.nazwisko_ucznia, Plec.nazwa_plci, Klasa.nazwa_klasy)
             .join_from(Uczen, Plec) 
             .join_from(Uczen, Klasa, JOIN.LEFT_OUTER))
    return render_template('uczniowie_lista.html', uczen=uczen)


@app.route("/lista_klas")
def lista_klas():
    klasa = Klasa.select()
    return render_template('klasy_lista.html', klasa=klasa)
