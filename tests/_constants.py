import os

DATASET_PATH = os.path.join("tests", "dataset")
CLICK_DETECTOR_DIR = os.path.join(DATASET_PATH, "ClickDetector")
WHISTLES_MOANS_DIR = os.path.join(DATASET_PATH, "WhistlesMoans")
LTSA_DIR = os.path.join(DATASET_PATH, "LTSA")
FILTERED_NOISE_MEASUREMENT_DIR = os.path.join(DATASET_PATH, "FilteredNoiseMeasurement")

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
    },
    {
        "json": "LTSA_v2_test1.json",
        "filename": "LTSA_v2_test1",
        "directory": LTSA_DIR,
        "keyword": "LTSA"
    },
    {
        "json": "FilteredNoiseMeasurement_v3_test1.json",
        "filename": "FilteredNoiseMeasurement_v3_test1",
        "directory": FILTERED_NOISE_MEASUREMENT_DIR,
        "keyword": "FilteredNoiseMeasurement",
    },
    {
        "json": "FilteredNoiseMeasurement_v3_test1_daterange.json",
        "filename": "FilteredNoiseMeasurement_v3_test1",
        "directory": FILTERED_NOISE_MEASUREMENT_DIR,
        "keyword": "FilteredNoiseMeasurement",
    },
    {
        "json": "FilteredNoiseMeasurement_v3_test1_uidlist.json",
        "filename": "FilteredNoiseMeasurement_v3_test1",
        "directory": FILTERED_NOISE_MEASUREMENT_DIR,
        "keyword": "FilteredNoiseMeasurement",
    }
]
