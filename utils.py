from typing import Optional, List, Any

def transform_number(strNum: str) -> int:

    if not isinstance(strNum, str):
        raise TypeError(f"The input value for transform_number must be a string\nYou've used {type(strNum)}")

    pieces: List[str] = strNum.split(',')
    num_as_string: str = ''.join(pieces)
    number: int = int(num_as_string)
    return number

def transform_date(garbage_date: str) -> str:

    if not isinstance(garbage_date, str):
        raise TypeError(f'garbage_date at transform_date must be a string, not {type(garbage_date)}')

    pieces: List[str] = garbage_date.split()
    day: str = pieces[0]
    year: str = pieces[2]
    month: str | None = None

    match pieces[1]:
        case 'Jan':
            month = '01'
        case 'Feb':
            month = '02'
        case 'March' | 'Mar':
            month = '03'
        case 'April' | 'Apr' | 'Ap':
            month = '04'
        case 'May':
            month = '05'
        case 'Jun' | 'June':
            month = '06'
        case 'July' | 'Jul':
            month = '07'
        case 'Aug':
            month = '08'
        case 'Sept' | 'Sep':
            month = '09'
        case 'Oct':
            month = '10'
        case 'Nov':
            month = '11'
        case 'Dec':
            month = '12'
    
    new_date = '-'.join([year, month, day])
    
    return new_date

def transform_time(garbage_time: str) -> int:

    if not isinstance(garbage_time, str):
        raise TypeError(f'garbage_time at transform_time must be a string, not {type(garbage_time)}')

    pieces = garbage_time.split()
    num = int(pieces[0])
    return num

def valid_email(email: str) -> bool:

    if not isinstance(email, str):
        raise TypeError('valid_email() must have a string at email argument')
    
    if '@' in email and '.com' in email:
        if email[-4:] == '.com':
            pieces: List[str] = email.split('@')
            if len(pieces[0]) > 0:
                subpieces: List[str] = pieces[1].split('.com')
                if len(subpieces[0]) > 0:
                    return True
    return False 

if __name__ == '__main__':
    print(valid_email('erick1204200100@gmail.com'))