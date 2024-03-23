from math import floor
from typing import List


class TimeParser:
    def __init__(self) -> None:
        pass

    def parse_seconds(self, seconds: int) -> str:
        time_parts: List[int] = []

        for i in range(3):
            time_part: int = floor(seconds / pow(60, i)) % 60
            time_parts.append(time_part)

        time_string: str = ''

        for time_part in time_parts[::-1]:
            time_string += str(time_part) + ':'

        return time_string[:-1]
