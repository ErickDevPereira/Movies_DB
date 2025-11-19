from typing import Any

def load_user(db: Any, username: str, first_name: str, last_name: str, email: str, password: str):

    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO Users (username, first_name, last_name, email, password) VALUES (%s, %s, %s, %s, %s)",
                   (username, first_name, last_name, email, password))
    db.commit()
    cursor.close()

def load_id(db: Any, user_ID, imdbID: str, title: str, genre: str, website: str) -> None:

    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO Identity VALUES (%s, %s, %s, %s, %s)", (user_ID, imdbID, title, genre, website))
    db.commit()
    cursor.close()

def load_people(db: Any, imdbID: str, director: str, actor: str, writer: str) -> None:

    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO People VALUES (%s, %s, %s, %s)", (imdbID, director, actor, writer))
    db.commit()
    cursor.close()

def load_details(db: Any,
                imdbID: str,
                imdbvotes: int,
                imdbRating: float,
                year: int,
                runtime: int,
                release_date: str,
                description: str,
                metascore: int,
                language: str,
                country: str,
                awards: str,
                website: str) -> None:
    
    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO Details VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (imdbID, imdbvotes, imdbRating, year, runtime, release_date, description, metascore, language, country, awards, website))
    db.commit()
    cursor.close()