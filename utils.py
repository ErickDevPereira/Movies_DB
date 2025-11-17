from typing import Optional, List, Any

def transform_number(strNum: str) -> int:

    if not isinstance(strNum, str):
        raise TypeError(f"The input value for transform_number must be a string\nYou've used {type(strNum)}")

    pieces: List[str] = strNum.split(',')
    num_as_int: str = ''.join(pieces)
    number: int = int(num_as_int)
    return number

if __name__ == '__main__':
    print(transform_number('12,120'))