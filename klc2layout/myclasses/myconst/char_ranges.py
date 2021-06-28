# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:02:29 2021

@author: Mark Skinner
"""
from itertools import chain

HEBREW = set(chain(range(0x0590, 0x600), \
               range(0xFB1D, 0xFB4F), \
               range(0xFD3E, 0xFD40)))

AJAMI = set(chain(range(0x0600, 0x0700), \
              range(0x0750, 0x0780), \
              range(0x08A0, 0x0900)))

GREEK = set(chain(range(0x0370, 0x0400), \
              range(0x1F00, 0x2000)))

CONTROLCHARS = {
                'U+0000': 'NULL',
                'U+0001': 'START OF HEADING',
                'U+0002': 'START OF TEXT',
                'U+0003': 'END OF TEXT',
                'U+0004': 'END OF TRANSMISSION',
                'U+0005': 'ENQUIRY',
                'U+0006': 'ACKNOWLEDGE',
                'U+0007': 'BELL',
                'U+0008': 'BACKSPACE',
                'U+0009': 'CHARACTER TABULATION',
                'U+000A': 'LINE FEED',
                'U+000B': 'LINE TABULATION',
                'U+000C': 'FORM FEED',
                'U+000D': 'CARRIAGE RETURN',
                'U+000E': 'SHIFT OUT',
                'U+000F': 'SHIFT IN',
                'U+0010': 'DATA LINK ESCAPE',
                'U+0011': 'DEVICE CONTROL ONE',
                'U+0012': 'DEVICE CONTROL TWO',
                'U+0013': 'DEVICE CONTROL THREE',
                'U+0014': 'DEVICE CONTROL FOUR',
                'U+0015': 'NEGATIVE ACKNOWLEDGE',
                'U+0016': 'SYNCHRONUS IDLE',
                'U+0017': 'END OF TRANSMISSION BLOCK',
                'U+0018': 'CANCEL',
                'U+0019': 'END OF MEDIUM',
                'U+001A': 'SUBSTITUTE',
                'U+001B': "ESCAPE",
                'U+001C': 'INFORMATION SEPARATOR FOUR',
                'U+001D': 'INFORMATION SEPARATOR THREE',
                'U+001E': 'INFORMATION SEPARATOR TWO',
                'U+001F': 'INFORMATION SEPARATOR ONE'
                }

PLACEHOLDERS = {
                'NUL': 'U+0000',
                'SOH': 'U+0001',
                'STX': 'U+0002',
                'ETX': 'U+0003',
                'EOT': 'U+0004',
                'ENQ': 'U+0005',
                'ACK': 'U+0006',
                'BEL': 'U+0007',
                'BS': 'U+0008',
                'HT': 'U+0009',
                'LF': 'U+000A',
                'VT': 'U+000B',
                'FF': 'U+000C',
                'CR': 'U+000D',
                'SO': 'U+000E',
                'SI': 'U+000F',
                'DLE': 'U+0010',
                'DC1': 'U+0011',
                'DC2': 'U+0012',
                'DC3': 'U+0013',
                'DC4': 'U+0014',
                'NAK': 'U+0015',
                'SYN': 'U+0016',
                'ETB': 'U+0017',
                'CAN': 'U+0018',
                'EM': 'U+0019',
                'SUB': 'U+001A',
                'ESC': 'U+001B',
                'FS': 'U+001C',
                'GS': 'U+001D',
                'RS': 'U+001E',
                'US': 'U+001F',
                'NBSP': 'U+00A0',
                'NQSP': 'U+2000',
                'MQSP': 'U+2001',
                'ENSP': 'U+2002',
                'EMSP': 'U+2003',
                '3/MSP': 'U+2004',
                '4/MSP': 'U+2005',
                '6/MSP': 'U+2006',
                'FSP': 'U+2007',
                'PSP': 'U+2008',
                'THSP': 'U+2009',
                'HSP': 'U+200A',
                'ZWSP': 'U+200B',
                'ZWNJ': 'U+200C',
                'ZWJ': 'U+200D',
                'LRM': 'U+200E',
                'RLM': 'U+200F',
                'NB-': 'U+2011',
                'LSEP': 'U+2028',
                'PSEP': 'U+2009',
                'LRE': 'U+202A',
                'RLE': 'U+200B',
                'PDF': 'U+202C',
                'LRO': 'U+202D',
                'RLO': 'U+202E',
                'NNBSP': 'U+202F',
                'WJ': 'U+2060'
                }
