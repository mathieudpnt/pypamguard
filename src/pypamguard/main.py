from . import *
from .logger import logger, Verbosity

if __name__ == "__main__":
    logger.set_verbosity(Verbosity.INFO)
    #pdgf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/Click_Detector_v4.pgdf")
    pdgf = load_pamguard_binary_file("/home/sulli/code/pypamguard/tests/samples/test.pgdf")