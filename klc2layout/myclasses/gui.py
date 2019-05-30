# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 04:37:05 2017

@author: marks
"""
#import sys
import fnmatch
import os
import platform
import webbrowser
#import queue
#import threading

import codecs
#import shutil
#import glob
#import hashlib
#import pickle
from urllib.parse import urlparse
import json
#import re
from tkinter import font, Tk, filedialog, messagebox, StringVar, \
                    IntVar, NO, Text, FALSE, Menu
from tkinter.ttk import Button, Checkbutton, Entry, Frame, Label, LabelFrame, \
                        Radiobutton, Scrollbar, Combobox, Notebook, \
                        Progressbar, Treeview, Style

#import ast
#import psutil
from PIL import Image, ImageTk
#from lxml import etree
#from unidecode import unidecode
#
#from .myconst.audio import AUDIO
#from .myconst.regexs import FIND_LEADING_DIGITS, FIND_LEADING_ALPHANUM, \
#                            FIND_TRAILING_DIGITS, TRIM_LEADING_DIGITS, \
#                            TRIM_TRAILING_DIGITS
#from .myconst.readTag import IDIOT_TAGS, READ_TAG_INFO, HASH_TAG_ON
#
from .myconst.therest import THIS_VERSION, PRJ_JSON
from .tooltip import CreateToolTip
#from .threads import MyThread
#from .backend import Backend
from .klc import Klc
from .pkl import write_ini
from .kmn import kmn_it

def get_script_directory():
    """return path to current script"""
    return os.path.dirname(__file__)

SCRIPT_DIR = get_script_directory()

#class PQueue(queue.PriorityQueue):
#  '''
#  A custom queue subclass that provides a :meth:`clear` method.
#  '''
#
#  def clear(self):
#    '''
#    Clears all items from the queue.
#    '''
#
#    with self.mutex:
#      unfinished = self.unfinished_tasks - len(self.queue)
#      if unfinished <= 0:
#        if unfinished < 0:
#          raise ValueError('task_done() called too many times')
#        self.all_tasks_done.notify_all()
#      self.unfinished_tasks = unfinished
#      self.queue.clear()
#      self.not_full.notify_all()
#
#
#qcommand = queue.Queue()
#qreport = queue.Queue()
#aqr = [PQueue(), PQueue(), PQueue(), PQueue(), \
#       PQueue(), PQueue(), PQueue(), PQueue()]




class GuiCore(Tk):
    """Handle the graphical interface for klc2layout and most of the logic"""
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self._initialize()

    def _initialize(self):
        """initialize the GuiCore"""
        self._initialize_variables()
#        self.backend = Backend(qcommand, qreport)
        
        with open('LOCALIZED_TEXT.json', 'r') as f:
            self.LOCALIZED_TEXT = json.load(f)
        langs = sorted(list(self.LOCALIZED_TEXT.keys()))
        self.INTERFACE_LANGS = langs
        lang = 'en-US'
        self._initialize_main_window(lang)

        if platform.system() not in  ['Windows', 'Linux']:
            # so on f0, the Project tab…
            messagebox.showwarning(\
                              'Warning', "Help I've been kidnaped by {}!!!".\
                                                   format(platform.system()))
            self.klc2layout = os.path.normpath(os.path.expanduser('~/klc2layout'))
#            self.klc2layout = os.path.expanduser('~') + '/klc2layout'
        if platform.system() == 'Linux':
            self.klc2layout = os.path.normpath(os.path.expanduser('~/klc2layout'))
        elif platform.system() == 'Windows':
            self.klc2layout = os.path.normpath(os.path.expanduser('~/klc2layout'))
#            self.klc2layout = '/'.join(os.path.expanduser('~').split("\\")[0:3]) \
#                                  + '/klc2layout'
        if not os.path.isdir(self.klc2layout):
            os.makedirs(self.klc2layout, 0o777) #make the dir

        #headers for f1 klctree
        self.header = ["file", "onpng", "offpng", "font", "mac-id", "section-id", "header", "nfc+nfd"]
        
        #the project held as json in self.klc2layout dir
        self.project_name = ""
        self.project = json.loads(PRJ_JSON)
        
    
        # all tabs will output to ~/klc2layout/tab dir
        # projects held in ~/klc2layout/project name.json
        self._initialize_f0(lang) # setup Project name on Next load project 
        self._initialize_f1(lang) # list msklc files, add attrib
        self._initialize_f2(lang) # will create skeleton SPKL, then add layouts with help docs
        self._initialize_f3(lang) # make KMFL files and help docs
        self._initialize_f4(lang) # make mac keylaout files and help docs
        self._initialize_f5(lang) # make keyman files and help docs

        if platform.system() == 'Linux': #create on f6
            self._initialize_f6(lang) #will be for locking/unlocking SD cards
        klc2layout_styles = Style()
        klc2layout_styles.configure('lowlight.TButton', \
                                font=('Sans', 8, 'bold'),)
        klc2layout_styles.configure('highlght.TButton', \
                                font=('Sans', 11, 'bold'), \
                                background='white', foreground='#007F00')
        klc2layout_styles.configure('wleft.TRadiobutton', \
                                anchor='w', justify='left')
#        self._process_report_queue()
        

#    def _process_report_queue(self):
#        lang = self.ddnGuiLanguage.get()
#        if not qreport.empty():
#            while not qreport.empty():
#                areport = qreport.get()
#                if 'STATUS{}' in areport:
#                    self.status['text'] = areport[1]
##                    self.status['text'] = self.LOCALIZED_TEXT[lang][areport[1][0]].\
##                                                        format(areport[1][1]) \
##                                                        if areport[1] else ''
#                if 'CLEARTAGTREE' in areport:
#                    map(self.tagtree.delete, self.tagtree.get_children())
#                elif 'CLEARTREE' in areport:
#                    self.tree.delete(*self.tree.get_children())
#                elif 'SEEFOCUS' in areport:
#                    self.tree.see(areport[1])
#                    self.tree.focus(areport[1])
#                    self.tree.selection_set(areport[1])
#                elif 'INSERTTAGTREETAGS' in areport:
#                    for item in areport[1]:
#                        if item not in self.tagtree.get_children():
#                            self.tagtree.insert('', index='end', iid=item, \
#                                    open=True, values=[0], \
#                                    text="({}) {}".format(\
#                                          item, SET_TAGS[lang][item]))
#                elif 'SETTAGTREE' in areport:
#                    self.tagtree.selection_set(areport[1])
#                elif 'SELECTIONTAGTREE' in areport:
#                    self.tagtree.selection_add(areport[1])
#                elif 'ENTERLIST' in areport:
#                    self.EnterList.set(areport[1])
#                elif 'IS_COPY_PLAYLISTS_TO_TOP' in areport:
#                    self.is_copy_playlists_to_top.set(areport[1])
#                elif 'M3UorM3U8' in areport:
#                    self.M3UorM3U8.set(areport[1])
#                elif 'ADD_FILE' in areport:
#                    focus = areport[1]
#                    iid = areport[2]
#                    vout = areport[3]
#                    self.tree.insert(focus, index='end', iid=iid, \
#                                     values=vout, open=True, text='file')
#                elif 'ADD_ITEMS' in areport:
#                    #items handled in the order thet were added to the list
#                    for item in areport[1]:
#                        iid = item[0]
#                        v = item[1]
#                        focus = v[0]
#                        vout = v[1]
#                        text = v[2]
#                        newItem = self.tree.insert(focus, index='end', \
#                                                   iid=iid, values=vout, \
#                                                   open=True, text=text)
#                        self.progbar.step()
#                    self._enable_tabs()
#                    self.update()
#                elif 'RENAME_CHILDREN' in areport:
#                    #so now rename them
#                    for iid in areport[1].keys():
#                        vout = areport[1][iid][0]
#                        for c,v in vout:
#                            self.tree.set(iid, c, v)
#                        self.tree.item(iid, text=areport[1][iid][1])
#                        self.progbar.step()
#                    self._enable_tabs()
#                    self.update()
#                elif 'PRINT' in areport:
#                    print(areport[1])
#                elif 'LISTPROJECTS' in areport:
#                    self.list_projects = [f.rstrip('.prj') \
#                                          for f in os.listdir(self.Pub2SD) \
#                                                         if f.endswith('.prj')]
#                    self.ddnCurProject['values'] = self.list_projects
#                    self.ddnCurProject.set(areport[1])
#                elif 'STATUS' in areport:
#                    self.status['text'] = LOCALIZED_TEXT[lang][areport[1]] \
#                                                        if areport[1] else ''
#                elif 'MESSAGEBOXASKOKCANCEL' in areport:
#                    result = messagebox.askokcancel(\
#                                        LOCALIZED_TEXT[lang][areport[1][0]], \
#                                        LOCALIZED_TEXT[lang][areport[1][1]])
#                    qcommand.put(('OKCANCEL', result))
#                elif 'MESSAGEBOXERROR' in areport:
#                    title, m1, m2, m3 = areport[1]
#                    title = LOCALIZED_TEXT[lang][title]
#                    m1 = LOCALIZED_TEXT[lang][m1]
#                    m3 = LOCALIZED_TEXT[lang][m3]
#                    messagebox.showerror(title, \
#                                            "{} <{}>, {}".format(m1, m2, m3))
#                elif 'MESSAGEBOXWARNTRACK' in areport:
#                    title, m1, m2, m3 = areport[1]
#                    messagebox.showwarning(title, \
#                        LOCALIZED_TEXT[lang]['Set'] + ' TRCK, >{}< {}'.format(\
#                                          text, \
#                                          LOCALIZED_TEXT[lang][\
#                       "'track in/set_of' doesn't contain a valid integers."]))
#                elif 'MESSAGEBOXSHOWWARNING2' in areport:
#                    messagebox.showwarning(areport[1][0], \
#                                    LOCALIZED_TEXT[lang][areport[1][1]])
#                elif 'MESSAGEBOXWARNTRACK2' in areport:
#                    title, column, url_str = areport[1]
#                    messagebox.showwarning(LOCALIZED_TEXT[lang][title] + \
#                                           ' {}'.format(column), \
#                                    LOCALIZED_TEXT[lang][url_str])
#                elif 'MESSAGEBOXSHOWWARNINGMULTPLEFILEICONS' in areport:
#                    messagebox.showwarning('', \
#                        LOCALIZED_TEXT[lang][areport[1][0]].\
#                        format(areport[1][1]))
#                elif 'MESSAGEBOXSHOWERRORIN' in areport:
#                    messagebox.showerror(areport[1][0], areport[1][1])
#                elif "MESSAGEBOXSHOWERRORERRORINON_PREPARE_FILES" in areport:
#                    messagebox.showerror(areport[1][0], areport[1][1])
#                elif 'MESSAGEBOXSHOWERRORINSUFFICENT' in areport:
#                    messagebox.showerror(\
#                                        LOCALIZED_TEXT[lang][areport[1][0]], \
#                                        LOCALIZED_TEXT[lang][areport[1[1]]].\
#                                        format(areport[1][2], areport[1][3]))
#                elif 'MESSAGEBOXSHOWHASHERROR' in areport:
#                    name, column, test, mhash = areport[1]
#                    self.complete = messagebox.showerror("Invalid number of parameters", \
#                                    "In row {}, {} tag=>{}<, {} required.".\
#                                    format(name,\
#                                    column, test, mhash))
#                    qcommand.put(('OKCANCEL', self.complete))
#                elif 'MESSAGEBOXSHOWERRORLOSTGRAPHIC' in areport:
#                    messagebox.showerror('', areport[1])
#                elif 'MESSAGEBOXSHOWERRORTHREADS' in areport:
#                    messagebox.showerror(LOCALIZED_TEXT[lang][areport[1][0]], \
#                                         LOCALIZED_TEXT[lang][areport[1][1]].\
#                                         format(areport[1][2]))
#                elif 'PROGSTEP' in areport:
#                    self.progbar.step(areport[1])
#                elif 'PROGSTOP' in areport:
#                    self.progbar.stop()
#                elif 'PROGMAX' in areport:
#                    self.progbar['maximum'] = areport[1]
#                    self.progbar['value'] = 0
#                    self.update()
#                elif 'PROGVALUE' in areport:
#                    self.progbar['value'] = areport[1]
#                    self.update()
#                elif 'COMPLETE' in areport:
#                    self.complete = areport[1]
#                elif 'LOCKGUI' in areport:
#                    self._disable_tabs()
#                elif 'UNLOCKGUI' in areport:
#                    self._enable_tabs()
#                    self.update()
#                elif 'FOLDERSIZE' in areport:
#                    self.needed = areport[1]
#                    self.lblOutputSize['text'] = \
#                                                "{:0.1f} MB".format(areport[1])
#                elif 'TXTPREFCHARDEL' in areport:
#                    self.txtPrefChar.delete(areport[1][0], areport[1][1])
#                elif 'TXTPREFCHARINSERT' in areport:
#                    self.txtPrefChar.insert(areport[1][0], areport[1][1])
#                elif 'CONTINUE_F0_NEXT' in areport:
#                    if areport[1]:
#                        self._on_click_f0_next_continued(lang)
#                    else:
#                        print("can't continue")
#                        pass
#                    self.update()
#                elif 'HASHEDGRAPHICS' in areport:
#                    self.hashed_graphics = areport[1]
#                elif 'FILES_PREPARED' in areport:
#                    self._on_prepare_files_continued()
#                elif 'DELETEDTEMP' in areport:
#                    self.destroy()
#                    return
#                elif 'PREFERRED' in areport:
#                    self.preferred.set(areport[1])
#                else:
#                    print('Unknown report >{}<'.format(areport))
#                qreport.task_done()
#        #now scan queues from pub to SD threads
##        for i in range(0, 8):
##            if not aqr[i].empty():
##                aqreport = aqr[i].get()
##                if 'PROGSTEP' in aqreport:
##                    self.progbar.step(1)
##                    aqr[i].task_done()
##                elif 'PRINT' in aqreport:
##                    print(aqreport[2])
##                elif 'STATUS' in aqreport:
##                    self.usb_status[i] = aqreport[2]
##                    self.status['text'] = ';'.join([t for t in self.usb_status if t])
##                else:
##                    pass
#        self.update()
#        self.lblProject.after(200, self._process_report_queue)


    def _initialize_project_variables(self):
        pass
#        """The project variables that will be saved on clicking 'save project'.
#        The sfn variable hold the settings for their associated tab (fn) of
#        the notebook widget on the main window. The child 'tree'holds a copy
#        of all the file locations and any modifications to their metadata"""
#        self.list_projects = []
#        self.project_lines = []
#        self.indent = 0
#        self.Treed = False
#        self.root = etree.Element('root')
#        #add child 'settings', all user configurable bits under here
#        self.settings = etree.SubElement(self.root, "settings")
#        self.old_mode = dict()
#        self.spreferred = etree.SubElement(self.settings, "preferred")
#        self.smode = etree.SubElement(self.settings, "mode")
#        self.stemp = etree.SubElement(self.settings, "template")
#        self.sf0 = etree.SubElement(self.settings, "f0")
#        self.sf1 = etree.SubElement(self.settings, "f1")
#        self.sf2 = etree.SubElement(self.settings, "f2")
#        self.sf4 = etree.SubElement(self.settings, "f4")
#        self.trout = etree.SubElement(self.root, "tree")
#        self.project_id = ''

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

    def _initialize_main_window_menu(self, lang='en-US'):
        """initialize the menubar on the main window"""

        self.option_add('*tearOff', FALSE)
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.filemenu = Menu(self.menubar)
        self.menubar.add_cascade(label=self.LOCALIZED_TEXT[lang]['File'], \
                                 menu=self.filemenu)
        self.filemenu.add_command(label=\
                            self.LOCALIZED_TEXT[lang]['Load project settings'], \
                                          command=self._on_click_f0_next)
        self.filemenu.add_command(label=self.LOCALIZED_TEXT[lang]['Save'], \
                                  command=self._on_save_project)
        self.filemenu.add_command(label=\
                            self.LOCALIZED_TEXT[lang]['Delete project settings'], \
                                          command=self._on_f0del_project)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=self.LOCALIZED_TEXT[lang]['Exit'], \
                                  command=self.quit)

        self.helpmenu = Menu(self.menubar)
        self.menubar.add_cascade(label=self.LOCALIZED_TEXT[lang]['Help'], \
                                 menu=self.helpmenu)
        self.helpmenu.add_command(label=self.LOCALIZED_TEXT[lang]['Read Me'], \
                                  command=self._on_read_me)
        self.helpmenu.add_command(label=self.LOCALIZED_TEXT[lang]['About...'], \
                                  command=on_copyright)

    def _initialize_main_window_notebook(self, lang):
        """initializes notebook widget on main window"""
        #self.n = Notebook(self, width=1400)
        #notebook
        self.n = Notebook(self, width=1015)
        self.n.grid(column=0, columnspan=7, row=1, padx=5, pady=5, sticky='ew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.n.grid_rowconfigure(0, weight=1)
        self.n.grid_columnconfigure(0, weight=1)
        # chose project name -
        #  defaults to last or pull downlist of existing ones?
        #  enter new, can delete selected project, move to next
        self.f0 = Frame(self.n)
        self.f1 = Frame(self.n)   # recommended tags show/hide
        self.f2 = Frame(self.n)   # special characters
        # Import and/or Edit file Hierachy,
        #  Edit MP3 tags for one file or for all files within a collection
        self.f3 = Frame(self.n)
#        self.f3.grid(column=0, row=0, sticky='news')
#        self.f3.grid_rowconfigure(0, weight=1)
#        self.f3.grid_columnconfigure(0, weight=1)
        # set additional options for featurephone specific locations for
        #  playlists, process files to temp dir and create playlists
        self.f4 = Frame(self.n)
        # output project to SD card copying play lists to any, may have
        #  additional options for featurephone specific locations for playlists
        self.f5 = Frame(self.n)
        self.f6 = Frame(self.n)   # Lock SD card

        self.n.add(self.f0, text=self.LOCALIZED_TEXT[lang]['Project name'])
        self.n.add(self.f1, \
                   text=self.LOCALIZED_TEXT[lang]["Load klc files"])
        self.n.add(self.f2, text=self.LOCALIZED_TEXT[lang]["Make SPKL folder"])
        self.n.add(self.f3, \
                   text=self.LOCALIZED_TEXT[lang]["Make .kmfl folder"])
        self.n.add(self.f4, text=self.LOCALIZED_TEXT[lang]["Make Mac folder"])
        self.n.add(self.f5, text=self.LOCALIZED_TEXT[lang]["Keyman"])
        self.n.add(self.f6, text=self.LOCALIZED_TEXT[lang]['???'])

        self.n.hide(1)
        self.n.hide(2)
        self.n.hide(3)
        self.n.hide(4)
        self.n.hide(5)
        self.n.hide(6)


    def _initialize_main_window(self, lang='en-US'):
        """ initialize the main window"""

        self._initialize_main_window_menu(lang)
        self.f_1 = Frame(self)
        self.f_1.grid(column=0, row=0, sticky='news')
        self.f_1.grid_rowconfigure(0, weight=0)
        self.f_1.grid_columnconfigure(0, weight=0)
       # in top of window
        self.btnSaveProject = Button(self.f_1, \
                                     text=self.LOCALIZED_TEXT[lang]["Save"], \
                                                command=self._on_save_project)
        self.btnSaveProject.grid(column=0, row=0, padx=5, pady=5, sticky='e')
        self.btnSaveProject['state'] = 'disabled'
        self.btnSaveProject_ttp = CreateToolTip(self.btnSaveProject, \
                                        self.LOCALIZED_TEXT[lang]['Save_ttp'])
        self.lblProject = Label(self.f_1, text=\
                                    self.LOCALIZED_TEXT[lang]['f0CurrentProject>'], \
                                                  width=50)
        self.lblProject.grid(column=1, row=0, columnspan=2, padx=5, pady=5, \
                             sticky='ew')
        self.lblProject['justify'] = 'left'

        self.lblGuiLanguage = Label(self.f_1, \
                            text=self.LOCALIZED_TEXT[lang]['0InterfaceLanguage>'])
        self.lblGuiLanguage.grid(column=4, row=0, padx=5, pady=5, sticky='e')
        self.lblGuiLanguage['justify'] = 'right'
        # Create and fill the dropdown ComboBox.
        self.ddnGuiLanguage = Combobox(self.f_1, \
                                       textvariable=self.selected_lang)
        self.ddnGuiLanguage.grid(column=5, columnspan=1, row=0, \
                                 padx=5, pady=5, sticky='w')
        self.ddnGuiLanguage['text'] = 'Interface language:'
        self.ddnGuiLanguage['justify'] = 'left'
        self.ddnGuiLanguage.bind('<<ComboboxSelected>>', self._change_lang)
#        self.ddnGuiLanguage['values'] = [self.INTERFACE_LANGS['langs'][k] \
#                                for k in sorted(self.INTERFACE_LANGS['langs'])]
        self.ddnGuiLanguage['values'] = self.INTERFACE_LANGS
        self.ddnGuiLanguage.set(self.INTERFACE_LANGS[0])

#        self.lblMode = Label(self.f_1, text=self.LOCALIZED_TEXT[lang]['Mode>'])
#        self.lblMode.grid(column=6, row=0, padx=5, pady=5, sticky='e')

        #assumes tab based interface
        #main frame holds gui interface lange pull down, lists current project,
        #and save settings button
        self._initialize_main_window_notebook(lang)

        self.progbar = Progressbar(self, maximum=100, variable=self.int_var)
        self.progbar.grid(column=0, row=6, columnspan=8, padx=5, pady=5, \
                          sticky='news')
        self.status = Label(self, text=self.LOCALIZED_TEXT[lang]['empty string'], \
                            anchor='w', justify='left')
        self.status.grid(column=0, row=7, columnspan=8, padx=5, pady=5, \
                         sticky='news')

    def _initialize_f0(self, lang='en-US'):
        """initialize Project Name tab"""

        self.f0_ttp = Label(self.f0, text=self.LOCALIZED_TEXT[lang]['f0_ttp'], \
                            anchor='w', justify='left', wraplength=600)
        self.f0_ttp.grid(column=0, row=0, columnspan=3, padx=5, pady=5, \
                                                                   sticky='ew')

        self.lblCurProject = Label(self.f0, \
                               text=self.LOCALIZED_TEXT[lang]['f0CurrentProject>'], \
                                                   anchor='w', justify='right')
        self.lblCurProject.grid(column=0, row=1, padx=5, pady=5, sticky='e')

        self.ddnCurProject = Combobox(self.f0, \
                                      textvariable=self.current_project)
        self.ddnCurProject.grid(column=1, row=1, padx=5, pady=5, sticky='news')
        self.ddnCurProject['text'] = 'Current Project:'
        self.ddnCurProject['justify'] = 'left'

        self.btnDelProject = Button(self.f0, \
                               text=self.LOCALIZED_TEXT[lang]['f0DeleteProject'], \
                                                  command=self._on_f0del_project)
        self.btnDelProject.grid(column=2, row=1, padx=5, pady=5, sticky='news')
        self.btnDelProject_ttp = CreateToolTip(self.btnDelProject, \
                                    self.LOCALIZED_TEXT[lang]['f0Delete Project_ttp'])

        # list projects in klc2layout and load to ddnCurProject
        self.list_projects = [f[:-4] for f in os.listdir(self.klc2layout) \
                                     if f.endswith('.prj')]

        self.ddnCurProject['values'] = sorted(self.list_projects)
        if self.list_projects:
            self.ddnCurProject.set(sorted(self.list_projects)[0])

        self.btnf0LoadCreatePrj = Button(self.f0, text=self.LOCALIZED_TEXT[lang]["f0LoadCreatePrj"], \
                                             command=self._on_click_f0_next, \
                                             style='highlight.TButton')
        self.btnf0LoadCreatePrj.grid(column=2, row=7, padx=5, pady=5, sticky='news')
        self.btnf0LoadCreatePrj_ttp = CreateToolTip(self.btnf0LoadCreatePrj, \
                                           self.LOCALIZED_TEXT[lang]['f0LoadCreatePrj_ttp'])

    def _initialize_f1(self, lang='en-US'):
        """initialize List MSKLC files tab"""

        self.labelf1 = Label(self.f1, text=self.LOCALIZED_TEXT[lang]['labelf1'], \
                             anchor='w', justify='left', wraplength=600)
        self.labelf1.grid(column=0, row=0, columnspan=5, padx=5, pady=5, \
                          sticky='w')
        #Source Directory -label, entrybox, browse button
        self.lblf1Source = Label(self.f1, \
                        text=self.LOCALIZED_TEXT[lang]['f1SourceDirectory>'],\
                        anchor='w', justify='left')
        self.lblf1Source.grid(column=0, row=1, columnspan=1, padx=5, pady=5, \
                          sticky='w')
#        self.currentSrcDir.set(self.LOCALIZED_TEXT[lang]['f1SourceDirectory>'])
        self.lblf1SrcDir = Label(self.f1, textvariable=self.currentSrcDir, \
                             anchor='w', justify='left')
        self.lblf1SrcDir.grid(column=1, row=1, columnspan=3, padx=5, pady=5, \
                          sticky='w')
        self.btnf1Browse = Button(self.f1, text="...", \
                                             command=self._on_f1_browse, \
                                             style='highlight.TButton')
        self.btnf1Browse.grid(column=4, row=1, padx=5, pady=5, sticky='news')
        self.btnf1Browse_ttp = CreateToolTip(self.f1, \
                                          self.LOCALIZED_TEXT[lang]['f1Browse_ttp'])
        

        self.klctree = Treeview(self.f1, selectmode="extended", height=8)
        self.klctree.grid(column=0, row=2, \
                       columnspan=12, rowspan=8, sticky='news', padx=5)
        ysb = Scrollbar(self.f1, orient='vertical', command=self.klctree.yview)
        xsb = Scrollbar(self.f1, orient='horizontal', command=self.klctree.xview)
        self.klctree.configure(yscroll=ysb.set, xscroll=xsb.set)
        ysb.grid(row=2, column=11, rowspan=8, padx=5, sticky='nse')
        xsb.grid(row=10, column=0, columnspan=12, padx=5, sticky='ews')

        #fill klctree
        self.klctree["columns"] = self.header
        self.klctree['show'] = 'headings'
        #make sure treeview is empty
        self.klctree.delete(*self.klctree.get_children())
        #set header for each field
        for head in self.header:
            self.klctree.column(head, width=10, anchor='c')
            self.klctree.heading(head, text=self.LOCALIZED_TEXT[lang][head])

        #load data for each item in self.project['klctree']
        for j in range(len(self.project["klctree"])):
            row = list(self.project["klctree"][j])
            self.klctree.insert("",'end',text=str(j),values=row)
        self.update_idletasks()

        self.btnf1AddItem = Button(self.f1, \
                               text=self.LOCALIZED_TEXT[lang]["f1AddItem"], \
                                               command=self._on_f1_add_item)
        self.btnf1AddItem.grid(column=0, row=11, padx=5, pady=5, \
                                 sticky='news')

        self.btnf1RemoveItem = Button(self.f1, \
                                text=self.LOCALIZED_TEXT[lang]["f1RemoveItem"], \
                                            command=self._on_f1_remove_item)
        self.btnf1RemoveItem.grid(column=1, row=11, padx=5, pady=5, \
                                    sticky='news')

        self.boxf1Enter = LabelFrame(self.f1, text='=', labelanchor='w', \
                                   borderwidth=1)
        self.boxf1Enter.grid(column=0, row=12, columnspan=3, padx=5, pady=5, \
                           sticky='news')
        self.lblf1SrcField = Label(self.boxf1Enter, \
                             text=self.LOCALIZED_TEXT[lang]['f1SrcField>'], \
                             anchor='w', justify='left')
        self.lblf1SrcField.grid(column=0, row=0, columnspan=1, padx=5, pady=5, \
                          sticky='w')
        self.ddnf1SelectField = Combobox(self.boxf1Enter, state='readonly', \
                                     textvariable=self.set_field, width=70)
        self.ddnf1SelectField.bind("<<ComboboxSelected>>", self._on_f1get)
        self.ddnf1SelectField.grid(column=1, row=0, columnspan=3, padx=5, pady=5, \
                               sticky='news')
        self.ddnf1SelectField['text'] = 'Field to set:'
        self.ddnf1SelectField['justify'] = 'left'
        self.ddnf1SelectField['values'] = self.header
#        print("ddnCurProject['values'] = {}".format(self.ddnf1SelectField['values']))
#        print("ddnCurProject.current() = {}".format(self.ddnf1SelectField.current()))
        self.ddnf1SelectField_ttp = CreateToolTip(self.ddnf1SelectField, \
                                    self.LOCALIZED_TEXT[lang]['ddnSelectField_ttp'])

        self.btnf1GetDefault = Button(self.boxf1Enter, \
                                text=self.LOCALIZED_TEXT[lang]["f1GetDefault"], \
                                                  command=self._on_f1get_default)
        self.btnf1GetDefault.grid(column=0, row=1, padx=5, pady=5, sticky='news')

        self.etrf1Field = Entry(self.boxf1Enter, \
                                 textvariable=self.currentEntry, width=70)
        self.etrf1Field.grid(column=1, row=1, \
                              columnspan=3, padx=5, pady=5, sticky='news')
        self.etrf1Field['justify'] = 'left'
        self.etrf1Field_ttp = CreateToolTip(self.etrf1Field, \
                                        self.LOCALIZED_TEXT[lang]['etrf1Field_ttp'])

        self.btnf1Set = Button(self.boxf1Enter, text=self.LOCALIZED_TEXT[lang]["f1Set"], \
                             command=self._on_f1set)
        self.btnf1Set_ttp = CreateToolTip(self.btnf1Set, \
                                        self.LOCALIZED_TEXT[lang]['f1Set_ttp'])
        self.btnf1Set.grid(column=4, row=1, padx=5, pady=5, sticky='news')
        

        self.btnf1LoadKlcFiles = Button(self.f1, text=self.LOCALIZED_TEXT[lang]["Load klc files"], \
                                command=self._on_f1_load_klc_files, \
                                style='highlight.TButton')
        self.btnf1LoadKlcFiles.grid(column=3, row=20, padx=5, pady=5, sticky='news')

    def _initialize_f2(self, lang='en-US'):
        """ initialize the SPKL tab"""

        self.labelf2 = Label(self.f2, text=self.LOCALIZED_TEXT[lang]['labelf2'], \
                             anchor='w', justify='left', wraplength=600)
        self.labelf2.grid(column=0, row=0, columnspan=5, padx=5, pady=5, \
                          sticky='w')

        self.lblf2Spkl = Label(self.f2, \
                             text=self.LOCALIZED_TEXT[lang]['SPKL Directory>'], \
                             anchor='w', justify='left')
        self.lblf2Spkl.grid(column=0, row=1, columnspan=1, padx=5, pady=5, \
                          sticky='w')
        self.lblf2SpklDir = Label(self.f2, textvariable=self.spklDir, \
                             anchor='w', justify='left')
        self.lblf2SpklDir.grid(column=2, row=1, columnspan=3, padx=5, pady=5, \
                          sticky='w')
        self.btnf2Browse = Button(self.f2, text="...", \
                                             command=self._on_f2_browse, \
                                             style='highlight.TButton')
        self.btnf2Browse.grid(column=5, row=1, padx=5, pady=5, sticky='news')
        self.btnf2Browse_ttp = CreateToolTip(self.f2, \
                                          self.LOCALIZED_TEXT[lang]['f1Browse_ttp'])
        self.btnf2MakeSpkl = Button(self.f2, text=self.LOCALIZED_TEXT[lang]["Make SPKL folder"], \
                                              command=self._on_f2_make_spkl, \
                                              style='highlight.TButton')
        self.btnf2MakeSpkl.grid(column=3, row=20, columnspan=2, padx=5, pady=5, \
                                                                 sticky='news')

    def _initialize_f3(self, lang='en-US'):
        """initialize the KMFL tab"""
        self.labelf3 = Label(self.f3, text=self.LOCALIZED_TEXT[lang]['labelf2'], \
                             anchor='w', justify='left', wraplength=600)
        self.labelf3.grid(column=0, row=0, columnspan=5, padx=5, pady=5, \
                          sticky='w')

        self.lblf3kmfl = Label(self.f3, \
                             text=self.LOCALIZED_TEXT[lang]['.kmfl Directory>'], \
                             anchor='w', justify='left')
        self.lblf3kmfl.grid(column=0, row=1, columnspan=1, padx=5, pady=5, \
                          sticky='w')
        self.lblf3kmflDir = Label(self.f2, textvariable=self.kmflDir, \
                             anchor='w', justify='left')
        self.lblf3kmflDir.grid(column=2, row=1, columnspan=3, padx=5, pady=5, \
                          sticky='w')
        self.btnf3Browse = Button(self.f2, text="...", \
                                             command=self._on_f2_browse, \
                                             style='highlight.TButton')
        self.btnf3Browse.grid(column=5, row=1, padx=5, pady=5, sticky='news')
        self.btnf3Browse_ttp = CreateToolTip(self.f2, \
                                          self.LOCALIZED_TEXT[lang]['f3Browse_ttp'])
        self.btnf3MakeKmfl = Button(self.f3, text=self.LOCALIZED_TEXT[lang]["Make .kmfl folder"], \
                                command=self._on_f3_make_kmfl, \
                                style='highlight.TButton')
        self.btnf3MakeKmfl_ttp = CreateToolTip(self.btnf3MakeKmfl, \
                                         self.LOCALIZED_TEXT[lang]['btnf3Next_ttp'])
        self.btnf3MakeKmfl.grid(column=2, row=4, padx=5, pady=5, sticky='news')

    def _initialize_f4(self, lang='en-US'):
        """initialize the 'Mac' tab"""
        
        self.btnF4Next = Button(self.f4, text=self.LOCALIZED_TEXT[lang]["Make Mac folder"], \
                                command=self._on_click_f4_next, \
                                style='highlight.TButton')
        self.btnF4Next_ttp = CreateToolTip(self.btnF4Next, \
                                         self.LOCALIZED_TEXT[lang]['btnF4Next_ttp'])
        self.btnF4Next.grid(column=2, row=4, padx=5, pady=5, sticky='news')

    def _initialize_f5(self, lang='en-US'):
        """initialize the 'Keyman' tab"""

        #label explaining what doing…, say what size needed to hold project,
        # choose pub to SD/USB or to hard disk under ~/klc2layout/project
        self.lblf5OutputIntro = Label(self.f5, \
                                    text=self.LOCALIZED_TEXT[lang]["f5OutputIntro"], \
                                    anchor='w', justify='left', wraplength=600)
        self.lblf5OutputIntro.grid(column=0, row=0, \
                                 columnspan=3, padx=5, pady=5, sticky='news')
        self.lblf5OutputSizeText = Label(self.f5, \
                                 text=self.LOCALIZED_TEXT[lang]["f5OutputSizeText"], \
                                    anchor='w', justify='left')


    def _initialize_f6(self, lang):
        """The lock unlock SD card tab, to be implemented?"""
        pass

    def _on_f0del_project(self):
        """Delete current project"""
        project_file = os.path.normpath('{}/{}.prj'.\
                                format(self.klc2layout, self.project_name))
        os.remove(project_file)
        self.list_projects = [f.rstrip('.prj') \
                              for f in os.listdir(self.klc2layout) \
                                                 if f.endswith('.prj')]
        self.ddnCurProject['values'] = self.list_projects
        if self.list_projects:
            self.ddnCurProject.set(self.list_projects[0])
        else:
            self.ddnCurProject.set('')

    def _on_save_project(self):
        """save current project"""
        thefile = os.path.normpath(self.klc2layout + '/' + self.project_name + '.prj')

        #update self.project
        self.project['currentSrcDir'] = self.currentSrcDir.get()
        self.project['klctree'] = list()
        for child in self.klctree.get_children():
            self.project['klctree'].append(list(self.klctree.set(child).values()))
        self.project['spklDir'] = self.spklDir.get()
        
#        print(self.project)
        with open(thefile, "w") as write_file:
            json.dump(self.project, write_file)
            write_file.close()
        #update self.project
        self._load_project()
#        with open(thefile, "r") as read_file:
#            self.project = json.load(read_file)
#            read_file.close()

    def _load_project(self):
        """loads project to the various tabs"""
        thefile = os.path.normpath('{}/{}.prj'.format(self.klc2layout, self.project_name))
        with open(thefile, "r") as read_file:
            self.project = json.load(read_file)
#        print('loaded>{}<'.format(self.project))
        #make sure treeview is empty
        self.klctree.delete(*self.klctree.get_children())
        #rebuild klctree
        self.currentSrcDir.set(self.project["currentSrcDir"])
        if self.project["klctree"]:
            for row in self.project["klctree"]:
                self.klctree.insert("",'end',text='',values=row)                
        self.spklDir.set(self.project["spklDir"])
        self.update()

    def _on_click_f0_next(self):
        """loads the setting on the 'Project Name' tab
                                  and proceeds to the 'MSKLC files' tab"""
#        qcommand.put(('SCRIPT_DIR', self.script_dir))

        lang = self.ddnGuiLanguage.get()

        self.project_name = self.ddnCurProject.get()
#        print('project_name={}'.format(self.project_name))
        if not self.project_name:
            messagebox.showinfo("'{}' {}.".format(\
                                self.LOCALIZED_TEXT[lang]['Current Project>'], \
                                self.LOCALIZED_TEXT[lang]['is empty']), \
                                "{}".format(self.LOCALIZED_TEXT[lang][\
                                     'Please enter a name for your project.']))
            self.status['text'] = 'unamed project'
            self.update()
            return

        self.lblProject['text'] = '{} {}'.format(\
                           self.LOCALIZED_TEXT[lang]['f0CurrentProject>'],\
                           self.project_name)
        self.update()
        thefile = os.path.normpath('{}/{}.prj'.format(self.klc2layout, self.project_name))
        self.status['text'] = 'loading from {}'.format(thefile)
        self.update()
                                                      
        if not os.path.isfile(thefile):
#            with open(thefile, "r") as read_file:
#                self.project = json.load(read_file)
#                read_file.close()
#            self.status['text'] = 'loaded {}'.format(self.project)
#            self.update()
#
#        else:
            #new project
#            print('new project')
            self.project = json.loads(PRJ_JSON)
            self._on_save_project()
#        print('loading saved project')
        self._load_project()
        self.update_idletasks()


        if self.ddnCurProject.get():
            self.n.add(self.f1)#show recommended tags
            self.n.select(1)
            self.btnSaveProject['state'] = 'normal'
        else:
            messagebox.showerror('Error in on_click_f0_next()', \
                                          "Error can't find project.")
        self.update()

    def _on_f1_browse(self, ):
        lang = self.ddnGuiLanguage.get()
        self.project["currentSrcDir"] = filedialog.askdirectory(\
                            initialdir=os.path.expanduser('~'),\
                            title=self.LOCALIZED_TEXT[lang]["SelectFolder"],\
                            mustexist=True)
#        print('>{}<'.format(self.project["currentSrcDir"]))
        self.currentSrcDir.set(self.project["currentSrcDir"])
#        self.lblf1Source['text'] = '{} {} '.format(\
#                        self.LOCALIZED_TEXT[lang]['f1SourceDirectory>'],\
#                        self.project["currentSrcDir"])
        self.update()
        pass

    def _on_f1_add_item(self):
        lang = self.ddnGuiLanguage.get()
        full_path = filedialog.askopenfilenames(\
                        initialdir=self.project["currentSrcDir"], \
                        filetypes=[('klc files', '*.klc'),], \
                        title=self.LOCALIZED_TEXT[lang]["SelectKLCfile"])[0]
        row = ['' for r in self.header]
#        print(len(full_path), full_path)
#        print(len(os.path.basename(full_path)),os.path.basename(full_path) )
#        print(len(full_path[:-len(os.path.basename(full_path))]), full_path[:-len(os.path.basename(full_path))])
#        print()
        if full_path[:-len(os.path.basename(full_path))].strip('/') == self.project["currentSrcDir"]:
            row[0] = os.path.basename(full_path)
        else:
            row[0] = os.path.basename(full_path)
        self.project["klctree"].append(row)
        focus = self.klctree.insert("",'end',text='',values=row)
        self.klctree.selection_set(focus)
        self.update()

    def _on_f1_remove_item(self):
        """If row(s) selected in klctree, delete it. 
            Else complain nothing selected"""
        pass

    def _on_f1get(self, dummy=''):
        """get the value of the field selected in self.ddnf1SelectField
            and display in self.etrf1Field"""
        lang = self.ddnGuiLanguage.get()
        field = self.ddnf1SelectField.get()
        focus = self.klctree.focus()
        if focus == '':
            messagebox.showinfo('', \
                                self.LOCALIZED_TEXT[lang]["PleaseSelectRow."])
        elif len(self.ddnf1SelectField.get()) < 4:
            messagebox.showinfo('', \
                                self.LOCALIZED_TEXT[lang]['PleaseSelectField'])
        else:
            self.etrf1Field.delete(0, len(self.etrf1Field.get()))
#            print(self.ddnf1SelectField.get())
            column = self.ddnf1SelectField.get().split(':')[0].lower()
#            print(column)
            got_it = self.klctree.set(focus, column)
            self.etrf1Field.insert(0, got_it)
        pass

    def _on_f1set(self):
        """Take the value in etr???? and store it in klctree
            (in the selected row and in the column specified by ddn)
            and self.project"""
        lang = self.ddnGuiLanguage.get()
        column = self.ddnf1SelectField.get().split(':')[0]
        text =  self.etrf1Field.get()
        #test if right nos parameters for this tag
        #- compare length with HAS_TAG_ON
        list_of_items = self.klctree.selection()
        if len(list_of_items):
            #so there are some rows selected
            for item in list_of_items:
                #for each row/item
#                print('before:{}'.format(self.klctree.set(item)))
                self.klctree.set(item, column, text)
#                print('after :{}'.format(self.klctree.set(item)))
                self.klctree.focus(item)
                self.klctree.see(item)
        else:
            messagebox.showinfo('', \
                                self.LOCALIZED_TEXT[lang]["PleaseSelectRow."])
        self.status['text'] = ''
        self.progbar['value'] = 0
        self.update()
        pass
    
    def _on_f1get_default(self):
        pass

    def _on_f1_load_klc_files(self):
        """open all the klc files and load into list of KLC objects"""

        lang = self.ddnGuiLanguage.get()
        #update project file
        self._on_save_project()
#        for item in self.project["klcfiles"]:
        the_path = self.project['currentSrcDir']
        klctree = self.project['klctree']
#        self.qr.put(('PRINT', "I'm in _load_klcfiles"))
        print("I'm in _load_klcfiles")
        self.progbar['maximum'] = len(klctree)
        self.progbar['value'] = 0
        for row in klctree:
            self.status['text'] = row[0]
            self.update
            self.klcfiles.append(Klc(the_path, row, self))
            self.progbar.step()
            self.update()
        self.status['text'] = 'klc files loaded'
        self.progbar['value'] = 0
        self.update()           
#        qcommand.put(('LOAD_KLCFILES', json.dumps(self.project)))
        self.n.add(self.f2) #make SPKL
        self.n.add(self.f3) #make KMFL
        self.n.add(self.f4) #make Mac
        self.n.add(self.f5) #make Keyman
        self.n.select(2)
#        self._set_btn_state_for_on_click_f1_next(lang)
#        self._change_lang()

    def _on_f2_browse(self, ):
        lang = self.ddnGuiLanguage.get()
        self.project["spklDir"] = filedialog.askdirectory(\
                            initialdir=os.path.expanduser('~'),\
                            title=self.LOCALIZED_TEXT[lang]["SelectFolder"],\
                            mustexist=True)
#        print('>{}<'.format(self.project["currentSrcDir"]))
        self.spklDir.set(self.project["spklDir"])
#        self.lblf1Source['text'] = '{} {} '.format(\
#                        self.LOCALIZED_TEXT[lang]['f1SourceDirectory>'],\
#                        self.project["currentSrcDir"])
        self.update()
        pass
    
    def _on_f2_make_spkl(self):
        """load settings and preferred character pairs,
            checking for illeagal combinations and proceed to 'Edit...' tab"""

        lang = self.ddnGuiLanguage.get()
        
        if self.spklDir.get() and os.path.isdir(self.spklDir.get()):
            for i in range(0,len(self.project['klctree'])):
                write_ini(self.klcfiles[i], \
                          self.project['klctree'][i], \
                          self.spklDir.get(), \
                          "NFC")
#                print(f'{} has {}')
                if self.project['klctree'][i][-1] == "True":
                    write_ini(self.klcfiles[i], \
                              self.project['klctree'][i], \
                              self.spklDir.get(), \
                              "NFD")
#            self.n.add(self.f3)
#            self.n.select(3)
        else:
            messagebox.showinfo('', \
                    self.LOCALIZED_TEXT[lang]["PleaseSelectSpklOuptutDir."])

    def _on_f3_browse(self, ):
        lang = self.ddnGuiLanguage.get()
        
        self.project["kmflDir"] = filedialog.askdirectory(\
                            initialdir=os.path.expanduser('~'),\
                            title=self.LOCALIZED_TEXT[lang]["SelectFolder"],\
                            mustexist=True)
#        print('>{}<'.format(self.project["currentSrcDir"]))
        self.kmflDir.set(self.project["kmflDir"])
#        self.lblf1Source['text'] = '{} {} '.format(\
#                        self.LOCALIZED_TEXT[lang]['f1SourceDirectory>'],\
#                        self.project["currentSrcDir"])
        self.update()
        pass

    def _on_f3_make_kmfl(self):
        """make kmfl"""
        lang = self.ddnGuiLanguage.get()
#        self.m.add(self.m1)
#        self.m.select(1)


    def _on_click_f4_next(self):
        """make Mac keylayout files"""

        lang = self.ddnGuiLanguage.get()

#        self.n.add(self.f5)
#        self.n.select(5)

    def _on_click_f5_next(self):
        """make Keyman help"""

        lang = self.ddnGuiLanguage.get()

        self.n.add(self.f6)
        self.n.select(6)



    def _on_add_item(self):
        """ add an item(mp3 file) to the selected collection"""

        lang = self.ddnGuiLanguage.get()
        focus = self.tree.focus()
        if len(focus) < 1:
            messagebox.showwarning('', self.LOCALIZED_TEXT[lang][\
                                                   "Please select a row."])
        else:
            if self.tree.set(focus, 'Type') == 'collection':
                full_path = filedialog.askopenfilenames(\
                                    initialdir=os.path.expanduser('~'), \
                                    filetypes=[('MP3 files', '*.mp3'),], \
                                              title="Select MP3 file…")
                filenames = full_path
                self.progbar['maximum'] = len(filenames)
                self.progbar['value'] = 0
                self._disable_tabs()

                ff = {}
                flist = {}
                for f in filenames:
                    filename = os.path.basename(f)[:-4]
                    lf = sort_key_for_filenames(filename)
                    ff[lf] = filename
                    flist[filename] = f

                for ll in sorted(ff):
                    filename = ff[ll]
                    f = flist[filename]
                    somevalues = self._read_idiot_mp3_tags(f) \
                                                    if self.mode.get() == 0 \
                                                    else self._read_mp3_tags(f)
                    self.tree.insert(focus, index='end', values=somevalues, \
                            open=True, text='file')

                    self.progbar.step()
                    self.update_idletasks()

        self._rename_children_of(self.project_id)
        self._enable_tabs()
        self.tree.see(focus)
        self.update()

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
            #need portugese version, default to eng
            url = os.path.normpath("file://" + app_dir + "/Read_Me.html")
        else:
            messagebox.showwarning(\
            'Warning', "Error in on_read_me: " +\
            "{} is unrecognised lang, defaulting to 'en-US.'".format(lang))
            url = os.path.normpath("file://" + app_dir + "/Read_Me.html")
        webbrowser.open(url)

    def _change_lang_1(self, lang):
        '''change lang of labels to interfacelang'''

        self.menubar.entryconfig(0, label=self.LOCALIZED_TEXT[lang]['File'])
        self.menubar.entryconfig(1, label=self.LOCALIZED_TEXT[lang]['Help'])

        self.filemenu.entryconfig(0, \
                        label=self.LOCALIZED_TEXT[lang]['Load project settings'])
        self.filemenu.entryconfig(1, label=self.LOCALIZED_TEXT[lang]['Save'])
        self.filemenu.entryconfig(2, \
                        label=self.LOCALIZED_TEXT[lang]['Delete project settings'])
        self.filemenu.entryconfig(4, label=self.LOCALIZED_TEXT[lang]['Exit'])

        self.helpmenu.entryconfig(0, label=self.LOCALIZED_TEXT[lang]['Read Me'])
        self.helpmenu.entryconfig(1, label=self.LOCALIZED_TEXT[lang]['About...'])

        self.lblGuiLanguage['text'] = \
                           self.LOCALIZED_TEXT[lang]['Interface language>']
        self.lblProject['text'] = self.LOCALIZED_TEXT[lang]['Current Project>'] + \
                                               ' ' + self.ddnCurProject.get()
        self.lblMode['text'] = '{}{}'.format(self.LOCALIZED_TEXT[lang]['Mode>'], \
                    self.LOCALIZED_TEXT[lang]['Simple' if self.mode.get() == 0 \
                                                  else 'Advanced'])

        self.lblCurTemplate_ttp['text'] = \
                               self.LOCALIZED_TEXT[lang]['CurTemplate_ttp']
        self.lblCurTemplate['text'] = self.LOCALIZED_TEXT[lang]['UseTemplate>']
        self.btnCreateTemplate['text'] = self.LOCALIZED_TEXT[lang]["CreateTemplate"]

        self.btnSavePref['text'] = self.LOCALIZED_TEXT[lang]["SavePref"]

        self.boxOptional['text'] = self.LOCALIZED_TEXT[lang]["Optional"]
        self.lblInitialDigit['text'] = self.LOCALIZED_TEXT[lang]['InitialDigit']

        self.lblIdiot['text'] = self.LOCALIZED_TEXT[lang]['IdiotMode']
        self.rdbIdiot['text'] = self.LOCALIZED_TEXT[lang]['Simple']
        self.rdbAdvanced['text'] = self.LOCALIZED_TEXT[lang]['Advanced']
        self.f0_ttp['text'] = self.LOCALIZED_TEXT[lang]['f0_ttp']

        self.lblLatin1['text'] = self.LOCALIZED_TEXT[lang]["AddLatin1Example"]
        self.btnF2Next['text'] = self.LOCALIZED_TEXT[lang]["Next"]

        self.lblM0['text'] = self.LOCALIZED_TEXT[lang]['M0_ttp']
        self.lblM2['text'] = \
                  self.LOCALIZED_TEXT[lang]['M2_ttp1' if self.mode.get() == 1 \
                                                 else 'M2_ttp']
        self.lblArt['text'] = self.LOCALIZED_TEXT[lang]["Art_ttp"]
        self.lblCurProject['text'] = self.LOCALIZED_TEXT[lang]['Current Project>']
        self.btnBuildOutputTo['text'] = self.LOCALIZED_TEXT[lang]['Output to>']
        self.lblTrimTitle['text'] = self.LOCALIZED_TEXT[lang]['TrimTitle_ttp']
        self.box0['text'] = self.LOCALIZED_TEXT[lang]["and/or"]
        self.box1['text'] = self.LOCALIZED_TEXT[lang]['Adjust order of files']
        self.box2['text'] = self.LOCALIZED_TEXT[lang]['As needed']
        self.box1M1['text'] = self.LOCALIZED_TEXT[lang]['Change indent']
        self.box2M1['text'] = self.LOCALIZED_TEXT[lang]['Change order']
        self.labelf1['text'] = self.LOCALIZED_TEXT[lang]['labelf1']

    def _change_lang_2(self, lang):
        '''change lang of labels to interfacelang'''

        self.lblPlayLists['text'] = self.LOCALIZED_TEXT[lang]["PlayListsIntro"]
        self.chkCopyPlayListsToTop['text'] = \
                                  self.LOCALIZED_TEXT[lang]["CopyPlayListsToTop"]
        self.boxM3U['text'] = \
           self.LOCALIZED_TEXT[lang]['Create playlists using Legacy/UTF-8 encoding']
        self.rdbBoth['text'] = self.LOCALIZED_TEXT[lang]["Both"]

        self.lblEnterList['text'] = self.LOCALIZED_TEXT[lang]["EnterList"]
        self.lblOutputIntro['text'] = self.LOCALIZED_TEXT[lang]["OutputIntro"]
        self.lblOutputSizeText['text'] = self.LOCALIZED_TEXT[lang]["OutputSizeText"]
        self.btnDelProject['text'] = self.LOCALIZED_TEXT[lang]['Delete Project']
        self.btnDelProject_ttp.text = \
                                self.LOCALIZED_TEXT[lang]['Delete Project_ttp']
        self.btnRefreshDrives['text'] = self.LOCALIZED_TEXT[lang]['Refresh']
        self.btnRefreshDrives_ttp.text = self.LOCALIZED_TEXT[lang]['Refresh_ttp']
        self.btnF0Next['text'] = self.LOCALIZED_TEXT[lang]['Next']
        self.btnF0Next_ttp.text = self.LOCALIZED_TEXT[lang]['F0Next_ttp']
        self.btnDefaultTags['text'] = self.LOCALIZED_TEXT[lang]["Set default tags"]
        self.btnF1Next['text'] = self.LOCALIZED_TEXT[lang]['Next']

        self.labelf2['text'] = self.LOCALIZED_TEXT[lang]['labelf2']
        self.lblPreferred['text'] = self.LOCALIZED_TEXT[lang]['lblPreferred']
        self.rdbDefault['text'] = self.LOCALIZED_TEXT[lang]['Default']
        self.rdbPreferred['text'] = self.LOCALIZED_TEXT[lang]['Preferred']

        self.btnF3M0Next['text'] = self.LOCALIZED_TEXT[lang]['Next']
        self.btnF3M1Next['text'] = self.LOCALIZED_TEXT[lang]['Next']
        self.btnF3M2Next['text'] = self.LOCALIZED_TEXT[lang]['Next']
        self.btnF3M2Next_ttp.text = self.LOCALIZED_TEXT[lang]['btnF3M2Next_ttp']
        self.btnF4Next['text'] = self.LOCALIZED_TEXT[lang]['Prepare Files']
        self.btnF4Next_ttp.text = self.LOCALIZED_TEXT[lang]['F0Next_ttp']

        self.btnAddCollection['text'] = self.LOCALIZED_TEXT[lang]['Add Collection']
        self.btnAddCollection_ttp.text = \
                                    self.LOCALIZED_TEXT[lang]['AddCollection_ttp']
        self.btnAddFiles['text'] = self.LOCALIZED_TEXT[lang]['Add Files']
        self.btnAddFiles_ttp.text = self.LOCALIZED_TEXT[lang]['AddFiles_ttp']
        self.btnPromote_ttp.text = self.LOCALIZED_TEXT[lang]['Promote_ttp']
        self.btnDemote_ttp.text = self.LOCALIZED_TEXT[lang]['Demote_ttp']
        self.btnMoveUp_ttp.text = self.LOCALIZED_TEXT[lang]['MoveUp_ttp']
        self.btnMoveDown_ttp.text = self.LOCALIZED_TEXT[lang]['MoveDown_ttp']
        self.btnDeleteItem['text'] = self.LOCALIZED_TEXT[lang]['Delete Item']
        self.btnDeleteItem_ttp.text = self.LOCALIZED_TEXT[lang]['Delete_ttp']
        self.btnSaveProject['text'] = self.LOCALIZED_TEXT[lang]['Save']
        self.btnSaveProject_ttp.text = self.LOCALIZED_TEXT[lang]['Save_ttp']
        self.btnSelectArtwork['text'] = self.LOCALIZED_TEXT[lang]['Select Artwork']
        self.btnImportHierarchy['text'] = \
                        self.LOCALIZED_TEXT[lang]["Add Folder and it's Contents"]
        self.btnImportHierarchy_ttp.text = \
                                        self.LOCALIZED_TEXT[lang]['AddFolder_ttp']
        self.btnImportContents['text'] = \
                             self.LOCALIZED_TEXT[lang]["Add the Contents of Folder"]
        self.btnImportContents_ttp.text = \
                                        self.LOCALIZED_TEXT[lang]['AddContents_ttp']
        self.etrTagValue_ttp.text = self.LOCALIZED_TEXT[lang]['entry1_ttp']
        self.ddnSelectTag_ttp.text = self.LOCALIZED_TEXT[lang]['ddnSelectTag_ttp']
        self.btnGet['text'] = self.LOCALIZED_TEXT[lang]["Get"]
        self.btnSet['text'] = self.LOCALIZED_TEXT[lang]['Set']
        self.btnSet_ttp.text = self.LOCALIZED_TEXT[lang]['Set_ttp']
        self.btnGetDefault['text'] = self.LOCALIZED_TEXT[lang]['Get default']

    def _change_lang_3(self, lang):
        '''change lang of labels to interfacelang'''

        self.btnTrimTitle['text'] = self.LOCALIZED_TEXT[lang]['Trim Title']
        self.btnklc2layout['text'] = self.LOCALIZED_TEXT[lang]["Publish to SD/USB"]
        project = self.ddnCurProject.get()
        self.btnPub2HD['text'] = \
            self.LOCALIZED_TEXT[lang]["Publish to '~\\klc2layout\\{}_SD'"].\
                          format(project if project else "<project>")
        self.n.tab(self.f0, text=self.LOCALIZED_TEXT[lang]['Project name'])
        self.n.tab(self.f1, \
                   text=self.LOCALIZED_TEXT[lang]['Commonly used MP3 tags'])
        self.n.tab(self.f2, text=self.LOCALIZED_TEXT[lang]['Special characters'])
        self.n.tab(self.f3, \
                   text=self.LOCALIZED_TEXT[lang]['Edit Hierachy and MP3 tags'])
        self.n.tab(self.f4, text=self.LOCALIZED_TEXT[lang]['Feature-phone options'])
        self.n.tab(self.f5, text=self.LOCALIZED_TEXT[lang]['Output to…'])
        self.n.tab(self.f6, text=self.LOCALIZED_TEXT[lang]['Lock SD card'])
        self.m.tab(self.m0, text=self.LOCALIZED_TEXT[lang]['Import hierarchy'])
        self.m.tab(self.m1, text=self.LOCALIZED_TEXT[lang]['Edit hierarchy'])
        self.m.tab(self.m2, text=self.LOCALIZED_TEXT[lang]['Edit MP3 tags'])
        self.boxlf5list['text'] = self.LOCALIZED_TEXT[lang]['Available']
        self.box1f5['text'] = self.LOCALIZED_TEXT[lang]['Or']

        if self.Treed:
            self.tree.heading('#0', text=self.LOCALIZED_TEXT[lang]['#0'])
            self.tree.heading('#1', text=self.LOCALIZED_TEXT[lang]['Type'])
            for item in self.displayColumns[1:-1]:
                sometext = item if self.mode.get() != 0 \
                                else SET_TAGS[lang][item]
                self.tree.heading(item, text=sometext)

        set_taga = [TRIM_TAG[lang]['Nothing'], \
                    TRIM_TAG[lang]['Leading digits'], \
                            TRIM_TAG[lang]['Leading alphanumerics'], \
                                    TRIM_TAG[lang]['Trailing digits']]

        self.ddnTrimFromTitle['values'] = set_taga
        self.ddnTrimFromTitle.set(set_taga[0])
        self.ddnTrimFromTitle_ttp.text = self.LOCALIZED_TEXT[lang]['dropdown5_ttp']

    def _change_lang(self, dummy=''):
        '''change lang of labels to interfacelang'''

        lang = self.ddnGuiLanguage.get()

        self._change_lang_1(lang)
        self._change_lang_2(lang)
        self._change_lang_3(lang)

        self.update()

    def _approved_char(self, achar):
        """is approved character"""
        return True if achar.isalnum() or achar in self.pref_char else False

    def _my_unidecode(self, text):
        """normalize strings to avoid unicode character which won't display
           correctly or whose use in filenames may crash filesystem"""
        l = list()
        if self.preferred.get() != 1:
            self.pref = list()
        #fix eng/Eng 'bug' in unidecode
        if 'ŋ' not in [v[0] for v in self.pref]:
            self.pref.append(['ŋ', 'ng', re.compile('ŋ')])
        if 'Ŋ' not in [v[0] for v in self.pref]:
            self.pref.append(['Ŋ', 'Ng', re.compile('Ŋ')])
        #scan list of preffered character/string pairs
        for kv in self.pref:# in range(0,len(text)):
            #build list of all hits in text
            l.extend([[m.start(), len(kv[0]), kv[1]] \
                       for m in kv[2].finditer(text)])
        if l:
            #now sort list of hits into sequence order
            l = sorted(l, key=lambda student: student[0])
            result = ''
            s = 0
            for ll in l:
                #from end of last match to start of new match + new match aggress
                result += ''.join([c if c.isalnum() or \
                                        c in self.pref_char else '_' \
                                    for c in unidecode(text[s:ll[0]])]) + ll[2]
                #start of match + len of match
                s = ll[0] + ll[1]
            if s < len(text):
                #from end of last match to end of string aggress
                result += ''.join([c if c.isalnum() or \
                                        c in self.pref_char else '_' \
                                        for c in unidecode(text[s:])])
            return result
        else:
            return ''.join([c if c.isalnum() or c in self.pref_char else '_' \
                            for c in unidecode(text)])


def on_copyright():
    """displays the copyright info when called from menubar"""
    messagebox.showinfo(\
                            "klc2layout v{}".format(THIS_VERSION), \
                            "©2019 SIL International\n" + \
                            "License: MIT license\n" + \
                            "Web: https://www.silsenelgal.org\n" + \
                            "Email: Academic_Computing_SEB@sil.org\n\n")

#def is_hashable(tag):
#    '''return true if tag hashable'''
#
#    return True if True in HASH_TAG_ON[tag] else False

def get_rid_of_multiple_spaces(tin):
    '''replace multiple spaces with single space and strip leading and
    trailing spaces'''
#    tout = tin.strip().split()
#    tout = tin.split(' ')
#    while '' in tout:
#        tout.remove('')
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
    for root, dirs, files, rootfd in os.fwalk(top, topdown=False):
        [os.remove(name, dir_fd=rootfd) for name in files]
        [os.rmdir(name, dir_fd=rootfd) for name in dirs]

#def delete_folder(path):
#    '''if folder exists remove it'''
#    if os.path.exists(path):
#        # remove if exists
#        shutil.rmtree(path)

def folder_size(top):
    '''return size used by folder in bytes'''
    this_folder_size = 0
    for (path, dirs, files) in os.walk(top):
        for file in files:
            filename = os.path.join(path, file)
            this_folder_size += os.path.getsize(filename)
    return this_folder_size

def forward_slash_path(apath):
    '''replace all backslashes with forward slash'''
    return '/'.join(apath.split('\\'))
