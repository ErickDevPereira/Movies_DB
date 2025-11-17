from typing import Dict, Any, Optional
import pandas as pd

class Movie:

    class Identity:

        def __init__(self, imdbID: str, title: str, genre: str, website: Optional[str | None] = None):
            self.imdbID: str = imdbID
            self.title: str = title
            self.genre: str = genre
            self.website: str | None = website
        
    class People:

        def __init__(self, director: str, actors: str, writer: str):
            self.director: str = director
            self.actors: str = actors
            self.writer: str = writer

    class Details:

        def __init__(self,
                    imdbVotes: int,
                    imdbRating: int,
                    year: int,
                    runtime: str,
                    release_date: str,
                    description: str,
                    metascore: int,
                    language: str,
                    country: str,
                    awards: str):
            self.imdbVotes: int = imdbVotes
            self.imdbRating: int = imdbRating
            self.year: int = year
            self.runtime: str = runtime
            self.release_date: str = release_date
            self.description: str = description
            self.metascore: int = metascore
            self.language: str = language
            self.countru: str = country
            self.awards: str = awards
    
    def __init__(self,
                imdbID: str,
                title: str,
                genre: str,
                director: str,
                actors: str,
                writer: str,
                imdbVotes: int,
                imdbRating: int,
                year: int,
                runtime: str,
                release_date: str,
                description: str,
                metascore: int,
                language: str,
                country: str,
                awards: str,
                website: Optional[str | None] = None):
        self.my_movie: Dict[str, Any] = {'Id': self.Identity(imdbID, title, genre, website),
                                        'People': self.People(director, actors, writer),
                                        'Details': self.Details(imdbVotes,
                                                                imdbRating, year,
                                                                runtime, release_date,
                                                                description, metascore,
                                                                language, country,
                                                                awards)}
    
    def __str__(self):
        return  f"This object concerns the movie:\n'{self.my_movie['Id'].title}' directed by {self.my_movie['People'].director}"
