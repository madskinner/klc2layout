# -*- coding: utf-8 -
#-------------------------------------------------------------------------------
# Name:        klc2layout
""" Purpose:     queues and threading"""
#
# Author:      marks
#
# Created:     27-04-2016
# Copyright:   (c)2016 SIL international
# Licence:     Creative Commons?
#-------------------------------------------------------------------------------


import sys
import os
import platform

from tkinter import messagebox, PhotoImage

from pkg_resources import resource_filename
if __name__ == '__main__' and __package__ is None:
    os.sys.path.append(os.path.dirname(os.path.dirname(\
                                                os.path.abspath(__file__))))
from klc2layoutthreaded.myclasses.myconst.therest import THIS_VERSION
from klc2layoutthreaded.myclasses.mini_gui import GuiCore

def hello_world():
    '''idiot test function'''
    return 'Hello world!'


def main():
    """the main routine"""

    frozen = False
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = True
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    gui = GuiCore(None) # see GuiCore's __init__ method
    gui.title(' test queue and threading v{}'.format(THIS_VERSION))

    if platform.system() == 'Windows':
        gui.wm_iconbitmap(os.path.normpath((\
                                    resource_filename(__name__, 'mainc.ico'))))
    elif platform.system() == 'Linux':
        img = PhotoImage(\
                        file=(resource_filename(__name__, 'images/mainc.png')))
#        img = PhotoImage(file=(get_script_directory() + '/images/mainc.png'))
        gui.tk.call('wm', 'iconphoto', gui._w, img)
    else:
        messagebox.showwarning('Warning', "Help I've been kidnaped by {}!!!".\
                               format(platform.system()))

    gui.mainloop()

if __name__ == '__main__':
    main()
