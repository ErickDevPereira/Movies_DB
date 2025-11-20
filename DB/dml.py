from typing import Any

def load_user(db: Any, username: str, first_name: str, last_name: str, email: str, password: str):

    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO Users (username, first_name, last_name, email, password) VALUES (%s, %s, %s, %s, %s)",
                   (username, first_name, last_name, email, password))
    db.commit()
    cursor.close()

def load_id(db: Any, user_ID: int, imdbID: str, title: str, genre: str, website: str) -> None:

    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO Identity VALUES (%s, %s, %s, %s, %s, %s)", (user_ID, imdbID, str(imdbID) + str(user_ID), title, genre, website))
    db.commit()
    cursor.close()

def load_people(db: Any, user_ID: int, imdbID: str, director: str, actor: str, writer: str) -> None:

    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO People VALUES (%s, %s, %s, %s, %s)", (user_ID, str(imdbID) + str(user_ID), director, actor, writer))
    db.commit()
    cursor.close()

def load_details(db: Any,
                user_ID: int,
                imdbID: str,
                imdbvotes: int,
                imdbRating: float,
                year: str,
                runtime: int,
                release_date: str,
                description: str,
                metascore: int,
                language: str,
                country: str,
                awards: str) -> None:
    
    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO Details VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (user_ID, str(imdbID) + str(user_ID), imdbvotes, imdbRating, year, runtime, release_date, description, metascore, language, country, awards))
    db.commit()
    cursor.close()