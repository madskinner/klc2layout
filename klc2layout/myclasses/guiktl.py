# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 04:37:05 2017

@author: marks
"""
# pylint: disable=C0301,C0103,W1309
# import sys
# import fnmatch
import os
import platform
import webbrowser

# import codecs
# from urllib.parse import urlparse
import json
# import re
from tkinter import font, Tk, filedialog, messagebox, StringVar, \
                    IntVar, FALSE, Menu
from tkinter.ttk import Button, Frame, Label, Style, \
                        Combobox, Notebook, Progressbar  # \

# from PIL import Image, ImageTk
from pathlib import Path
# from unidecode import unidecode

from .myconst.therest import KTL_VERSION
# from .myconst.tags import SET_TAGS, TRIM_TAG
from .tooltip import CreateToolTip
from .touch import Touch
# from .klc import Klc
# from .pkl import write_ini
# from .kmn import kmn_it


def get_script_directory():
    """return path to current script"""
    return os.path.dirname(__file__)


SCRIPT_DIR = get_script_directory()


class GuiKtl(Tk):
    """Handle the graphical interface for ktl2help and most of the logic"""

    def __init__(self, parent):
        """initialize the GuiCore"""
        Tk.__init__(self, parent)
        self.parent = parent
        self._initialize_variables()
        # with open('LOCALIZED_TEXT.json', 'r') as f:
        #     self.LT = json.load(f)
        lines = Path('LOCALIZED_TEXT.json').read_text(encoding='utf-8')
        self.LT = json.loads(lines)
        langs = sorted(list(self.LT.keys()))
        self.INTERFACE_LANGS = langs
        lang = 'en-US'
        self._initialize_main_window_menu(lang)
        self._initialize_main_window_notebook(lang)
        self._initialize_main_window(lang)
        if platform.system() not in ['Windows', 'Linux']:
            # so on f0, the Project tab…
            messagebox.showwarning(
                  'Warning', "Help I've been kidnaped by {platform.system()}!!!")

        self._initialize_f7(lang)  # make keyman files and help docs

        ktl2help_styles = Style()
        ktl2help_styles.configure('lowlight.TButton',
                                  font=('Sans', 8, 'bold'),)
        ktl2help_styles.configure('highlght.TButton',
                                  font=('Sans', 11, 'bold'),
                                  background='white', foreground='#007F00')
        ktl2help_styles.configure('wleft.TRadiobutton',
                                  anchor='w', justify='left')

    def _initialize_variables(self):
        """initialize variables for GuiCore"""
        self.font = font.Font()
        self.script_dir = SCRIPT_DIR
        self.klcfiles = list()

        self.int_var = IntVar()
        self.current_project = StringVar()
        self.currentSrcDir = StringVar()
        self.selected_lang = StringVar()
        self.currentEntry = StringVar()
        self.set_field = StringVar()
        self.spklDir = StringVar()
        self.kmflDir = StringVar()
        self.f7ktl = StringVar()
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar)
        self.helpmenu = Menu(self.menubar)

    def _initialize_main_window_menu(self, lang='en-US'):
        """initialize the menubar on the main window"""

        self.option_add('*tearOff', FALSE)
        self.config(menu=self.menubar)
        self.menubar.add_cascade(label=self.LT[lang]['File'],
                                 menu=self.filemenu)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=self.LT[lang]['Exit'],
                                  command=self.quit)

        self.menubar.add_cascade(label=self.LT[lang]['Help'],
                                 menu=self.helpmenu)
        self.helpmenu.add_command(label=self.LT[lang]['Read Me'],
                                  command=self._on_read_me)
        self.helpmenu.add_command(label=self.LT[lang]['About...'],
                                  command=on_copyright)

    def _initialize_main_window_notebook(self, lang):
        """initializes notebook widget on main window"""
        # self.n = Notebook(self, width=1400)
        # notebook
        self.n = Notebook(self, width=1015)
        self.n.grid(column=0, columnspan=7, row=1, padx=5, pady=5, sticky='ew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.n.grid_rowconfigure(0, weight=1)
        self.n.grid_columnconfigure(0, weight=1)
        self.f7 = Frame(self.n)
        self.n.add(self.f7, text=self.LT[lang]['Make help files'])

    def _initialize_main_window(self, lang='en-US'):
        """ initialize the main window"""

        self.f_1 = Frame(self)
        self.f_1.grid(column=0, row=0, sticky='news')
        self.f_1.grid_rowconfigure(0, weight=0)
        self.f_1.grid_columnconfigure(0, weight=0)
        # in top of window
        self.lblGuiLanguage = Label(self.f_1,
                                    text=self.LT[lang]['0InterfaceLanguage>'])
        self.lblGuiLanguage.grid(column=4, row=0, padx=5, pady=5, sticky='e')
        self.lblGuiLanguage['justify'] = 'right'
        # Create and fill the dropdown ComboBox.
        self.ddnGuiLanguage = Combobox(self.f_1,
                                       textvariable=self.selected_lang)
        self.ddnGuiLanguage.grid(column=5, columnspan=1, row=0,
                                 padx=5, pady=5, sticky='w')
        self.ddnGuiLanguage['text'] = 'Interface language:'
        self.ddnGuiLanguage['justify'] = 'left'
        self.ddnGuiLanguage.bind('<<ComboboxSelected>>', self._change_lang)
#        self.ddnGuiLanguage['values'] = [self.INTERFACE_LANGS['langs'][k] \
#                                for k in sorted(self.INTERFACE_LANGS['langs'])]
        self.ddnGuiLanguage['values'] = self.INTERFACE_LANGS
        self.ddnGuiLanguage.set(self.INTERFACE_LANGS[0])

#        self.lblMode = Label(self.f_1, text=self.LT[lang]['Mode>'])
#        self.lblMode.grid(column=6, row=0, padx=5, pady=5, sticky='e')

        # assumes tab based interface
        # main frame holds gui interface lange pull down, lists current project,
        # and save settings button

        self.progbar = Progressbar(self, maximum=100, variable=self.int_var)
        self.progbar.grid(column=0, row=6, columnspan=8, padx=5, pady=5,
                          sticky='news')
        self.status = Label(self, text=self.LT[lang]['empty string'],
                            anchor='w', justify='left')
        self.status.grid(column=0, row=7, columnspan=8, padx=5, pady=5,
                         sticky='news')

    def _initialize_f7(self, lang):
        """initialize Make/Remake help files tab from project ktl/kmn/kvks.
           Has text box and browse button to ktl file,
           plus OK - Make/Remake help files, creating any necessary folders.
           All help files created relative to position of ktl file.
           A common file name and location assumed for
           ktl, kmn and kvks files, only the extensions differ."""
        self.lblf7Intro = Label(self.f7,
                                text=self.LT[lang]["f7Intro"],
                                    anchor='w', justify='left')  # , wraplength=600)
        self.lblf7Intro.grid(column=0, row=0,
                                 columnspan=4, padx=5, pady=5, sticky='news')
        # Source Directory -label, entrybox, browse button
        self.lblf7ktl = Label(self.f7,
                              text=self.LT[lang]['f7ktl'],
                              anchor='w', justify='left')
        self.lblf7ktl.grid(column=0, row=1, columnspan=1, padx=5, pady=5,
                           sticky='w')
        self.lblf7ktlfile = Label(self.f7, textvariable=self.f7ktl,
                                  anchor='w', justify='left')
        self.lblf7ktlfile.grid(column=1, row=1, columnspan=2, padx=5, pady=5,
                               sticky='w')
        self.btnf7Browse = Button(self.f7, text="...",
                                  command=self._on_f7_browse,
                                  style='highlight.TButton')
        self.btnf7Browse.grid(column=3, row=1, padx=5, pady=5, sticky='news')
        self.btnf7Browse_ttp = CreateToolTip(self.f7,
                                             self.LT[lang]['f7Browse_ttp'])

        self.btnf7MakeHelp = Button(self.f7,
                                     text=self.LT[lang]["Make help files"],
                                     command=self._on_f7_make_help,
                                     style='highlight.TButton')
        self.btnf7MakeHelp.grid(column=2, row=20, columnspan=2, padx=5, pady=5,
                                                                 sticky='news')

    def _on_f7_browse(self):
        """browse to ktl file and load path into self.f7ktl"""
        lang = self.ddnGuiLanguage.get()
        self.f7ktl.set(filedialog.askopenfilename(
                         initialdir=os.path.expanduser('~/Documents/Keyman Developer/Projects'),
                         title=self.LT[lang]["SelectKTLfile"],
                         filetypes=(('keyman file', '*.keyman-touch-layout'),
                                    ("all files", "*.*"))))

    def _on_f7_make_help(self):
        """makes keyman help files"""
        touch = Touch(Path(self.f7ktl.get()), Path(SCRIPT_DIR), self.LT)
        touch.create_help_for_devices()

    def _on_read_me(self):
        """calls the appropriate 'help' file from the menubar"""

        lang = self.ddnGuiLanguage.get()
        app_dir = get_script_directory()
        # open an HTML file on my own computer
        if lang == 'en-US':
            url = os.path.normpath("file://" + app_dir + "/Read_Me.html")
        elif lang == 'fr-FR':
            url = os.path.normpath("file://" + app_dir + "/Lire_Moi.html")
        elif lang == 'pt-PT':
            # need portugese version, default to eng
            url = os.path.normpath("file://" + app_dir + "/Read_Me.html")
        else:
            messagebox.showwarning('Warning',
f"Error in on_read_me: {lang} is unrecognised lang, defaulting to 'en-US.'")
            url = os.path.normpath("file://" + app_dir + "/Read_Me.html")
        webbrowser.open(url)

    def _change_lang(self, lang):
        '''change lang of labels to interfacelang'''

        self.menubar.entryconfig(0, label=self.LT[lang]['File'])
        self.menubar.entryconfig(1, label=self.LT[lang]['Help'])

        self.filemenu.entryconfig(0,
                                  label=self.LT[lang]['Load project settings'])
        self.filemenu.entryconfig(1, label=self.LT[lang]['Save'])
        self.filemenu.entryconfig(2,
                                  label=self.LT[lang]['Delete project settings'])
        self.filemenu.entryconfig(4, label=self.LT[lang]['Exit'])

        self.helpmenu.entryconfig(0, label=self.LT[lang]['Read Me'])
        self.helpmenu.entryconfig(1, label=self.LT[lang]['About...'])

        self.lblGuiLanguage['text'] = \
                           self.LT[lang]['Interface language>']
        self.lblProject['text'] = self.LT[lang]['Current Project>'] + \
                                               ' ' + self.ddnCurProject.get()
        self.lblMode['text'] = ''.join([self.LT[lang]['Mode>'],
                                        self.LT[lang]["Simple"
                                                      if self.mode.get() == 0
                                                             else "Advanced"]])
        self.lblCurTemplate_ttp['text'] = self.LT[lang]['CurTemplate_ttp']
        self.lblCurTemplate['text'] = self.LT[lang]['UseTemplate>']
        self.btnCreateTemplate['text'] = self.LT[lang]["CreateTemplate"]

        self.btnSavePref['text'] = self.LT[lang]["SavePref"]

        self.boxOptional['text'] = self.LT[lang]["Optional"]
        self.lblInitialDigit['text'] = self.LT[lang]['InitialDigit']

        self.lblIdiot['text'] = self.LT[lang]['IdiotMode']
        self.rdbIdiot['text'] = self.LT[lang]['Simple']
        self.rdbAdvanced['text'] = self.LT[lang]['Advanced']
        self.f0_ttp['text'] = self.LT[lang]['f0_ttp']

        self.lblLatin1['text'] = self.LT[lang]["AddLatin1Example"]
        self.btnF2Next['text'] = self.LT[lang]["Next"]

        self.lblM0['text'] = self.LT[lang]['M0_ttp']
        self.lblM2['text'] = \
                  self.LT[lang]['M2_ttp1' if self.mode.get() == 1
                                                 else 'M2_ttp']
        self.lblArt['text'] = self.LT[lang]["Art_ttp"]
        self.lblCurProject['text'] = self.LT[lang]['Current Project>']
        self.btnBuildOutputTo['text'] = self.LT[lang]['Output to>']
        self.lblTrimTitle['text'] = self.LT[lang]['TrimTitle_ttp']
        self.box0['text'] = self.LT[lang]["and/or"]
        self.box1['text'] = self.LT[lang]['Adjust order of files']
        self.box2['text'] = self.LT[lang]['As needed']
        self.box1M1['text'] = self.LT[lang]['Change indent']
        self.box2M1['text'] = self.LT[lang]['Change order']
        self.labelf1['text'] = self.LT[lang]['labelf1']


def on_copyright():
    """displays the copyright info when called from menubar"""
    messagebox.showinfo(f"ktl2help v{KTL_VERSION}",
                        "\n".join(["©2019 SIL International",
                                   "License: MIT license",
                                   "Web: https://www.silsenelgal.org",
                                   "Email: Academic_Computing_SEB@sil.org",
                                   "", ""]))


def get_rid_of_multiple_spaces(tin):
    '''replace multiple spaces with single space and strip leading and
    trailing spaces'''
    return ' '.join(tin.strip().split())


def de_hex(tin):
    '''turn hex string to int and return string'''
    t = tin
    tout = ''
    i = 0
    while i < len(tin):
        if (len(tin) - i) > 5 and is_hex(tin[i: i + 6]):
            tout += chr(int(t[i:i + 6], 16))
            i += 6
        else:
            tout += tin[i]
            i += 1
    return tout


def is_hex(s):
    '''return true if string is hex value'''
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def to_alpha(anumber):
    """Convert a positive number n to its digit representation in base 26."""
    output = ''
    if anumber == 0:
        pass
    else:
        while anumber > 0:
            anumber = anumber - 1
            output += chr(anumber % 26 + ord('A'))
            anumber = anumber // 26
    return output[::-1]


def empty_the_dir(top):
    '''remove files and folders from the bottom of the tree upwards'''
    for _, dirs, files, rootfd in os.fwalk(top, topdown=False):
        _ = [os.remove(name, dir_fd=rootfd) for name in files]
        _ = [os.rmdir(name, dir_fd=rootfd) for name in dirs]


def folder_size(top):
    '''return size used by folder in bytes'''
    this_folder_size = 0
    for (path, _, files) in os.walk(top):
        for file in files:
            filename = os.path.join(path, file)
            this_folder_size += os.path.getsize(filename)
    return this_folder_size


def forward_slash_path(apath):
    '''replace all backslashes with forward slash'''
    return '/'.join(apath.split('\\'))


def sort_key_for_filenames(filename):
    """dummy sort key"""
    return filename
