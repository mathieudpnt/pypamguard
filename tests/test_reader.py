import pytest

from . import _constants
from pypamguard.main import load_pamguard_binary_file
from pypamguard.core.pgbfile import PGBFile



def test_reader():
    pgdf = load_pamguard_binary_file(_constants.CLICK_DETECTOR_FILEPATH)
    assert isinstance(pgdf, PGBFile)

def test_reader_doesnotexist():
    with pytest.raises(FileNotFoundError):
        load_pamguard_binary_file("doesnotexist.pgdf")

def test_reader_invalidorder():
    with pytest.raises(ValueError):
        load_pamguard_binary_file(_constants.CLICK_DETECTOR_FILEPATH, order="invalid")

def test_reader_invalidbuffer():
    with pytest.raises(ValueError):
        load_pamguard_binary_file(_constants.CLICK_DETECTOR_FILEPATH, buffering="1024")
