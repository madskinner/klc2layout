# -*- coding: utf-8 -
#-------------------------------------------------------------------------------
# Name:        klc2layout
""" Purpose:     Convert MSKLC files to SPKL, kmfl, (mac?), Keyman and generate documentaion."""
#
# Author:      marks
#
# Created:     24-05-2019
# Copyright:   (c)2019 SIL international
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
from klc2layout.myclasses.myconst.therest import THIS_VERSION
from klc2layout.myclasses.gui import GuiCore

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
    gui.title(' klc2layout v{}'.format(THIS_VERSION))

    if platform.system() == 'Windows':
        gui.wm_iconbitmap(os.path.normpath((\
                                    resource_filename(__name__, 'mainq.ico'))))
    elif platform.system() == 'Linux':
        img = PhotoImage(\
                        file=(resource_filename(__name__, 'images/mainq.png')))
#        img = PhotoImage(file=(get_script_directory() + '/images/mainc.png'))
        gui.tk.call('wm', 'iconphoto', gui._w, img)
    else:
        messagebox.showwarning('Warning', "Help I've been kidnaped by {}!!!".\
                               format(platform.system()))

    gui.mainloop()

if __name__ == '__main__':
    main()
