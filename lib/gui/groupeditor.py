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
# Copyright (c) 2011 Klaus Melcher (melcher.kla@gmail.com)

import wx
import xrcl

import logging as log
import sys 



class GroupEditDialog(wx.Dialog):

    def __init__(self, parent, ID=-1, title="Manage Groups"):

        wx.Dialog.__init__(self, parent, ID, title, 
                           style=wx.DEFAULT_DIALOG_STYLE
                                 #| wx.RESIZE_BORDER
                           )
        
        # read panel and get important controlers for convenience
        self.panel = xrcl.loadPanel(self, "groupeditor.xrc", "groupeditor")
        # self.cnam = xrcl.getControl(self.panel, "cn")
        # self.cdep = xrcl.getControl(self.panel, "cd")
        # self.ctit = xrcl.getControl(self.panel, "ct")
        # self.cjob = xrcl.getControl(self.panel, "cj")
        # self.cwhe = xrcl.getControl(self.panel, "cw")
        # self.clab = xrcl.getControl(self.panel, "cl")
        # self.ctyp = xrcl.getControl(self.panel, "cr")
        # self.csym = xrcl.getControl(self.panel, "cs")
        # self.cpri = xrcl.getControl(self.panel, "cp")
        
        xrcl.getControl(self.panel, "wxID_OK").Bind(wx.EVT_BUTTON, self.onOk)

        self.populateForm()
        
        space = 5
        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer.Add(self.panel, 1, wx.EXPAND, space)
        self.SetSizer(self.topSizer)
        self.topSizer.Fit(self)
        self.ShowModal()

    def populateForm(self):
        """Fills tha form with existing data if any."""
        # o = self.table.GetValue(self.row, self.col)
        pass

    def saveChanges(self):
        """Saves if anything (except primary or type) has been set."""
        pass


    def onOk(self, event):
        log.debug("Save changes in groups")
        self.saveChanges()
        self.Destroy()
        
