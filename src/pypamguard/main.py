from pypamguard.core.pgbfile import PGBFile
from pypamguard.utils.constants import BYTE_ORDERS, DEFAULT_BUFFER_SIZE
from pypamguard.core.filters import Filters, DateFilter
import datetime

def load_pamguard_binary_file(filename, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN, buffering: int | None = DEFAULT_BUFFER_SIZE) -> PGBFile:
    """
    Read a binary PAMGuard data file into a PAMFile object
    :param filename: absolute or relative path to the .pgdt file to read
    :param order: endianess of data (defaults to 'network')
    :param buffering: number of bytes to buffer
    
    """

    d1 = datetime.datetime.strptime('2016-09-03 00:42:30.404000+00:00', '%Y-%m-%d %H:%M:%S.%f%z')
    d2 = datetime.datetime.strptime('2016-09-03 00:42:40.404000+00:00', '%Y-%m-%d %H:%M:%S.%f%z')

    pg_filters = Filters({
        'daterange': DateFilter(d1, d2)
    })


    # pg_filters = Filters()


    if buffering and type(buffering) != int:
        raise ValueError(f"buffering must be of type int or None (got {type(buffering)}).")
    if not filename or type(filename) != str:
        raise ValueError(f"filename must be of type str (got {type(filename)}).")

    data = open(filename, "rb", buffering=buffering)
    pamfile = PGBFile(filename=filename, data=data, order=order, filters=pg_filters)
    pamfile.load()
    print(pamfile)

    # print(pamfile.data_set.get(500).date)
    # print(pamfile.data_set.get(1000).date)
    
    return pamfile

if __name__ == "__main__":
    # pdgf = load_pamguard_binary_file("/home/sulli/code/pypamguard/Click_Detector_Click_Detector_Clicks_20250627_144208.pgdf")
    pdgf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/test.pgdf")