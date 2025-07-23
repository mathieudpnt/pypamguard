import pypamguard.core.filters as filters
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