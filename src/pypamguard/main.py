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

    # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/dataset/FilteredNoiseMeasurement/FilteredNoiseMeasurement_v3_test1.pgdf", json_path="FilteredNoiseMeasurement_v3_test1.json", filters=pg_filters)

    filterednoisemeasurement_v3_test1 = load_pamguard_binary_file("../tests/dataset/processing/filterednoisemeasurement/filterednoisemeasurement_v3_test1.pgdf", json_path="filterednoisemeasurement_v3_test1.json")

    # spermwhaleipi_v1_test1 = load_pamguard_binary_file("../tests/dataset/spermwhaleipi/spermwhaleipi_v1_test1.pgdf", json_path="spermwhaleipi_v1_test1.json", filters=pg_filters)
    # spermwhaleipi_v1_test1_daterange = load_pamguard_binary_file("../tests/dataset/spermwhaleipi/spermwhaleipi_v1_test1_daterange.pgdf", json_path="spermwhaleipi_v1_test1_daterange.json", filters=Filters({'daterange': DateFilter(datetime.datetime.fromtimestamp(1751975639054 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1751975732265 / 1000, tz = datetime.UTC), ordered=True)}))
    # spermwhaleipi_v1_test1_uidlist = load_pamguard_binary_file("../tests/dataset/spermwhaleipi/spermwhaleipi_v1_tes1_uidlist.pgdf", json_path="spermwhaleipi_v1_test1_uidlist.json", filters=Filters({'uidlist': WhitelistFilter([2000002])}))