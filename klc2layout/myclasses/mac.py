#-------------------------------------------------------------------------------
# Name:        mac
# Purpose:  output 'keylayout' mac 10.7 keyboard file version of klc file.
#
# Author:      marks
#
# Created:     2013/05/01
# Copyright:   (c) marks 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import sys
import os
import codecs
#import klc
from unicodedata import normalize

class Mac():
    def __init__(self):
        #PC scancode address:Mac virtual key code
        self.ScanCode = {\
            "02":18,\
        	"03":19,\
        	"04":20,\
        	"05":21,\
        	"06":23,\
        	"07":22,\
        	"08":26,\
        	"09":28,\
        	"0a":25,\
        	"0b":29,\
        	"0c":27,\
        	"0d":24,\
        	"10":12,\
        	"11":13,\
        	"12":14,\
        	"13":15,\
        	"14":17,\
        	"15":16,\
        	"16":32,\
        	"17":34,\
        	"18":31,\
        	"19":35,\
        	"1a":33,\
        	"1b":30,\
        	"1e":0,\
        	"1f":1,\
        	"20":2,\
        	"21":3,\
        	"22":5,\
        	"23":4,\
        	"24":38,\
        	"25":40,\
        	"26":37,\
        	"27":41,\
        	"28":39,\
        	"29":10,\
        	"2b":42,\
        	"2c":6,\
        	"2d":7,\
        	"2e":8,\
        	"2f":9,\
        	"30":11,\
        	"31":45,\
        	"32":46,\
        	"33":43,\
        	"34":47,\
        	"35":44,\
        	"39":49,\
        	"56":50}
        
        
        self.mapss = {\
            0:[],\
            1:[],\
            2:[],\
            3:[],\
            4:[],\
            5:[],\
            6:[],\
            7:[],\
            8:[],\
            9:[],\
            10:[]\
            }
        self.maps = dict()
        self.dknum = 0
        self.dkout = dict()
        self.dkdkout = dict()
        
        self.actionstate = dict()
        self.actionoutput = dict()
        self.terminators = dict()
        self.maxout = 1
        
        self.UScommand = {\
            0: [0, 'output', 'a'],\
            1: [1, 'output', 's'],\
            2: [2, 'output', 'd'],\
            3: [3, 'output', 'f'],\
            4: [4, 'output', 'h'],\
            5: [5, 'output', 'g'],\
            6: [6, 'output', 'z'],\
            7: [7, 'output', 'x'],\
            8: [8, 'output', 'c'],\
            9: [9, 'output', 'v'],\
            10: [10, 'output', '&#xA7;'],\
            11: [11, 'output', 'b'],\
            12: [12, 'output', 'q'],\
            13: [13, 'output', 'w'],\
            14: [14, 'output', 'e'],\
            15: [15, 'output', 'r'],\
            16: [16, 'output', 'y'],\
            17: [17, 'output', 't'],\
            18: [18, 'output', '1'],\
            19: [19, 'output', '2'],\
            20: [20, 'output', '3'],\
            21: [21, 'output', '4'],\
            22: [22, 'output', '6'],\
            23: [23, 'output', '5'],\
            24: [24, 'output', '='],\
            25: [25, 'output', '9'],\
            26: [26, 'output', '7'],\
            27: [27, 'output', '-'],\
            28: [28, 'output', '8'],\
            29: [29, 'output', '0'],\
            30: [30, 'output', ']'],\
            31: [31, 'output', 'o'],\
            32: [32, 'output', 'u'],\
            33: [33, 'output', '['],\
            34: [34, 'output', 'i'],\
            35: [35, 'output', 'p'],\
            36: [36, 'output', '&#xD;'],\
            37: [37, 'output', 'l'],\
            38: [38, 'output', 'j'],\
            39: [39, 'output', '&#x27;'],\
            40: [40, 'output', 'k'],\
            41: [41, 'output', ';'],\
            42: [42, 'output', '&#x5C;'],\
            43: [43, 'output', ','],\
            44: [44, 'output', '/'],\
            45: [45, 'output', 'n'],\
            46: [46, 'output', 'm'],\
            47: [47, 'output', '.'],\
            48: [48, 'output', '&#x9;'],\
            49: [49, 'output', ' '],\
            50: [50, 'output', '`'],\
            51: [51, 'output', 'BS'],\
            52: [52, 'output', 'ETX'],\
            53: [53, 'output', 'ESC'],\
            65: [65, 'output', '.'],\
            66: [66, 'output', 'GS'],\
            67: [67, 'output', '*'],\
            69: [69, 'output', '+'],\
            70: [70, 'output', 'FS'],\
            71: [71, 'output', 'ESC'],\
            72: [72, 'output', 'US'],\
            75: [75, 'output', '/'],\
            76: [76, 'output', 'ETX'],\
            77: [77, 'output', 'RS'],\
            78: [78, 'output', '-'],\
            81: [81, 'output', '='],\
            82: [82, 'output', '0'],\
            83: [83, 'output', '1'],\
            84: [84, 'output', '2'],\
            85: [85, 'output', '3'],\
            86: [86, 'output', '4'],\
            87: [87, 'output', '5'],\
            88: [88, 'output', '6'],\
            89: [89, 'output', '7'],\
            91: [91, 'output', '8'],\
            92: [92, 'output', '9'],\
            96: [96, 'output', 'DLE;'],\
            97: [97, 'output', 'DLE'],\
            98: [98, 'output', 'DLE'],\
            99: [99, 'output', 'DLE'],\
            100: [100, 'output', 'DLE'],\
            101: [101, 'output', 'DLE'],\
            102: [102, 'output', ' '],\
            103: [103, 'output', 'DLE'],\
            104: [104, 'output', ' '],\
            105: [105, 'output', 'DLE'],\
            106: [106, 'output', 'DLE'],\
            107: [107, 'output', 'DLE'],\
            108: [108, 'output', 'DLE'],\
            109: [109, 'output', 'DLE'],\
            110: [110, 'output', 'DLE'],\
            111: [111, 'output', 'DLE'],\
            112: [112, 'output', 'DLE'],\
            113: [113, 'output', 'DLE'],\
            114: [114, 'output', 'ENQ'],\
            115: [115, 'output', 'ENQ;'],\
            116: [116, 'output', 'VT'],\
            117: [117, 'output', '&#x7F;'],\
            118: [118, 'output', 'DLE'],\
            119: [119, 'output', 'EOT'],\
            120: [120, 'output', 'DLE'],\
            121: [121, 'output', 'FF;'],\
            122: [122, 'output', 'DLE'],\
            123: [123, 'output', 'FS;'],\
            124: [124, 'output', 'GS'],\
            125: [125, 'output', 'US'],\
            126: [126, 'output', 'RS']}
        
        self.UScontrol = {
            0:[0, 'output', 'SOH'],\
            1:[1, 'output', 'DC3'],\
            2:[2, 'output', 'EOT'],\
            3:[3, 'output', 'ACK'],\
            4:[4, 'output', 'BS'],\
            5:[5, 'output', 'BEL'],\
            6:[6, 'output', 'SUB'],\
            7:[7, 'output', 'CAN'],\
            8:[8, 'output', 'ETX'],\
            9:[9, 'output', 'SYN'],\
            11:[11, 'output', 'STX'],\
            12:[12, 'output', 'DC1'],\
            13:[13, 'output', 'ETB'],\
            14:[14, 'output', 'ENQ'],\
            15:[15, 'output', 'DC2'],\
            16:[16, 'output', 'EM'],\
            17:[17, 'output', 'DC4'],\
            19:[19, 'output', 'NUL'],\
            22:[22, 'output', 'RS'],\
            27:[27, 'output', 'US'],\
            30:[30, 'output', 'GS'],\
            31:[31, 'output', 'SI'],\
            32:[32, 'output', 'NAK'],\
            33:[33, 'output', 'ESC'],\
            34:[34, 'output', '&#x9;'],\
            35:[35, 'output', 'DLE'],\
            36:[36, 'output', '&#xD;'],\
            37:[37, 'output', 'FF'],\
            38:[38, 'output', '&#xA;'],\
            40:[40, 'output', 'VT'],\
            42:[42, 'output', 'FS'],\
            45:[45, 'output', 'SO'],\
            46:[46, 'output', '&#xD;'],\
            48:[48, 'output', '&#x9;'],\
            49:[49, 'output', 'NUL'],\
            51:[51, 'output', 'BS'],\
            52:[52, 'output', 'ETX'],\
            53:[53, 'output', 'ESC'],\
            66:[66, 'output', 'GS'],\
            70:[70, 'output', 'FS'],\
            71:[71, 'output', 'ESC'],\
            72:[72, 'output', 'US'],\
            76:[76, 'output', 'ETX'],\
            77:[77, 'output', 'RS'],\
            96:[96, 'output', 'DLE'],\
            97:[97, 'output', 'DLE'],\
            98:[98, 'output', 'DLE'],\
            99:[99, 'output', 'DLE'],\
            100:[100, 'output', 'DLE'],\
            101:[101, 'output', 'DLE'],\
            102:[102, 'output', ' '],\
            103:[103, 'output', 'DLE'],\
            104:[104, 'output', ' '],\
            105:[105, 'output', 'DLE'],\
            106:[106, 'output', 'DLE'],\
            107:[107, 'output', 'DLE'],\
            108:[108, 'output', 'DLE'],\
            109:[109, 'output', 'DLE'],\
            110:[110, 'output', 'DLE'],\
            111:[111, 'output', 'DLE'],\
            112:[112, 'output', 'DLE'],\
            113:[113, 'output', 'DLE'],\
            114:[114, 'output', 'ENQ'],\
            115:[115, 'output', 'SOH'],\
            116:[116, 'output', 'VT'],\
            117:[117, 'output', '&#x7F;'],\
            118:[118, 'output', 'DLE'],\
            119:[119, 'output', 'EOT'],\
            120:[120, 'output', 'DLE'],\
            121:[121, 'output', 'FF'],\
            122:[122, 'output', 'DLE'],\
            123:[123, 'output', 'FS'],\
            124:[124, 'output', 'GS'],\
            125:[125, 'output', 'US'],\
            126:[126, 'output', 'RS']}
        
        self.CONTROL = { 0 :'NULL', \
                    1 :'SOH', \
                    2 :'STX', \
                    3 :'ETX', \
                    4 :'EOT', \
                    5 :'ENQ', \
                    6 :'ACK', \
                    7 :'BEL', \
                    8 :'BS', \
                    #9 :'HT', \
                    #10 :'SOH', \
                    11 :'VT', \
                    12 :'FF', \
                    #13 :'CR', \
                    14 :'SO', \
                    15 :'SI', \
                    16 :'DLE', \
                    17 :'DC1', \
                    18 :'DC2', \
                    19 :'DC3', \
                    20 :'DC4', \
                    21 :'NAK', \
                    22 :'SYN', \
                    23 :'ETB', \
                    24 :'CAN', \
                    25 :'EM', \
                    26 :'SUB', \
                    27 :'ESC', \
                    28 :'FS', \
                    29 :'GS', \
                    30 :'RS', \
                    31 :'US', \
                    }
    
    def escapeit(self, achar):
        anord = ord(achar)
        sout = '&#x{0:X};'.format(anord)
        so = sout if anord not in self.CONTROL else self.CONTROL[anord]
        return so
    
    
    def mac_it(self, klc, mac_file, macID, cmdname = '', ctrlname = '', _normalize="NFC"):
        self.dknum = 0
        self.dkout = dict()
        self.dkdkout = dict()
    
        self.terminators.clear()
        self.loadMaps(klc)
    #    print(self.actionstate)
        self.loadActions(klc)
        self.maxout = self.countMaxOut()
        self.loadCommand(cmdname)
        self.loadControl(ctrlname)
        mac_file.write( '\n'.join([\
            '<?xml version="1.0" encoding="UTF-8"?>',\
            '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">',\
            '<keyboard group="126" id="{0}" name="{1}" maxout="{2}">'.format(str(macID), klc.klc["KBD"][1], str(self.maxout)),\
            '    <layouts>',\
            '        <layout first="0" last="0" modifiers="48" mapSet="312" />',\
            '    </layouts>',\
            '    <modifierMap id="48" defaultIndex="0">',\
            '']))
    #assume SGCap present, will have empty key map index(8,9) if not present
    #index 10 is command
        mac_file.write( '\n'.join([\
    		'        <keyMapSelect mapIndex="0">',\
            '            <modifier keys="" />',\
    		'        </keyMapSelect>',\
    		'        <keyMapSelect mapIndex="1">',\
            '            <modifier keys="anyShift" />',\
    		'        </keyMapSelect>',\
    		'        <keyMapSelect mapIndex="2">',\
            '            <modifier keys="anyControl" />',\
    		'        </keyMapSelect>',\
    		'        <keyMapSelect mapIndex="3">',\
            '            <modifier keys="anyControl anyShift" />',\
    		'        </keyMapSelect>',\
    		'        <keyMapSelect mapIndex="4">',\
            '            <modifier keys="anyOption" />',\
    		'        </keyMapSelect>',\
    		'        <keyMapSelect mapIndex="5">',\
            '            <modifier keys="anyOption anyShift" />',\
    		'        </keyMapSelect>',\
    		'        <keyMapSelect mapIndex="6">',\
            '            <modifier keys="anyControl anyOption" />',\
    		'        </keyMapSelect>',\
    		'        <keyMapSelect mapIndex="7">',\
            '            <modifier keys="anyControl anyOption anyShift" />',\
    		'        </keyMapSelect>',\
    		'        <keyMapSelect mapIndex="8">',\
            '            <modifier keys="caps anyOption? anyControl?" />',\
    		'        </keyMapSelect>',\
    		'        <keyMapSelect mapIndex="9">',\
            '            <modifier keys="caps anyShift anyOption? anyControl?" />',\
    		'        </keyMapSelect>',\
    		'        <keyMapSelect mapIndex="10">',\
            '            <modifier keys="command caps? anyShift? anyOption? anyControl?" />',\
    		'        </keyMapSelect>',\
            '']))
        mac_file.write( '\n'.join([\
            '    </modifierMap>',\
            '    <keyMapSet id="312">',\
            '']))
        mapIndex = -1
        for mapIndex in range(0, 11):
            #mapIndex = mapIndex + 1
            mac_file.write(normalize(_normalize, '        <keyMap index="{0}">\n'.format(str(mapIndex))))
            #print('        <keyMap index="{0}">\n'.format(str(mapIndex)))
            self.maps[mapIndex].sort()
            #print(self.maps[mapIndex])
            lastcode = -1
            mapout = []
            if mapIndex not in [2,3,10]:
                for keycode in self.maps[mapIndex]:
                    #print('keycode = {}, map = {}'.format(keycode, mapIndex))
    
                    if keycode[0] > (lastcode + 1):
        #                if (keycode[0] - (lastcode + 1) )==1:
                        if (keycode[0] - (lastcode + 1) )==1:
                            mapout.append('            <!-- gap, {0} -->'.format(str(lastcode+1)))
                        else:
                            mapout.append("            <!-- gap, {0}-{1} -->".format(str(lastcode+1),str(keycode[0] - 1)))
        #            else:
                    if (keycode[1] == 'output') and (keycode[2][0:3] != '&#x'):
                        sout = ''
                        for achar in keycode[2]:
                            sout = '{0}{1}'.format(sout, self.escapeit(achar))
                        mapout.append('            <key code="{0}" {1}="{2}" />'.format(str(keycode[0]),keycode[1], sout))
                    else:
                        mapout.append('            <key code="{0}" {1}="{2}" />'.format(str(keycode[0]),keycode[1],keycode[2]))
                    lastcode = keycode[0]
            else:
                lastcode = -1
            if lastcode < 126:
                    if lastcode == 125:
                        mapout.append('            <!-- gap, {0} -->'.format(str(lastcode+1)))
                    else:
                        mapout.append('            <!-- gap, {0}-{1} -->'.format(str(lastcode+1),"126"))
            mapout.append('        </keyMap>')
            mapout.append('')
            #print("mapout for index ={}, {}".format(mapIndex, '\n'.join(mapout)))
            mac_file.write(normalize(_normalize, '\n'.join(mapout)))
    
        mac_file.write("    </keyMapSet>\n")
        mac_file.write( "    <actions>\n")
        actionout = []
        for key in sorted(self.actionstate):
            actionout.append( '        <action id="{0}">'.format(key))
    #        for action in self.actionstate[key]:
            for action in self.actionstate[key]:
                actionout.append( '            <when state="{0}" next="{1}" />'.format(action[0], action[1]))
            actionout.append( '        </action>')
        for key in sorted(self.actionoutput):
            actionout.append( '        <action id="{0}">'.format(key))
            for action in (self.actionoutput[key]):
                sout = ''
                for achar in normalize("NFC", action[1]):
                    sout = '{0}{1}'.format(sout, self.escapeit(achar))
                actionout.append( '            <when state="{0}" output="{1}" />'.format(action[0], sout))
            actionout.append( '        </action>')
        actionout.append( '')
        mac_file.write(normalize(_normalize, '\n'.join(actionout)))
        mac_file.write('    </actions>\n')
        actionout = []
        actionout.append( '    <terminators>')
    #    print(sorted(self.terminators))
        for action in sorted(self.terminators):
    #        print(action)
            sout = ''
            for achar in self.terminators[action]:
                sout = '{0}{1}'.format(sout, self.escapeit(achar))
            actionout.append( '        <when state="{0}" output="{1}" />'.format(action, sout))
        actionout.append( '    </terminators>')
        actionout.append( '')
        mac_file.write(normalize(_normalize, '\n'.join(actionout)))
        mac_file.write('</keyboard>\n')
        mac_file.close()
    
    
    
    
    def loadMaps(self, klc):
        #print("load_maps")
        self.maps = dict()
        for amap in self.mapss:
            self.maps[amap] = self.mapss[amap]
        for pkl in klc.spkl:
    #        vkn = int("0x" + self.ScanCode[int("0x" + pkl[0][3:],0)],0)
            if pkl[0][3:] != "53":
                vkn = self.ScanCode[pkl[0][3:]]
                states = pkl[3:]
                #print('vkn = {}, states = {}'.format(vkn, states))
                if len(states) < len(klc.klc["SHIFTSTATE"]):
                    states.extend(['--', '--'])
                for j in range(len(klc.klc["SHIFTSTATE"])):
                    if states[j]  == "--":
                        pass # null entry, skip it
                    elif len(states[j]) == 1:
                        self.maps[int(klc.klc["SHIFTSTATE"][j])].append([vkn,"output",'{0}'.format(states[j])])
                    elif states[j][0] == "%":
                        self.maps[int(klc.klc["SHIFTSTATE"][j])].append([vkn,"output",'{0}'.format(states[j][1:])])
                    elif states[j][0:2] == "dk":
                        self.dknum = int(states[j][2:])
                        dkn = 'dk{0:02}'.format(self.dknum)
                        self.maps[int(klc.klc["SHIFTSTATE"][j])].append([vkn,"action",dkn])
                        self.actionstate[dkn] =[["none",dkn]]
                    else:
                        #error
                        print("unkown key state =>{0}< at {1} in {2}".format(states[j],str(j),str(pkl)))
                    #print('maps[{}] = "{}"'.format(int(klc.klc["SHIFTSTATE"][j]),self.maps[int(klc.klc["SHIFTSTATE"][j])]))
    
    def loadActions(self, klc):
        #print("load_actions")
        self.dknum = 0
        self.dkout = dict()
        self.dkdkout = dict()
        for deadkeys in klc.deadkeysList:
            self.dknum = self.dknum + 1
            thedeadchar = chr(deadkeys[0][1][0])
            if thedeadchar == '"':
                thedeadchar = "&#x22;"
            self.terminators["dk{0:02}".format(self.dknum)] = thedeadchar
            for deadkey in deadkeys[1:]:
                #deadkey = [base,list of outputs,displayform]
                # so for maps 0-9 wherever base is output change to action dk:base
    #            dkbase = "dk:{0}".format(chr(deadkey[0]))
                dkbase = "dk:x{0:X}".format(deadkey[0])
                for j in range(10):
                    for keycode in self.maps[j]:
                        if keycode[1] == "output" and keycode[2] == chr(deadkey[0]):
                            keycode[1] = "action"
                            keycode[2] = dkbase
    #            dkv["{0}_{1}".format(self.dknum, deadkey[0]) ] = deadkey[1]
                if len(deadkey[1]) == 1:
                    if deadkey[1][0] not in self.dkout:
                        self.dkout[deadkey[1][0]] = [[self.dknum, deadkey[0]]]
                    else:
                        self.dkout[deadkey[1][0]].append([self.dknum, deadkey[0]])
    #                print(self.dkout[deadkey[1][0]])
                # add action dk:base if not exist
                if dkbase not in self.actionoutput:
                    self.actionoutput[dkbase] = [["none", chr(deadkey[0])]]
                # add to action dk:base, state=dknum output
                n = ""
                for i in range(0,len(deadkey[1])):
                    if len(n) > 0:
                        n = "{0}{1}".format(n,chr(deadkey[1][i]))
                    else:
                        n = chr(deadkey[1][i])
                self.actionoutput[dkbase].append(["dk{0:02}".format(self.dknum),n])
        maxdknum = self.dknum
    
    def countMaxOut(self):
    #    print(maps)
        self.maxout = 1
        for k in self.maps:
    #        print(map)
            for keycode in self.maps[k]:
                if (keycode[1] =="output") and (len(keycode[2])>self.maxout):
                    self.maxout = len(keycode[2])
        for actions in self.actionoutput:
            for action in self.actionoutput[actions]:
                if len(action[1])>self.maxout:
                    self.maxout = len(action[1])
        return self.maxout
    
    def loadCommand(self, cmdname):
        if cmdname == "US":
            l = [keycode[0] for keycode in self.maps[10]]
            for j in range(127):
                if j in self.UScommand:
                    if self.UScommand[j][0] not in l:
                        self.maps[10].append(self.UScommand[j])
    
    
    def loadControl(self, ctrlname):
        if ctrlname == "US":
            l = [keycode[0] for keycode in self.maps[2]]
            k = [keycode[0] for keycode in self.maps[3]]
            for j in range(127):
                if j in self.UScontrol:
                    if self.UScontrol[j][0] not in l:
                        self.maps[2].append(self.UScontrol[j])
                    if self.UScontrol[j][0] not in k:
                        self.maps[3].append(self.UScontrol[j])

def main():
    pass

if __name__ == '__main__':
    main()
