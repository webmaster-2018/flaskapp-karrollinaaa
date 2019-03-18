# -*- coding: utf-8 -*-
# quiz-orm/views.py

from flask import Flask
from flask import render_template, request, flash, redirect, url_for, abort
from modele import *
from forms import *

app = Flask(__name__)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            if type(error) is list:
                error = error[0]
            flash("Błąd: {}. Pole: {}".format(
                error,
                getattr(form, field).label.text))

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/lista_uczniow")
def lista_uczniow():
    uczen = (Uczen
             .select(Uczen.id, Uczen.imie_ucznia, Uczen.nazwisko_ucznia))
    return render_template('uczniowie_lista.html', uczen=uczen)


@app.route("/lista_klas")
def lista_klas():
    klasa = Klasa.select(Klasa.id, Klasa.nazwa_klasy)
    return render_template('klasy_lista.html', klasa=klasa)


@app.route("/dodaj_nowego_ucznia", methods=['GET', 'POST'])
def dodaj_nowego_ucznia():

    form = UczenForm()
    form.klasa_ucznia.choices = [(k.id, k.nazwa_klasy) for k in Klasa.select()]
    form.plec_ucznia.choices = [(p.id, p.nazwa_plci) for p in Plec.select()]

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


@app.route("/uczniowie_szczegoly/<id>")
def uczniowie_szczegoly(id):
    uczen = (Uczen
             .select(Uczen.id, Uczen.imie_ucznia, Uczen.nazwisko_ucznia, Plec.nazwa_plci, Klasa.nazwa_klasy)
             .join_from(Uczen, Plec)
             .join_from(Uczen, Klasa, JOIN.LEFT_OUTER)
             .where(Uczen.id == id))
    return render_template('uczniowie_szczegoly.html', uczen=uczen)

@app.route("/klasy_szczegoly/<id>")
def klasy_szczegoly(id):
    klasa = Klasa.select().where(Klasa.id==id)
    return render_template('klasy_szczegoly.html', klasa=klasa)


def get_or_404(uid):
    try:
        u = Uczen.get_by_id(uid)
        return u
    except Uczen.DoesNotExist:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/uczniowie_edytuj/<int:uid>", methods=['GET', 'POST'])
def uczniowie_edytuj(uid):

    u = get_or_404(uid)

    form = UczenForm(obj=u)
    form.klasa_ucznia.choices = [(k.id, k.nazwa_klasy) for k in Klasa.select()]
    form.klasa_ucznia.data = u.klasa_ucznia.id
    form.plec_ucznia.choices = [(p.id, p.nazwa_plci) for p in Plec.select()]
    form.plec_ucznia.data = u.plec_ucznia.id

    if form.validate_on_submit():
        print(form.data)
        u.imie_ucznia = form.imie_ucznia.data
        u.nazwisko_ucznia = form.nazwisko_ucznia.data
        u.plec_ucznia = form.plec_ucznia.data
        u.klasa_ucznia = form.klasa_ucznia.data
        u.save()

        flash("Zaktualizowano dane o uczniu: {} {}".format(
            form.imie_ucznia.data, form.nazwisko_ucznia.data))
        return redirect(url_for('lista_uczniow'))
    elif request.method == 'POST':
        flash_errors(form)

    return render_template('uczniowie_edytuj.html', form=form)


def getOr404(kid):
    try:
        k = Klasa.get_by_id(kid)
        return k
    except Klasa.DoesNotExist:
        abort(404)

@app.route("/klasy_edytuj/<int:kid>", methods=['GET', 'POST'])
def klasy_edytuj(kid):

    k = getOr404(kid)

    form = KlasaForm(obj=k)

    if form.validate_on_submit():
        print(form.data)
        k.nazwa_klasy = form.nazwa_klasy.data
        k.rok_naboru = form.rok_naboru.data
        k.rok_matury = form.rok_matury.data
        k.save()

        flash("Zaktualizowano dane o klasie: {}".format(
            form.nazwa_klasy.data))
        return redirect(url_for('lista_klas'))
    elif request.method == 'POST':
        flash_errors(form)

    return render_template('klasy_edytuj.html', form=form)


@app.route("/usun/<int:uid>", methods=['GET', 'POST'])
def usun(uid):
    u = get_or_404(uid)

    if request.method == 'POST':
        flash('Usunięto ucznia {} {}'.format(
            u.imie_ucznia.data, u.nazwisko_ucznia.data), 'sukces')
        for u in Uczen.select():
            u.delete_instance()
        u.delete_instance()
        return redirect(url_for('lista_uczniow'))

    return render_template("uczniowie_usun.html", uczen=u)
