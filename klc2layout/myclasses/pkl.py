# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:49:35 2019

@author: marks
"""
import os
import codecs
from unicodedata import normalize
import time
from  .myconst.ctrl import ctrl, combiningChars
from  .myconst.pstates import pstates

controls = {'BACKSPACE' : '<-×', \
	'TAB' : '|<=>|', \
	'CAPSLOCK' : '∏', \
	'CAPSLOCK_' : '‗∏‗', \
	'ENTER' : '<==', \
	'LSHIFT' : '∆', \
	'LSHIFT_' : '‗∆‗', \
	'RSHIFT' : '∆', \
	'RSHIFT_' : '‗∆‗', \
	'LCTRL' : 'Ctrl', \
	'LCTRL_' : 'C\u0333T\u0333R\u0333L\u0333', \
	'LALT' : 'Alt', \
	'LALT_' : 'A\u0333L\u0333T\u0333', \
	'RALT' : 'AltGr', \
	'RALT_' : 'A\u0333L\u0333T\u0333G\u0333R\u0333', \
	'RCTRL' : 'Ctrl', \
	'RCTRL_' : 'C\u0333T\u0333R\u0333L\u0333'}

def write_ini(klc, row, spklDir, mode="NFC"):
        #create folder under spklDir/layouts
        thislayout = os.path.normpath('{}/layouts/{}'.format(spklDir, row[0][:-4]))
        os.makedirs(thislayout, exist_ok=True)
        fileout = '{}/{}.ini'.format(thislayout, mode)
        print(fileout)
        pkl_file = codecs.open(fileout, mode='w',encoding='utf-8')
        pkl_file.write( '\n'.join([codecs.BOM_UTF8.decode() + ";",\
            "; Keyboard Layout definition for",\
            "; Senegal Portable Keyboard Layout",\
            "; http://www.silsenegal.org/",\
            ";",\
            "" ,\
            "[information]", \
            "layoutname           = " + klc.klc["KBD"][1] + "-" + mode, \
            "layoutcode           = " + klc.klc["KBD"][0] + mode, \
            "localeid             = " + klc.klc["LOCALEID"], \
            "copyright            = " + klc.klc["COPYRIGHT"].rstrip('"'), \
            "company              = " + klc.klc["COMPANY"].rstrip('"'), \
            "homepage             = http://www.silsenegal.org/", \
            "version              = " +  klc.klc["VERSION"], \
            "", \
            "generated_at         = " + time.asctime(), \
            "generated_from       = " + row[0], \
            "modified_after_generate = no", \
            "", \
            "", \
            "[global]", \
            "; extend_key = CapsLock", \
            "shiftstates = " + ":".join(klc.klc["SHIFTSTATE"]), \
            "FontSize = 12", \
            "FontName = {0}  ; This can be blank to use the system's default font.".format(row[3]), \
            "FontStyle = Regular    ; Example of an alternatives: Bold,  Italic, Underline", \
            "KeySize = 3", \
            "", \
            "[layout]", \
            ";scan = VK	CapStat	0Norm	1Sh	2Ctrl	3CtrlSh	6AGr	7AGrSh	8SGCaps	9SGCapsSh", \
            ""]))
        for item in klc.spkl:
#            print( item )
#            print("\t".join([" = ".join(item[0:2]),str(item[2]),normalize(mode, "\t".join(item[3:])),";"]))
            pkl_file.write( "\t".join([" = ".join(item[0:2]),str(item[2]),normalize(mode, "\t".join(item[3:])),";"]) + '\n' )
            if item[0] in klc.map102a:
                pos = klc.map102a[item[0]]
                pstate = 0
                for pchar in item[3:]:
                    temp = ''
                    if pchar[0:2] == 'dk':
                        dknum = int(pchar[2:]) - 1
                        temp = '(' + chr(klc.deadkeysList[dknum][0][1][0]) + ')'
                    elif ord(pchar[0]) in ctrl:
                        temp = ctrl[ord(pchar[0])]
                    else:
                        for arange in combiningChars:
                            if (ord(pchar[0]) in arange):
                                temp ='\u25cc' + pchar
                    if temp == '':
                        temp = pchar
                    pstates[pstate][pos[0]][pos[1]] = temp
                    pstate = pstate + 1
        pkl_file.write( '\n'.join(["", ""] ))
        pkl_file.write( '\n'.join(["[controls]", \
            "SC00e = BACKSPACE\t0\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t;".format(**controls), \
            "SC00f = TAB\t0\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t;".format(**controls), \
            "SC03a = CAPSLOCK\t0\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK_}\t%{CAPSLOCK_}\t;".format(**controls), \
            "SC01c = ENTER\t0\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t;".format(**controls), \
            "SC02a = LSHIFT\t0\t%{LSHIFT}\t%{LSHIFT_}\t%{LSHIFT}\t%{LSHIFT_}\t%{LSHIFT}\t%{LSHIFT_}\t%{LSHIFT}\t%{LSHIFT_}\t%{LSHIFT}\t%{LSHIFT_}\t;".format(**controls), \
            "SC036 = RSHIFT\t0\t%{RSHIFT}\t%{RSHIFT_}\t%{RSHIFT}\t%{RSHIFT_}\t%{RSHIFT}\t%{RSHIFT_}\t%{RSHIFT}\t%{RSHIFT_}\t%{RSHIFT}\t%{RSHIFT_}\t;".format(**controls), \
            "SC01d = LCTRL\t0\t%{LCTRL}\t%{LCTRL}\t%{LCTRL_}\t%{LCTRL_}\t%{LCTRL}\t%{LCTRL}\t%{LCTRL_}\t%{LCTRL_}\t;".format(**controls), \
            "SC038 = LALT\t0\t%{LALT}\t%{LALT}\t%{LALT}\t%{LALT}\t%{LALT_}\t%{LALT_}\t%{LALT_}\t%{LALT_}\t;".format(**controls), \
            "SCe038 = RALT\t0\t%{RALT}\t%{RALT}\t%{RALT}\t%{RALT}\t%{RALT_}\t%{RALT_}\t%{RALT_}\t%{RALT_}\t;".format(**controls), \
            "SCe01d = RCTRL\t0\t%{RCTRL}\t%{RCTRL}\t%{RCTRL_}\t%{RCTRL_}\t%{RCTRL}\t%{RCTRL}\t%{RCTRL_}\t%{RCTRL_}\t;".format(**controls), \
            "", "", ""] ))

        dknum = 0
    #    print(klc.deadkeysList)
        for deadkeys in klc.deadkeysList :
            dknum = dknum + 1
            pkl_file.write( "\n" )
            pkl_file.write( "\n" )
            pkl_file.write( "[deadkey%s]\n" % dknum)
            for deadkey in deadkeys:
                n = ""
                #print(deadkey)
                if mode == "NFC":
                    for j in range(0,len(deadkey[1])):
                        if len(n) > 0:
                            n = "{0},{1}".format(n,deadkey[1][j])
                        else:
                            n = str(deadkey[1][j])
                else:#is NFD
                    for j in range(0,len(deadkey[1])):
                        if len(n) > 0:
                            nfd = normalize("NFD",chr(deadkey[1][j]))
    
                            for nchar in nfd:
                                n = "{0},{1}".format(n, str(ord(nchar)))
                        else:
                            nfd = normalize("NFD",chr(deadkey[1][j]))
                            for nchar in nfd:
                                if len(n)>0:
                                    n = "{0},{1}".format(n, str(ord(nchar)))
                                else:
                                    n = str(ord(nchar))
                pkl_file.write("{0}\t=\t{1}\t{2}\t;\n".format(deadkey[0],n,deadkey[2]))



        pkl_file.write( "\n\n\n" )
        pkl_file.close()
        
        
#        #fileout = fileout + "\layout.ini", forces NFD
#        fileout = filein[:-4] + "NFD.ini"
#        print(fileout)
#
#        pkl_file = codecs.open(fileout, mode='w',encoding='utf-8')
#        pkl_file.write( '\n'.join([codecs.BOM_UTF8.decode() + ";",\
#            "; Keyboard Layout definition for",\
#            "; Senegal Portable Keyboard Layout",\
#            "; http://www.silsenegal.org/",\
#            ";",\
#            "" ,\
#            "[information]", \
#            "layoutname           = " + klc.klc["KBD"][1] + "-NFD", \
#            "layoutcode           = " + klc.klc["KBD"][0] + "NFD", \
#            "localeid             = " + klc.klc["LOCALEID"], \
#            "copyright            = " + klc.klc["COPYRIGHT"].rstrip('"'), \
#            "company              = " + klc.klc["COMPANY"].rstrip('"'), \
#            "homepage             = http://www.silsenegal.org/", \
#            "version              = " +  klc.klc["VERSION"], \
#            "", \
#            "generated_at         = " + time.asctime(), \
#            "generated_from       = " + filein, \
#            "modified_after_generate = no", \
#            "", \
#            "", \
#            "[global]", \
#            "; extend_key = CapsLock", \
#            "shiftstates = " + ":".join(klc.klc["SHIFTSTATE"]), \
#            "FontSize = 12", \
#            "FontName = {0}  ; This can be blank to use the system's default font.".format(fontIn), \
#            "FontStyle = Regular    ; Example of an alternatives: Bold,  Italic, Underline", \
#            "KeySize = 3", \
#            "", \
#            "[layout]", \
#            ";scan = VK	CapStat	0Norm	1Sh	2Ctrl	3CtrlSh	6AGr	7AGrSh	8SGCaps	9SGCapsSh", \
#            ""]))
#        for item in klc.spkl:
#            pkl_file.write( "\t".join([" = ".join(item[0:2]),str(item[2]),normalize("NFD", "\t".join(item[3:])),";"]) + '\n' )
#            if item[0] in klc.map102a:
#                pos = klc.map102a[item[0]]
#                pstate = 0
#                for pchar in item[3:]:
#                    temp = ''
#                    if pchar[0:2] == 'dk':
#                        dknum = int(pchar[2:]) - 1
#                        temp = '(' + chr(klc.deadkeysList[dknum][0][1][0]) + ')'
#                    elif ord(pchar[0]) in ctrl.ctrl:
#                        temp = ctrl.ctrl[ord(pchar[0])]
#                    else:
#                        for arange in ctrl.combiningChars:
#                            if (ord(pchar[0]) in arange):
#                                temp ='\u25cc' + pchar
#                    if temp == '':
#                        temp = pchar
#                    pstates[pstate][pos[0]][pos[1]] = temp
#                    pstate = pstate + 1
#        pkl_file.write( '\n'.join(["", ""] ))
#        pkl_file.write( '\n'.join(["[controls]", \
#            "SC00e = BACKSPACE\t0\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t%{BACKSPACE}\t;".format(**controls.controls), \
#            "SC00f = TAB\t0\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t%{TAB}\t;".format(**controls.controls), \
#            "SC03a = CAPSLOCK\t0\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK}\t%{CAPSLOCK_}\t%{CAPSLOCK_}\t;".format(**controls.controls), \
#            "SC01c = ENTER\t0\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t%{ENTER}\t;".format(**controls.controls), \
#            "SC02a = LSHIFT\t0\t%{LSHIFT}\t%{LSHIFT_}\t%{LSHIFT}\t%{LSHIFT_}\t%{LSHIFT}\t%{LSHIFT_}\t%{LSHIFT}\t%{LSHIFT_}\t%{LSHIFT}\t%{LSHIFT_}\t;".format(**controls.controls), \
#            "SC036 = RSHIFT\t0\t%{RSHIFT}\t%{RSHIFT_}\t%{RSHIFT}\t%{RSHIFT_}\t%{RSHIFT}\t%{RSHIFT_}\t%{RSHIFT}\t%{RSHIFT_}\t%{RSHIFT}\t%{RSHIFT_}\t;".format(**controls.controls), \
#            "SC01d = LCTRL\t0\t%{LCTRL}\t%{LCTRL}\t%{LCTRL_}\t%{LCTRL_}\t%{LCTRL}\t%{LCTRL}\t%{LCTRL_}\t%{LCTRL_}\t;".format(**controls.controls), \
#            "SC038 = LALT\t0\t%{LALT}\t%{LALT}\t%{LALT}\t%{LALT}\t%{LALT_}\t%{LALT_}\t%{LALT_}\t%{LALT_}\t;".format(**controls.controls), \
#            "SCe038 = RALT\t0\t%{RALT}\t%{RALT}\t%{RALT}\t%{RALT}\t%{RALT_}\t%{RALT_}\t%{RALT_}\t%{RALT_}\t;".format(**controls.controls), \
#            "SCe01d = RCTRL\t0\t%{RCTRL}\t%{RCTRL}\t%{RCTRL_}\t%{RCTRL_}\t%{RCTRL}\t%{RCTRL}\t%{RCTRL_}\t%{RCTRL_}\t;".format(**controls.controls), \
#            "", "", ""] ))
#
#        dknum = 0
#        for deadkeys in klc.deadkeysList :
#            dknum = dknum + 1
#            pkl_file.write( "\n" )
#            pkl_file.write( "\n" )
#            pkl_file.write( "[deadkey%s]\n" % dknum)
#            for deadkey in deadkeys:
#                n = ""
#                deadkey[2] = normalize("NFD", deadkey[2])
#                if (len(deadkey[2]) != len(deadkey[1])) and (deadkey[2][0] != chr(0x25CC)):
#                    deadkey[1] = []
#                    for achar in deadkey[2]:
#                        deadkey[1].append(ord(achar))
#                for j in range(0,len(deadkey[1])):
#                    if len(n) > 0:
#                        nfd = normalize("NFD",chr(deadkey[1][j]))
#
#                        for nchar in nfd:
#                            n = "{0},{1}".format(n, str(ord(nchar)))
#                    else:
#                        nfd = normalize("NFD",chr(deadkey[1][j]))
#                        for nchar in nfd:
#                            if len(n)>0:
#                                n = "{0},{1}".format(n, str(ord(nchar)))
#                            else:
#                                n = str(ord(nchar))
#                dkv["{0}_{1}".format(dknum, deadkey[0]) ] = [deadkey[1],deadkey[2]]
#
#
#
#        pkl_file.write( "\n\n\n" )
#        pkl_file.close()
