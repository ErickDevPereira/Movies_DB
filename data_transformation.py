from movie_abstraction import Movie
import pandas as pd
from typing import List, Dict, Any, Tuple
import API_conn as api
import utils
import json
import DB.dql as dql
import os
import DB.ddl as ddl

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
            year: str | None = treat(data['Year'])
            runtime: int | None = treat(data['Runtime']) if treat(data['Runtime']) is None else utils.transform_time(treat(data['Runtime']))
            release_date: str | None = treat(data['Released']) if treat(data['Released']) is None else utils.transform_date(treat(data['Released']))
            description: str | None = treat(data['Plot'])
            metascore: int | None = int(treat(data['Metascore'])) if treat(data['Metascore']) is not None else None
            language: str | None = treat(data['Language'])
            country: str | None = treat(data['Country'])
            awards: str | None = treat(data['Awards'])
            try:
                website: str | None = treat(data['Website'])
            except:
                website: str | None = None
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

def export_single_JSON_for_regular_user(db: Any, userID: int) -> int:

    all_data = dql.get_everything_by_user(db, userID)
    rating_stats_over_avg_by_user = dql.get_rating_stats_over_avg_by_user(db, userID)
    movies_over_avg_rating_by_user = dql.get_rating_data_over_avg_by_user(db, userID)
    genre_data_by_user = dql.get_genre_data_by_user(db, userID)
    year_data_by_user = dql.get_year_data_by_user(db, userID)
    country_data_by_user = dql.get_country_data_by_user(db, userID)
    overall_stats_by_user = dql.get_all_averages(db, userID)
    user_data = dql.get_user_data(db, userID)

    DATA = {
        'Information about user' : user_data,
        'Movies registered by user' : utils.transform_data_structure(all_data),
        'Movies over average rating' : utils.transform_data_structure(movies_over_avg_rating_by_user),
        'Statistics of movies over average' : utils.transform_data_structure(rating_stats_over_avg_by_user),
        'Data by genre' : utils.transform_data_structure(genre_data_by_user),
        'Data by year' : utils.transform_data_structure(year_data_by_user),
        'Data by country' : utils.transform_data_structure(country_data_by_user),
        'Statistics concerning all registered movies by user' : utils.transform_data_structure(overall_stats_by_user)
    }

    try:
        if not os.path.exists('DATA_HERE'):
            os.mkdir('DATA_HERE')
            os.mkdir('DATA_HERE/JSON_files')
        else:
            if not os.path.exists('DATA_HERE/JSON_files'):
                os.mkdir('DATA_HERE/JSON_files')
        JSON_txt = json.dumps(DATA, indent = 3)
        f = open(f'DATA_HERE/JSON_files/data_{user_data['Nickname']}.json', 'w')
        f.write(JSON_txt)
        f.close()
        return 1 #1 means that the operation happened with success
    except Exception as err:
        print(err)
        return 0 #0 means that a failure occurred during the operation

if __name__ == '__main__':
    print(export_single_JSON_for_regular_user(ddl.define_conn('root', 'Ichigo007*'), 1))