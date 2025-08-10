import pytest, os, glob, datetime

from pypamguard.core.pamguardfile import PAMGuardFile
from pypamguard.core.filters import Filters, WhitelistFilter, DateFilter
from pypamguard.chunks.generics import GenericModule, GenericBackground
from ._constants import DIRS, DATASET_PATH, CLICK_DIR
from pypamguard import load_pamguard_binary_folder, load_pamguard_binary_file

EXTENSIONS = ["*.pgdf", "*.pgnf", "*.pgdx", "**/*.pgdf", "**/*.pgnf", "**/*.pgdx"]

@pytest.mark.parametrize("ext", EXTENSIONS)
@pytest.mark.parametrize("dir", DIRS + [DATASET_PATH])
def test_load_folder(ext, dir):
    exp_files = glob.glob(os.path.join(dir, ext), recursive=True)
    data, background, report = load_pamguard_binary_folder(dir, ext)
    total_data_length = 0
    total_background_length = 0
    for file in exp_files:
        bf = load_pamguard_binary_file(file)
        total_data_length += len(bf.data)
        total_background_length += len(bf.background)
    assert len(data) == total_data_length
    assert len(background) == total_background_length
    for d in data:
        assert isinstance(d, GenericModule)
        assert hasattr(d, "file_info")
    for d in background:
        assert isinstance(d, GenericBackground)
        assert hasattr(d, "file_info")

def test_load_folder_missing():
    with pytest.raises(FileNotFoundError):
        load_pamguard_binary_folder("missing", "*.pgdf")

def test_load_folder_filter_uidlist():
    # One UID from each of the three files in CLICK_DIR
    UIDS = [5000001, 11000001, 2000001]
    filter_obj = Filters({
        "uidlist": WhitelistFilter(UIDS)
    })
    data, background, report = load_pamguard_binary_folder(CLICK_DIR, "*.pgdf", filters=filter_obj)
    assert len(data) == 3
    assert len(background) == 0


date1 = 1504477735008 # millis
date2 = 1259994147056 # millis
date3 = 1751975563187 # millis

DATERANGE_PARAMS = [
    {
        "start": date1,
        "end": date1 + 1000,
        "expected_data": 127,
        "expected_background": 0,
    },
    {
        "start": date1,
        "end": date3 + 1000,
        "expected_data": 8383,
        "expected_background": 0,
    },
]

@pytest.mark.parametrize("params", DATERANGE_PARAMS)
def test_load_folder_filter_daterange_ordered(params):
    filter_obj = Filters({
        "daterange": DateFilter(datetime.datetime.fromtimestamp(params["start"] / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(params["end"] / 1000, tz = datetime.UTC), ordered=True)
    })

    data, background, report = load_pamguard_binary_folder(CLICK_DIR, "*.pgdf", filters=filter_obj)
    assert type(data) ==  list
    assert type(background) == list
    assert len(report.errors) == 0

@pytest.mark.parametrize("ext", EXTENSIONS)
def test_load_folder_remove_waveform(ext):
    data, background, report = load_pamguard_binary_folder(DATASET_PATH, ext, clear_fields=["wave", "channel_map"])
    for d in data:
        assert "wave" not in d.__dict__
        assert "channel_map" not in d.__dict__