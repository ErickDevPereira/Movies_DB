from movie_abstraction import Movie
import pandas as pd
from typing import List, Dict, Any, Tuple
import API_conn as api
import utils

#First returned value is an object from the class Movie, second is the runtime of the function download_data and the last value is the a status of the operation.
def read_and_load(title: str) -> Tuple[Movie, str, str]:

    def treat(msg: str) -> None | str:
        if msg == 'N/A': #Happens when the API can't give value for an attribute
            return None
        return msg

    data, status, time = api.download_data(title)
    api_runtime: str = f'{time:.2f} sec'
    if data is not None:
        if not isinstance(data, str):
            #This case will be accomplished if data is the correct dictionary from the JSON file.
            imdbID: str | None = treat(data['imdbID'])
            title_: str | None = treat(data['Title'])
            genre: str | None = treat(data['Genre'])
            director: str | None = treat(data['Director'])
            actors: str | None = treat(data['Actors'])
            writer: str | None = treat(data['Writer'])
            imdbVotes: int | None = utils.transform_number(treat(data['imdbVotes'])) if treat(data['imdbVotes']) is not None else None
            imdbRating: float | None = float(treat(data['imdbRating'])) if treat(data['imdbRating']) is not None else None
            year: int | None = int(treat(data['Year'])) if treat(data['Year']) is not None else None
            runtime: int | None = treat(data['Runtime']) if treat(data['Runtime']) is None else utils.transform_time(treat(data['Runtime']))
            release_date: str | None = treat(data['Released']) if treat(data['Released']) is None else utils.transform_date(treat(data['Released']))
            description: str | None = treat(data['Plot'])
            metascore: int | None = int(treat(data['Metascore'])) if treat(data['Metascore']) is not None else None
            language: str | None = treat(data['Language'])
            country: str | None = treat(data['Country'])
            awards: str | None = treat(data['Awards'])
            website: str | None = treat(data['Website'])
            movie_obj: Movie = Movie(
                imdbID = imdbID,
                title = title_,
                genre = genre,
                director = director,
                actors = actors,
                writer = writer,
                imdbVotes = imdbVotes,
                imdbRating = imdbRating,
                year = year,
                runtime = runtime,
                release_date = release_date,
                description = description,
                metascore = metascore,
                language = language,
                country = country,
                awards = awards,
                website = website)
            return movie_obj, api_runtime, 'Ok'
        else:
            return Movie(), api_runtime, data
    else:
        return Movie(), api_runtime, 'ERROR'

if __name__ == '__main__':
    obj, api_runtime, status = read_and_load('Chainsaw Massacre')
    print(obj)