import sys
from pathlib import Path
sys.path.append( r'.' )

import RMpy.common as RMc  # type: ignore

#from enum import Enum
import enum
from datetime import date



# RM Internal Date structure
# organized as characters, numbered from left, origin 0
# 24 chars total (except for types: . and T)
# 2 chars  type & structure
# 11 chars part 1
# 11 chars part 2

#   0123456789A123456789B1234
#   0       1   type
#   1       1   structure
# part 1
#   2       1   BC-AD  (+ or -)
#   3-10    8   YYYYMMDD
#   11      1   slash date (. or /)
#   12      1   confidence
# part 2
#   13      1   BC-AD  (+ or -)
#   14-21   8   YYYYMMDD
#   22      1   slash date (. or /)
#   23      1   confidence

# if structure does not use a part 2, then part 2= "+00000000.."

# eg    D.+20250216..+00000000..

# all RM External human readable formats (from RM v9 preferences)
#  10 Jan 1959
#  Jan 10, 1959
#  10 January 1950
#  January 10, 1959
#  10 JAN 1959
#  JAN 10, 1950
#  10 JANUARY 1950
#  JANUARY 10, 1950

# Sort Dates
# Organized as bits, numbered from the right, origin 0

# SYYYYYYYYYYYYYYMMMMDDDDDD-----YYYYYYYYYYYYYYMMMMDDDDDDFFFFFFFFFF

# num of bits: 1 sign, 14 year, 4 month, 6 day, 5 unused, 14 year, 4 month, 6 day, 10 flag

# S YYYYYYYYYYYYYY MMMM DDDDDD ----- YYYYYYYYYYYYYY MMMM DDDDDD FFFFFFFFFF
# 3 21F987654321E9 8765 4321D9 87654 321C987654321B 9876 54321A 9876543210

# Part 1 (P1) and Part 2 (P2) date,
# P2-M&D=1      0xFFC00                                        11111111110000000000
# P2-Y&M&D =1   0x3FFFFFC00                    001111111111111111111111110000000000
# P1-M&D =1     0x1FF8<<36     0001111111111000000000000000000000000000000000000000

# RMDate '.'  and 'Tanytext' both => RMSortDate 9223372036854775807

# ===================================================DIV60==
def now_RMDate()-> str:
    return to_RMDate(str(date.today()))


# ===================================================DIV60==
def now_RMSortDate()-> int:
    return to_RMSortDate(to_RMDate(str(date.today())))


# ===================================================DIV60==
def to_RMDate(DateStr : str)-> str:
    # ISO date to RMDate str

    # form is Format.LONG, Format.SHORT
    # may want to first implement with strict canonical format and
    # later implement logic found in RM to interpret strings.

    # Take the inout string and parse it with assumed format

    if (len(DateStr) != 10
        or DateStr[4] != '-'
        or DateStr[7] != '-' ):
        raise RMc.RM_Py_Exception("ToRMDate: only YYYY-MM-DD format allowed.")

    YYYY = DateStr[0:4]
    MM = DateStr[5:7]
    DD = DateStr[8:10]

    if ( int(YYYY) < 1
        or int(MM) > 12
        or int(MM) < 1
        or int(DD) > 31
        or int (DD) < 1 ):
        raise RMc.RM_Py_Exception("ToRMDate: integers out of allowed range.")

#            0123   4567   89   A1    23456789B1234
    return  'D.+' + YYYY + MM + DD + '..+00000000..'


# ===================================================DIV60==
def from_RMDate(RMDate : str, form)-> str:
    # RMDate str to English str

    # form is Format.LONG, Format.SHORT

    char_0_1 = RMDate[0:1]
    if char_0_1 == 'T':
        return RMDate[1:]
    elif char_0_1 == 'Q':
        raise Exception("RM Quaker dates not yet supported")
    elif char_0_1 == 'R':
        raise Exception("RM Quarter dates not yet supported")
    elif char_0_1 == '.':
        return ""
    elif char_0_1 == 'D':
        pass  # continue and process D type below
    else:
        raise Exception("Malformed RM Date: unsupported start character")

    # Process D type dates

    if len(RMDate) != 24:
        raise Exception("Malformed RM Date: wrong length")

    if RMDate[11:12] == '/' or  RMDate[22:23] == '/':
        raise Exception("Slash dates not yet supported")

    char_1_2 = RMDate[1:2]
    data_s = RMdate_structure()
    StructCodeE = data_s.get_enum_from_symbol(char_1_2)

    char_2_3 = RMDate[2:3]
    if char_2_3 == '-':
        bc_ad_1 = ' BC'
    elif char_2_3 == '+':
        bc_ad_1 = ''
    else:
        raise Exception("Malformed RM Date: bc_ad_1 indicator")

    try:
        year_1 = (RMDate[3:7]).lstrip("0")
        month_1_i = int(RMDate[7:9])
        day_1 = RMDate[9:11].lstrip("0")
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date 1")

    char_11_12 = RMDate[11:12]
    DoubleDate_1 = False
    if char_11_12 == '/':
        DoubleDate_1 = True
    elif char_11_12 != '.':
        raise Exception("Malformed RM Date: Double Date 1 indicator")

    char_12_13 = RMDate[12:13]
    data_c = RMdate_confidence()
    ConfidenceE_1 = data_c.get_enum_from_symbol(char_12_13)

    char_13_14 = RMDate[13:14]
    if char_13_14 == '-':
        bc_ad_2 = ' BC'
    elif char_13_14 == '+':
        bc_ad_2 = ''
    else:
        raise Exception("Malformed RM Date: bc_ad_2 indicator")

    # must be all 0 if not date range Confidence
    try:
        year_2 = RMDate[14:18].lstrip("0")
        month_2_i = int(RMDate[18:20])
        day_2 = RMDate[20:22].lstrip("0")
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date 1")

    # complicated TODO
    char_22_23 = RMDate[22:23]
    DoubleDate_2 = False
    if char_22_23 == '/':
        DoubleDate_2 = True
    elif char_22_23 != '.':
        raise Exception("Malformed RM Date: Double Date 2 indicator")

    # only if 2nd date
    char_23_24 = RMDate[23:24]
    ConfidenceE_2 = data_c.get_enum_from_symbol(char_23_24)

    single_date = False
    if year_2 == '' and month_2_i == 0 and day_2 == '' and bc_ad_2 == '':
        single_date = True

    if single_date and data_s.get_num_from_enum(StructCodeE) != 1:
        raise Exception(
            "Malformed date: conflict between struct code & second date empty")

    month_trsp_1 = ''  # month's trailing space
    if year_1 != '' and day_1 != '' and month_1_i == 0:
        month_1_i = 13
    if day_1 != '':
        day_1 = day_1 + ' '
    if year_1 == '' or (year_1 != '' and month_1_i == 0):
        month_trsp_1 = ''
    else:
        month_trsp_1 = ' '

    fDate_1 = (data_s.get_str_1(StructCodeE, form) + data_c.get_str(ConfidenceE_1, form)
                + day_1 + NumToMonthStr(month_1_i, form) + month_trsp_1 + year_1 + bc_ad_1)

    month_trsp_2 = ''
    fDate = ''
    if single_date:
        fDate = fDate_1
    else:
        if year_2 != '' and day_2 != '' and month_2_i == 0:
            month_2_i = 13
        if day_2 != '':
            day_2 = day_2 + ' '
        if year_2 == '' or (year_2 != '' and month_2_i == 0):
            month_trsp_2 = ''
        else:
            month_trsp_2 = ' '
        fDate_2 = (data_s.get_str_2(StructCodeE, form) + data_c.get_str(ConfidenceE_2, form)
             + day_2 + NumToMonthStr(month_2_i, form) + month_trsp_2 + year_2 + bc_ad_2)
        fDate = fDate_1 + fDate_2

    return fDate


# ===================================================DIV60==
def to_RMSortDate(RMDate : str)-> int :
    # RMDate is an RM internal date string

    date_type = RMDate[0:1]
    if date_type == 'T':
        #  9223372036854775807    ( 2^63,  sign bit is 0, largest possible signed 64 bit int)
        return 0x7F_FF_FF_FF_FF_FF_FF_FF
    elif date_type == 'Q':
        raise Exception("RM Quaker dates not yet supported")
    elif date_type == 'R':
        raise Exception("RM Quarter dates not yet supported")
    elif date_type == '.':
        #  9223372036854775807    ( 2^63,  sign bit is 0, largest possible signed 64 bit int)
        return 0x7F_FF_FF_FF_FF_FF_FF_FF
    elif date_type == 'D':
        pass  # continue and process D type below
    else:
        raise Exception("Malformed RM Date: unsupported Type character")

    # Process D type dates

    # Julian date / slash date
    date_type_slash_1 = False
    date_type_slash_2 = False
    if  RMDate[11:12]== '/':
        date_type_slash_1 == True
        raise Exception("J-G / Slash dates not yet supported")
    if  RMDate[22:23]== '/':
        date_type_slash_1 == True
        raise Exception("J-G / Slash dates not yet supported")

    try:
        # include +/- sign in year
        year_1 = int(RMDate[2:7])
        month_1 = int(RMDate[7:9])
        day_1 = int(RMDate[9:11])
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date part 1  " + ve)
    try:
        # include +/- sign in year
        year_2 = int(RMDate[13:18])
        month_2 = int(RMDate[18:20])
        day_2 = int(RMDate[20:22])
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date part 2  " + ve)

    Char_1_2 = RMDate[1:2]
    struct_data = RMdate_structure()
    offset = struct_data.get_offset_from_symbol(Char_1_2)


    if year_1 == 0 and ((month_1 != 0) or (day_1 != 0)):
        # year 1 is 0 but either month or day present
        y1 =  0x3F_FF << 49   # a date with no year  16383<<49 = 9,222,809,086,901,354,496
    else:
        # Slash date is in Julian and sort date year must increased by 1
        y1 = (year_1 + 10000 + (1 if date_type_slash_1 else 0)) << 49

    if (offset == (27 + 0xFFC00) and month_1==0 and day_1==0 ):
        offset  = 27
        month_1 = 0xF
        day_1   = 0x3F
        y2      = 0x3FFF << 20
        month_2 = 0xF
        day_2   = 0x3F

    if (offset == (27 + 0xFFC00) and month_1!=0 and day_1==0 ):
        offset  = 27
        # month_1 = 0xF
        day_1   = 0x3F
        y2      = 0x3FFF << 20
        month_2 = 0xF
        day_2   = 0x3F


    if year_2 == 0 and month_2 == 0 and day_2 == 0:
        y2 = 0x3FFF << 20        # 17178820608
    elif year_2 == 0 and ((month_2 != 0) or (day_2 != 0)):
        # year 2 is 0 but either month or day present
        # this step by RJO. Seems to work.TODO test
        y2 = (0x18EF + 10000) << 20
    else:
        y2 = (year_2 + 10000 + (1 if date_type_slash_2 else 0)) << 20
        # correction for julian year by RJO. TODO test

    return     (y1 + (month_1 << 45) + (day_1 << 39)
              + y2 + (month_2 << 16) + (day_2 << 10) + offset)


# ===================================================DIV60==
def from_RMSortDate(sd: int) -> str:
    """
    Inverse of to_RMSortDate(RMDate) for D-type, non-slash RM dates.
    Returns a 24-character RM internal date string.
    """

    # Special case: T / '.' types mapped to max 64-bit
    if sd == 0x7F_FF_FF_FF_FF_FF_FF_FF:
        # You mapped both 'T' and '.' here; we can't distinguish.
        # Choose '.' with completely empty dates.
        return "."

    # ---- Extract packed fields ----
    y1     = (sd >> 49) & 0x7FFF   # 15 bits
    month1 = (sd >> 45) & 0xF      # 4 bits
    day1   = (sd >> 39) & 0x3F     # 6 bits

    y2     = (sd >> 20) & 0x3FFF   # 14 bits
    month2 = (sd >> 16) & 0xF      # 4 bits
    day2   = (sd >> 10) & 0x3F     # 6 bits

    # Offset is stored in low 20 bits (because of 0xFFC00 usage)
    offset_raw = sd & 0xFFFFF

    # ---- Undo special FROM/SINCE/AFT encoding for offset 27 + 0xFFC00 ----
    # In to_RMSortDate you do:
    #   if offset == (27 + 0xFFC00) and month_1==0 and day_1==0:
    #       offset  = 27
    #       month_1 = 0xF
    #       day_1   = 0x3F
    #       y2      = 0x3FFF
    #       month_2 = 0xF
    #       day_2   = 0x3F
    #
    #   if offset == (27 + 0xFFC00) and month_1!=0 and day_1==0:
    #       offset  = 27
    #       day_1   = 0x3F
    #       y2      = 0x3FFF
    #       month_2 = 0xF
    #       day_2   = 0x3F
    #
    # So if we see offset_raw == 27 and y2/month2/day2 == 0x3FFF/0xF/0x3F,
    # we restore the original offset 27 + 0xFFC00.
    if offset_raw == 27 and y2 == 0x3FFF and month2 == 0xF and day2 == 0x3F:
        offset = 27 + 0xFFC00
    else:
        offset = offset_raw

    struct = RMdate_structure()
    symbol = struct.get_symbol_from_offset(offset)
    struct_enum = struct.get_enum_from_symbol(symbol)  # not strictly needed here, but symmetric

    # ---- Decode years (undo +10000 bias and sentinels) ----

    def decode_year_1(y, m, d):
        # You used:
        #   if year_1 == 0 and ((month_1 != 0) or (day_1 != 0)):
        #       y1 = 0x3FFF
        # So if we see y1 == 0x3FFF and month/day non-zero, that means "no year, but month/day present".
        if y == 0x3FFF and (m != 0 or d != 0):
            return 0  # year_1 == 0 in RM string
        # Otherwise normal bias
        return y - 10000

    def decode_year_2(y, m, d):
        # You used:
        #   if year_2 == 0 and month_2 == 0 and day_2 == 0:
        #       y2 = 0x3FFF
        #   elif year_2 == 0 and ((month_2 != 0) or (day_2 != 0)):
        #       y2 = (0x18EF + 10000)
        #
        # So we reverse those:
        if y == 0x3FFF and m == 0 and d == 0:
            return 0  # completely empty second date
        if y == (0x18EF + 10000):
            return 0  # year_2 == 0 but month/day present
        # Otherwise normal bias
        return y - 10000

    year1 = decode_year_1(y1, month1, day1)
    year2 = decode_year_2(y2, month2, day2)

    # ---- Build RM internal date string ----
    # RM format (24 chars):
    #   0:  Type ('D','T','Q','R','.')
    #   1:  Struct symbol
    #   2:  '+' or '-' for year1
    # 3-6:  year1 (4 digits)
    # 7-8:  month1 (2 digits)
    # 9-10: day1 (2 digits)
    # 11:   '.' or '/' (we only support '.')
    # 12:   confidence1 (we'll use '+', since encoder ignores it)
    # 13:   '+' or '-' for year2
    # 14-17: year2 (4 digits)
    # 18-19: month2 (2 digits)
    # 20-21: day2 (2 digits)
    # 22:   '.' or '/' (we only support '.')
    # 23:   confidence2 (we'll use '+')

    def encode_year(y):
        sign = '+' if y >= 0 else '-'
        return sign, f"{abs(y):04d}"

    def encode_md(m, d):
        return f"{m:02d}", f"{d:02d}"

    sign1, year1_str = encode_year(year1)
    m1_str, d1_str = encode_md(month1, day1)

    sign2, year2_str = encode_year(year2)
    m2_str, d2_str = encode_md(month2, day2)

    # We cannot recover original confidence chars; encoder never used them.
    # To be symmetric with your *supported* input, we choose '+' for both.
    conf1 = '.'
    conf2 = '.'

    rm = (
        "D" +          # type
        symbol +       # struct symbol
        sign1 +
        year1_str +
        m1_str +
        d1_str +
        "." +          # no slash support
        conf2 +
        sign2 +
        year2_str +
        m2_str +
        d2_str +
        "." +          # no slash support
        conf2
    )

    return rm


# ===================================================DIV60==
class StructCode(enum.IntEnum):
    NORM = 1
    AFT = 2
    BEF = 3
    FROM = 4
    SINC = 5
    TO = 6
    UNTL = 7
    BY = 8
    OR = 9
    BTWN = 10
    FRTO = 11
    DASH = 12

# ===================================================DIV60==
class RMdate_structure:

    _data = (
        #  fmt: off
        #          0          1      2              3    4         5           6        7
        #          enum       sym    offset         num  1stShort  1stLong     2ndShort 2ndLong
        ( StructCode.NORM,    '.',   12,            1,   '',       '',         '',      ''     ),
        ( StructCode.AFT,     'A',   31 + 0xFFC00,  1,   'aft ',   'after ',   '',      ''     ),
        ( StructCode.BEF,     'B',   0,             1,   'bef ',   'before ',  '',      ''     ),
        ( StructCode.FROM,    'F',   27 + 0xFFC00,  1,   'from ',  'from ',    '',      ''     ),
        ( StructCode.SINC,    'I',   30 + 0xFFC00,  1,   'since ', 'since ',   '',      ''     ),
        ( StructCode.TO,      'T',   6,             1,   'to ',    'to ',      '',      ''     ),
        ( StructCode.UNTL,    'U',   9,             1,   'until ', 'until ',   '',      ''     ),
        ( StructCode.BY,      'Y',   3,             1,   'by ',    'by ',      '',      ''     ),
        ( StructCode.OR,      'O',   24,            2,   '',       '',         ' or ',  ' or ' ),
        ( StructCode.BTWN,    'R',   15,            2,   'bet ',   'between ', ' and ', ' and '),
        ( StructCode.FRTO,    'S',   18,            2,   'from ',  'from ',    ' to ',  ' to ' ),
        ( StructCode.DASH,    '-',   21,            2,   '',       '',         '–',     '–'    )
        # fmt: on
    )
# Sort order  TODO
# F FROM  = 1047579 = (27 + xFFC00)
# I SINCE = 1047582 = (30 + xFFC00)
# A AFTER = 1047583 = (31 + xFFC00)

    def get_num_from_enum(self, enum : StructCode)-> int:
        for date_type in RMdate_structure._data:
            if enum == date_type[0]:
                return date_type[3]
        raise Exception(
            "Malformed RM Date: unsupported StructCode: " + str(enum))

    def get_enum_from_symbol(self, symbol : str)-> int:
        for date_type in RMdate_structure._data:
            if symbol == date_type[1]:
                return date_type[0]
        raise Exception(
            "Malformed RM Date: unsupported symbol: " + symbol)

    def get_offset_from_symbol(self, symbol : str)-> int:
        for date_type in RMdate_structure._data:
            if symbol == date_type[1]:
                return date_type[2]
        raise Exception(
            "Malformed RM Date: unsupported character: " + symbol)

    def get_symbol_from_offset(self, offset : int)-> str:
        for date_type in RMdate_structure._data:
            if offset == date_type[2]:
                return date_type[1]
        raise Exception(
            "Malformed RM Date: unsupported offset: " + offset)

    def get_str_1(self, type, format : Format)-> str:
        for date_type in RMdate_structure._data:
            if type == date_type[0]:
                if format == Format.SHORT:
                    return date_type[4]
                elif format == Format.LONG:
                    return date_type[5]
                else:
                    raise Exception("Format not supported")
        raise Exception(
            "Malformed RM Date: StructCode character, no offset available")

    def get_str_2(self, type, format)-> str:
        for date_type in RMdate_structure._data:
            if type == date_type[0]:
                if format == Format.SHORT:
                    return date_type[6]
                elif format == Format.LONG:
                    return date_type[7]
                else:
                    raise Exception("Format not supported")
        raise Exception(
            "Malformed RM Date: StructCode character, no offset available")

 # ===================================================DIV60==
class ConfidenceCode(enum.IntEnum):
    NONE = 1
    ABT = 2
    SAY = 3
    CIR = 4
    EST = 5
    CAL = 6
    MAY = 7
    PER = 8
    APAR = 9
    LKLY = 10
    POSS = 11
    PROB = 12
    CERT = 13


# ===================================================DIV60==
class RMdate_confidence:

    _data = (
        # fmt: off
        #                0        1       2              3
        #                enum     sym     short          long
        ( ConfidenceCode.NONE,    '.',    "",            ""           ),
        ( ConfidenceCode.ABT,     'A',    "abt ",        "about "     ),
        ( ConfidenceCode.SAY,     'S',    "say ",        "say "       ),
        ( ConfidenceCode.CIR,     'C',    "ca ",         "circa "     ),
        ( ConfidenceCode.EST,     'E',    "est ",        "estimated " ),
        ( ConfidenceCode.CAL,     'L',    "calc ",       "calculated "),
        ( ConfidenceCode.MAY,     '?'   , "maybe ",      "maybe "     ),
        ( ConfidenceCode.PER,     '1',    "perhaps ",    "perhaps "   ),
        ( ConfidenceCode.APAR,    '2',    "apparently ", "apparently "),
        ( ConfidenceCode.LKLY,    '3',    "likely ",     "likely "    ),
        ( ConfidenceCode.POSS,    '4',    "poss ",       "possibly "  ),
        ( ConfidenceCode.PROB,    '5',    "prob ",       "probably "  ),
        ( ConfidenceCode.CERT,    '6',    "cert ",       "certainly " )
        # fmt: on
    )

    def get_enum_from_symbol(self, symbol : str)-> int:
        for date_type in RMdate_confidence._data:
            if symbol == date_type[1]:
                return date_type[0]
        raise Exception("Malformed RM Date: Confidence character unknown")

    def get_str(self, type, format : Format)-> str:
        for date_type in RMdate_confidence._data:
            if type == date_type[0]:
                if format == Format.SHORT:
                    return date_type[2]
                elif format == Format.LONG:
                    return date_type[3]
                else:
                    raise Exception("Format not supported")
        raise Exception("Confidence enum not supported")


# ===================================================DIV60==
class Direction(enum.IntEnum):
    FROM_RM = 1
    TO_RM = 2


# ===================================================DIV60==
class Format(enum.IntEnum):
    SHORT = 1
    LONG = 2


# ===================================================DIV60==
def NumToMonthStr(MonthNum : int, style : Format)-> str:
    if MonthNum < 0 or MonthNum > 13:
        raise Exception("Month number out of range")
    if style == Format.LONG:
        index=1
    elif style == Format.SHORT:
        index=0
    else:
        raise Exception("style not supported")

   # Items must appear in this order
    Months = (
        ('',   ''),
        ('Jan',  "January"),
        ('Feb',  "February"),
        ('Mar',  "March"),
        ('Apr',  "April"),
        ('May',  "May"),
        ('Jun',  "June"),
        ('Jul',  "July"),
        ('Aug',  "August"),
        ('Sep',  "September"),
        ('Oct',  "October"),
        ('Nov',  "November"),
        ('Dec',  "December"),
        ('???',  "???")
    )
    return Months[MonthNum][index]

# ===================================================DIV60==
