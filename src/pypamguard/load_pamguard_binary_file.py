from pypamguard.core.pamguardfile import PAMGuardFile
from pypamguard.utils.constants import BYTE_ORDERS, DEFAULT_BUFFER_SIZE
from pypamguard.core.filters import Filters, DateFilter
from pypamguard.core.readers import Report
from .logger import logger, Verbosity, logger_config
import io, json
from pypamguard.utils.timer import timer

def load_pamguard_binary_file(filename, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN, buffering: int | None = DEFAULT_BUFFER_SIZE, filters: Filters = None, json_path: str = None, report: Report = None) -> PAMGuardFile:
    """
    Read a binary PAMGuard data file into a PAMFile object
    :param filename: absolute or relative path to the .pgdt file to read
    :param order: endianess of data (defaults to 'network')
    :param buffering: number of bytes to buffer
    :param verbosity: logger verbosity level
    :param filters: filters to apply to data
    :param json_path: write json to a specific path
    """
    if not filters: filters = Filters()

    with timer("loading PAMGuard binary file"):
        with open(filename, "rb", buffering=buffering) as f:
            pgbfile = PAMGuardFile(path=filename, fp=f, order=order, filters=filters, report=report)
            pgbfile.load()
    if json_path:
        with open(json_path, 'w') as output:
            json_data = json.dumps(pgbfile.to_json(), indent=0, separators=(",", ": "))
            with timer(f"writing output JSON to {output.name}"):
                output.write(json_data)
    return pgbfile

