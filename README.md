# Välipalautus 2
Huomiot:
- Applikaation featureita ei ole päivitetty.
- Applikaatio täyttää suurimman osan 2. välipalautukseen vaadittavattavasti kriteereistä.
  1. Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään (Register New User -> Login)
  2. Käyttäjä pystyy lisäämään tietokohteita (Login -> Projects -> Add -> Create)
  3. Käyttäjä pystyy muokkaamaan tietokohteita (Ei vielä toteutettu)
  4. Käyttäjä pystyy positamaan tietokohteita (Login -> Projects -> Manage -> Search -> Delete)
  5. Käyttäjä näkee sovellukseen lisätyt tietokohteet ja pystyy etsimään niitä (Login -> Projects -> Manage -> Search)
Applikaation on tällä hetkellä hyvin alkutekijöissään ja vain perustoimintoja testattu.

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
