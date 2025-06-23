import pytest

from . import _constants
from pypamguard.reader import pamread
from pypamguard.pamfile import PAMFile



def test_reader():
    pgdf = pamread(_constants.CLICK_DETECTOR_FILEPATH)
    assert isinstance(pgdf, PAMFile)

def test_reader_doesnotexist():
    with pytest.raises(FileNotFoundError):
        pamread("doesnotexist.pgdf")

def test_reader_invalidorder():
    with pytest.raises(ValueError):
        pamread(_constants.CLICK_DETECTOR_FILEPATH, order="invalid")

def test_reader_invalidbuffer():
    with pytest.raises(ValueError):
        pamread(_constants.CLICK_DETECTOR_FILEPATH, buffering="1024")
