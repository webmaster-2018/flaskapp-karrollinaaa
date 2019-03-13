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


@app.route("/dodaj_nowego_ucznia", methods=['GET', 'POST'])
def dodaj_nowego_ucznia():

    form = UczenForm()
    form.klasa_ucznia.choices = [(k.id, k.nazwa_klasy)
                          for k in Klasa.select()]
    form.plec_ucznia.choices = [(p.id, p.nazwa_plci)
                         for p in Plec.select()]

    if form.validate_on_submit():
        u = Uczen(imie_ucznia=form.imie_ucznia.data,
                  nazwisko_ucznia=form.nazwisko_ucznia.data,
                  plec_ucznia=form.plec_ucznia.data,
                  klasa_ucznia=form.klasa_ucznia.data)
        u.save()

        flash("Dodano ucznia: {} {}".format(
            form.imie_ucznia.data, form.nazwisko_ucznia.data))
        return redirect(url_for('lista_uczniow'))

    return render_template('uczniowie_dodaj.html', form=form)


@app.route("/dodaj_nowa_klase", methods=['GET', 'POST'])
def dodaj_nowa_klase():

    form = KlasaForm()

    if form.validate_on_submit():
        k = Klasa(nazwa_klasy=form.nazwa_klasy.data,
                  rok_naboru=form.rok_naboru.data,
                  rok_matury=form.rok_matury.data
                  )
        k.save()

        flash("Dodano klasę: {}".format(
            form.nazwa_klasy.data))
        return redirect(url_for('lista_klas'))

    return render_template('klasy_dodaj.html', form=form)


def get_klasa_or_404(kid):
  try:
    klasa = Klasa.get_by_id(kid)
    return klasa
  except Klasa.DoesNotExist:
    abort(404)


@app.route('/edytuj_klase/<int:kid>', methods=['GET', 'POST'])
def edytuj_klase(kid):
  klasa = get_klasa_or_404(kid)
  form = KlasaForm(nazwa=klasa.nazwa_klasy)


  if form.validate_on_submit():
    print(form.data)
    klasa.nazwa_klasy = form.nazwa_klasy.data
    klasa.rok_naboru = form.rok_naboru.data
    klasa.rok_matury = form.rok_matury.data
    klasa.save()
    flash("Zaktualizowano klasę: {}".format(form.nazwa_klasy.data))
    return redirect(url_for('lista_klas'))

  return render_template('edytuj_klase.html', form=form, klasa=klasa)

