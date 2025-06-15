# Välipalautus 3

Huomiot:

-   Applikaation featureita ei ole päivitetty.
-   Applikaatio täyttää suurimman osan 3. välipalautukseen vaadittavattavasti kriteereistä, tosin hyvin heikosti koska suurin osa ajasta meni tällä viikolla koodin siistimiseen.
-   Virheentarkistusta vähän lisätty edelliseen viikkoon, mutta ei vielä täydellinen.
-   Search-funktio edelleen aika kehno, ei muutoksia tehty.
-   Paljon vielä tekemättä. Onneksi on vielä aikaa!

-   Nykyiset toiminnot:
-   Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään.
-   Käyttäjä pystyy luomaan projektin ja tapahtumia projektille, mutta tapahtumat eivät vielä tee muutoksia projektin balanceen.
-   Projektit ovat näkyvissä vain niille käyttäjille joilla on view_permission
-   Käyttäjät pystyvät lisäämään transactioneita projektiin jos heillä on edit_permission
-   Project Owner pystyy lisäämään käyttäjiä ja määrittää heille view & edit permissions
  
# Budget Monitor

This application is a project for the University of Helsinki's TKT20019 - Databases and Web Programming course Summer/2025.

## Application features

-   Users can log in and out, and create a new user profile.
-   Users can create new projects, track the project budget and manage project visibility.
-   Users can add income and expense transactions. Transactions must be assigned to a project.
-   Users can view or edit project transactions they have permission for.

## Documentation

### Installation

**Option 1: Manual Installation**
Install flask library

```
$ pip install flask
```

Create a database and initialize the database schema

```
$ python install.py
```

**Option 2: Automatic Installation**

Run install.sh

### Launch

**Option 1: Manual Launch**

```
$ flask run
```

**Option 2: Automatic Launch**

Run app.sh
