from typing import List, Any, Tuple, Callable
import requests
import os
from time import time

def catch_time(func: Callable[[str],  Tuple[None, int] | Tuple[str, int] | Tuple[Any, int]]):

    def wrapper(*args, **kwargs):
        Ti: float = time()
        data, status = func(*args, **kwargs)
        Tf: float = time()
        dt: float = Tf - Ti
        return data, status, dt
    
    return wrapper

@catch_time
def download_data(title: str) -> Tuple[None, int] | Tuple[str, int] | Tuple[Any, int]:
    
    if os.path.exists('src_files/api.txt'):
        f: Any = open('src_files/api.txt', 'r')
    else:
        raise FileNotFoundError("Can't finde the file api.txt on src_files. Please, recover the file!")
    lines: List[str] = f.readlines()
    URL: str = lines[1][:-1]
    key: str = lines[3]

    try:
        response: Any = requests.get(URL, params = {'apikey': key, 't': title})
        status = response.status_code
        if status == 200:
            data: Any = response.json()
            if data['Response'] == 'False':
                if data['Error'] == 'Movie not found!':
                    return 'Not found', status
                return None, status
            else:
                return data, status
        return None, status
    except Exception as err:
        print(err)
        return 'ERROR', -1

if __name__ == '__main__':
    x, y, dt = download_data('Chainsaw Massacre')
    print(f'{x}, {y}, {dt}')