import os

DATASET_PATH = os.path.join("tests", "dataset")
CLICK_DIR = os.path.join(DATASET_PATH, "detectors", "click")
WHISTLEANDMOAN_DIR = os.path.join(DATASET_PATH, "detectors", "whistleandmoan")
LONGTERMSPECTRALAVERAGE_DIR = os.path.join(DATASET_PATH, "processing", "longtermspectralaverage")
NOISEBAND_DIR = os.path.join(DATASET_PATH, "processing", "noiseband")
SPERMWHALEIPI_DIR = os.path.join(DATASET_PATH, "spermwhaleipi")

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
]
