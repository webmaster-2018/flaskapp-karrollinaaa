# Aplikacja "Uczniowie"
Aplikacja sieciowa pozwalająca na dodawanie uczniów do klas.

## Widoki

1. Strona główna: z wyjaśnieniem przeznaczenia aplikacji.
2. Dodaj klasę: widok umożliwiający dodawanie klas.
3. Edytuj klasę: widok umożliwiający edycję danych klasy.
4. Dodaj ucznia: widok umożliwiający dodawanie ucznia.
5. Dodaj ucznia: widok umożliwiający edycję danych ucznia.
6. Lista klas: wyświetla klasy i ich dane.
7. Lista uczniów: wyświetla uczniów i ich dane.

## Wygląd

1. Szablon oparty na Bootstrapie.

## Narzędzia

1. Python 3
2. Flask
3. flask-wtf
4. Peewee

Ewentualne przygotowanie wirtualnego środowiska:

```python
python3 -m venv pve
source pve/bin/activate
```

Instalacja bibliotek:

```python
pip install flask flask-wtf peewee
```

Uruchomienie serwera deweloperskiego:

```python
python app.py
```

## Realizacja – wskazówki

1. Zdefiniuj modele Klasa i Uczen w pliku modele.py.
2. Na podstawie modeli utwórz bazę danych.
3. Zdefiniuj formularze dla dodawania/edycji klas i uczniów.
4. Wgraj do katalogu templates szablon bazowy w Bootstrapie.
5. W katalogu static umieść zasoby css, js itp.
6. Wszystkie szablony powinny dziedziczyć kod z szablonu bazowego.
7. Przygotuj widok dodawania klas.
8. Przygotuj widok listy klas.
9. Przygotuj widok edytowania klas.
10. Przygotuj widok dodawania uczniów.
11. Przygotuj widok listy uczniów.
12. Przygotuj widok edytowania uczniów.
