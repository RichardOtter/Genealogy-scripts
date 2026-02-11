import datetime
from zoneinfo import ZoneInfo

MJD_OFFSET = 2415018.5
FILETIME_EPOCH = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)

def mjd_float_to_datetime(mjd, LocalTZ=False):
    jd = mjd + MJD_OFFSET

    Z = int(jd + 0.5)
    F = (jd + 0.5) - Z

    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - (alpha // 4)

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    day = B - D - int(30.6001 * E) + F
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715

    day_int = int(day)
    frac = day - day_int
    seconds = frac * 86400

    dt = datetime.datetime(year, month, day_int, tzinfo=datetime.timezone.utc) \
         + datetime.timedelta(seconds=seconds)

    if LocalTZ:
        return dt.astimezone()   # system local timezone

    return dt


JD = 46054.8325689583

print(mjd_float_to_datetime(JD).strftime("%Y-%m-%d %H:%M:%S"))

print(mjd_float_to_datetime(JD, LocalTZ=True).strftime("%Y-%m-%d %H:%M:%S"))

