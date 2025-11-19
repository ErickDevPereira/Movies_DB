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

if __name__ == '__main__':
    pass