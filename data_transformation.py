from movie_abstraction import Movie
import pandas as pd
from typing import List, Dict, Any, Tuple
import API_conn as api
import utils
import json
import DB.dql as dql
import os
import DB.ddl as ddl
import numpy as np
import custom_ERROR as ERROR

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

def export_JSON_for_regular_user(db: Any, userID: int, mode: str = 'together') -> int:

    if mode not in ('together', 'separate'):
        raise ERROR.NotAnOption(mode, 'separate', 'together')

    all_data = dql.get_everything_by_user(db, userID)
    rating_stats_over_avg_by_user = dql.get_rating_stats_over_avg_by_user(db, userID)
    movies_over_avg_rating_by_user = dql.get_rating_data_over_avg_by_user(db, userID)
    genre_data_by_user = dql.get_genre_data_by_user(db, userID)
    year_data_by_user = dql.get_year_data_by_user(db, userID)
    country_data_by_user = dql.get_country_data_by_user(db, userID)
    overall_stats_by_user = dql.get_all_averages(db, userID)
    user_data = dql.get_user_data(db, userID)

    if mode == 'together':
        DATA: Dict[str, Dict[str, str] | List[Dict[str, Any]]] = {
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
            utils.auto_dir(db, userID)
            JSON_txt: str = json.dumps(DATA, indent = 3)
            f: Any = open(f'DATA_HERE/JSON_files/JSON_{user_data['Nickname']}/data_{user_data['Nickname']}.json', 'w')
            f.write(JSON_txt)
            f.close()
            return 1 #1 means that the operation happened with success
        except Exception as err:
            print(err)
            return 0 #0 means that a failure occurred during the operation
    elif mode == 'separate':
        try:
            utils.auto_dir(db, userID)
            JSON_matrix: np.ndarray = np.array([np.array([f'DATA_HERE/JSON_files/JSON_{user_data['Nickname']}/JSON_{user_data['Nickname']}_Movies_registered_by_user.json',
                                            json.dumps(utils.transform_data_structure(all_data), indent = 2)]),
                                            np.array([f'DATA_HERE/JSON_files/JSON_{user_data['Nickname']}/JSON_{user_data['Nickname']}_Movies_over_average_rating.json',
                                            json.dumps(utils.transform_data_structure(movies_over_avg_rating_by_user), indent = 2)]),
                                            np.array([f'DATA_HERE/JSON_files/JSON_{user_data['Nickname']}/JSON_{user_data['Nickname']}_Statistics_of_movies_over_average.json',
                                            json.dumps(utils.transform_data_structure(rating_stats_over_avg_by_user), indent = 2)]),
                                            np.array([f'DATA_HERE/JSON_files/JSON_{user_data['Nickname']}/JSON_{user_data['Nickname']}_Data_by_genre.json',
                                            json.dumps(utils.transform_data_structure(genre_data_by_user), indent = 2)]),
                                            np.array([f'DATA_HERE/JSON_files/JSON_{user_data['Nickname']}/JSON_{user_data['Nickname']}_Data_by_year.json',
                                            json.dumps(utils.transform_data_structure(year_data_by_user), indent = 2)]),
                                            np.array([f'DATA_HERE/JSON_files/JSON_{user_data['Nickname']}/JSON_{user_data['Nickname']}_Data_by_country.json',
                                            json.dumps(utils.transform_data_structure(country_data_by_user), indent = 2)]),
                                            np.array([f'DATA_HERE/JSON_files/JSON_{user_data['Nickname']}/JSON_{user_data['Nickname']}_Statistics_concerning_all_registered_movies_by_user.json',
                                            json.dumps(utils.transform_data_structure(overall_stats_by_user), indent = 2)])])
            for JSON in JSON_matrix:
                FILE = open(JSON[0], 'w')
                FILE.write(JSON[1])
                FILE.close()
            return 1
        except Exception as err:
            print(err)
            return 0

def export_JSON_for_admin(db: Any, admin_id: int) -> int:

    try:
        DATA = dql.get_all_averages(db)
        JSON_as_str = json.dumps(DATA, indent = 2)
        utils.JSON_auto_dir_for_user(db, admin_id)
        nickname = dql.get_user_data(db, admin_id)['Nickname']
        FILE = open(f'DATA_HERE/JSON_files/JSON_{nickname}/ALL_DATA_FOR_ADMIN.json', 'w')
        FILE.write(JSON_as_str)
    except Exception as err:
        print(err)
        return 0
    else:
        FILE.close()
        return 1


def export_CSV_for_admin(db: Any, admin_id: int) -> int:

    try:
        DATA = dql.get_all_averages(db)
        utils.auto_dir(db, admin_id, format = 'CSV')
        Nickname = dql.get_user_data(db, admin_id)['Nickname']
        df = pd.DataFrame(DATA)
        df.to_csv(f'DATA_HERE/CSV_files/CSV_{Nickname}/ALL_DATA_FOR_ADMIN.csv', index = False)
    except Exception as err:
        print(err)
        return 0
    else:
        return 1

def clean_Movies_dataframe(Movies_df: Any) -> Any:

    semi_treated_df: Any = Movies_df.fillna({'genre': 'Genre Not defined',
                      'description': "Not available",
                      'runtime' : 0,
                      'director': "Not available",
                      'actors': "Not available",
                      'writer': "Not available",
                      'release date': "Not available",
                      'imdb rating': 0.0,
                      'metascore': 0,
                      'language': "Not available",
                      'country': "Undefined",
                      'imdb votes': 0,
                      'Website': "Not available",
                      'awards': "Not defined"}, inplace = False)
    indexes = semi_treated_df.index

    for index in indexes:
        if semi_treated_df.loc[index, 'runtime'] <= 20:
            semi_treated_df.loc[index, 'runtime'] = 0
        if semi_treated_df.loc[index, 'metascore'] < 0:
            semi_treated_df.loc[index, 'runtime'] = 0
        if semi_treated_df.loc[index, 'imdb votes'] < 0:
            semi_treated_df.loc[index, 'imdb votes'] = 0
        if semi_treated_df.loc[index, 'imdb rating'] < 0 or semi_treated_df.loc[index, 'imdb rating'] > 10:
            semi_treated_df.loc[index, 'imdb rating'] = 0
    return semi_treated_df

def export_CSV_for_regular_user(db: Any, user_id: int) -> int:

    all_data = dql.get_everything_by_user(db, user_id)
    rating_stats_over_avg_by_user = dql.get_rating_stats_over_avg_by_user(db, user_id)
    movies_over_avg_rating_by_user = dql.get_rating_data_over_avg_by_user(db, user_id)
    genre_data_by_user = dql.get_genre_data_by_user(db, user_id)
    year_data_by_user = dql.get_year_data_by_user(db, user_id)
    country_data_by_user = dql.get_country_data_by_user(db, user_id)
    overall_stats_by_user = dql.get_all_averages(db, user_id)
    user_data = dql.get_user_data(db, user_id)
    nickname = user_data['Nickname']
    utils.auto_dir(db, user_id, format = 'CSV')
    START: str = f'DATA_HERE/CSV_FILES/CSV_{nickname}/'

    CSV_matrix: List[List[Any]] = [[START + f'CSV_{nickname}_Data_by_country.csv', pd.DataFrame(country_data_by_user)],
                                    [START + f'CSV_{nickname}_Data_by_genre.csv', pd.DataFrame(genre_data_by_user)],
                                    [START + f'CSV_{nickname}_Data_by_year.csv', pd.DataFrame(year_data_by_user)],
                                    [START + f'CSV_{nickname}_Movies_registered_by_user.csv', clean_Movies_dataframe(pd.DataFrame(all_data))],
                                    [START + f'CSV_{nickname}_Statistics_concerning_all_registered_movies_by_user.csv', pd.DataFrame(overall_stats_by_user)],
                                    [START + f'CSV_{nickname}_Movies_over_average_rating.csv', pd.DataFrame(movies_over_avg_rating_by_user)],
                                    [START + f'CSV_{nickname}_Statistics_of_movies_over_average.csv', pd.DataFrame(rating_stats_over_avg_by_user)]]

    try:
        for CSV in CSV_matrix:
            CSV[1].to_csv(CSV[0], index = False)
    except Exception as err:
        print(err)
        return 0
    else:
        return 1

if __name__ == '__main__':
    print(export_CSV_for_regular_user(ddl.define_conn('root', 'Ichigo007*'), 1))