from . import *
from .logger import logger, Verbosity
from pypamguard.core.filters import Filters, DateFilter, WhitelistFilter
import datetime

if __name__ == "__main__":

    d1 = datetime.datetime.fromtimestamp(1029326351847 / 1000, tz = datetime.UTC)
    d2 = datetime.datetime.fromtimestamp(1029326375040 / 1000, tz = datetime.UTC)

    pg_filters = Filters({
        # 'daterange': DateFilter(d1, d2, ordered=True),
        # 'uidlist': WhitelistFilter([15002421])
    })

    pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/dataset/Energy Sum/Energy_Sum_Detector_Ishmael_energy_sum_Ishmael_Detections_20170903_222900.pgdf")
    # pgdf = load_pamguard_binary_file("Click_Detector_Click_Detector_Clicks_20020814_115848.pgdf", verbosity=Verbosity.INFO, filters=pg_filters)
    # print(pgdf)