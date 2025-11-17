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
            self.imdbRating: float | None = imdbRating
            self.year: int | None = year
            self.runtime: int | None = runtime
            self.release_date: str | None = release_date
            self.description: str | None = description
            self.metascore: int | None = metascore
            self.language: str | None = language
            self.country: str | None = country
            self.awards: str | None = awards
    
    def __init__(self,
                imdbID: str | None = None,
                title: str | None = None,
                genre: str | None = None,
                director: str | None = None,
                actors: str | None = None,
                writer: str | None = None,
                imdbVotes: int | None = None,
                imdbRating: float | None = None,
                year: int | None = None,
                runtime: int | None = None,
                release_date: str | None = None,
                description: str | None = None,
                metascore: int | None = None,
                language: str | None = None,
                country: str | None = None,
                awards: str | None = None,
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
        return  f"""This object concerns the movie:\n'{self.my_movie['Id'].title}' directed by {self.my_movie['People'].director}\n
Here are the attributes:\n
Genre >> {self.my_movie['Id'].genre}\n
Website >> {self.my_movie['Id'].website}\n
Actors >> {self.my_movie['People'].actors}\n
Writer >> {self.my_movie['People'].writer}\n
Imdb rating >> {self.my_movie['Details'].imdbRating}\n
Imdb votes >> {self.my_movie['Details'].imdbVotes}\n
Year >> {self.my_movie['Details'].year}\n
Runtime >> {self.my_movie['Details'].runtime}\n
Release Date >> {self.my_movie['Details'].release_date}\n
Description >> {self.my_movie['Details'].description}\n
Metascore >> {self.my_movie['Details'].metascore}\n
Language >> {self.my_movie['Details'].language}\n
Country >> {self.my_movie['Details'].country}\n
Awards >> {self.my_movie['Details'].awards}"""