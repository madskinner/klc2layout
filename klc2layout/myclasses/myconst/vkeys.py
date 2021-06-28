# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 17:56:32 2021

@author: Mark Skinner
"""
#width of each each key - for desktop
VKEYS = {
		"1": {\
			"K_BKQUOTE": 40, \
			"K_1": 40, \
			"K_2": 40, \
			"K_3": 40, \
			"K_4": 40, \
			"K_5": 40, \
			"K_6": 40, \
			"K_7": 40, \
			"K_8": 40, \
			"K_9": 40, \
			"K_0": 40, \
			"K_HYPHEN": 40, \
			"K_EQUAL": 40, \
			"K_BKSP": 72, \
			},\
		"2": {\
			"K_TAB": 62, \
			"K_Q": 40, \
			"K_W": 40, \
			"K_E": 40, \
			"K_R": 40, \
			"K_T": 40, \
			"K_Y": 40, \
			"K_U": 40, \
			"K_I": 40, \
			"K_O": 40, \
			"K_P": 40, \
			"K_LBRKT": 40, \
			"K_RBRKT": 40, \
			"K_BKSLASH": 50, \
			},\
		"3": {\
			"K_CAPS": 69, \
			"K_A": 40, \
			"K_S": 40, \
			"K_D": 40, \
			"K_F": 40, \
			"K_G": 40, \
			"K_H": 40, \
			"K_J": 40, \
			"K_K": 40, \
			"K_L": 40, \
			"K_COLON": 40, \
			"K_QUOTE": 40, \
			"K_ENTER": 85, \
			},\
		"4": {\
			"K_LSHIFT":	42, \
			"K_oE2": 40, \
			"K_Z": 40, \
			"K_X": 40, \
			"K_C": 40, \
			"K_V": 40, \
			"K_B": 40, \
			"K_N": 40, \
			"K_M": 40, \
			"K_COMMA": 40, \
			"K_PERIOD": 40, \
			"K_SLASH": 40, \
			"K_RSHIFT": 112, \
			},\
		"5": {\
			"K_LCTRL": 82, \
			"K_LALT": 82, \
			"K_SPACE": 282, \
			"K_RALT": 82, \
			"K_RCTRL": 82, \
			}\
		}

#Caps and shift Caps not supported
STATES = {\
            "default":0, \
            "":0, \
            "S":1, \
            "C":2, \
            "SC":3, \
            "A":4, \
            "SA":5, \
            "CA":6, \
            "SCA":7\
         }