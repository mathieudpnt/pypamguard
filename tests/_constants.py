import os

DATASET_PATH = os.path.join("tests", "dataset")
CLICK_DIR = os.path.join(DATASET_PATH, "detectors", "click")
CLIPGENERATOR_DIR = os.path.join(DATASET_PATH, "processing", "clipgenerator")
WHISTLEANDMOAN_DIR = os.path.join(DATASET_PATH, "detectors", "whistleandmoan")
LONGTERMSPECTRALAVERAGE_DIR = os.path.join(DATASET_PATH, "processing", "longtermspectralaverage")
NOISEBAND_DIR = os.path.join(DATASET_PATH, "processing", "noiseband")
SPERMWHALEIPI_DIR = os.path.join(DATASET_PATH, "spermwhaleipi")
CLICKTRIGGERBACKGROUND_DIR = os.path.join(DATASET_PATH, "detectors", "clicktriggerbackground")
NOISEMONITOR_DIR = os.path.join(DATASET_PATH, "processing", "noisemonitor")
DIFAR_DIR = os.path.join(DATASET_PATH, "processing", "difar")
ISHMAEL_DIR = os.path.join(DATASET_PATH, "processing", "ishmael")

TESTS = [
    {
        "json": "click_v4_test1.json",
        "filename": "click_v4_test1",
        "directory": CLICK_DIR,
        "keyword": "click"
    },
    {
        "json": "click_v4_test1_daterange.json",
        "filename": "click_v4_test1",
        "directory": CLICK_DIR,
        "keyword": "click"
    },
    {
        "json": "click_v4_test1_uidlist.json",
        "filename": "click_v4_test1",
        "directory": CLICK_DIR,
        "keyword": "click"
    },
    {
        "json": "click_v4_test2.json",
        "filename": "click_v4_test2",
        "directory": CLICK_DIR,
        "keyword": "click"
    },
    {
        "json": "click_v4_test2_daterange.json",
        "filename": "click_v4_test2",
        "directory": CLICK_DIR,
        "keyword": "click"
    },
    {
        "json": "click_v4_test2_uidlist.json",
        "filename": "click_v4_test2",
        "directory": CLICK_DIR,
        "keyword": "click"
    },
    {
        "json": "click_v4_test3.json",
        "filename": "click_v4_test3",
        "directory": CLICK_DIR,
        "keyword": "click"
    },
    {
        "json": "click_v4_test3_daterange.json",
        "filename": "click_v4_test3",
        "directory": CLICK_DIR,
        "keyword": "click"
    },
    {
        "json": "click_v4_test3_uidlist.json",
        "filename": "click_v4_test3",
        "directory": CLICK_DIR,
        "keyword": "click"
    },
    {
        "json": "clipgenerator_v3_test1.json",
        "filename": "clipgenerator_v3_test1",
        "directory": CLIPGENERATOR_DIR,
        "keyword": "clipgenerator"
    },
    {
        "json": "clipgenerator_v3_test1_daterange.json",
        "filename": "clipgenerator_v3_test1",
        "directory": CLIPGENERATOR_DIR,
        "keyword": "clipgenerator"
    },
    {
        "json": "clipgenerator_v3_test1_uidlist.json",
        "filename": "clipgenerator_v3_test1",
        "directory": CLIPGENERATOR_DIR,
        "keyword": "clipgenerator"
    },
    {
        "json": "clipgenerator_v3_test2.json",
        "filename": "clipgenerator_v3_test2",
        "directory": CLIPGENERATOR_DIR,
        "keyword": "clipgenerator"
    },
    {
        "json": "clipgenerator_v3_test2_daterange.json",
        "filename": "clipgenerator_v3_test2",
        "directory": CLIPGENERATOR_DIR,
        "keyword": "clipgenerator"
    },
    {
        "json": "clipgenerator_v3_test2_uidlist.json",
        "filename": "clipgenerator_v3_test2",
        "directory": CLIPGENERATOR_DIR,
        "keyword": "clipgenerator"
    },
    {
        "json": "whistleandmoan_v2_test1.json",
        "filename": "whistleandmoan_v2_test1",
        "directory": WHISTLEANDMOAN_DIR,
        "keyword": "whistleandmoan"
    },
    {
        "json": "longtermspectralaverage_v2_test1.json",
        "filename": "longtermspectralaverage_v2_test1",
        "directory": LONGTERMSPECTRALAVERAGE_DIR,
        "keyword": "longtermspectralaverage"
    },
    {
        "json": "noiseband_v3_test1.json",
        "filename": "noiseband_v3_test1",
        "directory": NOISEBAND_DIR,
        "keyword": "noiseband",
    },
    {
        "json": "noiseband_v3_test1_daterange.json",
        "filename": "noiseband_v3_test1",
        "directory": NOISEBAND_DIR,
        "keyword": "noiseband",
    },
    {
        "json": "noiseband_v3_test1_uidlist.json",
        "filename": "noiseband_v3_test1",
        "directory": NOISEBAND_DIR,
        "keyword": "noiseband",
    },
    {
        "json": "noisebandnoise_v3_test1.json",
        "filename": "noisebandnoise_v3_test1",
        "directory": NOISEBAND_DIR,
        "keyword": "noiseband",
    },
    {
        "json": "noisebandnoise_v3_test1_daterange.json",
        "filename": "noisebandnoise_v3_test1",
        "directory": NOISEBAND_DIR,
        "keyword": "noiseband",
    },
    {
        "json": "noisebandnoise_v3_test1_uidlist.json",
        "filename": "noisebandnoise_v3_test1",
        "directory": NOISEBAND_DIR,
        "keyword": "noiseband",
    },
    {
        "json": "noisebandpulses_v3_test1.json",
        "filename": "noisebandpulses_v3_test1",
        "directory": NOISEBAND_DIR,
        "keyword": "noiseband",
    },
    {
        "json": "noisebandpulses_v3_test1_daterange.json",
        "filename": "noisebandpulses_v3_test1",
        "directory": NOISEBAND_DIR,
        "keyword": "noiseband",
    },
    {
        "json": "noisebandpulses_v3_test1_uidlist.json",
        "filename": "noisebandpulses_v3_test1",
        "directory": NOISEBAND_DIR,
        "keyword": "noiseband",
    },
    {
        "json": "spermwhaleipi_v1_test1.json",
        "filename": "spermwhaleipi_v1_test1",
        "directory": SPERMWHALEIPI_DIR,
        "keyword": "spermwhaleipi",
    },
    {
        "json": "spermwhaleipi_v1_test1_daterange.json",
        "filename": "spermwhaleipi_v1_test1",
        "directory": SPERMWHALEIPI_DIR,
        "keyword": "spermwhaleipi",
    },
    {
        "json": "spermwhaleipi_v1_test1_uidlist.json",
        "filename": "spermwhaleipi_v1_test1",
        "directory": SPERMWHALEIPI_DIR,
        "keyword": "spermwhaleipi",
    },
    {
        "json": "clicktriggerbackground_v0_test1.json",
        "filename": "clicktriggerbackground_v0_test1",
        "directory": CLICKTRIGGERBACKGROUND_DIR,
        "keyword": "clicktriggerbackground",
    },
    {
        "json": "clicktriggerbackground_v0_test1_daterange.json",
        "filename": "clicktriggerbackground_v0_test1",
        "directory": CLICKTRIGGERBACKGROUND_DIR,
        "keyword": "clicktriggerbackground",
    },
    {
        "json": "clicktriggerbackground_v0_test1_uidlist.json",
        "filename": "clicktriggerbackground_v0_test1",
        "directory": CLICKTRIGGERBACKGROUND_DIR,
        "keyword": "clicktriggerbackground",
    },
    {
        "json": "noisemonitor_v2_test1.json",
        "filename": "noisemonitor_v2_test1",
        "directory": NOISEMONITOR_DIR,
        "keyword": "noisemonitor",
    },
    {
        "json": "noisemonitor_v2_test1_daterange.json",
        "filename": "noisemonitor_v2_test1",
        "directory": NOISEMONITOR_DIR,
        "keyword": "noisemonitor",
    },
    {
        "json": "noisemonitor_v2_test1_uidlist.json",
        "filename": "noisemonitor_v2_test1",
        "directory": NOISEMONITOR_DIR,
        "keyword": "noisemonitor",
    },
    {
        "json": "difar_v2_test1.json",
        "filename": "difar_v2_test1",
        "directory": DIFAR_DIR,
        "keyword": "difar",
    },
    {
        "json": "difar_v2_test1_daterange.json",
        "filename": "difar_v2_test1",
        "directory": DIFAR_DIR,
        "keyword": "difar",
    },
    {
        "json": "difar_v2_test1_uidlist.json",
        "filename": "difar_v2_test1",
        "directory": DIFAR_DIR,
        "keyword": "difar",
    },
    {
        "json": "difar_v2_test2.json",
        "filename": "difar_v2_test2",
        "directory": DIFAR_DIR,
        "keyword": "difar",
    },
    {
        "json": "difar_v2_test2_daterange.json",
        "filename": "difar_v2_test2",
        "directory": DIFAR_DIR,
        "keyword": "difar",
    },
    {
        "json": "difar_v2_test2_uidlist.json",
        "filename": "difar_v2_test2",
        "directory": DIFAR_DIR,
        "keyword": "difar",
    },
    {
        "json": "difar_v2_test3.json",
        "filename": "difar_v2_test3",
        "directory": DIFAR_DIR,
        "keyword": "difar",
    },
    {
        "json": "difar_v2_test3_daterange.json",
        "filename": "difar_v2_test3",
        "directory": DIFAR_DIR,
        "keyword": "difar",
    },
    {
        "json": "difar_v2_test3_uidlist.json",
        "filename": "difar_v2_test3",
        "directory": DIFAR_DIR,
        "keyword": "difar",
    },
    {
        "json": "ishmaeldetections_energysum_v2_test1.json",
        "filename": "ishmaeldetections_energysum_v2_test1",
        "directory": ISHMAEL_DIR,
        "keyword": "ishmael",
    },
    {
        "json": "ishmaeldetections_energysum_v2_test2.json",
        "filename": "ishmaeldetections_energysum_v2_test2",
        "directory": ISHMAEL_DIR,
        "keyword": "ishmael",
    },
    {
        "json": "ishmaeldetections_energysum_v2_test3.json",
        "filename": "ishmaeldetections_energysum_v2_test3",
        "directory": ISHMAEL_DIR,
        "keyword": "ishmael",
    },
    {
        "json": "ishmaeldetections_matchedfilter_v2_test1.json",
        "filename": "ishmaeldetections_matchedfilter_v2_test1",
        "directory": ISHMAEL_DIR,
        "keyword": "ishmael",
    },
    {
        "json": "ishmaeldetections_matchedfilter_v2_test2.json",
        "filename": "ishmaeldetections_matchedfilter_v2_test2",
        "directory": ISHMAEL_DIR,
        "keyword": "ishmael",
    },
    {
        "json": "ishmaeldetections_spectrogramcorrelation_v2_test1.json",
        "filename": "ishmaeldetections_spectrogramcorrelation_v2_test1",
        "directory": ISHMAEL_DIR,
        "keyword": "ishmael",
    },
    {
        "json": "ishmaeldetections_spectrogramcorrelation_v2_test2.json",
        "filename": "ishmaeldetections_spectrogramcorrelation_v2_test2",
        "directory": ISHMAEL_DIR,
        "keyword": "ishmael",
    },
]
