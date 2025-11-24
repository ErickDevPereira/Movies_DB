from typing import Tuple, List, Dict, Any
import pprint
'''
def fetch_user(db):

    cursor = db.cursor()
    cursor.execute("SELECT username, password FROM users")
    users_data = cursor.fetchall()
    organized_data = {'username' : [loggin_data[0] for loggin_data in users_data],
                    'password' : [loggin_data[1] for loggin_data in users_data]}
    cursor.close()
    return organized_data'''

def to_float(data: str) -> float:

    if not isinstance(data, str):
        raise TypeError("The input value for to_float() must be a string")
    
    num = float(''.join(data.split(',')))

    return num

def search_user(db: Any, username: str, pw: str) -> bool:

    cursor: Any = db.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = %s AND password = %s", (username, pw))
    searched_data: List[Tuple[str, str]] = cursor.fetchall()
    if len(searched_data) > 0:
        return True
    return False

def get_user_id(db: Any, username: str, pw: str) -> int | str:

    cursor: Any = db.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = %s AND password = %s", (username, pw))
    id: List[Tuple[int,...]] = cursor.fetchall()
    if len(id) > 0:
        return int(id[0][0]) #Returning the id
    return 'User not found'

def get_user_data(db: Any, userID: int) -> Dict[str, str]:

    cursor: Any = db.cursor()
    cursor.execute("SELECT username, email, CONCAT(first_name, ' ', last_name) FROM users WHERE user_id = %s", (userID,))
    data: Any = cursor.fetchall()
    organized_data: Dict[str, str] = {
        'Nickname' : data[0][0],
        'full name': data[0][1],
        'email' : data[0][2]
    }
    return organized_data

def get_everything_by_user(db: Any, user_id: int, show = False) -> Dict[str, List[Any]]:

    complement: str = ''
    if show:
        complement = """"u.user_id AS id,
                         u.username AS nickname,
                         CONCAT(u.username, ' ', u.last_name) AS full_name,"""

    cursor: Any = db.cursor()
    cursor.execute(f"""
                SELECT
                    {complement}
                    i.imdbID AS imdbID,
                    i.title AS title,
                    i.genre AS genre,
                    i.website AS website_url,
                    p.director AS director,
                    p.actors AS actors,
                    p.writer as writer,
                    d.imdbVotes AS imdb_votes,
                    d.release_date AS release_date,
                    d.description AS description,
                    d.metascore AS metascore,
                    d.language AS language,
                    d.country AS country,
                    d.awards as awards,
                    d.runtime as runtime,
                    d.imdbRating as imdb_rating
                FROM
                    Identity AS i INNER JOIN People AS p
                    ON i.imdb_user = p.imdb_user INNER JOIN Details AS d
                    ON i.imdb_user = d.imdb_user INNER JOIN Users AS u
                    ON u.user_id = i.user_id
                WHERE
                    u.user_id = %s
                """, (user_id,))
    messy_data: List[Tuple[Any,...]] = cursor.fetchall()
    if show:
        organized_data = {'user Id' : [record[0] for record in messy_data],
                        'Nickname' : [record[1] for record in messy_data],
                        'full name' : [record[2] for record in messy_data],
                        'imdb ID' : [record[3] for record in messy_data],
                        'Title' : [record[4] for record in messy_data],
                        'Genre' : [record[5] for record in messy_data],
                        'description' : [record[12] for record in messy_data],
                        'runtime': [record[17] for record in messy_data],
                        'director' : [record[7] for record in messy_data],
                        'actors' : [record[8] for record in messy_data],
                        'writer' : [record[9] for record in messy_data],
                        'release date' : [str(record[11]) for record in messy_data],
                        'imdb rating': [float(record[18]) for record in messy_data],
                        'metascore' : [record[13] for record in messy_data],
                        'language' : [record[14] for record in messy_data],
                        'country' : [record[15] for record in messy_data],
                        'awards' : [record[16] for record in messy_data],
                        'imdb votes' : [record[10] for record in messy_data],
                        'Website' : [record[6] for record in messy_data]}
    else:
        organized_data = {'imdb ID' : [record[0] for record in messy_data],
                        'Title' : [record[1] for record in messy_data],
                        'Genre' : [record[2] for record in messy_data],
                        'description' : [record[9] for record in messy_data],
                        'runtime': [record[14] for record in messy_data],
                        'director' : [record[4] for record in messy_data],
                        'actors' : [record[5] for record in messy_data],
                        'writer' : [record[6] for record in messy_data],
                        'release date' : [str(record[8]) for record in messy_data],
                        'imdb rating': [float(record[15]) for record in messy_data],
                        'metascore' : [record[10] for record in messy_data],
                        'language' : [record[11] for record in messy_data],
                        'country' : [record[12] for record in messy_data],
                        'awards' : [record[13] for record in messy_data],
                        'imdb votes' : [record[7] for record in messy_data],
                        'Website' : [record[3] for record in messy_data]}
    return organized_data

def get_rating_stats_over_avg_by_user(db: Any, user_id: int) -> Dict[str, List[Any]]:

    cursor_view: Any = db.cursor()
    cursor_view.execute("""
                    CREATE OR REPLACE VIEW avg_distinct_data AS
                SELECT 
                    AVG(dim0.imdbRating) AS avg_data
                FROM
                    (SELECT 
                        DISTINCT i.imdbID, d.imdbRating AS imdbRating 
                    FROM 
                        Identity as i INNER JOIN Details as d 
                        ON i.imdb_user = d.imdb_user
                        ) AS dim0
                    """)
    cursor: Any = db.cursor()
    cursor.execute("""
                SELECT 
                    COUNT(*) AS quantity,
                    MAX(above_avg.imdbRating) AS max_imdbRating,
                    MIN(above_avg.imdbRating) AS min_imdbRating,
                    (SELECT avg_data FROM avg_distinct_data) AS overall_average,
                    CONCAT(FORMAT(100 * COUNT(*) / (SELECT COUNT(*) FROM users AS u INNER JOIN identity AS i ON u.user_id = i.user_id WHERE i.user_id = %s), 2), '%') AS percentage_for_user
                FROM
                    (SELECT
                        i.imdbID AS imdbID,
                        i.title AS Title,
                        d.imdbRating AS imdbRating
                    FROM
                        Identity AS i INNER JOIN people AS p
                        ON i.imdb_user = p.imdb_user INNER JOIN
                        Details AS d ON d.imdb_user = i.imdb_user
                        INNER JOIN users AS u ON u.user_id = i.user_id
                    WHERE
                        u.user_id = %s AND d.imdbRating > (SELECT avg_data FROM avg_distinct_data)
                    ) AS above_avg
                """, (user_id, user_id))
    messy_data: Any = cursor.fetchall()
    cursor.close()
    cursor_view.close()
    organized_data: Dict[str, List[Any]] = {
                    'quantity': [int(messy_data[0][0])],
                    'max imdbRating': [float(messy_data[0][1])],
                    'min imdbRating': [float(messy_data[0][2])],
                    'overall average': [float(messy_data[0][3])],
                    'percentage': [str(messy_data[0][4])]
                    }
    return organized_data

def get_rating_data_over_avg_by_user(db: Any, user_id: int) -> Dict[str, Any]:

    cursor: Any = db.cursor()
    cursor.execute(
        """
        SELECT
            i.imdbID AS imdbID,
            i.title AS Title,
            d.imdbRating AS imdbRating
        FROM
            Identity AS i INNER JOIN people AS p
            ON i.imdb_user = p.imdb_user INNER JOIN
            Details AS d ON d.imdb_user = i.imdb_user
            INNER JOIN users AS u ON u.user_id = i.user_id
        WHERE
            u.user_id = %s AND d.imdbRating > 
            (
            SELECT 
                AVG(dim0.imdbRating)
            FROM
                (SELECT 
                    DISTINCT i.imdbID, d.imdbRating AS imdbRating 
                FROM 
                    Identity as i INNER JOIN Details as d 
                    ON i.imdb_user = d.imdb_user
                    ) AS dim0
                )
        ORDER BY
            d.imdbRating DESC;
        """, (user_id,))
    messy_data: Any = cursor.fetchall()
    organized_data: Dict[str, Any] = {
        'imdb ID' : [str(record[0]) for record in messy_data],
        'title' : [str(record[1]) for record in messy_data],
        'imdb rating' : [float(record[2]) for record in messy_data]
    }
    return organized_data

def get_genre_data_by_user(db: Any, user_id: int) -> Dict[str, Any]:

    cursor: Any = db.cursor()
    cursor.execute("""
                SELECT
                    i.genre AS genre,
                    COUNT(*) AS quantity,
                    FORMAT(AVG(d.runtime), 2) AS average_runtime,
                    FORMAT(AVG(d.imdbRating), 2) AS average_imdb_rating,
                    FORMAT(AVG(d.imdbVotes), 2) AS average_imdb_votes
                FROM
                    identity AS i INNER JOIN details AS d
                    ON i.imdb_user = d.imdb_user INNER JOIN
                    people AS p ON p.imdb_user = i.imdb_user
                WHERE
                    i.user_id = %s
                GROUP BY
                    genre
                ORDER BY
                    AVG(d.imdbRating) DESC
                """, (user_id,))
    messy_data: Any = cursor.fetchall()
    organized_data: Dict[str, Any] = {
        'genre' : [record[0] for record in messy_data],
        'quantity' : [record[1] for record in messy_data],
        'average runtime' : [to_float(record[2]) for record in messy_data],
        'average rating' : [to_float(record[3]) for record in messy_data],
        'average votes' : [to_float(record[4]) for record in messy_data]
    }
    return organized_data

def get_year_data_by_user(db: Any, user_id: int, order_by: str = 'year') -> Dict[str, Any]:

    complement: None | str = None
    if order_by == 'year':
        complement = 'ORDER BY release_year DESC'
    elif order_by == 'average_runtime':
        complement = 'ORDER BY AVG(d.runtime) DESC'
    elif order_by == 'average_rating':
        complement = 'ORDER BY AVG(d.imdbRating) DESC'
    else:
        complement = ''

    cursor: Any = db.cursor()
    cursor.execute("""
                SELECT
                    YEAR(d.Release_date) AS release_year,
                    COUNT(*) AS quantity,
                    FORMAT(AVG(d.imdbRating), 2) AS average_rating,
                    FORMAT(AVG(d.runtime), 2) AS average_runtime,
                    FORMAT(AVG(d.imdbVotes), 2) AS average_votes
                FROM
                    identity AS i INNER JOIN details AS d
                    ON i.imdb_user = d.imdb_user INNER JOIN
                    people AS p ON i.imdb_user = p.imdb_user
                WHERE
                    i.user_id = %s
                GROUP BY
                    release_year
                """ + complement, (user_id,))
    messy_data: Any = cursor.fetchall()
    organized_data: Dict[str, Any] = {
        'year' : [record[0] for record in messy_data],
        'quantity' : [record[1] for record in messy_data],
        'avg_rating' : [to_float(record[2]) for record in messy_data],
        'avg_runtime' : [to_float(record[3]) for record in messy_data],
        'avg_votes' : [to_float(record[4]) for record in messy_data]
    }
    return organized_data

def get_country_data_by_user(db: Any, user_id: int, order_by: str = 'quantity') -> Dict[str, Any]:

    complement: None | str = None
    if order_by == 'quantity':
        complement = 'ORDER BY quantity DESC'
    elif order_by == 'average_runtime':
        complement = 'ORDER BY AVG(d.runtime) DESC'
    elif order_by == 'average_rating':
        complement = 'ORDER BY AVG(d.imdbRating) DESC'
    else:
        complement = ''

    cursor: Any = db.cursor()
    cursor.execute("""
                SELECT
                    d.country AS country,
                    COUNT(*) AS quantity,
                    FORMAT(AVG(d.runtime), 2) AS avg_runtime,
                    FORMAT(AVG(d.imdbRating), 2) AS avg_rating,
                    FORMAT(AVG(d.imdbVotes), 2) AS avg_votes
                FROM
                    Identity AS i INNER JOIN Details AS d
                    ON i.imdb_user = d.imdb_user INNER JOIN
                    People as p ON p.imdb_user = i.imdb_user
                WHERE
                    i.user_id = %s
                GROUP BY
                    country
                """ + complement, (user_id,))
    messy_data: Any = cursor.fetchall()
    organized_data: Dict[str, Any] = {
        'country' : [record[0] for record in messy_data],
        'quantity' : [record[1] for record in messy_data],
        'avg_runtime' : [to_float(record[2]) for record in messy_data],
        'avg_rating' : [to_float(record[3]) for record in messy_data],
        'avg_votes' : [to_float(record[4]) for record in messy_data]
    }
    return organized_data

def get_all_averages(db: Any, user_id: int | None = None) -> Dict[str, int | float | str]:

    sql = """   SELECT
                    u.user_id AS user_id,
                    u.username AS nickname,
                    u.email AS email,
                    COUNT(*) AS quantity,
                    FORMAT(AVG(d.Runtime), 2) AS avg_runtime,
                    FORMAT(AVG(d.imdbRating), 2) AS avg_rating,
                    FORMAT(AVG(d.imdbVotes), 2) AS avg_votes,
                    COUNT(DISTINCT i.genre) AS quanitity_of_genres,
                    COUNT(i.website) AS quantity_of_websites,
                    FORMAT(AVG(d.metascore), 2) AS avg_metascore
                FROM
                    Identity AS i INNER JOIN Details AS d
                    ON i.imdb_user = d.imdb_user INNER JOIN
                    People as p ON p.imdb_user = i.imdb_user
                    INNER JOIN Users AS u ON i.user_id = u.user_id
                GROUP BY
                    i.user_id"""

    cursor = db.cursor()
    if isinstance(user_id, int):
        cursor.execute(sql + f' HAVING user_id = {user_id}')
    elif user_id is None:
        cursor.execute(sql)
    messy_data = cursor.fetchall()
    organized_data = {
        'user_id' : [record[0] for record in messy_data],
        'username' : [record[1] for record in messy_data],
        'email' : [record[2] for record in messy_data],
        'quantity' : [record[3] for record in messy_data],
        'average runtime' : [to_float(record[4]) for record in messy_data],
        'average rating' : [to_float(record[5]) for record in messy_data],
        'average votes' : [to_float(record[6]) for record in messy_data],
        'quantity of genres' : [record[7] for record in messy_data],
        'quantity of websites' : [record[8] for record in messy_data],
        'average metascore' : [to_float(record[9]) for record in messy_data]
    }
    return organized_data

if __name__ == '__main__':
    pprint.pprint(get_all_averages(ddl.define_conn("root", "Ichigo007*"), None))