from typing import Any, List, Tuple

def load_id(db: Any, imdbID: str, title: str, genre: str, website: str) -> None:

    cursor = db.cursor()
    cursor.execute("INSERT INTO Identity VALUES (%s, %s, %s, %s)", (imdbID, title, genre, website))
    cursor.commit()
    cursor.close()

def load_people(db: Any, imdbID: str, director: str, actor: str, writer: str) -> None:

    cursor = db.cursor()
    cursor.execute("INSERT INTO People VALUES (%s, %s, %s, %s)", (imdbID, director, actor, writer))
    cursor.commit()
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
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO Details VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (imdbID, imdbvotes, imdbRating, year, runtime, release_date, description, metascore, language, country, awards, website))
    cursor.commit()
    cursor.close()