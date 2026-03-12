import sys
from pathlib import Path
#sys.path.append( r'..\RMPy package' )

import common as RMc  # type: ignore

from enum import Enum
from datetime import date

class StructCode(Enum):
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

    def get_num_from_enum(self, enum):
        for date_type in RMdate_structure._data:
            if enum == date_type[0]:
                return date_type[3]
        raise Exception(
            "Malformed RM Date: unsupported StructCode: " + str(enum))

    def get_enum_from_symbol(self, symbol):
        for date_type in RMdate_structure._data:
            if symbol == date_type[1]:
                return date_type[0]
        raise Exception(
            "Malformed RM Date: unsupported symbol: " + symbol)

    def get_offset_from_symbol(self, symbol):
        for date_type in RMdate_structure._data:
            if symbol == date_type[1]:
                return date_type[2]
        raise Exception(
            "Malformed RM Date: unsupported character: " + symbol)

    def get_symbol_from_offset(self, offset):
        for date_type in RMdate_structure._data:
            if offset == date_type[2]:
                return date_type[1]
        raise Exception(
            "Malformed RM Date: unsupported offset: " + offset)

    def get_str_1(self, type, format):
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

    def get_str_2(self, type, format):
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




class RM_date():

    
    def __init__(self, RM_date_str):
        self.RM_date_str = RM_date_str

    @classmethod
    def from_str(cls, RM_date_str : str) -> RM_date:

        # initial validity check
        if len(RM_date_str) != 24:
            raise Exception("Malformed RM Date: wrong length")

        self.__rd_type = RM_date_str[0:1]
        if self.__rd_type not in "D.TQR":
            raise Exception("Malformed RM Date: unsupported start character")
        

        data_s = RMdate_structure()
        self.__rd_struct =  data_s.get_enum_from_symbol(RM_date_str[1:2])

        # if self.__rd_type in "DQR"  and structure requires 1 part date  test for p2 all standard '+00000000..'

        slash1 = RM_date_str[11:12] == '/'
        slash2 = RM_date_str[22:23] == '/'
        if slash1 and slash2:
            self.__rd_JG_slash = True
        else:
             self.__rd_JG_slash = False
             if slash1 or slash2:
                raise Exception("Malformed slash date")


        p1_BCAD = RM_date_str[2:3]
        if p1_BCAD == '+':
            self.__rd_p1_CE = True
        elif p1_BCAD == '-':
            self.__rd_p1_CE = False
        else:
            raise Exception("Malformed RM Date: date part 1 BC/AD indicator")
        
        try:
            self.__rd_p1_YYYY = (RM_date_str[3:7]).lstrip("0")
            self.__rd_p1_MM = int(RM_date_str[7:9])
            self.__rd_p1_DD = RM_date_str[9:11].lstrip("0")
        except ValueError as ve:
            raise Exception("Malformed RM Date: Invalid characters in date 1")

        char_11_12 = RM_date_str[11:12]
        DoubleDate_1 = False
        if char_11_12 == '/':
            DoubleDate_1 = True
        elif char_11_12 != '.':
            raise Exception("Malformed RM Date: Double Date 1 indicator")

        char_12_13 = RMDate[12:13]
        data_c = RMdate_confidence()
        ConfidenceE_1 = data_c.get_enum_from_symbol(char_12_13)



        self.__rd_p1_YYYY
        self.__rd_p1_MM
        self.__rd_p1_DD
        self.__rd_p1_confidence


        p2_BCAD = RMDate[2:3]
        if p2_BCAD == '+':
            self.__rd_pw_CE = True
        elif p2_BCAD == '-':
            self.__rd_pw_CE = False
        else:
            raise Exception("Malformed RM Date: date part 2 BC/AD indicator")

        self.__rd_p2_YYYY
        self.__rd_p2_MM
        self.__rd_p2_DD
        self.__rd_p2_confidence


        # What is currently supported?
        if self.__rd_JG_slash:
            raise Exception("Slash dates not yet supported")
        return cls( )

mine = RM_date('D-+19450023..+00010000..')

pass
