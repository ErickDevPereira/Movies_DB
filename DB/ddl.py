import mysql.connector
from typing import Any

def define_conn(username: str, password: str) -> Any:
    
    try:
        db: Any = mysql.connector.connect(
                host = 'localhost',
                username = username,
                password = password,
                database = 'moviesDB'
                )
        return db
    except Exception as err:
        print(err)
        return None

def create_everything(username: str, password: str) -> Any:
    db: Any = mysql.connector.connect(
        host = 'localhost',
        username = username,
        password = password
    )
    cursor: Any = db.cursor()
    cursor.execute("CREATE DATABASE if not exists moviesDB")
    cursor.close()
    db.close()
    db_: Any = define_conn(username, password)
    cursor: Any = db_.cursor()
    cursor.execute("""
            CREATE TABLE if not exists Users (
                user_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                CHECK ( email LIKE '_%@_%.com' ),
                CONSTRAINT unique_username UNIQUE (username)
            )""")
    cursor.close()
    cursor: Any = db_.cursor()
    cursor.execute(
            """
            CREATE TABLE if not exists Identity (
                user_id INT UNSIGNED NOT NULL,
                imdbID VARCHAR(255) PRIMARY KEY,
                Title VARCHAR(255),
                Genre VARCHAR(255),
                Website VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES Users (user_id)
            )""")
    cursor.close()
    cursor: Any = db_.cursor()
    cursor.execute("""
            CREATE TABLE if not exists People (
                imdbID VARCHAR(255),
                Director VARCHAR(255),
                Actors VARCHAR(255),
                Writer VARCHAR(255),
            CONSTRAINT fk_id_to_people FOREIGN KEY (imdbID) REFERENCES Identity (imdbID)
            )""")
    cursor.close()
    cursor: Any = db_.cursor()
    cursor.execute("""
            CREATE TABLE if not exists Details (
                imdbID VARCHAR(255),
                imdbVotes INT,
                imdbRating DECIMAL(5, 2),
                Year INT,
                Runtime INT,
                Release_date DATE,
                Description VARCHAR(255),
                Metascore INT,
                Language VARCHAR(255),
                Country VARCHAR(255),
                Awards VARCHAR(255),
                Website VARCHAR(255),
            CONSTRAINT fk_id_to_details FOREIGN KEY (imdbID) REFERENCES Identity (imdbID)
            )""")
    cursor.close()
    
    return db_

def drop_everything(db):
    cursor = db.cursor()
    cursor.execute("DROP DATABASE moviesDB")
    cursor.close()

if __name__ == '__main__':
    drop_everything(define_conn('root', 'Ichigo007*'))
    create_everything('root', 'Ichigo007*')