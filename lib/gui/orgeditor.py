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


# what is needed for type
from domaindata.metadata import WORK_REL
from domaindata.metadata import OTHER_REL
from domaindata.metadata import REL_LABEL

import domaindata.orgf as orgf # makes life easier 


class OrgEditDialog(wx.Dialog):

    def __init__(self, parent, ID, table, row, col, title="Edit Organization"):

        wx.Dialog.__init__(self, parent, ID, title, 
                           style=wx.DEFAULT_DIALOG_STYLE
                                 #| wx.RESIZE_BORDER
                           )
        self.table = table
        self.row = row
        self.col = col
        
        self.types = ["", REL_LABEL[WORK_REL], REL_LABEL[OTHER_REL]]
        
        # read panel and get important controlers for convenience
        self.panel = xrcl.loadPanel(self, "orgeditor.xrc", "orgeditor")
        self.cnam = xrcl.getControl(self.panel, "cn")
        self.cdep = xrcl.getControl(self.panel, "cd")
        self.ctit = xrcl.getControl(self.panel, "ct")
        self.cjob = xrcl.getControl(self.panel, "cj")
        self.cwhe = xrcl.getControl(self.panel, "cw")
        self.clab = xrcl.getControl(self.panel, "cl")
        self.ctyp = xrcl.getControl(self.panel, "cr")
        self.csym = xrcl.getControl(self.panel, "cs")
        self.cpri = xrcl.getControl(self.panel, "cp")
        
        # Setup/customize form
        if not orgf.hasWhere(): # disable if not present
            self.ctyp.SetItems(items=self.types)
            xrcl.getControl(self.panel, "lw").Hide()
        self.cwhe.Hide()
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
        o = self.table.GetValue(self.row, self.col)
        if orgf.isOrganization(o): # else it is empty or other unusable stuff...
            log.debug("organization: %s" % str(o))

            if orgf.getLabel(o):        self.clab.SetValue(orgf.getLabel(o))
            if orgf.getDepartment(o):   self.cdep.SetValue(orgf.getDepartment(o))
            if orgf.getDescription(o):  self.cjob.SetValue(orgf.getDescription(o))
            if orgf.getName(o):         self.cnam.SetValue(orgf.getName(o))
            if orgf.getSymbol(o):       self.csym.SetValue(orgf.getSymbol(o))
            if orgf.getTitle(o):        self.ctit.SetValue(orgf.getTitle(o))
            if orgf.getPrimary(o):      self.cpri.SetValue(orgf.getPrimary(o))
            if orgf.getType(o):         self.ctyp.SetSelection(self.types.index(orgf.getType(o)))
            if orgf.getWhere(o):        self.cwhe.SetValue(orgf.getWhere(o))

    def saveChanges(self):
        """Saves if anything (except primary or type) has been set."""
        lab=(self.clab.GetValue() or None)
        dep=(self.cdep.GetValue() or None)
        des=(self.cjob.GetValue() or None)
        nam=(self.cnam.GetValue() or None)
        sym=(self.csym.GetValue() or None)
        tit=(self.ctit.GetValue() or None)
        pri=(self.cpri.GetValue() or None)
        whe=(self.cwhe.GetValue() or None)
        if self.ctyp.GetSelection() > 0: 
            typ=self.types[self.ctyp.GetSelection()]
        else:
            typ=None

        log.debug("lab set to %s" % lab)
        log.debug("dep set to %s" % dep)
        log.debug("des set to %s" % des)
        log.debug("nam set to %s" % nam)
        log.debug("sym set to %s" % sym)
        log.debug("tit set to %s" % tit)
        log.debug("pri set to %s" % pri)
        log.debug("whe set to %s" % whe)
        log.debug("typ set to %s" % typ)

        if lab or dep or des or nam or sym or tit or whe:
            log.debug("Generate object and save")
            o=orgf.getOrganization(label=lab, 
                                   department=dep, 
                                   description=des, 
                                   name=nam,
                                   symbol=sym, 
                                   title=tit, 
                                   primary=pri, 
                                   typel=typ, 
                                   where=whe)
            self.table.SetValue(self.row, self.col, o)


    def onOk(self, event):
        log.debug("Save changes in organization")
        self.saveChanges()
        self.Destroy()
        
