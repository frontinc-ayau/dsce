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
# Copyright (c) 2012 Klaus Melcher (melcher.kla@gmail.com)

import wx
import xrcl

import logging as log
import sys 

import domaindata

import observer
from observer import pmsg

# list control configuration
COLIDX_NAME = 0
COLIDX_TYPE = 1
LABEL_NAME = "Group Name"
LABEL_TYPE = "Editable"
TYPE_TXT_PRI = "Yes"
TYPE_TXT_SYS = "No"

LABEL_ADD = "Add"
LABEL_UPD = "Update"
LABEL_DEL = "Delete"

class ChangedGroups(object):
    def __init__(self):
        self.addedGroups = []
        self.deletedGroups = []
        self.updatedGroups = []

    def add(self, gname):
        log.debug("Add group %s" % gname)
        if self.addedGroups.count(gname.strip()) == 0:
            self.addedGroups.append(gname.strip())
        else:
            raise Exception("%s already exists!" % gname.strip())

    def delete(self, gname): 
        self.deletedGroups.append(gname.strip())

    def update(self, src, dest):
        self.updatedGroups.append((src.strip(), dest.strip()))

    def publishChanges(self):
        """Publishes changes, if any, so they can be handled properly by
        observers who are interested (mainly domaindata)
        """
        if len(self.addedGroups) > 0:
            for g in self.addedGroups:
                log.debug("Published GROUP_ADDED %s" % g)
                observer.send_message(pmsg.GROUP_ADDED, data=g)


class GroupEditDialog(wx.Dialog):

    def __init__(self, parent, ID=-1, title="Manage Groups"):

        wx.Dialog.__init__(self, parent, ID, title, 
                           style=wx.DEFAULT_DIALOG_STYLE
                                 #| wx.RESIZE_BORDER
                           )
        self.idx = -1
        self.changedGroups = ChangedGroups()

        # sg = system groups, pg = private groups
        self.sg, self.pg = domaindata.get_group_names()

        self.panel = xrcl.loadPanel(self, "groupeditor.xrc", "groupeditor")
        self.glc = xrcl.getControl(self.panel, "grplstctrl")

        self.gnc = xrcl.getControl(self.panel, "grpname")


        self.uab = xrcl.getControl(self.panel, "upaddbutton")
        self.uab.SetLabel(LABEL_ADD)
        self.deb = xrcl.getControl(self.panel, "delbutton")
        self.deb.SetLabel(LABEL_DEL)
        

        self.populateForm()
        
        space = 5
        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer.Add(self.panel, 1, wx.EXPAND, space)
        self.SetSizer(self.topSizer)
        self.topSizer.Fit(self)

        self.binEvents()

        self.ShowModal()

    def populateForm(self):
        """Fills tha form with existing data if any."""

        self.glc.InsertColumn(COLIDX_NAME, LABEL_NAME)
        self.glc.InsertColumn(COLIDX_TYPE, LABEL_TYPE)
        for g in self.sg:
            self.appendGroup(g, TYPE_TXT_SYS)
        for g in self.pg:
            self.appendGroup(g, TYPE_TXT_PRI)


    def binEvents(self):
        xrcl.getControl(self.panel, "wxID_OK").Bind(wx.EVT_BUTTON, self.onOk)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected, self.glc)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeselected, self.glc)
        self.Bind(wx.EVT_BUTTON, self.onAddOrUpdate, self.uab)
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.deb)


    def isSystemGroup(self, idx):
        if idx < 0 or (self.glc.GetItem(idx, COLIDX_TYPE).GetText() != TYPE_TXT_SYS):
            return False
        else:
            return True

    def onItemSelected(self, event):
        self.idx = event.GetIndex()
        self._setDelButton()
        if self.isSystemGroup(self.idx) == False:
            self.gnc.SetValue(self.glc.GetItem(self.idx, COLIDX_NAME).GetText())
            self._setUAButton()

    def clearForm(self):
        self.idx = -1
        self.gnc.SetValue("")
        self._setDelButton()
        self._setUAButton()

    def onDelete(self, event):
        if self.idx >= 0:
            self.glc.DeleteItem(self.idx)
            self.clearForm()


    def onAddOrUpdate(self, event):
        name = self.gnc.GetValue().strip()

        if len(name) == 0: return

        if self.idx < 0:
            self.changedGroups.add(name)
            self.appendGroup( name, TYPE_TXT_PRI)
            self.clearForm()
        else:
            self.updateGroup( self.idx, name, TYPE_TXT_PRI)


    def onItemDeselected(self, event):
        self.clearForm()

    def _setDelButton(self):
        if self.idx >= 0 and self.isSystemGroup(self.idx) == False:
            self.deb.Enable()
        else:
            self.deb.Disable()

    def _setUAButton(self):
        if self.idx < 0:
            self.uab.SetLabel(LABEL_ADD)
        else:
            self.uab.SetLabel(LABEL_UPD)


    def saveChanges(self):
        self.changedGroups.publishChanges()

    def appendGroup(self, name, gtype=TYPE_TXT_PRI):
        idx = self.glc.InsertStringItem(sys.maxint, name)
        self.glc.SetStringItem(idx, COLIDX_TYPE, gtype)

    def updateGroup(self, idx, name, gtype=TYPE_TXT_PRI):
        self.glc.SetStringItem(idx, COLIDX_NAME, name)
        self.glc.SetStringItem(idx, COLIDX_TYPE, gtype)


    def onOk(self, event):
        log.debug("Save changes in groups")
        self.saveChanges()
        self.Destroy()
        
