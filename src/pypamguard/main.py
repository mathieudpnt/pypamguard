from . import *
from .logger import logger, Verbosity
from pypamguard.core.filters import Filters, DateFilter, WhitelistFilter
import datetime

if __name__ == "__main__":

    pg_filters = Filters()

    d1 = datetime.datetime.fromtimestamp(1504477746918 / 1000, tz = datetime.UTC)
    d2 = datetime.datetime.fromtimestamp(1504477758400 / 1000, tz = datetime.UTC)

    pg_filters = Filters({
        # 'daterange': DateFilter(d1, d2, ordered=True),
        # 'uidlist': WhitelistFilter([5000037])
    })

    with open("test1.json", "w") as f:
        pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/dataset/LTSA/LTSA_Long_Term_Spectral_Average_LTSA_20170709_035643.pgdf", output=f, verbosity=Verbosity.DEBUG)
        # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/dataset/ClickDetector/Click_Detector_Click_Detector_Clicks_20020814_115547.pgdf")
        # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/dataset/ClickDetector/ClickDetector_v4_test1.pgdf", verbosity=Verbosity.INFO, filters=pg_filters)
        # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/src/Click_Detector_Click_Detector_90kHz_Clicks_20191114_222426.pgdf")
        # pdgf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/test.pgdf")
        # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/RW_Edge_Detector_Right_Whale_Edge_Detector_Edges_20090328_000000.pgdf", verbosity=Verbosity.INFO)
        # pgdf = load_pamguard_binary_file("Click_Detector_Click_Detector_Clicks_20020814_115848.pgdf", verbosity=Verbosity.INFO)
        
        #pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/Clip_Generator_Clip_generator_Clips_20170903_222955.pgdf", verbosity=Verbosity.DEBUG)
        # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/dataset/WhistlesMoans/WhistlesMoans_v2_test1.pgdf", verbosity=Verbosity.DEBUG)
        # for i in range(len(pgdf.data[0].data)):
        #     print(pgdf.data[0].data[i], pgdf.data[0].byte_data[i])
