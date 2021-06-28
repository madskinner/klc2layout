# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 17:02:15 2021

@author: 44773
"""

import os
import json
from pathlib import Path
from html import unescape, escape

WELCOMES = ['C:/Users/44773/Desktop/Keyman Developer/Projects/sil_srr_latn_azerty/source/welcome/welcome.htm', \
            'C:/Users/44773/Desktop/Keyman Developer/Projects/sil_wo_latn_azerty/source/welcome/welcome.htm', \
            'C:/Users/44773/Desktop/Keyman Developer/Projects/sil_wo_ajami_arab/source/welcome/welcome.htm', \
            'C:/Users/44773/Desktop/Keyman Developer/Projects/sil_srr_ajami_arab/source/welcome/welcome.htm']

def main():
    names = dict()
    names['en-US']= dict()
    names['pt-PT'] = dict()
    names['fr-FR'] = dict()
    for fin in WELCOMES:
        print(f'processing {fin}')
        af = Path(fin)
        lines = af.read_text(encoding='utf-8').split('\n')
        grab = False
        codepoint = ''
        lang = ''
        for aline in lines:
            l = aline.strip()
            # print(l)
            if '<!--Starting English-->' in l:
                lang = 'en-US'
                # print(f"{lang}")
            elif '<!--Starting Portuguese-->' in l:
                lang = 'pt-PT'
                # print(f"{lang}")
            elif '<!--Starting French-->' in l:
                lang = 'fr-FR'
                # print(f"{lang}")
            elif lang and '<input ' in l and '-Character' in l:
                grab = True
                # print(f"{grab}")
            elif lang and grab:
                # print(f"lang = {lang}, grab = {grab}")
                # print(l)
                start = 0
                if '<td>U+' in l:
                    start = l.find('<td>U+') + 4
                    end = l.find('</td>')
                    codepoint = l[start:end]
                    # print(f"codepoint = {codepoint}")
                elif codepoint:
                    start = l.find('<td>') + 4
                    end = l.find('</td>')
                    was = l[start:end]
                    name = unescape(was)
                    if len(codepoint.split()) == 2:
                        print(unescape(l))
                        print(codepoint.split())
                        if lang == 'en_US':
                            # name = name.replace(' WITH ', ', COMBINING ')
                            bits = name.split('WITH')
                            print(f'bits=>{bits}<')
                            name = bits[0].strip() + ', COMBINING ' + bits[1].strip()
                        elif lang == 'pt-PT':
                            name = name.replace(' COM ', ', COMBINANDO ')
                        elif lang == 'fr-FR':
                            name = name.replace(' AVEC ', ', COMBINANT ')
                        else:
                            pass# panic
                        print(name)
                    names[lang][codepoint] = name
                    # print(f"names[{lang}][{counescapedepoint}] = {name}")
                    codepoint = ''
                else:
                    # print(f"skipped {l}")
                    pass
            elif '<!--Ending ' in l:
                lang = ''
                grab = False

            else:
                pass
    # print(f"names=>{names}<")
    with open("C:/Users/44773/Desktop/gits/klc2layout/klc2layout/names.json", "w") as names_file:
        json.dump(names, names_file, indent=4, sort_keys=True)

if __name__ == '__main__':
    main()
