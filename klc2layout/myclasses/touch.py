# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 08:57:03 2021

@author: Mark Skinner
"""
# pylint: disable=C0301,C0103,W1309
# import os
from pathlib import Path
from unicodedata import normalize, name, category, combining
import json
import re
import shutil
import subprocess
from html import unescape, escape
from PIL import Image, ImageDraw, ImageFont
# from zopflipng import png_optimize
# from .kmn import Kmn
from lxml import objectify

from .myconst.therest import STORE_AND, DEVICE_PNGS, STATE, KEYSTROKE, \
                             LOOKUP, MODIFIER, REVERSE
from .myconst.vkeys import VKEYS, STATES
from .myconst.char_ranges import HEBREW, AJAMI, GREEK, \
                                 CONTROLCHARS, PLACEHOLDERS
from .myconst.fonts import FONTNAME
from .myconst.shapes import SHAPES

KTL_COLOUR = {
                '0': 'white',
                '1': 'lightgray',
                '2': 'lightskyblue',
                '9': 'gray',
                '10': 'white'
             }


class Touch():
    """handles everything touch keyboard related"""

    def __init__(self, _ktlpath, _scriptdir, _LT):
        """initialise touch class"""
        self.LT = _LT
        if not (_ktlpath.exists() and _ktlpath.is_file()):
            # panic
            print('Invalid kmnpath')
        else:
            self.ktlpath = Path(_ktlpath).with_suffix('.keyman-touch-layout')
            self.scriptdir = _scriptdir
            # if not (self.ktlpath.exists() and self.ktlpath.is_file()):
            #     # panic
            #     print('Invalid ktlpath')
            # else:
            # load k.kmn and k.kvks dicts
            self.ktl = json.loads(self.ktlpath.read_text(encoding='utf-8'))
            # self.kvks = _loadkvks(self.ktlpath.with_suffix('.kvks')
            #                                 .read_text(encoding='utf-8'))
            self.kvks = _loadkvks(str(self.ktlpath.with_suffix('.kvks').resolve()))
            self.kmn = dict()
            self.kmn = _loadkmn(self.ktlpath.with_suffix('.kmn').read_text(encoding='utf-8'))
            self.names = dict()
            self.uninames = dict()
            if Path('names.json').exists() and Path('names.json').is_file():
                self.uninames = json.loads(Path('names.json').read_text(encoding='utf-8'))
            #uninames = {'en-US':{'U+NNNN':'name of charater', ...}, /
            #         'pt-PT':{'u+nnnn':'name in portuguese', ...}, /
            #         'fr-FR':{U+NNNN:'nom en francais', ...}}
            self._makenames()
            self.chartables = dict()
            self._make_character_tables()
            self.device = ''
            self.welcomedir = Path(self.ktlpath.parent, 'welcome')
            self.helpdir = Path(self.ktlpath.parent, 'help')

    def create_help_for_devices(self):
        """creates help files for specified devices(list of strings)"""
        # create welcome dir if it doesn't exist and empty it if it does
        if self.welcomedir.exists():
            for afile in self.welcomedir.iterdir():
                afile.unlink()
        else:
            self.welcomedir.mkdir()
        # create help dir if it doesn't exist and empty it if it does
        if self.helpdir.exists():
            for afile in self.helpdir.iterdir():
                afile.unlink()
        else:
            self.helpdir.mkdir()
        # for each device create png files
        for device in self.ktl:
            self._make_layer_pngs(device)
        self._make_state_pngs()
        self._make_character_tables()
        lout = self._make_header()
        # add tabs for en, pt, fr
        devices = sorted(self.ktl.keys())
        lout.extend(self._add_lang_tab('\t\t\t', 'en-US', devices))
        lout.extend(self._add_lang_tab('\t\t\t', 'pt-PT', devices))
        lout.extend(self._add_lang_tab('\t\t\t', 'fr-FR', devices))
        lout.extend([
f'\t\t</div>',
f'\t</body>',
f'</html>',
f''])
        # now save welcome file
        Path(self.welcomedir, 'welcome.htm').write_text('\n'.join(lout),
                                                        encoding='utf-8')
        # copy css and pngs to welcome folder
        filelist = ['kb.css', 'latin.css', 'Harmattan.css', 'Scheherazade.css',
                    'splash.png']
        for afile in filelist:
            shutil.copy(Path(self.scriptdir.parent, 'fonts', afile),
                        Path(self.welcomedir, afile))
        stem = self.ktlpath.stem
        shutil.copy(Path(self.ktlpath.parent, stem + '.ico'),
                    Path(self.welcomedir, 'icon.ico'))
        shutil.copy(Path(self.ktlpath.parent, stem + '.png'),
                    Path(self.welcomedir, 'icon.png'))
        #crush pngs
        crush_pngs(self.welcomedir)

        # now make help php file!
        print("That's all folks!")

    def _makenames(self):
        """fills any missing names for all output in project(from kvks)
           any translated names need to be filled manually"""
        for state in self.kvks['states']:
            for vk in self.kvks['states'][state].keys():
                output = norm_output(self.kvks['states'][state][vk])
                self._add_bits_to_names(list_codepoints(output))
                nfd = normalize('NFD', output)
                if output != nfd:
                    self._add_bits_to_names(list_codepoints(nfd))

    def _add_bits_to_names(self, _bits):
        for bit in _bits:
            # for lang in ['en-US', 'pt-PT', 'fr-FR']:
            if bit not in self.names.keys():
                aname = CONTROLCHARS[bit.upper()] if bit.upper() in CONTROLCHARS.keys()\
                                                  else name(char_from_codepoint(bit))
                self.names[bit] = [char_from_codepoint(bit),
                                   category(char_from_codepoint(bit)),
                                   aname,
                                   '',
                                   '']

    def _make_layer_pngs(self, _device):
        """from ktl create png for each layer"""
        print("making layer pngs")
        # for each layer in ktl draw png
        # test device in ktl
        # [0] is always default latin font
        # [1] is complex or specific font if char not in font
        #     will fallback to latin font
        fontpaths = self._make_fontpaths(self.ktl[_device]['font'])
        abar = Image.open(Path(self.scriptdir.parent, 'fonts', "bar.png"))
        # # make output directory tdir
        # parts = self.welcomedir.parts
        # tdir = parts[0] + '/'.join(parts[1:])

        for layer in self.ktl[_device]['layer']:
            # name = f"{_device}-{layer['id']}"
            nosrows = len(layer['row'])
            # create backgound image
            # background is Black for touch with white keys
            background = round_rectangle((420, 42 * nosrows), 2, "black")
            # next_row_pos = (int(layer['row']['id']) - 1) * 42
            for arow in layer['row']:
                next_key_pos = 0
                this_row_pos = (int(arow['id']) - 1) * 42 + 1
                # so for each key in this row
                for akey in arow['key']:
                    next_key_pos += int(int(myget(akey, 'pad', '0')) * 40 / 100) + 1
                    key_width = int(int(myget(akey, 'width', '100')) * 40 / 100)
                    # load font
                    font = pick_font(akey.get("text", ""), fontpaths)
                    text = akey.get("text", "")
                    # create key image
                    # key colour depends on type of key
                    key = center_text((key_width, 40), font, text,
                                      KTL_COLOUR[akey.get('sp', '0')])
                    if "sk" in akey.keys():
                        key.paste(abar, (key_width - 13, 1), abar)
                    background.paste(key, (next_key_pos, this_row_pos), key)
                    next_key_pos += int(int(myget(akey, 'width', '100')) * 40 / 100) + 1
                    # make lp pngs
                    self._make_lp_pngs(_device, layer, akey, fontpaths, abar)
            # now output to temp file and compress to final
            background.save(self.welcomedir.__str__() + f"\\{_device}-{layer['id']}.png")
            # shrink_png(pout)

    def _make_lp_pngs(self, _device, _layer, _akey, _fontpaths, _bar):
        """make longpress pngs for this layer, only create spacebar
           once for all layers, assumes space lp common to all layers!"""
        # there is lp?
        if 'sk' in _akey.keys():
            if _akey['id'] == 'K_SPACE':
                filename = f"{_device}_lp_K_SPACE.png"
            else:
                filename = f"{_device}_lp_{_layer['id']}_{_akey['id']}.png"
            nos_lp = len(_akey['sk'])
            aw = int(myget(_akey, 'width', '100'))
            ew = int((aw if _akey['id'] != 'K_SPACE' else aw / 2.0) * 40 / 100)
            # ew is larger if K_SPACE and is same for all other keys
            # make background
            background = round_rectangle(((ew + 44 + (ew + 2) * nos_lp), 42), 2, "black")
            # initial key
            next_key_pos = 1
            font = pick_font(_akey.get("text", ""), _fontpaths)
            text = _akey.get("text", "")
            key = center_text((ew, 40), font, text, 'white')
            key.paste(_bar, (ew - 13, 1), _bar)
            background.paste(key, (next_key_pos, 1), key)
            # => key
            next_key_pos += ew + 2
            font = pick_font('=>', _fontpaths)
            key = center_text((40, 40), font, '=>', 'black')
            background.paste(key, (next_key_pos, 1), key)
            # rest of keys
            next_key_pos += 42
            for lp in _akey['sk']:
                font = pick_font(lp['text'], _fontpaths)
                key = center_text((ew, 40), font, lp['text'], 'white')
                background.paste(key, (next_key_pos, 1), key)
                next_key_pos += ew + 2
            # ouput lp png
            background.save(self.welcomedir.__str__() + '\\' + filename)

    def _make_fontpaths(self, _name):
        """return default latin font path and specific font path"""
        fontpaths = [
             Path(self.scriptdir.parent, 'fonts', FONTNAME['Andika Afr']),
             Path(self.scriptdir.parent, 'fonts',
                  FONTNAME[_name])]
        return fontpaths

    def _make_state_pngs(self):
        """from kvks create png for each state"""
        print("making state pngs")
        fontpaths = self._make_fontpaths(self.kvks['fontname'])

        # for each state in kvks draw png
        for state in self.kvks['states']:
            # draw background
            filename = f"\\state-{STATES[state]}.png"
            background = round_rectangle((620, 210), 2, "white")
            # now work through list of vk names and positions
            for row in VKEYS.keys():
                next_key_pos = 1
                next_row_pos = (int(row) - 1) * 42 + 1
                for key in VKEYS[row].keys():
                    # picking key widths and colour/type from lists.
                    key_colour = "black"
                    if key in ["K_BKSP", "K_TAB", "K_CAPS", "K_ENTER"]:
                        key_colour = "gray"
                    elif (key in ["K_LSHIFT", "K_RSHIFT"]) and ("S" in state):
                        key_colour = "lightskyblue"
                    elif (key in ["K_LCTRL", "K_RCTRL"]) and ("C" in state):
                        key_colour = "lightskyblue"
                    elif (key in ["K_LALT", "K_RALT"]) and ("A" in state):
                        key_colour = "lightskyblue"
                    else:
                        key_colour = "black"
                    # drawing eack key with text where present,
                    if key not in self.kvks['states'][state].keys():
                        self.kvks['states'][state][key] = ""
                    font = pick_font(self.kvks['states'][state][key],
                                     fontpaths)
                    text = self.kvks['states'][state][key]
                    akey = center_text((VKEYS[row][key], 40), font, text,
                                       key_colour if text else 'dimgray')
                    background.paste(akey, (next_key_pos, next_row_pos))
                    next_key_pos += VKEYS[row][key] + 2
            # background.show()
            background.save(Path(self.welcomedir).__str__() + filename)

    def _make_character_tables(self):
        """making char tables"""
        print("making char tables")
        for state in self.kvks['states']:
            for vk in self.kvks['states'][state].keys():
                if vk not in ['K_BKSP', 'K_TAB', 'K_CAPS', 'K_ENTER',
                              'K_LSHIFT', 'K_RSHIFT', 'K_LCTRL', 'K_LALT',
                              'K_RALT', 'K_RCTRL']\
                        and self.kvks['states'][state][vk]:
                    # a char or string of chars without placeholders
                    output = norm_output(self.kvks['states'][state][vk])
                    cat = category(output[0])
                    if cat not in self.chartables:
                        self.chartables[cat] = dict()
                    codepoints = codepoints_from_chars(output)
                    if codepoints not in self.chartables[cat].keys():
                        self.chartables[cat][codepoints] = \
                                                       {'display': '',
                                                        'nfc': '',
                                                        'nfd': ''}
                        self.chartables[cat][codepoints]['display'] = \
                            self.kvks['states'][state][vk]
                        nfd = normalize('NFD', output)
                        self.chartables[cat][codepoints]['nfc'] = codepoints
                        if output != nfd:
                            self.chartables[cat][codepoints]['nfd'] = \
                                                    codepoints_from_chars(nfd)

    def _add_lang_tab(self, _prefix, _lang, _devices):
        # add asst tables in _lang
        lang = _lang if _lang else 'en-US'
        print(f"making lang tab {lang}")
        langlist = sorted(list(self.LT.keys()))
        # pick the two keys not in lang
        print(f"\t from {langlist} by subtracting {lang}")
        l0id = langlist.index(lang)
        l0 = langlist.pop(l0id)
        # langlist = langlist.remove(lang)
        print(f"\t\tresult=>{langlist}<")
        l1 = langlist[0]
        l2 = langlist[1]

        # if lang in sorted(langlist) and len(sorted(langlist)) == 3:
        #     l1, l2 = sorted(langlist).remove(lang)
        # else:
        #     print(f"Arrgh, expecting three items in {sorted(self.LT.keys())}, or can't find {lang}")
        # if l1 == lang:
        #     l1 = l0
        # else:
        #     l2 = l1
        #     l1 = l0
        lout = [
f"{self.LT[lang]['<!--Starting lang-->']}",
f'<div id="{lang[:2]}" class="tab-content" lang="{lang[:2]}">',
f'\t<p><a class="buttonlang" href="#{l1[0:2]}">{self.LT[l1]["See this page in lang"]}</a>, <a class="buttonlang" href="#{l2[0:2]}">{self.LT[l2]["See this page in lang"]}</a></p>',
f'\t<div class="container col">',
f'\t\t<table class="compact">',
f'\t\t\t<tr class="compact">',
f'\t\t\t\t<td class="compact"><img src="splash.png" width="70" height="101"/></td>',
f'\t\t\t\t<td class="compact">&nbsp;&nbsp;&nbsp;</td>',
f'\t\t\t\t<td class="compact">',
f'\t\t\t\t\t<h1t style="text-align: center"> <strong>{self.kmn["NAME"]}:</strong> {self.kmn["MESSAGE"]}</h1t><br>',
f'\t\t\t\t\t<p>{self.LT[lang]["Created by SIL Senegal."]} {self.kmn["COPYRIGHT"]}</p>',
'\t\t\t\t</td>',
'\t\t\t\t<td class="compact">&nbsp;&nbsp;</td>',
'\t\t\t\t<td class="compact"style="text-align: center"><img src="icon.png" width="75" height="101"/></td>',
'\t\t\t</tr>',
'\t\t</table>']
        for device in _devices:
            lout.extend([
'\t\t<div class="wrap-collabsible">',
f'\t\t\t<input id="collapsible-{device}-touch-{lang[:2]}" class="toggle" type="checkbox">'])
            if device == 'phone':
                lout.append(
f'\t\t\t<label for="collapsible-{device}-touch-{lang[:2]}" class="lbl-toggle indent">{self.LT[lang]["Phone touch keyboard (Android, iOS)."]}</label>')
            else:
                lout.append(
f'\t\t\t<label for="collapsible-{device}-touch-{lang[:2]}" class="lbl-toggle indent">{self.LT[lang]["Tablet touch keyboard (Android, iOS)."]}</label>')
            lout.extend([
'\t\t\t<div class="collapsible-content">',
'\t\t\t\t<div class="content-inner">'])
            for alayer in DEVICE_PNGS:
                this_layer = f"layer_{alayer}"
                if Path(self.welcomedir, f"{device}-{alayer}.png").exists():
                    lout.extend([
f'\t\t\t\t\t<div class="container col">',
f'\t\t\t\t\t\t<header style=''font-family: "Andika Afr", andika, geneva, arial, helvetica, sans-serif;''>{}</header>'.format(self.LT[lang][this_layer]),
f'\t\t\t\t\t\t<div class="container col" id="{alayer}">',
f'\t\t\t\t\t\t\t<img src="{device}-{alayer}.png" alt="image for layer default" width="510" height="204">',
f'\t\t\t\t\t\t</div>',
f'\t\t\t\t\t</div>'])
                else:
                    pass
            lout.extend(self._add_lp_pngs('\t\t\t\t\t', device, lang))
        lout.extend([
f'\t\t\t\t</div>',
f'\t\t\t</div>'])
        lout.append(
f'\t\t</div>')
        # web and physical
        lout.extend(self._add_web_and_physical('\t\t', lang))
        # now add the char tables
        lout.extend(self._add_char_tables('\t\t', lang))
        lout.extend([
f'\t</div>',
f'</div>',
f"{self.LT[lang]['<!--Ending lang-->']}"])
        return [_prefix + item for item in lout]

    def _add_modifiers(self, _prefix, _lang):
        """add modifiers sequences"""
        lout = list()
        if self.kmn['modifiers']:
            lout.extend([
'<div class="container col">',
'\t<p style=''font-family: "Andika Afr", andika, geneva, arial, helvetica, sans-serif;''>{}</p>'.format(self.LT[_lang]["Modifier sequences..."])])
            for amod in sorted(self.kmn['modifiers'].keys()):
                # amod is 'U+NNNN' form
                modifier = chr(int(amod[2:], 16))
                for atup in sorted(self.kmn['modifiers'][amod]):
                    prior = chr(int(atup[0], 16))
                    output = ''
                    # assumes output in form 'U+NNNN'
                    for achar in atup[1].split():
                        output += chr(int(achar[2:], 16))
                    strout = f"'{prior}' + '{modifier}' => '{output}'"
                    style = 'font-family: "Andika Afr", andika, geneva, arial, helvetica, sans-serif;'
                    lout.append(
f"\t<p style='{style}'>\t{strout}</p>")
            lout.append(
'</div>')
        return [_prefix + item for item in lout]

    def _add_lp_pngs(self, _prefix, device, _lang):
        """add the lp pngs"""
        lout = list()
        if Path(self.welcomedir, f"{device}_lp_K_SPACE.png").exists():
            lout.extend([
'<div class="container col">',
'\t<p style=''font-family: "Andika Afr", andika, geneva, arial, helvetica, sans-serif;''>{}</p>'.format(self.LT[_lang]["On every layer..."]),
f'\t<img src="{device}_lp_K_SPACE.png" alt="image for layer default">',
'</div>'])
        for alayer in DEVICE_PNGS:
            this_layer = f"layer_{alayer}"

            lp_pngs = list()
            lp_pngs.extend(self.welcomedir.glob(f'{device}_lp_{alayer}_*.png'))
            if lp_pngs:
                lout.extend([
'<div class="container col">',
'\t<header style=''font-family: "Andika Afr", andika, geneva, arial, helvetica, sans-serif;''>{}</header>'.format(self.LT[_lang][this_layer])])
                for lp in lp_pngs:
                    lout.append(
f'\t<img src="{lp.name}" alt="image for {lp.stem}">')
                lout.append(
f'</div>')
        lout.extend(self._add_modifiers('', _lang))
        return [_prefix + item for item in lout]

    def _add_web_and_physical(self, _prefix, lang):
        """add web and physical layouts"""
        lout = [\
f'<div class="wrap-collabsible">',
f'\t<input id="collapsible-web-{lang[:2]}" class="toggle" type="checkbox">',
f'\t<label for="collapsible-web-{lang[:2]}" class="lbl-toggle indent">{self.LT[lang]["Layout for Web and physical"]}</label>',
f'\t<div class="collapsible-content">',
f'\t\t<div class="content-inner">',
f'\t\t\t<div class="container col">',
f'\t\t\t\t<p>{self.LT[lang]["A non-breaking space is indicated ..."]}</p>',
f'\t\t\t\t<table class="compact" style="text-align: left;">']
        for astate in range(0,8):
            if Path(self.welcomedir, f"state-{astate}.png").exists():
                lout.extend([\
f'\t\t\t\t\t<tr class="compact" style="text-align: left;">',
f'\t\t\t\t\t\t<td class="compact" style="text-align: left;">',
f'\t\t\t\t\t\t\t<p>{STATE[astate]}</p>',
f'\t\t\t\t\t\t\t<img src="state-{astate}.png" alt="default" width="638" height="210">',
f'\t\t\t\t\t\t</td>',
f'\t\t\t\t\t</tr>'])
        lout.extend([\
f'\t\t\t\t</table>',
f'\t\t\t</div>'])
        lout.extend(self._add_modifiers('\t\t\t', lang))
        lout.extend([\
f'\t\t</div>',
f'\t</div>',
f'</div>'])
        return [_prefix + item for item in lout]


    def _add_char_tables(self, _prefix, _lang):
        lout = [\
f'<div class="wrap-collabsible">',
f'\t<input id="collapsible-chars-{_lang[:2]}" class="toggle" type="checkbox">',
f'\t<label for="collapsible-chars-{_lang[:2]}" class="lbl-toggle indent">{self.LT[_lang]["Character tables"]}</label>',
f'\t<div class="collapsible-content">',
f'\t\t<div class="content-inner">',
f'\t\t\t<div class="container col">']
        ajami = 'ajami' in self.kmn['NAME']
        lout.extend(self._build_char_table('\t\t\t\t', ('Ll',), _lang, ajami))
        lout.extend(self._build_char_table('\t\t\t\t', ('Lu',), _lang, ajami))
        lout.extend(self._build_char_table('\t\t\t\t', ('Lo',), _lang, ajami))
        lout.extend(self._build_char_table('\t\t\t\t', ('Mc', 'Me', 'Mn'), _lang, ajami))
        lout.extend(self._build_char_table('\t\t\t\t', ('Pi', 'Pf'), _lang, ajami))
        lout.extend(self._build_char_table('\t\t\t\t', ('Ps', 'Pe'), _lang, ajami))
        lout.extend(self._build_char_table('\t\t\t\t', ('Sc', 'Sm', 'So', 'Pd', 'Pc'), _lang, ajami))
        lout.extend(self._build_char_table('\t\t\t\t', ('Sk', 'Lm'), _lang, ajami))
        lout.extend(self._build_char_table('\t\t\t\t', ('Zz',), _lang, ajami))
        lout.extend([\
f'\t\t\t</div>',
f'\t\t</div>',
f'\t</div>',
f'</div>'])
        return [_prefix + item for item in lout]


    def _make_header(self):
        header = [
'<!DOCTYPE html>',
'<html lang="en">',
'\t<head>',
'\t\t<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>',
'\t\t<meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=2.0, minimum-scale=0.5" name="viewport"/>',
'\t\t<title>{}</title>'.format(self.kvks['kbdname']),
'\t\t<link rel="stylesheet" href="kb.css"/>',
'\t\t<link rel="stylesheet" href="latin.css"/>']
        if 'ajami' in self.kvks['kbdname']:
            if 'Harmattan' in self.kvks['fontname']:
                header.append(\
'\t\t<link rel="stylesheet" href="Harmattan.css"/>')
            elif 'Scheherazade' in self.kvks['fontname']:
                header.append(
'\t\t<link rel="stylesheet" href="Scheherazade.css"/>')
        header.extend([
'\t\t<link rel="icon" href="icon.ico"/>',
'\t</head>',
'\t<body>',
'\t\t<div class="tab-folder">'])
        return header

    def _build_char_table(self, _prefix, _cats, _lang, _ajami=False):
        """_cats holds list of char categories, returns
        list of strings holding html for char table"""
        lout = list()
        aname = '-'.join(_cats)
        if True in [True for cat in _cats if cat in self.chartables.keys()]:
            lout.extend([
f'<div class="wrap-collabsible">',
f'\t<input id="{_lang}-{"-".join(_cats)}-Character" class="toggle" type="checkbox">',
f'\t<label for="{_lang}-{"-".join(_cats)}-Character" class="lbl-toggle indent">{self.LT[_lang][aname]}</label>',
f'\t<div class="collapsible-content">',
f'\t\t<div class="content-inner">',
f'\t\t\t<div class="container col">',
f'\t\t\t\t<table>',
f'\t\t\t\t\t<tr>',
f'\t\t\t\t\t\t<th>Character</th>',
f'\t\t\t\t\t\t<th>NFC</th><th>Unicode Name</th>',
f'\t\t\t\t\t\t<th>NFD</th><th>Unicode Name</th>',
f'\t\t\t\t\t</tr>'])

            # chart = dict()
            chart = list()
            for cat in _cats:
                if cat in self.chartables.keys():
                    for o in self.chartables[cat].keys():
                        display = self.chartables[cat][o]['display']
                        # display = display
                        nfc = self.chartables[cat][o]['nfc'] \
                                if display not in LOOKUP else LOOKUP[display]
                        if nfc not in list(self.uninames[_lang].keys()):
                            nfcname = myname(nfc)
                        else:
                            nfcname = self.uninames[_lang][nfc]
                        nfd = self.chartables[cat][o]['nfd'] \
                                if display not in LOOKUP else ''
                        if nfd not in list(self.uninames[_lang].keys()):
                            nfdname = myname(nfd)
                        else:
                            nfdname = self.uninames[_lang][nfd]
                        withit = nfcname.find('WITH')
                        if nfd:
                            sortkey = (nfdname, '')
                        elif withit > 0:
                            sortkey = (nfcname[:withit].strip(), nfcname[withit + 4:].strip())
                        else:
                            sortkey = (nfcname, '')
                        chart.append((display, nfc, nfcname, nfd, nfdname,
                                     sortkey))
            for o in sorted(chart, key=lambda x: x[5]):
                font_size = '120%' if not _ajami else '26pt'
                lout.extend([
f'\t\t\t\t\t<tr>',
f'\t\t\t\t\t\t<td style="font-size: {font_size};">{escape(o[0])}</td>',
f'\t\t\t\t\t\t<td>{o[1]}</td>',
f'\t\t\t\t\t\t<td>{o[2]}</td>', \
f'\t\t\t\t\t\t<td>{o[3]}</td>',
f'\t\t\t\t\t\t<td>{o[4]}</td>',
f'\t\t\t\t\t</tr>'])
            lout.extend([\
f'\t\t\t\t</table>',
f'\t\t\t</div>',
f'\t\t</div>',
f'\t</div>',
f'</div>'])
        return [_prefix + item for item in lout]

def crush_pngs(_dir):
    """crush all pngs in Path _dir"""
    # pngs = sorted([p for p in self.welcomedir.glob('*.png')])
    saved = 0
    print(f"Crushing {sum(1 for x in _dir.glob('*.png') if x.is_file())} pngs")
    for png in _dir.glob('*.png'):
        saved += crush_a_png(png)
    print(f"Saved {int(saved/1024 + 0.5)}Kb")

def crush_a_png(_pin):
    """crush the png at _pin"""
    saved = 0
    pout = Path(_pin.parent, 'temp.png')
    was = _pin.stat().st_size
    completed = subprocess.run(['pngcrush_1_8_11_w64.exe', '-brute', _pin.resolve(), pout.resolve() ], check=False)
    if completed:
        _pin.unlink()
        wis = pout.stat().st_size
        pout.rename(_pin.resolve())
        saved = (was - wis)
        print(f"Crushed {_pin.name} by {int(saved/was * 100 + 0.5)}%")
    elif pout.exists():
        pout.unlink()
        saved = 0
    return saved

def norm_output(_astr):
    """unescapes ay chars and placeholders and oupt normalized to nfc"""
    output = unescape(_astr)
    # if length of output > 1 and initial char is dotted ring
    # or tatwell, lose first char
    if len(output) > 1 and ord(output[0]) in [0x25cc, 0x0640]:
        output = output[1:]
    # now have string of chars which may contain placeholder
    # (e.g. ESC, NBSP, etc...)
    if output in PLACEHOLDERS.keys():
        output = PLACEHOLDERS[output]
    return normalize('NFC', output)


def _loadkvks(_kvksfile):
    root = objectify.parse(_kvksfile).getroot()
    kvks = dict()
    kvks['kbdname'] = root.header.kbdname.text
    kvks['encoding'] = root.encoding.attrib['name']
    kvks['fontname'] = root.encoding.attrib['fontname']
    kvks['fontsize'] = root.encoding.attrib['fontsize']
    kvks['states'] = dict()
    for layer in root.encoding.iterchildren():
        state = layer.attrib['shift'] if layer.attrib['shift'] else "default"
        if state not in kvks:
            kvks['states'][state] = dict()
        for key in layer.iterchildren():
            vkey = key.attrib['vkey']
            # text is utf-8 characters and or html escape codes
            kvks['states'][state][vkey] = key.text
        if 'K_oE2' not in [k.attrib['vkey'] for k in layer.iterchildren()]:
            kvks['states'][state]['K_oE2'] = ""
        if 'K_SPACE' not in [k.attrib['vkey'] for k in layer.iterchildren()]:
            kvks['states'][state]['K_SPACE'] = " "
        kvks['states'][state]['K_BKSP'] = "*Backspace*"
        kvks['states'][state]['K_TAB'] = "*Tab*"
        kvks['states'][state]['K_CAPS'] = "*Caps*"
        kvks['states'][state]['K_ENTER'] = "*Enter*"
        kvks['states'][state]['K_LSHIFT'] = "*Shift*"
        kvks['states'][state]['K_RSHIFT'] = "*Shift*"
        kvks['states'][state]['K_LCTRL'] = "Ctrl"
        kvks['states'][state]['K_LALT'] = "Alt"
        kvks['states'][state]['K_RALT'] = "Alt/AltGr"
        kvks['states'][state]['K_RCTRL'] = "Ctrl"
    return kvks


def _loadkmn(_kmnstr):
    """loads kmn to dict, assumes physical layaout NOT mneumonic
       assumes all outputs expessed as string of codepoints"""
    kmn = dict()
    kmn['modifiers'] = dict()
    lines = _kmnstr.splitlines()
    for aline in lines:
        gotstore = re.findall(STORE_AND, aline)
        gotstroke = re.findall(KEYSTROKE, aline)
        if gotstore:
            kmn[gotstore[0][0].strip()] = gotstore[0][1].strip()
        elif gotstroke:
            output = gotstroke[0][1].strip()
            if len(output.split()) == 1:
                # multi char output not modifier so ignored
                kmn[gotstroke[0][0].strip()] = output
    # now scan for modifier sequences
    for aline in lines:
        gotmodifier = re.findall(MODIFIER, aline)
        if gotmodifier:
            # assume all modifier sequences listed after all keystrokes!
            prior = gotmodifier[0][0].strip()
            # find U+NNNN code for modifier key
            modifier = kmn[gotmodifier[0][1].strip()]
            output = gotmodifier[0][2].strip()
            if not  kmn['modifiers'].get(modifier, ""):
                kmn['modifiers'][modifier] = list()
            kmn['modifiers'][modifier].append((prior, output))
    return kmn


def chars_from_codepoint(_code):
    """return string of chars from string of codepoints"""
    result = ''
    if _code.isinstance('str'):
        # convert string to list
        bits = _code.split()
    else:
        # assume is list
        bits = _code
    for bit in bits:
        if 'U+' in bit[0:2]:
            result += chr(int(bit[2:6], 16))
    return result


def char_from_codepoint(_code):
    """return string of a single char from string of a single codepoint"""
    return chr(int(_code[2:6], 16))


def codepoints_from_chars(_chars):
    """return list of codepoints for chars in string"""
    return ' '.join(list_codepoints(_chars))


def list_codepoints(_astr):
    """lists the codeponts in string"""
    result = list()
    for achar in _astr:
        result.append('U+{:04X}'.format(ord(achar)))
    return result


def round_corner(radius, fill):
    """Draw a round corner"""
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner


def round_rectangle(size, radius, fill):
    """Draw a rounded rectangle"""
    # make x8 size key and resize antialiased to x1?
    width, height = size
    rectangle = Image.new('RGBA', size, fill)
    corner = round_corner(radius, fill)
    rectangle.paste(corner, (0, 0), corner)
    # Rotate the corners and paste them
    rectangle.paste(corner.rotate(90), (0, height - radius), corner)
    rectangle.paste(corner.rotate(180), (width - radius, height - radius), corner)
    rectangle.paste(corner.rotate(270), (width - radius, 0), corner)
    return rectangle


def center_text(_size, _fontpath, _text, _key_background):
    """returns image with text resized to fit with chosen font
       _size is (width,height) to fit text in
       _fontpath is string
       _text is the text
       _key_background is background colour for key
       font colour needs to be decided for max contrast"""
    text = normalize("NFC", _text)
    width, height = _size
    widthx = width * 8
    heightx = height * 8
    im = round_rectangle((widthx, heightx), 2 * 8, _key_background)  # if _text else 'gray')
    if not _text:
        pass
    elif _text in DRAWIT.keys():
        im = DRAWIT[text](im, widthx, heightx, _key_background)
    elif len(text) == 2 and combining(text[-1]) > 0:
        image1, fudge_it = draw_text(im, _fontpath, widthx, heightx, text[0],
                                     _key_background, 0)
        image2, fudge_it = draw_text(im, _fontpath, widthx, heightx, text[1],
                                     _key_background, fudge_it)  # fudge_it)
        im = Image.blend(image1, image2, 0.5)
    else:
        ts = text.strip('*') if len(text) > 1 else text
        im, _ = draw_text(im, _fontpath, widthx, heightx, ts, _key_background, 0)
    return im.resize((width, height), Image.LANCZOS)


def draw_text(image, _fontpath, width, height, _text, _key_background, _fudge_it=(0, 0)):
    """draw text and return image and (x offset, y offset)"""
    draw = ImageDraw.Draw(image)
    # default_font_size = 40
    # _fontpath is string
    font = ImageFont.truetype(_fontpath.resolve().as_posix(), size=40)
    font_ascent, font_descent = font.getmetrics()
    # what about empty string?
    x_scale = width / font.getlength(_text) if font.getlength(_text) > 0 else 9999999999
    y_scale = height / (font_ascent + font_descent)
    scale = x_scale if x_scale < y_scale else y_scale
    # font_size = int(40 * scale)
    x_offset = int((width - font.getlength(_text) * scale) / 2.0)
    y_offset = int((height - (font_ascent + font_descent) * scale) / 2.0)
    if _text[0] == '\u0303':
        x_offset += _fudge_it[0]
        y_offset -= _fudge_it[1]
    if _text[0] == '\u0325':
        x_offset += _fudge_it[0] * 2
    font = ImageFont.truetype(_fontpath.resolve().as_posix(), size=int(40 * scale))
    # how to auto size font to fit, enlarge/reduce???
    # font height likely determining factor
    if _key_background in ["black", "gray"]:
        # white full opacity
        text_colour = (255, 255, 255, 255)
    else:
        # black full opacity
        text_colour = (0, 0, 0, 255)
    draw.text((x_offset, y_offset), _text, fill=text_colour,
                  font=font)
    yoff = int(font.getsize(_text)[1] / 5) if _text[0] in ['W', 'H', 'h'] else 0
    if _text[0] in ['L', 'W', 'w']:  # 'l',
        xoff = int(font.getlength(_text) / 3.0)
    else:
        xoff = int(font.getlength(_text) / 2.0)
    return image, (xoff, yoff)


def pick_fill(_key_background):
    """pick rgba colour"""
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    return black if _key_background in ['white', 'lightgray', 'lightskyblue'] else white


def draw_backarrow(_image, _width, _height, _key_background):
    """draws backarrow on black background and box plus cross on white"""
    im = ImageDraw.Draw(_image)
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    fill = pick_fill(_key_background)
    if _key_background != 'lightgray':
        scalex = _width / 70.0
        scaley = _height / 40.0
        poly = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["backarrow"]]
        im.polygon(poly, fill=fill)
        poly = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["backarrowi"]]
        im.polygon(poly, fill=_key_background)
    else:
        scalex = _width / 100.0
        scaley = _height / 40.0
        poly = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["box"]]
        im.polygon(poly, fill=black)
        width = int(2 * scaley) if scaley > 1 else 2
        line = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["xline1"]]
        im.line(line, fill=white, width=width)
        line = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["xline2"]]
        im.line(line, fill=white, width=width)
    return _image


def draw_enter(_image, _width, _height, _key_background):
    """draws enter arrow"""
    im = ImageDraw.Draw(_image)
    # white = (255,255,255,255)
    # black = (0,0,0,255)
    fill = pick_fill(_key_background)
    scalex = _width / 100.0
    scaley = _height / 40.0
    poly = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["enterarrow"]]
    im.polygon(poly, fill=fill)
    poly = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["enterarrowi"]]
    im.polygon(poly, fill=_key_background)
    return _image


def draw_tab(_image, _width, _height, _key_background):
    """draws enter arrow"""
    im = ImageDraw.Draw(_image)
    # white = (255,255,255,255)
    # black = (0,0,0,255)
    fill = pick_fill(_key_background)
    scalex = _width / 52.0
    scaley = _height / 40.0
    poly = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["smallarrow"]]
    im.polygon(poly, fill=fill)
    # poly  = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["smallarrowi"]]
    # im.polygon(poly, fill=_key_background)
    poly = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["smallbar"]]
    im.polygon(poly, fill=fill)
    # now flip and drop
    poly = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["smallarrow2"]]
    im.polygon(poly, fill=fill)
    # poly  = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["smallarrow2i"]]
    # im.polygon(poly, fill=_key_background)
    poly = [(int(x * scalex), int(y * scaley)) for x, y in SHAPES["smallbar2"]]
    im.polygon(poly, fill=fill)
    return _image


def draw_shift(_image, _width, _height, _key_background):
    """draws shift arrow"""
    im = ImageDraw.Draw(_image)
    # white = (255,255,255,255)
    # black = (0,0,0,255)
    fill = pick_fill(_key_background)
    offx = int((_width - 320) / 2)
    # scalex = _width / 40.0
    scaley = _height / 40.0
    poly = [(int(x * scaley) + offx, int(y * scaley)) for x, y in SHAPES["broadarrow"]]
    im.polygon(poly, fill=fill)
    poly = [(int(x * scaley) + offx, int(y * scaley)) for x, y in SHAPES["broadarrowi"]]
    im.polygon(poly, fill=_key_background)
    return _image


def draw_caps(_image, _width, _height, _key_background):
    """draws caps lock arrow and bar"""
    im = ImageDraw.Draw(_image)
    # white = (255,255,255,255)
    # black = (0,0,0,255)
    offx = int((_width - 320) / 2.0)
    fill = pick_fill(_key_background)
    # scalex = _width / 40.0
    scaley = _height / 40.0
    poly = [(int(x * scaley) + offx, int(y * scaley)) for x, y in SHAPES["broadarrow"]]
    im.polygon(poly, fill=fill)
    poly = [(int(x * scaley) + offx, int(y * scaley)) for x, y in SHAPES["broadarrowi"]]
    im.polygon(poly, fill=_key_background)
    poly = [(int(x * scaley) + offx, int(y * scaley)) for x, y in SHAPES["broadbar"]]
    im.polygon(poly, fill=fill)
    return _image


def draw_globe(_image, _width, _height, _key_background):
    """draws caps lock arrow and bar"""
    im = ImageDraw.Draw(_image)
    # white = (255,255,255,255)
    # black = (0,0,0,255)
    fill = pick_fill(_key_background)
    im.ellipse(SHAPES['circle'], outline=fill)
    # crosshairs vertical
    im.line(SHAPES['dia'], fill=fill, width=1, joint='curve')
    # arc left
    im.arc(SHAPES['arc'][0], SHAPES['arc'][1], SHAPES['arc'][2])
    # arc right
    im.arc(SHAPES['arc'][0], SHAPES['arc'][2], SHAPES['arc'][1])
    line = ((SHAPES['dia'][0][1], SHAPES['dia'][0][0]), (SHAPES['dia'][1][1], SHAPES['dia'][1][0]))
    # crosshairs horizontal
    im.line(line, fill=fill, width=1, joint='curve')
    # arcs
    # upper
    im.arc(line, SHAPES['arc'][1] + 90, (SHAPES['arc'][2] + 90) % 360)
    # lower
    im.arc(line, SHAPES['arc'][1] - 90, SHAPES['arc'][2] - 90)
    return _image


DRAWIT = {
          '*Backspace*': draw_backarrow,
          '*BkSp*': draw_backarrow,
          '*Tab*': draw_tab,
          '*Shift*': draw_shift,
          '*Caps*': draw_caps,
          '*Enter*': draw_enter,
          '*Menu*': draw_globe
         }


def _states(astr):
    result = ''
    if 'SHIFT' in astr:
        result += 'S'
    if 'CTRL' in astr:
        result += 'C'
    if 'ALT' in astr:
        result += 'A'
    return result


def myget(_adict, _akey, _default):
    """my version of dict.get()"""
    if _akey in _adict.keys() and _adict[_akey]:
        result = _adict[_akey]
    else:
        result = _default
    return result


def pick_font(_text, _fontpaths):
    """if any non latin font chars pick fp[1]
       else pick fp[0]"""
    these_chars = {ord(c) for c in _text}
    if AJAMI.intersection(these_chars) \
        or HEBREW.intersection(these_chars) \
            or GREEK.intersection(these_chars):
        font = _fontpaths[1]
    else:
        font = _fontpaths[0]
    return font


def text_direction(_text):
    """returns rtl if any ajami or hebrew chars"""
    these_chars = {ord(c) for c in _text}
    if AJAMI.intersection(these_chars) \
            or HEBREW.intersection(these_chars):
        adir = 'rtl'
    else:
        adir = 'ltr'
    return adir

def myname(_str):
    """returns Unicode name for list of code points"""
    output = list()
    chrlst = _str.split()
    for achr in chrlst:
        if achr in REVERSE:
            # print(f"Codepoint {achr} is: ")
            # print(f"\t\t{REVERSE[achr.upper()]}")
            output.append(REVERSE[achr.upper()])
        else:
            # print(f"Codepoint {achr} is: ")
            # print(f"\t\t{name(chr(int(achr[2:], 16)))}")
            output.append(name(chr(int(achr[2:], 16))))
    return ', '.join(output)
