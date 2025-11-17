from typing import Dict, Any, Optional

class Movie:

    class Identity:

        def __init__(self, imdbID: str | None, title: str | None, genre: str | None, website: Optional[str | None] = None):
            self.imdbID: str | None = imdbID
            self.title: str | None = title
            self.genre: str | None = genre
            self.website: str | None = website
        
    class People:

        def __init__(self, director: str | None, actors: str | None, writer: str | None):
            self.director: str | None = director
            self.actors: str | None = actors
            self.writer: str | None = writer

    class Details:

        def __init__(self,
                    imdbVotes: int | None,
                    imdbRating: int | None,
                    year: int | None,
                    runtime: str | None,
                    release_date: str | None,
                    description: str | None,
                    metascore: int | None,
                    language: str | None,
                    country: str | None,
                    awards: str | None):
            self.imdbVotes: int | None = imdbVotes
            self.imdbRating: int | None = imdbRating
            self.year: int | None = year
            self.runtime: int | None = runtime
            self.release_date: str | None = release_date
            self.description: str | None = description
            self.metascore: int | None = metascore
            self.language: str | None = language
            self.countru: str | None = country
            self.awards: str | None = awards
    
    def __init__(self,
                imdbID: str | None,
                title: str | None,
                genre: str | None,
                director: str | None,
                actors: str | None,
                writer: str | None,
                imdbVotes: int | None,
                imdbRating: int | None,
                year: int | None,
                runtime: int | None,
                release_date: str | None,
                description: str | None,
                metascore: int | None,
                language: str | None,
                country: str | None,
                awards: str | None,
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