import time
import pytz
import tzlocal

LOCAL_TIMEZONE = tzlocal.get_localzone()


def get_local(utc_datetime):
    """Get the local datetime"""
    return LOCAL_TIMEZONE.normalize(
        utc_datetime.replace(tzinfo=pytz.utc).astimezone(LOCAL_TIMEZONE))


def get_utc(naive_datetime):
    """Get the UTC time for the local datetime object.

    (controlling for daylight savings time)"""
    return LOCAL_TIMEZONE.localize(
        naive_datetime,
        is_dst=(time.localtime().tm_isdst > 0)
    ).astimezone(pytz.utc)
