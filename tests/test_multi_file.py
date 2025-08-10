import pytest

from pypamguard import load_pamguard_multi_file
from pypamguard.core.exceptions import CriticalException
from ._constants import DATASET_PATH, CLICK_DIR

FNAMES = ['click_v4_test1.pgdf', 'click_v4_test2.pgdf', 'click_v4_test3.pgdf']
UIDS = [5000001, 11000001, 2000001]

def test_multi_file():
    data, report = load_pamguard_multi_file(CLICK_DIR, FNAMES, UIDS)
    assert len(data) == 3
    assert len(report.errors) == 0

def test_multi_file_missing_folder():
    with pytest.raises(FileNotFoundError):
        data, report = load_pamguard_multi_file("missing_folder", FNAMES, UIDS)

def test_multi_file_fnames_and_uids_not_same_length():
    with pytest.raises(ValueError):
        data, report = load_pamguard_multi_file(CLICK_DIR, FNAMES, UIDS[:-1])

def test_multi_file_missing_filename():
    fnames = FNAMES + ["missing_file.pgdf"]
    uids = UIDS + [0]
    data, report = load_pamguard_multi_file(CLICK_DIR, fnames, uids)
    assert len(data) == 3
    assert len(report.errors) == 1

def test_multi_file_missing_uid():
    uids = UIDS
    uids.pop(-1)
    uids.append(0)
    data, report = load_pamguard_multi_file(CLICK_DIR, FNAMES, uids)
    assert len(data) == 2
    assert len(report.errors) == 1
