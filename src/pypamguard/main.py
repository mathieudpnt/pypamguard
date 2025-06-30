from . import *
from .logger import logger, Verbosity

if __name__ == "__main__":
    logger.set_verbosity(Verbosity.INFO)
    #pdgf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/Click_Detector_v4.pgdf")
    # pdgf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/test.pgdf")
    pgdf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/RW_Edge_Detector_Right_Whale_Edge_Detector_Edges_20090328_000000.pgdf")