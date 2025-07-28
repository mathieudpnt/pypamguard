import datetime
import pypamguard.core.filters as filters
from pypamguard.core.exceptions import *
import pytest

def _whitelist_filter(whitelist):
    return filters.WhitelistFilter(whitelist)

@pytest.mark.parametrize("whitelist", [[1, 2, 3], {1, 2, 3}])
def test_whitelist_filter(whitelist):
    f = filters.WhitelistFilter(whitelist)
    assert f.whitelist == {1, 2, 3}
    assert f.check(0) == filters.FILTER_POSITION.SKIP
    assert f.check(1) == filters.FILTER_POSITION.KEEP
    assert f.check(2) == filters.FILTER_POSITION.KEEP
    assert f.check(3) == filters.FILTER_POSITION.KEEP
    assert f.check(4) == filters.FILTER_POSITION.SKIP

@pytest.mark.parametrize("ignore_none", [True, False])
@pytest.mark.parametrize("ordered", [True, False])
def test_range_filter(ignore_none, ordered):
    f = filters.RangeFilter(1, 3, ordered=ordered, ignore_none=ignore_none)
    assert f.check(0.5) == filters.FILTER_POSITION.SKIP
    assert f.check(1) == filters.FILTER_POSITION.KEEP
    assert f.check(1.81) == filters.FILTER_POSITION.KEEP
    assert f.check(3) == filters.FILTER_POSITION.KEEP
    assert f.check(3.19) == filters.FILTER_POSITION.STOP if ordered else filters.FILTER_POSITION.SKIP
    assert f.check(None) == filters.FILTER_POSITION.KEEP if ignore_none else filters.FILTER_POSITION.SKIP

@pytest.mark.parametrize("ignore_none", [True, False])
@pytest.mark.parametrize("ordered", [True, False])
def test_range_filter_comparator(ignore_none, ordered):
    f = filters.RangeFilter(1, 3, comparator=lambda a,b: a <= b, ordered=ordered, ignore_none=ignore_none)
    assert f.check(0.5) == filters.FILTER_POSITION.SKIP
    assert f.check(1) == filters.FILTER_POSITION.SKIP
    assert f.check(1.81) == filters.FILTER_POSITION.KEEP
    assert f.check(3) == filters.FILTER_POSITION.STOP if ordered else filters.FILTER_POSITION.SKIP
    assert f.check(3.19) == filters.FILTER_POSITION.STOP if ordered else filters.FILTER_POSITION.SKIP
    assert f.check(None) == filters.FILTER_POSITION.KEEP if ignore_none else filters.FILTER_POSITION.SKIP

@pytest.mark.parametrize("ignore_none", [True, False])
@pytest.mark.parametrize("ordered", [True, False])
def test_range_filter_validation(ignore_none, ordered):
    f = filters.RangeFilter(1, 6, validation_func=lambda a: a % 2 == 0, ordered=ordered, ignore_none=ignore_none)
    assert f.check(0.5) == filters.FILTER_POSITION.SKIP
    assert f.check(1) == filters.FILTER_POSITION.SKIP
    assert f.check(1.81) == filters.FILTER_POSITION.SKIP
    assert f.check(3) == filters.FILTER_POSITION.SKIP
    assert f.check(4) == filters.FILTER_POSITION.KEEP
    assert f.check(6.19) == filters.FILTER_POSITION.SKIP
    assert f.check(8) == filters.FILTER_POSITION.STOP if ordered else filters.FILTER_POSITION.SKIP
    assert f.check(None) == filters.FILTER_POSITION.KEEP if ignore_none else filters.FILTER_POSITION.SKIP


@pytest.mark.parametrize("ignore_none", [True, False])
@pytest.mark.parametrize("ordered", [True, False])
def test_date_filter_validation(ignore_none, ordered):
    d1 = datetime.datetime.fromtimestamp(1000000000000 / 1000, tz = datetime.UTC)
    d2 = datetime.datetime.fromtimestamp(1000000000100 / 1000, tz = datetime.UTC)
    f = filters.DateFilter(d1, d2, ordered=ordered, ignore_none=ignore_none)
    assert f.check(datetime.datetime.fromtimestamp(999999999999 / 1000, tz = datetime.UTC)) == filters.FILTER_POSITION.SKIP
    assert f.check(datetime.datetime.fromtimestamp(1000000000000 / 1000, tz = datetime.UTC)) == filters.FILTER_POSITION.KEEP
    assert f.check(datetime.datetime.fromtimestamp(1000000000100 / 1000, tz = datetime.UTC)) == filters.FILTER_POSITION.KEEP
    assert f.check(datetime.datetime.fromtimestamp(1000000000101 / 1000, tz = datetime.UTC)) == filters.FILTER_POSITION.STOP if ordered else filters.FILTER_POSITION.SKIP
    assert f.check(None) == filters.FILTER_POSITION.KEEP if ignore_none else filters.FILTER_POSITION.SKIP

def test_date_filter_no_tz_start():
    with pytest.raises(ValueError):
        filters.DateFilter(datetime.datetime.fromtimestamp(1000000000000 / 1000), datetime.datetime.fromtimestamp(1000000000100 / 1000, tz = datetime.UTC))

def test_date_filter_no_tz_end():
    with pytest.raises(ValueError):
        filters.DateFilter(datetime.datetime.fromtimestamp(1000000000000 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1000000000100 / 1000))

def test_date_filter_no_tz_ignore():
    assert filters.DateFilter(datetime.datetime.fromtimestamp(1000000000000 / 1000), datetime.datetime.fromtimestamp(1000000000100 / 1000), ignore_timezone=True)

def test_date_filter_no_tz():
    f = filters.DateFilter(datetime.datetime.fromtimestamp(1000000000000 / 1000, tz = datetime.UTC), datetime.datetime.fromtimestamp(1000000000100 / 1000, tz = datetime.UTC))
    with pytest.raises(ValueError):
        f.check(datetime.datetime.fromtimestamp(1000000000101 / 1000))

@pytest.fixture
def filters_obj():
    return filters.Filters()

def test_filters_empty():
    fs = filters.Filters()
    assert len(fs) == 0

def test_filters_add():
    fs = filters.Filters()
    fs.add("daterange", filters.DateFilter(datetime.datetime.fromtimestamp(1, tz = datetime.UTC), datetime.datetime.fromtimestamp(2, tz = datetime.UTC)))
    assert len(fs) == 1
    fs.add("uidlist", filters.WhitelistFilter([1]))
    assert len(fs) == 2
    fs.add("uidrange", filters.RangeFilter(1, 2))
    assert len(fs) == 3

def test_filters_add_invalid_daterange(filters_obj):
    invalid = filters.WhitelistFilter([1])
    with pytest.raises(ValueError):
        filters.Filters({'daterange': invalid})
    with pytest.raises(ValueError):
        filters_obj.add("daterange", invalid)

def test_filters_add_invalid_uidlist(filters_obj):
    invalid = filters.DateFilter(datetime.datetime.fromtimestamp(1, tz = datetime.UTC), datetime.datetime.fromtimestamp(2, tz = datetime.UTC))
    with pytest.raises(ValueError):
        filters.Filters({'uidlist': invalid})
    with pytest.raises(ValueError):
        filters_obj.add("uidlist", invalid)
    
def test_filters_add_invalid_uidrange(filters_obj):
    invalid = filters.WhitelistFilter([1])
    with pytest.raises(ValueError):
        filters.Filters({'uidrange': invalid})
    with pytest.raises(ValueError):
        filters_obj.add("uidrange", invalid)

def test_filters_add_none(filters_obj):
    with pytest.raises(ValueError):
        filters_obj.add("uidrange", None)

def test_filters_add_custom(filters_obj):
    filters_obj.add("custom", filters.WhitelistFilter([1]))
    assert len(filters_obj) == 1

def test_multi_filter(filters_obj):
    filters_obj.add("daterange", filters.DateFilter(datetime.datetime.fromtimestamp(1, tz = datetime.UTC), datetime.datetime.fromtimestamp(10, tz = datetime.UTC)))
    filters_obj.add("uidlist", filters.WhitelistFilter([1]))
    assert len(filters_obj) == 2
    
    filters_obj.filter("uidlist", 1) == filters.FILTER_POSITION.KEEP
    assert filters_obj.position == filters.FILTER_POSITION.KEEP
    with pytest.raises(filters.FilterMismatchException): filters_obj.filter("uidlist", 2)

    filters_obj.filter("daterange", datetime.datetime.fromtimestamp(5, tz = datetime.UTC))
    assert filters_obj.position == filters.FILTER_POSITION.KEEP
    
    
    
    # with pytest.raises(filters.FilterMismatchException): assert filters_obj.filter("daterange", datetime.datetime.fromtimestamp(15, tz = datetime.UTC))

    assert filters_obj.position == filters.FILTER_POSITION.SKIP
    with pytest.raises(filters.FilterMismatchException): assert filters_obj.filter("daterange", datetime.datetime.fromtimestamp(0, tz = datetime.UTC))
