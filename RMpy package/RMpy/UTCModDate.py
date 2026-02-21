import datetime

# https://docs.python.org/3/library/datetime.html

MS_MJD_EPOCH = datetime.datetime(1899, 12, 30, tzinfo=datetime.timezone.utc)

def ms_mjd_to_datetime(mjd: float, to_local: bool = False) -> datetime.datetime:
    """Convert Microsoft Modified Julian Date → Python datetime."""
    dt_utc = MS_MJD_EPOCH + datetime.timedelta(days=mjd)

    if to_local:
        return dt_utc.astimezone()  # system local timezone

    return dt_utc


# examples from an RM database

print(ms_mjd_to_datetime( 46070.9849900231, True))
print(ms_mjd_to_datetime( 46070.9849900231, False))
print(ms_mjd_to_datetime(45442.2219532755, True))
print(ms_mjd_to_datetime(45442.2219532755, False))
print(ms_mjd_to_datetime(44710.6778276273, True))
print(ms_mjd_to_datetime(44710.6778276273, False))


# 2026-02-17 15:38:23.137996-08:00
# 2026-02-17 23:38:23.137996+00:00
# 2024-05-29 22:19:36.763003-07:00
# 2024-05-30 05:19:36.763003+00:00
# 2022-05-29 09:16:04.306999-07:00
# 2022-05-29 16:16:04.306999+00:00

# why are some -07:00 and one -08:00 ?


import datetime

MS_MJD_EPOCH = datetime.datetime(1899, 12, 30, tzinfo=datetime.timezone.utc)

def datetime_to_ms_mjd(dt: datetime.datetime) -> float:
    """Convert a Python datetime → Microsoft Modified Julian Date (float days)."""
    # Ensure timezone-aware; assume UTC if naive
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    else:
        dt = dt.astimezone(datetime.timezone.utc)

    delta = dt - MS_MJD_EPOCH
    return delta.total_seconds() / 86400.0

local_tz = datetime.datetime.now().astimezone().tzinfo

print( datetime_to_ms_mjd( datetime.datetime ( 2026,  2, 17, 15, 38, 23, 137996, tzinfo= None)))
print( datetime_to_ms_mjd( datetime.datetime ( 2026,  2, 17, 23, 38, 23, 137996, tzinfo= local_tz)))
print( datetime_to_ms_mjd( datetime.datetime ( 2024,  5, 29, 22, 19, 36, 763003, tzinfo= None)))
print( datetime_to_ms_mjd( datetime.datetime ( 2024,  5, 30,  5, 19, 36, 763003, tzinfo= local_tz)))
print( datetime_to_ms_mjd( datetime.datetime ( 2022,  5, 29,  9, 16,  4, 306999, tzinfo= None)))
print( datetime_to_ms_mjd( datetime.datetime ( 2022,  5, 29, 16, 16,  4, 306999, tzinfo= local_tz)))

# 46070.65165668977
# 46071.318323356434
# 45441.93028660883
# 45442.55528660883
# 44710.38616096064
# 44711.01116096064


# Determine the system's local timezone
local_tz = datetime.datetime.now().astimezone().tzinfo

# Construct a timezone-aware datetime using the local timezone
original_dt = datetime.datetime(
    2026, 2, 17, 23, 38, 23, 137996,
    tzinfo=local_tz
)

# Step 1: Convert datetime → MS-MJD
mjd_value = datetime_to_ms_mjd(original_dt)

# Step 2: Convert MS-MJD → datetime (UTC)
roundtrip_dt_utc = ms_mjd_to_datetime(mjd_value)

# Step 3: Convert back to the original local timezone
roundtrip_dt_local = roundtrip_dt_utc.astimezone(local_tz)

print("Original datetime:        ", original_dt)
print("MS-MJD value:             ", mjd_value)
print("Round-trip UTC datetime:  ", roundtrip_dt_utc)
print("Round-trip local datetime:", roundtrip_dt_local)