from . import *
from .logger import logger, Verbosity
from pypamguard.core.filters import Filters, DateFilter, WhitelistFilter
import datetime

if __name__ == "__main__":

    d1 = datetime.datetime.fromtimestamp(1499572333281 / 1000, tz = datetime.UTC)
    d2 = datetime.datetime.fromtimestamp(1499572363281 / 1000, tz = datetime.UTC)

    pg_filters = Filters({
        # 'daterange': DateFilter(d1, d2, ordered=True),
        # 'uidlist': WhitelistFilter([2000006, 2000003])
    })

    pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/dataset/FilteredNoiseMeasurement/FilteredNoiseMeasurement_v3_test1.pgdf", json_path="FilteredNoiseMeasurement_v3_test1.json", filters=pg_filters)