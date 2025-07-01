import os

DATASET_PATH = os.path.join("tests", "dataset")

PATH_CLICK_DETECTOR = os.path.join(DATASET_PATH, "ClickDetector")

PATHS = {
    "Click Detector": os.path.join(DATASET_PATH, "ClickDetector"),
    "Right Whale Edge Detector": os.path.join(DATASET_PATH, "RightWhaleEdgeDetector")
}

DEFAULT_FILE_HEADER_LENGTH = 103

FILE_HEADER_IDENTIFIER = -1
FILE_FOOTER_IDENTIFIER = -2
MODULE_HEADER_IDENTIFIER = -3
MODULE_FOOTER_IDENTIFIER = -4

TESTS = [
    {
        "json": "ClickDetector_v4_test1.json",
        "filename": "ClickDetector_v4_test1",
        "directory": PATH_CLICK_DETECTOR,
        "keyword": "ClickDetector"
    },
    {
        "json": "ClickDetector_v4_test1_daterange.json",
        "filename": "ClickDetector_v4_test1",
        "directory": PATH_CLICK_DETECTOR,
        "keyword": "ClickDetector"
    },
    {
        "json": "ClickDetector_v4_test1_uidlist.json",
        "filename": "ClickDetector_v4_test1",
        "directory": PATH_CLICK_DETECTOR,
        "keyword": "ClickDetector"
    }
]
