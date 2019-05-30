#-------------------------------------------------------------------------------
# Name:        kmn
# Purpose:  output 'kmn' keyman version 6 non-mneumonic version of klc file.
#
# Author:      marks
#
# Created:     09/01/2013
# Copyright:   (c) marks 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
#import klc
from unicodedata import normalize


ScanCode = {0x02:"K_1",\
	0x03:"K_2",\
	0x04:"K_3",\
	0x05:"K_4",\
	0x06:"K_5",\
	0x07:"K_6",\
	0x08:"K_7",\
	0x09:"K_8",\
	0x0a:"K_9",\
	0x0b:"K_0",\
	0x0c:"K_HYPHEN",\
	0x0d:"K_EQUAL",\
	0x10:"K_Q",\
	0x11:"K_W",\
	0x12:"K_E",\
	0x13:"K_R",\
	0x14:"K_T",\
	0x15:"K_Y",\
	0x16:"K_U",\
	0x17:"K_I",\
	0x18:"K_O",\
	0x19:"K_P",\
	0x1a:"K_LBRKT",\
	0x1b:"K_RBRKT",\
	0x1e:"K_A",\
	0x1f:"K_S",\
	0x20:"K_D",\
	0x21:"K_F",\
	0x22:"K_G",\
	0x23:"K_H",\
	0x24:"K_J",\
	0x25:"K_K",\
	0x26:"K_L",\
	0x27:"K_COLON",\
	0x28:"K_QUOTE",\
	0x29:"K_BKQUOTE",\
	0x2b:"K_BKSLASH",\
	0x2c:"K_Z",\
	0x2d:"K_X",\
	0x2e:"K_C",\
	0x2f:"K_V",\
	0x30:"K_B",\
	0x31:"K_N",\
	0x32:"K_M",\
	0x33:"K_COMMA",\
	0x34:"K_PERIOD",\
	0x35:"K_SLASH",\
	0x39:"K_SPACE",\
	0x56:"K_oE2",\
	0x53:"K_NPDOT",\
    0x73:"K_ABNT_C1",
    0x7e:"K_ABNT_C2"}

modifier = ["", \
    "SHIFT ", \
    "CTRL ", \
    "CTRL SHIFT ", \
    "ALT ", \
    "ALT SHIFT ", \
    "ALT CTRL ", \
    "ALT CTRL SHIFT ",\
    "CAPS ",\
    "CAPS SHIFT "]

Nmodifier = ["NCAPS ", \
    "NCAPS SHIFT ", \
    "NCAPS CTRL ", \
    "NCAPS CTRL SHIFT ", \
    "NCAPS ALT ", \
    "NCAPS ALT SHIFT ", \
    "NCAPS ALT CTRL ", \
    "NCAPS ALT CTRL SHIFT ",\
    "CAPS ",\
    "CAPS SHIFT "]

def kmn_it(klc, kmn_file, iconIn, _normalization="NFC"):
    dko = {}
    if "DESCRIPTIONS" in klc.klc:
        if len(klc.klc["DESCRIPTIONS"][0]) == 0:
            klc.klc["DESCRIPTIONS"][0]=["", ]
    else:
        klc.klc["DESCRIPTIONS"]= ["",]

    kmn_file.write( '\n'.join([\
        "NAME\t\"" + klc.klc["KBD"][1] + "\"",\
        "COPYRIGHT\t\"" + klc.klc["COPYRIGHT"] + "\"",\
    	"BITMAP {0}".format(iconIn),\
        "VERSION 6.0",\
        'MESSAGE\t"{0}"'.format(str(klc.klc["DESCRIPTIONS"][0])),\
        "",\
        'store(&mnemoniclayout) "0" ',\
        "",\
        "begin Unicode > use(Main)",\
        "",\
        "group(Main) using keys",\
        "", \
        "c setup deadkeys", "\n"]))

    dknum = 0
    for deadkeys in klc.deadkeysList :
        dknum = dknum + 1
        temp = "[" + modifier[int(klc.deadchar[dknum][2])] +  \
            ScanCode[klc.deadchar[dknum][1]] + "]"
        kmn_file.write(normalize(_normalization, "+ " + temp + "\t>\tdeadkey(dk" +str(dknum) + ")\n"))

    kmn_file.write("\nc simple deadkeys\n")
    dknum = 0
    for deadkeys in klc.deadkeysList :
        dknum = dknum + 1
        kmn_file.write("\n")
        for deadkey in deadkeys[1:]:
            if len(deadkey[1]) == 1:
                dko[deadkey[1][0]] = [dknum, deadkey[0], deadkey[1][0]]
                #print(dko[deadkey[1][0]])
            if deadkey[0] in klc.characters:
                for achar in klc.characters[deadkey[0]]:
                    anum = int(achar[1])
                    if anum > 7 :
                        abase = Nmodifier[anum]
                    else :
                        abase = modifier[anum]
#                    dkout = "U+{0:04x}".format(deadkey[1][0])
                    dkout = chr(deadkey[1][0])
                    if len(deadkey[1])>1:
                        for key in deadkey[1][1:]:
                            dkout = dkout + chr(key)
                    normout = normalize(_normalization, dkout)
                    dkout = ""
                    for key in normout:
                        dkout += " U+{0:04x}".format(ord(key))
                    kmn_file.write("deadkey(dk{0}) + [{1}{2}]\t>\t{3}\n".format(str(dknum), abase, ScanCode[achar[0]], dkout.strip() ))

    kmn_file.write("\nc setup 'simple' keys\n")
    for pkl in klc.spkl:
        kmn_file.write("\n")
        for j in list(range(len(pkl[3:]))):
            if int(pkl[2]) > 7:
                abase = Nmodifier[int(klc.klc["SHIFTSTATE"][j])]
            else :
                abase = modifier[int(klc.klc["SHIFTSTATE"][j])]
            #i = len(pkl[3][j])
            i = len(pkl[3 + j])
            if pkl[3 + j][:2] == 'dk':
                pass
            elif i == 1:
                kmn_file.write(normalize(_normalization, "+ [{0}{1}]\t>\tU+{2:04x}\n".format(abase, ScanCode[int(pkl[0][2:], 16)], ord(pkl[3 + j]))))
            elif i > 2:
                dout = "+ [{0} {1}]\t>\t".format(abase, ScanCode[int(pkl[0][2:], 16)])
                for char in pkl[3 + j][1:]:
                    dout = dout + " U+{0:04x}".format(ord(char))
                kmn_file.write(normalize(_normalization, dout + "\n"))

    kmn_file.write("")
    kmn_file.close()

def main():
    pass

if __name__ == '__main__':
    main()
