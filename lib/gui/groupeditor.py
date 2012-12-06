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

class GroupName(object):
    def __init__(self, name):
        self.current = name
        self.previous = None
        self.flag = None # pmsg.GROUP_UPDATED, pmsg.GROUP_ADDED, pmsg.GROUP_DELETED or None

    def update(self, new_name):
        if self.current == new_name:
            return

        if not self.flag:
            self.previous = self.current
            self.current = new_name
            self.flag = pmsg.GROUP_UPDATED
        else:
            if self.previous == new_name: # means step back to previous name
                self.current = self.previous
                self.previous = None
                if self.flag != pmsg.GROUP_ADDED:
                    self.clearFlag()
            else:
                self.previous = self.current
                self.current = new_name
                if self.flag != pmsg.GROUP_ADDED: # added should remain added
                    self.flag = pmsg.GROUP_UPDATED


    def delete(self):
        self.flag = pmsg.GROUP_DELETED
    
    def new(self):
        self.flag = pmsg.GROUP_ADDED

    def clearFlag(self):
        self.flag = None


class Groups(object):
    def __init__(self, names):
        self.groups = []
        if type(names) != list:
            raise Exception("Groups needs a list to initialize!")
        for n in names:
            if type(n) == str or type(n) == unicode:
                self.groups.append(GroupName(n))
            else:
                raise Exception("Cannot initialize GroupName from type %s" % str(type(n)))

    def groupExists(self, name):
        for g in self.groups:
            if g.current == name:
                return True
        return False

    def add(self, name):
        if self.groupExists(name):
            raise Exception("Group %s already exists" % name)
        else:
            g=GroupName(name)
            g.new()
            self.groups.append(g)

    def delete(self, name):
        for g in self.groups:
            if g.current == name:
                g.delete()
                return
        raise Exception("Cannot delete private group '%s' because it does not exist" % name)
        

    def update(self, old, new):
        for g in self.groups:
            if g.current == old:
                g.update(new)

    def get(self):
        return self.groups

    def publishChanges(self):
        for g in self.groups:
            if g.flag:
                observer.send_message(g.flag, data=g)
                g.clearFlag()
                log.debug("Published %s %s" % (str(g.flag), g.current))
        
class GroupEditDialog(wx.Dialog):

    def __init__(self, parent, ID=-1, title="Manage Groups"):

        wx.Dialog.__init__(self, parent, ID, title, 
                           style=wx.DEFAULT_DIALOG_STYLE
                                 #| wx.RESIZE_BORDER
                           )
        self.idx = -1

        # s = system groups, p = private groups
        s, p = domaindata.get_group_names()
        self.sg = Groups(s)
        self.pg = Groups(p)
        

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
        for g in self.sg.get():
            self.appendGroup(g.current, TYPE_TXT_SYS)
        for g in self.pg.get():
            self.appendGroup(g.current, TYPE_TXT_PRI)


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
            name = self.gnc.GetValue().strip()
            try:
                self.pg.delete(name)
                self.glc.DeleteItem(self.idx)
            except Exception, e:
                observer.send_message(pmsg.ALERT, data=str(e))

            self.clearForm()


    def onAddOrUpdate(self, event):
        name = self.gnc.GetValue().strip()

        if len(name) == 0: return

        if self.idx < 0:
            try:
                self.pg.add(name)
                self.appendGroup( name, TYPE_TXT_PRI)
            except Exception, e:
                observer.send_message(pmsg.ALERT, data=str(e))
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
        self.pg.publishChanges()

    def appendGroup(self, name, gtype=TYPE_TXT_PRI):
        idx = self.glc.InsertStringItem(sys.maxint, name)
        self.glc.SetStringItem(idx, COLIDX_TYPE, gtype)

    def updateGroup(self, idx, name, gtype=TYPE_TXT_PRI):
        oldname = self.glc.GetItem(idx, COLIDX_NAME).GetText()
        self.glc.SetStringItem(idx, COLIDX_NAME, name)
        self.glc.SetStringItem(idx, COLIDX_TYPE, gtype)
        self.pg.update(oldname, name)


    def onOk(self, event):
        log.debug("Save changes in groups")
        self.saveChanges()
        self.Destroy()
        
