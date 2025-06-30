from . import *
from .logger import logger, Verbosity

if __name__ == "__main__":
    logger.set_verbosity(Verbosity.INFO)
    pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/dataset/ClickDetector/ClickDetector_v4_test1.pgdf")
    # pdgf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/test.pgdf")
    # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/RW_Edge_Detector_Right_Whale_Edge_Detector_Edges_20090328_000000.pgdf")
    #pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/Clip_Generator_Clip_generator_Clips_20170903_222955.pgdf", verbosity=Verbosity.DEBUG)
    # pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/WhistlesMoans_Whistle_and_Moan_Detector_Contours_20240806_121502.pgdf", verbosity=Verbosity.INFO)

    with open("test.json", "w") as f:
        import json
        json.dump(pgdf.json(), f, indent=1)