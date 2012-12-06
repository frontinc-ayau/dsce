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

"""This is the implementation of the main frame which uses the AUIManager to
organize the user interface.
Each view on the DomainContact(s) is implemented as a Pane. 
"""
import wx
import wx.aui
import wx.grid
import logging

import observer
from observer import pmsg

import resources
from observer import *
from gridview import GridView



class MainFrame(wx.Frame):
    def __init__(self, parent, id=-1, title="Domain Shared Contacts Editor", ico=None,
                pos = wx.DefaultPosition,
                size= (950,600),
                style = wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER | wx.CLIP_CHILDREN):
        """Setup and configure the main UI
        """

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        # Make this frame known to the FrameManager
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self.SetMinSize(wx.Size(900, 500))

        if ico:
            self.SetIcon(ico)

        self.createToolbar()
        # make messages available for subscribers
        self.registerMessages()

        # Each supported pane has to be put here
        self.grid = GridView(self)
        self._mgr.AddPane(self.grid, wx.aui.AuiPaneInfo().
                          Name("ContactsTable").Caption("Contacts Table View").CenterPane().
                          CloseButton(False).MaximizeButton(False))



        # bind this frame events
        self.binEvents()

        self._mgr.Update()


    def createToolbar(self):
        self.tb = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)

        self.tb.SetToolBitmapSize(wx.Size(34,24))

        # toolbar bitmaps
        exit_bmp = resources.getasbitmap(resources.R_EXIT)
        add_bmp = resources.getasbitmap(resources.R_ADD)
        del_bmp = resources.getasbitmap(resources.R_DEL)
        grp_bmp = resources.getasbitmap(resources.R_GRP)
        pub_bmp = resources.getasbitmap(resources.R_PUB)
        get_bmp = resources.getasbitmap(resources.R_GET)

        # toolbar dimension
        tsize = exit_bmp.GetSize()
        self.tb.SetToolBitmapSize(tsize)
        self.tb.SetToolSeparation(8)

        # give ids a name
        self.EXIT_ID = 10
        self.ADD_ID  = 20
        self.DEL_ID  = 30
        self.GRP_ID  = 40
        self.GET_ID  = 50
        self.PUB_ID  = 60


        # tools
        self.tb.AddLabelTool(self.EXIT_ID, "Exit", exit_bmp, shortHelp="Exit application", 
                                                             longHelp="Exit application")
        self.tb.AddSeparator()

        self.tb.AddLabelTool(self.ADD_ID, "Add", add_bmp, shortHelp="Add contact", 
                                                          longHelp="Add contact")
        self.tb.AddLabelTool(self.DEL_ID, "Del", del_bmp, shortHelp="Delete contact", 
                                                          longHelp="Delete contact")
        self.tb.AddLabelTool(self.GRP_ID, "Grp", grp_bmp, shortHelp="Manage groups", 
                                                          longHelp="Add, update and delete groups")
        self.tb.AddSeparator()
        self.tb.AddLabelTool(self.GET_ID, "Get", get_bmp, shortHelp="Get contact", 
                                                          longHelp="Get contact")
        self.tb.AddLabelTool(self.PUB_ID, "Pub", pub_bmp, shortHelp="Publish contact", 
                                                          longHelp="Publish contact")

        self.tb.AddSeparator()
        self.search = wx.SearchCtrl(self.tb, size=(150,-1), style=wx.TE_PROCESS_ENTER)
        self.search.SetMenu(None)
        self.search.ShowCancelButton(1)
        
        self.tb.AddControl(self.search)

        self.tb.Realize()


        # add the toolbar to the manager
        self._mgr.AddPane(self.tb, wx.aui.AuiPaneInfo().
                          Name("tb").Caption("Toolbar").
                          ToolbarPane().Top().
                          LeftDockable(True).RightDockable(True))

    def registerMessages(self):
        pmsg.register("ADD_CONTACT") # request to add a contact
        pmsg.register("DEL_CONTACT") # request to delete a contact
        pmsg.register("MAN_GROUPS")  # request to globally manage groups
        pmsg.register("PUB_CONTACT")
        pmsg.register("SEARCH")
        pmsg.register("CANCEL_SEARCH")

    def binEvents(self):
        # toolbar events
        self.tb.Bind(wx.EVT_TOOL, self.publishEvent, id=self.EXIT_ID)
        self.tb.Bind(wx.EVT_TOOL, self.publishEvent, id=self.ADD_ID)
        self.tb.Bind(wx.EVT_TOOL, self.publishEvent, id=self.DEL_ID)
        self.tb.Bind(wx.EVT_TOOL, self.publishEvent, id=self.GRP_ID)
        self.tb.Bind(wx.EVT_TOOL, self.publishEvent, id=self.GET_ID)
        self.tb.Bind(wx.EVT_TOOL, self.publishEvent, id=self.PUB_ID)
        self.tb.Bind(wx.EVT_TEXT, self.onSearch)
        self.tb.Bind(wx.EVT_TEXT_ENTER, self.onSearch)
        self.tb.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearch)
        self.tb.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.resetSearch)

    def publishEvent(self, event):
        """Depending on the id the event with the appropriate message 
        will be published.
        """
        if event.GetId() == self.ADD_ID:
            observer.send_message(pmsg.ADD_CONTACT, event)

        elif event.GetId() == self.DEL_ID:
            observer.send_message(pmsg.DEL_CONTACT, data=self.grid.getActiveRows())

        elif event.GetId() == self.GRP_ID:
            observer.send_message(pmsg.MAN_GROUPS, event)

        elif event.GetId() == self.PUB_ID:
            observer.send_message(pmsg.PUB_CONTACT, event)

        elif event.GetId() == self.GET_ID:
            observer.send_message(pmsg.PUB_CONTACT, event)

        elif event.GetId() == self.EXIT_ID:
            observer.send_message(pmsg.EXIT_APP, event)


    def onSearch(self, evt):
        s = self.search.GetValue()
        if len(s) > 0:
            observer.send_message(pmsg.SEARCH, data=s)
        else:
            observer.send_message(pmsg.CANCEL_SEARCH, data=s)

    def resetSearch(self, evt):
        self.search.Clear()
        observer.send_message(pmsg.CANCEL_SEARCH)
