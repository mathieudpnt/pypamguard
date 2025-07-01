import time
from pypamguard.core.pgbfile import PGBFile
from pypamguard.utils.constants import BYTE_ORDERS, DEFAULT_BUFFER_SIZE
from pypamguard.core.filters import Filters, DateFilter
from .logger import logger, Verbosity, logger_config
import io, json
from contextlib import contextmanager

@contextmanager
def timer(label):
    logger.info(f"Started {label}")
    start_time = time.perf_counter()
    yield
    total_time = time.perf_counter() - start_time
    logger.info(f"Finished {label} in {total_time:.3f} seconds")

def load_pamguard_binary_file(filename, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN, buffering: int | None = DEFAULT_BUFFER_SIZE, verbosity: Verbosity = Verbosity.INFO, filters: Filters = Filters(), output: io.TextIOWrapper | None = None) -> PGBFile:
    """
    Read a binary PAMGuard data file into a PAMFile object
    :param filename: absolute or relative path to the .pgdt file to read
    :param order: endianess of data (defaults to 'network')
    :param buffering: number of bytes to buffer
    :param verbosity: logger verbosity level
    :param filters: filters to apply to data
    :param output: write json to a file stream (must be write-enabled)
    """

    with logger_config(verbosity=verbosity):
        with timer("loading PAMGuard binary file"):
            with open(filename, "rb", buffering=buffering) as f:
                pgbfile = PGBFile(path=filename, fp=f, order=order, filters=filters)
                pgbfile.load()
        if output:
            with timer(f"writing output JSON to {output.name}"):
                json.dump(pgbfile.to_json(), output, indent=4, separators=(",", ": "))
    return pgbfile

