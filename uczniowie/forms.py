# -*- coding: utf-8 -*-
# quiz-orm/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, HiddenField, FieldList
from wtforms import SelectField, FormField, BooleanField
from wtforms.validators import Required

blad1 = 'To pole jest wymagane'

class KlasaForm(FlaskForm):
    id = HiddenField()
    nazwa_klasy = StringField('Nazwa klasy: ', validators=[
                              Required(message="blad_1")])
    rok_naboru = StringField('Rok naboru: ', validators=[Required(message="blad_1")])
    rok_matury = StringField('Rok matury: ', validators=[Required(message="blad_1")])

class UczenForm(FlaskForm):
    id = HiddenField()
    imie_ucznia = StringField('Imię ucznia: ', validators=[
                              Required(message="blad_1")])
    nazwisko_ucznia = StringField('Nazwisko ucznia: ', validators=[
                                  Required(message="blad_1")])
    plec_ucznia = SelectField('Płeć ucznia: ', coerce=int)
    klasa_ucznia = SelectField('Klasa: ', coerce=int)
