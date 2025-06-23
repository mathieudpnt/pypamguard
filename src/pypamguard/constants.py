# Arguments that can be used when reading
TIME_RANGE = "timerange"
UID_RANGE = "uidrange"
UID_LIST = "uidlist"
FILTER = "filter"
CHANNEL = "channel"

DEFAULT_BUFFER_SIZE = 1024

ORDER_MODIFIERS = {
    "native": "@",
    "little-endian": "<",
    "big-endian": ">",
    "network": "!"
}

INT_SIZE = {
    "b": 8,
    "h": 16,
    "i": 32,
    "q": 64
}

UINT_SIZE = {
    "B": 8,
    "H": 16,
    "I": 32,
    "Q": 64
}

FLOAT_SIZE = {
    "f": 32,
    "d": 64
}

CHAR = "b"
UCHAR = "B"
SHORT = "h"
USHORT = "H"
INT = "i"
UINT = "I"
LONG = "q"
ULONG = "Q"
FLOAT = "f"
DOUBLE = "d"

SIZES = {
    CHAR: 1, # char
    UCHAR: 1, # unsigned char
    SHORT: 2, # short
    USHORT: 2, # unsigned short
    INT: 4, # int
    UINT: 4, # unsigned int
    LONG: 8, # long long
    ULONG: 8, # unsigned long long
    FLOAT: 4, # float
    DOUBLE: 8, # double
}


HEADER_FORMAT = [
    {"name": "length", "dtype": INT},
    {"name": "identifier", "dtype": INT},
]