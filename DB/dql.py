from typing import Tuple, List, Dict, Any

'''
def fetch_user(db):

    cursor = db.cursor()
    cursor.execute("SELECT username, password FROM users")
    users_data = cursor.fetchall()
    organized_data = {'username' : [loggin_data[0] for loggin_data in users_data],
                    'password' : [loggin_data[1] for loggin_data in users_data]}
    cursor.close()
    return organized_data'''

def search_user(db, username, pw):

    cursor = db.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = %s AND password = %s", (username, pw))
    searched_data = cursor.fetchall()
    if len(searched_data) > 0:
        return True
    return False

def get_user_id(db: Any, username: str, pw: str) -> int | str:

    cursor: Any = db.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = %s AND password = %s", (username, pw))
    id = cursor.fetchall()
    if len(id) > 0:
        return int(id[0][0]) #Returning the id
    return 'User not found'

if __name__ == '__main__':
    pass