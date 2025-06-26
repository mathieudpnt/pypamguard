import constants
from binary_file import PGBFile
import io
from constants import BYTE_ORDERS, DEFAULT_BUFFER_SIZE

def load_pamguard_binary_file(filename, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN, buffering: int | None = DEFAULT_BUFFER_SIZE) -> PGBFile:
    """
    Read a binary PAMGuard data file into a PAMFile object
    :param filename: absolute or relative path to the .pgdt file to read
    :param order: endianess of data (defaults to 'network')
    :param buffering: number of bytes to buffer
    
    """

    if buffering and type(buffering) != int:
        raise ValueError(f"buffering must be of type int or None (got {type(buffering)}).")
    if not filename or type(filename) != str:
        raise ValueError(f"filename must be of type str (got {type(filename)}).")


    data = open(filename, "rb", buffering=buffering)
    pamfile = PGBFile(filename=filename, data=data, order=order)
    pamfile.load()
    
    return pamfile

if __name__ == "__main__":
    pdgf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/test.pgdf")