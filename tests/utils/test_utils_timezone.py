import datetime
import time
import pytz
import tzlocal
from jawaf.utils import timezone

UTC_OFFSET = datetime.datetime.now(tzlocal.get_localzone()).utcoffset().total_seconds() / 3600

def test_get_local():
    """Test converting from utc to local."""
    target = datetime.datetime(2017, 4, 11, 8, 0, tzinfo=pytz.utc)
    local_target = timezone.get_local(target)
    assert local_target.hour == int(8 + UTC_OFFSET)

def test_get_utc():
    """Test converting a naive datetime to a utc datetime with timezone info."""
    target = datetime.datetime(2017, 4, 11, 0, 0)
    utc_target = timezone.get_utc(target)
    assert utc_target.tzinfo == pytz.utc
    assert utc_target.hour == int(0 - UTC_OFFSET)