from re import split
from typing import List, Union


def dms2dd(degrees: str, minutes: str, seconds: str, direction: str) -> float:
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    return dd if direction in ("N", "E") else -dd


def dd2dms(deg: float) -> List[Union[int, float]]:
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]


def parse_dms(dms: str) -> float:
    parts = split("[^\d\w]+", dms)
    if len(parts) == 4:
        return dms2dd(parts[0], parts[1], parts[2], parts[3])
    elif len(parts) == 5:  # decimals on seconds
        return dms2dd(parts[0], parts[1], '.'.join(parts[2:3]), parts[4])
    raise Exception(f"Unexpected {len(parts)} DMS parts {dms}")
