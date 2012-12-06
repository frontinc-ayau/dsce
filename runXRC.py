#!env python

# This file is part of the DomainSharedContactsEditor (DSCE) application.
#
# DSCE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DSCE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DSCE.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (c) 2010 Klaus Melcher (melcher.kla@gmail.com)

"""Used to run the passed xrc file for testing it
"""
import wx
import wx.xrc as xrc
import os, sys, getopt

import logging as log
log.basicConfig(format="%(asctime)s %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=log.DEBUG)


_USAGE__TXT ="""runXRC.py - Run passed xrc file

Usage: release.py [options] 

Options
 mandatory:
    -x xrc-file # file that contains the XRC resources to run
    -n name     # name of the frame or dialog within the XRC file that should loaded
    -t [d|f!p]  # 'd' if it is a dialog, 'f' if it is a frame or p if it is a panel
 optional:
    -h          # this screen
"""
GUI_FILENAME=None
GUI_MAINFRAME_NAME=None

GUI_TYPE=None
DIALOG="d"
FRAME="f"
PANEL="p"

def usage():
    print(_USAGE__TXT)


def exit_on_error(msg, rc=1):
    log.fatal("%s" % msg)
    sys.exit(rc)


class MyApp(wx.App):
    def OnInit(self):
        self.res = xrc.XmlResource(GUI_FILENAME)
        if GUI_TYPE == FRAME:
            log.info("Load frame")
            self.frame = self.res.LoadFrame(None, GUI_MAINFRAME_NAME)
            self.SetTopWindow(self.frame)
            self.frame.Show(1)
        elif GUI_TYPE == DIALOG:
            log.info("Load dialog")
            self.frame = wx.Frame(None, id=-1, title="Test XRC Dialog")
            self.SetTopWindow(self.frame)
            self.dlg = self.res.LoadDialog(self.frame, GUI_MAINFRAME_NAME)
            # self.frame.Show(1) # we do not realy want to see the main frame
            self.dlg.ShowModal()
            self.frame.Close() # after exiting the dialog we can also close the application
            sys.exit(0)
        elif GUI_TYPE == PANEL:
            log.info("Load pane")
            self.frame = wx.Frame(None, id=-1, title="Test XRC Dialog", style=wx.DEFAULT_DIALOG_STYLE)
            self.SetTopWindow(self.frame)

            self.panel = self.res.LoadPanel(self.frame, GUI_MAINFRAME_NAME)
            self.topSizer = wx.BoxSizer(wx.VERTICAL)
            self.topSizer.Add(self.panel, 1, wx.EXPAND, 6)
            self.frame.SetSizer(self.topSizer)
            self.topSizer.Fit(self.frame)

            self.frame.Show(1)
            self.frame.SendSizeEvent()
        return True


def setType(t):
    """t = d or f"""
    global GUI_TYPE

    if (t != DIALOG) and (t != FRAME) and (t != PANEL):
        exit_on_error("Display type must be either '%s', '%s' or '%s'. The type '%s' is not supported!" % 
                            (DIALOG, FRAME, PANEL, str(t)))
    if GUI_TYPE:
        exit_on_error("The type option '-t' is not allowed multiple times. Type already set to '%s'" % GUI_TYPE)
    else:
        GUI_TYPE = t


def main():
    try:
        app = MyApp()
        app.MainLoop()
    except Exception, e:
        exit_on_error(str(e))


if __name__ == "__main__":

    if len(sys.argv) == 1:
        usage()
        exit_on_error("Too view arguments!")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hx:n:t:")
    except getopt.GetoptError, err:
        usage()
        exit_on_error(str(err))
        
    for o,a in opts:
        if o == "-x":
            GUI_FILENAME = os.path.abspath(a)
        elif o == "-n":
            GUI_MAINFRAME_NAME = a
        elif o == "-t":
            setType(a)
        elif o == "-h":
            usage()
            sys.exit(0)
        else:
            usage()
            exit_on_error("Not handled option %s" % o)
        
    if not GUI_FILENAME: exit_on_error("Missing XRC file")
    if not os.path.isfile(GUI_FILENAME): exit_on_error("File %s does not exist!" % GUI_FILENAME)
    if not GUI_MAINFRAME_NAME: exit_on_error("Missing frame name (-f)")
    

    main()
    sys.exit(0)

