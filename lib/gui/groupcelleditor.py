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

import domaindata

import logging as log

class DlgGroupData(object):
    def __init__(self):
        self.availableGroups = []
        self.memberGroupsIdx = []

    def initialize(self, table, row, col):
        self.table = table
        self.row = row
        self.col = col
        self.__initAvailable__()
        self.__initMemberGroups__()


    def __initAvailable__(self):
        s, p = domaindata.get_group_names()
        self.availableGroups = s+p

    def __initMemberGroups__(self):
        g=self.table.GetValue(self.row, self.col)
        if type(g) == str: # empty
            return u" "

        for l in g:
            if l:   
                self.memberGroupsIdx.append(self.availableGroups.index(
                                            unicode(domaindata.get_group_name(l.href)))
                                        )
    def groupsChanged(self, gidx):

        if len(self.memberGroupsIdx) != len(gidx):
            return False

        for i in gidx:
            if self.memberGroupsIdx.count(i) == 0:
                return False
        return True


    def saveChanges(self, gidx):
        if self.groupsChanged(gidx) == True:
            log.debug("Nothing changed")
        else:
            log.debug("Groups changed")
            newGroups = []
            for i in gidx:
                g=domaindata.get_group_id( self.availableGroups[i])
                newGroups.append(g)
                log.debug("Added group membership %s" % str(g))
            self.table.SetValue(self.row, self.col, newGroups)
        


class GroupCellEditDialog(wx.Dialog):

    def __init__(self, parent, ID, table, row, col, title="Edit Group Membership"):

        wx.Dialog.__init__(self, parent, ID, title, 
                           style=wx.DEFAULT_DIALOG_STYLE
                                 #| wx.RESIZE_BORDER
                           )

        # read panel and get important controlers for convenience
        
        self.panel = xrcl.loadPanel(self, "groupcelleditor.xrc", "groupcelleditor")
        self.lb = xrcl.getControl(self.panel, "chkgroupbox")

        self.groups = DlgGroupData()
        self.groups.initialize(table, row, col)

        self.populateGroupList()
        self.binEvents()
        

        space = 5
        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        self.topSizer.Add(self.panel, 1, wx.EXPAND, space)
        self.SetSizer(self.topSizer)
        self.topSizer.Fit(self)
        self.ShowModal()


    def binEvents(self):
        xrcl.getControl(self.panel, "wxID_OK").Bind(wx.EVT_BUTTON, self.onOk)

    def populateGroupList(self):
        self.lb.SetItems(self.groups.availableGroups)
        for i in self.groups.memberGroupsIdx:
            self.lb.Check(i)

    def onOk(self, event):
        log.debug("Save group changes to contact %s" % str(self.lb.GetChecked()))
        self.groups.saveChanges(self.lb.GetChecked())
        self.Destroy()

