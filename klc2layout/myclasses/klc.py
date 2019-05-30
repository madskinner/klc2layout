#-------------------------------------------------------------------------------
# Name:        klc
# Purpose:  functions for grabbig data from '.klc' file
#
# Author:      marks
#
# Created:     08/12/2012
# Copyright:   (c) marks 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
#import sys
import codecs
from unicodedata import normalize
#from .myconst.audio import AUDIOimport json
from  .myconst.ctrl import ctrl, combiningChars

class Klc():
    def __init__(self, _path, _arow, _thegui):
        self.path = _path
        self.row =_arow
        self.threadID = 1
        self.name = 'backend'
        self.gui = _thegui
#        self.qc = qc
#        self.qr = qr

        self.klc = dict()
        self.characters = dict()
        self.deadchar = dict()
        self.spkl = list()
        self.pkl = list()
        self.deadkeysList = list()
        self.klcFunc = {\
                        'KBD': self._KBD,\
                        'COPYRIGHT': self._COPYRIGHT,\
                        'COMPANY': self._COMPANY,\
                        'LOCALENAME': self._LOCALENAME,\
                        'LOCALEID': self._LOCALEID,\
                        'VERSION': self._VERSION,\
                        'ATTRIBUTES': self._ATTRIBUTES,\
                        'SHIFTSTATE': self._SHIFTSTATE,\
                        'LAYOUT': self._LAYOUT,\
                        'LIGATURE': self._LIGATURE,\
                        'DEADKEY': self._DEADKEY,\
                        'KEYNAME': self._KEYNAME,\
                        'KEYNAME_EXT': self._KEYNAME_EXT,\
                        'KEYNAME_DEAD': self._KEYNAME_DEAD,\
                        'DESCRIPTIONS': self._DESCRIPTIONS,\
                        'LANGUAGENAMES': self._LANGUAGENAMES,\
                        'ENDKBD': self._ENDKBD,\
                        'DEFAULT': self._DEFAULT,\
                        }

        self._load_klc_file('{}/{}'.format(self.path, self.row[0]))
        self.map102a = { \
                "SC029":[0,0],\
        		"SC002":[0,1],\
        		"SC003":[0,2],\
        		"SC004":[0,3],\
        		"SC005":[0,4],\
        		"SC006":[0,5],\
        		"SC007":[0,6],\
        		"SC008":[0,7],\
        		"SC009":[0,8],\
        		"SC00a":[0,9],\
        		"SC00b":[0,10],\
        		"SC00c":[0,11],\
        		"SC00d":[0,12],\
        		"SC010":[1,0],\
        		"SC011":[1,1],\
        		"SC012":[1,2],\
        		"SC013":[1,3],\
        		"SC014":[1,4],\
        		"SC015":[1,5],\
        		"SC016":[1,6],\
        		"SC017":[1,7],\
        		"SC018":[1,8],\
        		"SC019":[1,9],\
        		"SC01a":[1,10],\
        		"SC01b":[1,11],\
        		"SC02b":[1,12],\
        		"SC01e":[2,0],\
        		"SC01f":[2,1],\
        		"SC020":[2,2],\
        		"SC021":[2,3],\
        		"SC022":[2,4],\
        		"SC023":[2,5],\
        		"SC024":[2,6],\
        		"SC025":[2,7],\
        		"SC026":[2,8],\
        		"SC027":[2,9],\
        		"SC028":[2,10],\
        		"SC056":[3,0],\
        		"SC02c":[3,1],\
        		"SC02d":[3,2],\
        		"SC02e":[3,3],\
        		"SC02f":[3,4],\
        		"SC030":[3,5],\
        		"SC031":[3,6],\
        		"SC032":[3,7],\
        		"SC033":[3,8],\
        		"SC034":[3,9],\
        		"SC035":[3,10],\
        		"SC039":[4,0]\
                }
    
    def _KBD(self, aline):
        self.klc["KBD"] = aline.split("\t")[1:]
        self.klc["KBD"][1] = self.klc["KBD"][1].strip('\u0022')
        astring = self._next_line()
        while len(astring) < 3:
            astring = self._next_line()
        return astring
    
    def _COPYRIGHT(self, aline):
        self.klc["COPYRIGHT"] = aline.split("\t")[1].strip('\u0022')
        astring = self._next_line()
        while len(astring) < 3:
            astring = self._next_line()
        return astring
    
    def _COMPANY(self, aline):
        self.klc["COMPANY"] = aline.split("\t")[1].strip('\u0022')
        astring = self._next_line()
        while len(astring) < 3:
            astring = self._next_line()
        return astring
    
    def _LOCALENAME(self, aline):
        self.klc["LOCALENAME"] = aline.split("\t")[1].strip('\u0022')
        astring = self._next_line()
        while len(astring) < 3:
            astring = self._next_line()
        return astring
    
    def _LOCALEID(self, aline):
        self.klc["LOCALEID"] = aline.split("\t")[1].strip('\u0022')
        astring = self._next_line()
        while len(astring) < 3:
            astring = self._next_line()
        return astring
    
    def _VERSION(self, aline):
        self.klc["VERSION"] = aline.split("\t")[1]
        astring = self._next_line()
        while len(astring) < 3:
            astring = self._next_line()
        return astring
    
    def _ATTRIBUTES(self, aline):
        self.klc["ATTRIBUTES"] = []
        astring = self._next_line()
        while len(astring) < 3:
            astring = self._next_line()
        while len(astring) > 2:
            self.klc["ATTRIBUTES"].append(astring.strip())
            astring = self._next_line()
        while len(astring) < 3:
            astring = self._next_line()
        return astring
    
    def _SHIFTSTATE(self, aline):
        self.klc["SHIFTSTATE"] = []
        astring = self._next_line().strip()
        while len(astring) < 3:
            astring = self._next_line()
        while len(astring) > 2:
            self.klc["SHIFTSTATE"].append(astring.split("\t")[0])
            astring = self._next_line().strip()
        while len(astring) < 3:
            astring = self._next_line()
        return astring
    
    def _LAYOUT(self, aline):
        self.klc["LAYOUT"] = []
        dknum = 0
        nosStates = len(self.klc["SHIFTSTATE"])
        astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        while len(astring) > 2:
            layout = astring.strip().split()
            astring = self._next_line()
            sc = layout[0]
            vk = layout[1]
    
            cap = layout[2]
            n = 3
            if "//" in layout:
                m = layout.index("//")
            else:
                m = n
            states = layout[n:m]
            if cap == "SGCap":
                lenStates = nosStates + 2
                if  "9" not in self.klc["SHIFTSTATE"]:
                    self.klc["SHIFTSTATE"].append("8")
                    self.klc["SHIFTSTATE"].append("9")
                astring = self._next_line()
                states.extend(astring.split()[3:5])
                cap = 8
            else:
                lenStates = nosStates
    
            self.pkl = ["SC0" + sc, vk, cap]
            print(self.pkl)
            for j in range(lenStates):
                #temp is either "-1", "%%", "q", "q@", "0000", "0000@"
                temp = states[j]
                if len(temp) == 1 :
                    if ord(temp) in self.characters:
                        self.characters[ord(temp)].append([int("0x" + sc, 0), \
                            self.klc["SHIFTSTATE"][j]])
                    else:
                        self.characters[ord(temp)] = [int("0x" + sc, 0), \
                            self.klc["SHIFTSTATE"][j]]
    
                    self.pkl.append(temp)
                    temp = "{0:04x}".format(ord(temp))
                    states[j] = [temp,""]
                elif len(temp) == 2:
                    if temp[1] == "@":
                        dknum = dknum + 1
                        self.pkl.append(temp[0])
                        self.characters[ord(temp[0])].append([int("0x" + sc, 0), \
                            self.klc["SHIFTSTATE"][j]])
                        temp = "{0:04x}".format(ord(temp[0]))
                        states[j] = [temp,str(dknum)]
                        self.deadchar[dknum] = \
                            [temp, int("0x" + sc, 0),self.klc["SHIFTSTATE"][j]]
                        self.pkl.append("dk" + str(dknum))
                    elif temp == "%%":
                        self.pkl.append("%%" + vk + "_" + str(j))
                    else:
                        self.pkl.append("--")
                elif len(temp) == 4:
                    states[j] = [temp,""]
                    if int("0x" + temp, 0) in self.characters:
                        self.characters[int("0x" + temp, 0)].append([int("0x" + sc, 0), \
                            self.klc["SHIFTSTATE"][j]])
                    else:
                        self.characters[int("0x" + temp, 0)] = [int("0x" + sc, 0), \
                            self.klc["SHIFTSTATE"][j]]
                    self.pkl.append(chr(int("0x" + temp, 0)))
                elif len(temp) == 5:
                    dknum = dknum + 1
                    states[j] = [temp[0:4],""]
                    if int("0x" + temp[0:4], 0)  in self.characters:
                        self.characters[int("0x" + temp[0:4], 0)].append( \
                            [int("0x" + sc, 0), self.klc["SHIFTSTATE"][j]])
                    else:
                        self.characters[int("0x" + temp[0:4], 0)] = \
                            [int("0x" + sc, 0), self.klc["SHIFTSTATE"][j]]
                    self.pkl.append("dk" + str(dknum))
                    self.deadchar[dknum] = \
                       [temp[0:4], int("0x" + sc, 0),self.klc["SHIFTSTATE"][j]]
                else:
                    pass
    
            self.klc["LAYOUT"].append([sc, vk, cap, states])
            self.spkl.append(pkl)
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        return astring
    
    def _LIGATURE(self, aline):
        astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        while len(astring) > 2:
            astring = astring[0:astring.find('//')].strip()
            ligature = astring.split()
            astring = self._next_line()
    
            lid = ['%%' + ligature[0] + "_" + ligature[1],'%' +''.join([chr(int(str(item),16)) for item in ligature[2:] ])]
    
            #msklc lists ligatures in alphabetical order of virtualkey name!!!
            #so brute force scan whole self.spkl() and zstates() for each ligature
            for aline in self.spkl:
                if lid[0] in aline:
                    aline[aline.index(lid[0])] = lid[1]
            for aline in self.klc["LAYOUT"]:
                if lid[0] in aline[3]:
                    aline[3][aline[3].index(lid[0])] = lid[1]
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        return astring
    
    def _DEADKEY(self, aline):
        n = []
        n.append(int( aline.split()[1], 16))
        deadkeys = []
        deadkey = [0, n , 0]
        deadkeys.append(deadkey)
        astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        while len(astring) > 2:
            deadIn = astring.split()
            astring = self._next_line()
            n = list([int(deadIn[1], 16),])
            m = int(deadIn[0], 16)
            deadkeys.append([m, n, "blank"])
        diacritic = 0
        # scan deadkeys for combuning diacritic as output of deadkey
        for deadkey in deadkeys:
            for arange in combiningChars:
                if (deadkey[1][0] in arange):
                    diacritic = deadkey[1][0]
        if diacritic > 0:
            for deadkey in deadkeys:
                if deadkey[0] == deadkey[1][0] and len(deadkey[1])==1:
                    deadkey[1].append(diacritic)
        for deadkey in deadkeys:
            l = len(deadkey[1])
            n = ""
            for i in range(0,l):
                m = deadkey[1][i]
                if m in ctrl:
                    o = ctrl[m]
                else:
                    o = chr(m)
                n = "".join([n, o])
            if len(n) > 0:
                p = ord(n[0])
                for arange in combiningChars:
                    if p in arange:
                        n = "".join([chr(9676), n])
                deadkey[2] = normalize("NFC", n)
        self.deadkeysList.append(deadkeys)
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        return astring
    
    def _KEYNAME(self, aline):
        self.klc["KEYNAME"] = []
        astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        while len(astring) > 2:
            self.klc["KEYNAME"].append(astring.split())
            astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        return astring
    
    def _KEYNAME_EXT(self, aline):
        self.klc["KEYNAME_EXT"] = []
        astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        while len(astring) > 2:
            self.klc["KEYNAME_EXT"].append(astring.split())
            astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        return astring
    
    def _KEYNAME_DEAD(self, aline):
        self.klc["KEYNAME_DEAD"] = []
        astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        while len(astring) > 2:
            self.klc["KEYNAME_DEAD"].append(astring.split())
            astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        return astring
    
    def _DESCRIPTIONS(self, aline):
        self.klc["DESCRIPTIONS"] = []
        astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        while (len(astring) > 2) and (astring.strip().split("\t")[0] != 'LANGUAGENAMES'):
            self.klc["DESCRIPTIONS"].append(astring.split())
            astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        return astring
    
    def _LANGUAGENAMES(self, aline):
        self.klc["LANGUAGENAMES"] = []
        astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        while (len(astring) > 2) and (astring.strip().split("\t")[0] != 'ENDKBD') :
            self.klc["LANGUAGENAMES"].append(astring.split())
            astring = self._next_line()
        while (len(astring) < 3) or (astring[0:2] == "//"):
            astring = self._next_line()
        return astring
    
    def _ENDKBD(self, aline):
        return ""
    
    def _DEFAULT(self, aline):
        return ""
    
    def _next_line(self):
        result = self.linesin[self.index]
        self.index += 1
        self.gui.progbar.step()
        self.gui.update()
        return result
    
    def _load_klc_file(self,_path):
        klc_file = codecs.open(_path, mode='r',encoding='utf-16LE')
#        dkv = {}
    #    klc_file = codecs.open(filein, mode='r',encoding='UNICODE')
#        astring = ''
        self.linesin = klc_file.read().lstrip('\uFEFF').split('\n')
        klc_file.close()
        self.gui.progbar['maximum'] = len(self.linesin)
        self.gui.progbar['value'] = 0
        self.gui.update()
        self.index = 0
        astring = self._next_line().lstrip('\uFEFF')
        while len(astring) :
            command = astring.strip().split()
            if "LAYOUT" in command[0]:
                self.klc["LAYOUT"] = list()
                dknum = 0
                nosStates = len(self.klc["SHIFTSTATE"])
                astring = self._next_line()
                while (len(astring) < 3) or (astring[0:2] == "//"):
                    astring = self._next_line()
                while len(astring) > 2:
                    layout = astring.strip().split()
                    astring = self._next_line()
                    sc = layout[0]
                    vk = layout[1]
                    #ignore extra keys on ABNT keyboard for Brazil
                    if (layout[0] == "73") or (layout[0] == "7e"):
                        pass
                    else:
                        cap = layout[2]
                        n = 3
                        if "//" in layout[-1]:
                            m = layout.index(layout[-1])
                        elif "//" in layout:
                            m = layout.index("//")
                        else:
                            m = n
                        states = layout[n:m]

                        if cap == "SGCap":
                            lenStates = nosStates + 2
                            if not self.klc["SHIFTSTATE"][-1] == "9":
                                self.klc["SHIFTSTATE"].append("8")
                                self.klc["SHIFTSTATE"].append("9")
#                            print('SGCap line', astring)
#                            ds = ['-1', '-1']
                            if len(astring.split('\t')[3:5]) > 1:
#                                ds = astring.split('\t')[3:5]
                                ds = astring.split()[3:5]
                            else:
#                                ds = [astring.split('\t')[3], '-1']
                                ds = [astring.split()[3], '-1']
#                            states.extend(astring.split('\t')[3:5])
                            states.extend(ds)
                            cap = '8'
                            astring = self._next_line()
                        else:
                            lenStates = nosStates
                        self.pkl = ["SC0" + sc, vk, str(cap)]
                        for j in range(lenStates):
                            temp = states[j]
                            if len(temp) == 1 :
                                self.pkl.append(temp)
                                temp = "{0:04x}".format(ord(temp))
                                states[j] = [temp,""]
                                if int("0x" + temp, 0) not in self.characters:
                                    self.characters[int("0x" + temp, 0)] = []
                                self.characters[int("0x" + temp, 0)].append([int("0x" + sc, 0), \
                                    self.klc["SHIFTSTATE"][j], int(cap)])
                            elif len(temp) == 2:
                                if temp[1] == "@":
                                    #is a deadkey of form 'char'@
                                    dknum = dknum + 1
                                    self.pkl.append(temp[0])
                                    temp = "{0:04x}".format(ord(temp[0]))
                                    states[j] = [temp,str(dknum)]
                                    if int("0x" + temp, 0) not in self.characters:
                                        self.characters[int("0x" + temp, 0)] = []
                                    self.characters[int("0x" + temp, 0)].append([int("0x" + sc, 0), \
                                        self.klc["SHIFTSTATE"][j], int(cap)])
                                    self.deadchar[dknum] = \
                                        [temp, int("0x" + sc, 0),klc["SHIFTSTATE"][j], int(cap)]
                                    self.pkl.append("dk" + str(dknum))
                                elif temp == "%%":
                                    #is ligature
                                    self.pkl.append("%%" + vk + "_" + str(j))
                                else:
                                    #is blank
                                    self.pkl.append("--")
                            elif len(temp) == 4:
                                #is hex codepoint
                                states[j] = [temp,""]
                                if int("0x" + temp, 0) not in self.characters:
                                    self.characters[int("0x" + temp, 0)] = []
                                self.characters[int("0x" + temp, 0)].append([int("0x" + sc, 0), \
                                    self.klc["SHIFTSTATE"][j], int(cap)])
                                self.pkl.append(chr(int("0x" + temp, 0)))
                            elif len(temp) == 5:
                                #is deadkey of form 'hex codepoint'@
                                #'hex codepoint
                                dknum = dknum + 1
                                temp = temp[0:4]
                                states[j] = [temp,""]
                                if int("0x" + temp, 0) not in self.characters:
                                    self.characters[int("0x" + temp, 0)] = []
                                self.characters[int("0x" + temp, 0)].append([int("0x" + sc, 0), \
                                    self.klc["SHIFTSTATE"][j], int(cap)])
                                self.pkl.append("dk" + str(dknum))
                                self.deadchar[dknum] = \
                                   [temp, int("0x" + sc, 0),self.klc["SHIFTSTATE"][j], int(cap)]
                            else:
                                pass

                    self.klc["LAYOUT"].append([sc, vk, cap, states])
                    self.spkl.append(self.pkl)
                while (len(astring) < 3) or (astring[0:2] == "//"):
                    astring = self._next_line()
            elif "LIGATURE" in command[0]:
                astring = self._next_line()
                while (len(astring) < 3) or (astring[0:2] == "//"):
                    astring = self._next_line()
                while len(astring) > 2:
                    astring = astring[0:astring.find('//')].strip()
                    ligature = astring.split()
#                    print('ligature', ligature)
                    astring = self._next_line()
    #                print(ligature)
                    alig = '%'
                    for achar in ligature[2:]:
#                        print('ligature[2:]', ligature[2:], 'achar', achar)
                        lchr = str(achar)
                        lint = int(lchr, 16)
                        lowc = chr(lint)
                        alig = "{0}{1}".format(alig, chr(int(str(achar),16)))
                    lid = ['%%' + ligature[0] + "_" + ligature[1], alig]
            #msklc lists ligatures in alphabetical order of virtualkey name!!!
            #so brute force scan whole SPKL() and zstates() for each ligature
                    for aline in self.spkl:
                        if lid[0] in aline:
#                            print('before', aline)
                            aline[aline.index(lid[0])] = lid[1]
#                            print('after ', aline)
                    for aline in self.klc["LAYOUT"]:
                        if lid[0] in aline[3]:
                            aline[3][aline[3].index(lid[0])] = lid[1]
    #            print(self.spkl)
                while (len(astring) < 3) or (astring[0:2] == "//"):
                    astring = self._next_line()

            else:
                #print(command[0],self.klc["SHIFTSTATE"])
                astring = self.klcFunc[command[0]]((astring.strip()))
        pass
    
    

def main():
    pass

if __name__ == '__main__':
    main()

