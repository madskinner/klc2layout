# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 04:02:23 2017

@author: marks
"""
import re

THIS_VERSION = '0.1.1'
KTL_VERSION = '0.0.1'


#klctree holds a list of lists
# of ["file","onpng",'"offpng","font","id","header":""]
PRJ_JSON = '{"currentSrcDir":"", "klctree":[], "spklDir":"~/spkl", ' +\
                '"kmflDir":"~/dotkmfl", "macDir":"~/mac", "keymanDir":""}'

STORE_AND = r"^store\(&(.+?)\)\s'(.+?)'$"
KEYSTROKE = r"^\+\s\[(.+?)\]\s>\s(.+?)$"
MODIFIER = r"^U\+(.+?)\s\+\s\[(.+?)\]\s?>\s(.+?)$"
LOOKUP = {'NBSP':'U+00A0', 'NNBSP':'U+202F', 'ESC':'U+001B', 'FS':'U+001C', \
          'GS':'U+001D', 'RLM':'U+200F', 'LRM':'U+200E', 'LRE':'U+202A', \
          'PDF':'U+202C', 'ZWJ':'U+200d', 'ZWNJ':'U+200c'}
REVERSE = {'U+001B':'ESCAPE', 'U+001C':'INFORMATION SEPARATOR FOUR', 'U+001D':'INFORMATION SEPARATOR THREE'}

DEVICE_PNGS = ["default", "shift", "numeric", "indic", "symbol", "symbols", "other", "others"]
STATE = {
            0: "default",
            1: "shift",
            2: "ctrl",
            3: "shift-ctrl",
            4: "alt",
            5: "shift-alt",
            6: "ctrl-alt",
            7: "shift-ctrl-alt"}