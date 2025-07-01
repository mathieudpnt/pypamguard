import os

DATASET_PATH = os.path.join("tests", "dataset")
CLICK_DETECTOR_DIR = os.path.join(DATASET_PATH, "ClickDetector")
WHISTLES_MOANS_DIR = os.path.join(DATASET_PATH, "WhistlesMoans")

TESTS = [
    {
        "json": "ClickDetector_v4_test1.json",
        "filename": "ClickDetector_v4_test1",
        "directory": CLICK_DETECTOR_DIR,
        "keyword": "ClickDetector"
    },
    {
        "json": "ClickDetector_v4_test1_daterange.json",
        "filename": "ClickDetector_v4_test1",
        "directory": CLICK_DETECTOR_DIR,
        "keyword": "ClickDetector"
    },
    {
        "json": "ClickDetector_v4_test1_uidlist.json",
        "filename": "ClickDetector_v4_test1",
        "directory": CLICK_DETECTOR_DIR,
        "keyword": "ClickDetector"
    },
    {
        "json": "WhistlesMoans_v2_test1.json",
        "filename": "WhistlesMoans_v2_test1",
        "directory": WHISTLES_MOANS_DIR,
        "keyword": "WhistlesMoans"
    }
]
