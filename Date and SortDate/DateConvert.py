# ------------------------------------------------------------
# RootsMagic SortDate encoder/decoder with full date-type support
# ------------------------------------------------------------

import re
from datetime import date, timedelta


# ------------------------------------------------------------
# Modifier mapping
# ------------------------------------------------------------

RM_MODIFIERS = {
    "D.": 0,     # definite
    "ABT": 1,
    "BEF": 2,
    "AFT": 3,
    "CAL": 4,
    "EST": 5,
    "INT": 6,
    "FROM": 7,   # RM uses 7 for interval/range start
}

def decode_modifier(s: str) -> int:
    return RM_MODIFIERS.get(s.upper(), 0)

def encode_modifier(code: int) -> str:
    for k, v in RM_MODIFIERS.items():
        if v == code:
            return k
    return "D."


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def parse_ymd(s: str):
    """Parse YYYYMMDD or partial YYYYMM or YYYY."""
    year = int(s[0:4])
    month = int(s[4:6]) if len(s) >= 6 else 0
    day = int(s[6:8]) if len(s) >= 8 else 0
    return year, month, day


def days_between(y1, m1, d1, y2, m2, d2):
    """Compute span in days for ranges."""
    try:
        d1 = date(y1, m1 or 1, d1 or 1)
        d2 = date(y2, m2 or 1, d2 or 1)
        return (d2 - d1).days
    except:
        return 0


# ------------------------------------------------------------
# ENCODER
# ------------------------------------------------------------

def encode_sort_date(RMDate: str) -> int:
    RMDate = RMDate.strip().upper()

    # --------------------------------------------------------
    # 1. RANGE: BETxxxxANDxxxx
    # --------------------------------------------------------
    m = re.match(r"BET(\d{4,8})AND(\d{4,8})", RMDate)
    if m:
        y1, m1, d1 = parse_ymd(m.group(1))
        y2, m2, d2 = parse_ymd(m.group(2))
        modifier = decode_modifier("FROM")  # RM uses 7
        span = days_between(y1, m1, d1, y2, m2, d2)
        year, month, day = y1, m1, d1

        return (
            (modifier << 29) |
            (year     << 14) |
            (month    << 10) |
            (day      << 5)  |
            (span & 31)
        )

    # --------------------------------------------------------
    # 2. INTERVAL: FROMxxxxTOxxxx or FROMxxxx
    # --------------------------------------------------------
    m = re.match(r"FROM(\d{4,8})(TO(\d{4,8}))?", RMDate)
    if m:
        y1, m1, d1 = parse_ymd(m.group(1))
        if m.group(3):
            y2, m2, d2 = parse_ymd(m.group(3))
            span = days_between(y1, m1, d1, y2, m2, d2)
        else:
            span = 0

        modifier = decode_modifier("FROM")

        return (
            (modifier << 29) |
            (y1       << 14) |
            (m1       << 10) |
            (d1       << 5)  |
            (span & 31)
        )

    # --------------------------------------------------------
    # 3. SIMPLE / MODIFIED DATES
    # --------------------------------------------------------
    modifier = decode_modifier(RMDate[0:3])
    ymd = RMDate[3:]
    y, m, d = parse_ymd(ymd)
    span = 0

    return (
        (modifier << 29) |
        (y        << 14) |
        (m        << 10) |
        (d        << 5)  |
        span
    )


# ------------------------------------------------------------
# DECODER
# ------------------------------------------------------------

def decode_sort_date(sortdate: int) -> dict:
    modifier = (sortdate >> 29) & 0b111
    year     = (sortdate >> 14) & 0x7FFF
    month    = (sortdate >> 10) & 0xF
    day      = (sortdate >> 5)  & 0x1F
    span     = sortdate & 0x1F

    return {
        "modifier_code": modifier,
        "modifier_str": encode_modifier(modifier),
        "year": year,
        "month": month,
        "day": day,
        "span": span
    }


#   TEST   ================================================================

print( encode_sort_date("D.19940315"))
      