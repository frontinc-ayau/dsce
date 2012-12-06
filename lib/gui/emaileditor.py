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

import wx
import wx.lib.mixins.listctrl  as  listmix
import logging as log
import sys 

from domaindata.metadata import WORK_REL
from domaindata.metadata import HOME_REL
from domaindata.metadata import OTHER_REL
from domaindata.metadata import REL_LABEL

# for convenience
COLIDX_EMAIL   = 0
COLIDX_TYPE    = 1
COLIDX_LABEL   = 2
COLIDX_PRIMARY = 3

# Labels to use
LABEL_EMAIL = "Email Address"
LABEL_TYPE = "Type"
LABEL_LABEL= "Label"
LABEL_PRIMARY = "Primary"

class EmailListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.LIST_AUTOSIZE):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self._insertHeader()
        
    def _insertHeader(self):
        self.InsertColumn(COLIDX_EMAIL, LABEL_EMAIL)
        self.InsertColumn(COLIDX_TYPE, LABEL_TYPE)
        self.InsertColumn(COLIDX_LABEL, LABEL_LABEL)
        self.InsertColumn(COLIDX_PRIMARY, LABEL_PRIMARY)

    def _setPrimary(self, idx, primary):
        """This method takes also care that only one primary email
        address exists. If this behaviour is not wanted, change it 
        here.
        """
        if primary=="Yes" or primary == True:
            i = -1
            while True:
                i = self.GetNextItem(i, wx.LIST_NEXT_ALL)
                if i != -1:
                    if i == idx:
                        log.debug("In set primary idx %d - i %d" % (idx, i))
                        log.debug("SET YES")
                        self.SetStringItem(i, COLIDX_PRIMARY, "Yes")
                    else:
                        log.debug("SET NO")
                        self.SetStringItem(i, COLIDX_PRIMARY, "No")
                else:
                    break
        else:
            self.SetStringItem(idx, COLIDX_PRIMARY, "No")

    def appendRow(self, address="", type="", label="", primary=False):
        idx = self.InsertStringItem(sys.maxint, address)
        self.SetStringItem(idx, COLIDX_TYPE, type)
        self.SetStringItem(idx, COLIDX_LABEL, label)
        self._setPrimary(idx, primary)


    def updateRow(self, idx, address, type, label, primary):
        self.SetStringItem(idx, COLIDX_EMAIL, address)
        self.SetStringItem(idx, COLIDX_TYPE, type)
        self.SetStringItem(idx, COLIDX_LABEL, label)
        self._setPrimary(idx, primary)


    def deleteRow(self, idx):
        self.DeleteItem(idx)

    def getColumnText(self, idx, col):
        item = self.GetItem(idx, col)
        return item.GetText()



class EmailEditor(wx.Panel):
    def __init__(self, parent, id, table, row, col, style=0 ):
        wx.Panel.__init__(self, parent, id, style=style)

        self.labels = [LABEL_EMAIL, LABEL_TYPE, LABEL_LABEL, LABEL_PRIMARY]
        self.types = [ REL_LABEL[OTHER_REL], 
                       REL_LABEL[HOME_REL], 
                       REL_LABEL[WORK_REL]
                     ]
        self.updateLabel = {"add":"Add", "update":"Update"}

        self.gridTable = table
        self.row = row
        self.col = col

        # Safes the index of the current selected list item or -1 if
        # none is selected
        self.idx = -1 

        self.sizer = wx.FlexGridSizer(rows = 2, vgap=6, hgap=6)

        self.addEmailListCtrl()
        self.populate()
        self.addEmailForm()

        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0)
        self.SetSizer(self.sizer)

        self.binEvents()


    def binEvents(self):
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected, self.emailListCtrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeselected, self.emailListCtrl)
        self.Bind(wx.EVT_BUTTON, self.onAddOrUpdate, self.updateB)
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.deleteB)

    def addEmailListCtrl(self, id=-1):
        self.emailListCtrl = EmailListCtrl(self, id,
                                 style=wx.LC_REPORT 
                                 | wx.BORDER_SUNKEN
                                 # | wx.BORDER_NONE
                                 # | wx.LC_EDIT_LABELS
                                 | wx.LC_SORT_ASCENDING
                                 #| wx.LC_NO_HEADER
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 | wx.LC_SINGLE_SEL
                                 )
        self.sizer.Add(self.emailListCtrl, 1, wx.EXPAND)

        

    def addEmailForm(self, address="", type="other", label="", primary=False):
        
        et = wx.StaticText(self, -1, "Email Address")
        self.ec = wx.TextCtrl(self, -1, address, size=(200, -1))
        self.ec.SetFocus()
        tt = wx.StaticText(self, -1, "Type")
        self.tc = wx.Choice(self, -1, (-1, -1), choices = self.types)
        lt = wx.StaticText(self, -1, "Label")
        self.lc = wx.TextCtrl(self, -1, label, size=(100, -1))
        ct = wx.StaticText(self, -1, "Primary")
        self.cc = wx.CheckBox(self, -1 )

        self.updateB = wx.Button(self, 10, self.updateLabel["add"], (30, -1))
        self._setButtonLabel()
        self.deleteB = wx.Button(self, 20, "Delete", (30, -1))
        self._setDeleteButton()

        formSizer = wx.FlexGridSizer(rows=2, cols=5, vgap=6, hgap=6)
        formSizer.Add(et)
        formSizer.Add(self.ec)
        formSizer.Add(tt)
        formSizer.Add(self.tc)
        formSizer.Add(self.updateB)
        formSizer.Add(lt)
        formSizer.Add(self.lc)
        formSizer.Add(ct)
        formSizer.Add(self.cc)
        formSizer.Add(self.deleteB)

        self.sizer.Add(formSizer, 1, wx.ALIGN_CENTRE)


    def setFormType(self, type):
        try:
            self.tc.SetSelection(self.types.index(type))
        except:
            self.tc.SetSelection(-1)

    def setFormEmail(self, email):
        self.ec.SetValue(email)

    def setFormLabel(self, label):
        self.lc.SetValue(label)

    def setFormPrimary(self, primary):
        if primary == "Yes" or primary == True:
            self.cc.SetValue(True)
        else:
            self.cc.SetValue(False)

    def populate(self):
        log.debug("In populate()")
        for e in self.gridTable.GetValue(self.row, self.col):
            a = unicode(e.address) if e.address else u""
            t = unicode(REL_LABEL[e.rel]) if e.rel else u""
            l = unicode(e.label) if e.label else u""
            p = True if (e.primary and e.primary == "true") else False
            log.debug("a: %s  t: %s  l: %s  p: %s" % (a,t,l,p))
            self.emailListCtrl.appendRow( address=a, 
                                          type=t, 
                                          label=l, 
                                          primary=p)
 
    def _setButtonLabel(self):
        """Sets the label if idx refers to an existing entry or not
        """
        if self.idx < 0:
            self.updateB.SetLabel(self.updateLabel["add"])
        else:
            self.updateB.SetLabel(self.updateLabel["update"])


    def _setDeleteButton(self):
        if self.idx < 0:
            self.deleteB.Disable()
        else:
            self.deleteB.Enable()

    def onItemSelected(self, event):
        self.idx = event.GetIndex()
        self.setFormEmail(self.emailListCtrl.getColumnText(self.idx, COLIDX_EMAIL))
        self.setFormType(self.emailListCtrl.getColumnText(self.idx, COLIDX_TYPE))
        self.setFormLabel(self.emailListCtrl.getColumnText(self.idx, COLIDX_LABEL))
        self.setFormPrimary(self.emailListCtrl.getColumnText(self.idx, COLIDX_PRIMARY))
        self._setButtonLabel()
        self._setDeleteButton()

    def onItemDeselected(self, event):
        self.idx = -1
        self.setFormEmail("")
        self.setFormType(-1)
        self.setFormLabel("")
        self.setFormPrimary("No")
        self._setButtonLabel()
        self._setDeleteButton()

    def getTypeString(self, idx):
        if idx < 0:
            return unicode("")
        else:
            return unicode(self.types[idx])


    def addEntry(self):
        self.emailListCtrl.appendRow( address = self.ec.GetValue(), 
                                      type = self.getTypeString(self.tc.GetSelection()),
                                      label = self.lc.GetValue(), 
                                      primary = self.cc.GetValue()
                                    )
    def updateEntry(self):
        self.emailListCtrl.updateRow( idx = self.idx, 
                                      address = self.ec.GetValue(),  
                                      type = self.getTypeString(self.tc.GetSelection()),
                                      label = self.lc.GetValue(), 
                                      primary = self.cc.GetValue()
                                    )
    def resetForm(self):
        """Just to make it more readable or understandable
        """
        self.onItemDeselected(None) 
        

    def onAddOrUpdate(self, event):
        """Adds a new entry or updates an existing one
        """

        if self.idx < 0:
            log.debug("Add new entry")
            self.addEntry()
            self.resetForm()
        else:
            log.debug("Update existing entry")
            self.updateEntry()

    def onDelete(self, event):
        if self.idx >= 0:
            self.emailListCtrl.deleteRow(self.idx)
            self.resetForm()

    def saveChanges(self):
        """Saves changes made to emails.
        """
        emails = []
        idx = -1
        while True:
            idx = self.emailListCtrl.GetNextItem(idx, wx.LIST_NEXT_ALL)
            if idx != -1:

                e = self.emailListCtrl.getColumnText(idx, COLIDX_EMAIL)
                t = REL_LABEL.getKey(self.emailListCtrl.getColumnText(idx, COLIDX_TYPE))
                l = self.emailListCtrl.getColumnText(idx, COLIDX_LABEL)
                p = "true" if (self.emailListCtrl.getColumnText(idx, COLIDX_PRIMARY) == "Yes") else "false"

                emails.append([e,t,l,p])
            else:
                break

        self.gridTable.SetValue(self.row, self.col, emails)
            

class EmailEditDialog(wx.Dialog):

    def __init__(self, parent, ID, table, row, col, title="Edit Email Addresses"):

            wx.Dialog.__init__(self, parent, ID, title="Edit Email Addresses", 
                               style=wx.DEFAULT_DIALOG_STYLE
                                      | wx.RESIZE_BORDER
                                )

            self.emailEd = EmailEditor(self, -1, table, row, col)

            self.okB = wx.Button(self, wx.ID_OK)
            self.okB.SetDefault()
            self.Bind(wx.EVT_BUTTON, self.onOk, self.okB)
            
            self.cancelB = wx.Button(self, wx.ID_CANCEL)
            btnSizer = wx.StdDialogButtonSizer()
            btnSizer.Add(self.cancelB)
            btnSizer.Add(self.okB)
            btnSizer.Realize()

            space = 5
            self.topSizer = wx.BoxSizer(wx.VERTICAL)
            self.topSizer.Add(self.emailEd, 1, wx.EXPAND, space)
            self.topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND| wx.ALL, space)
            self.topSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT, space)

            self.SetSizer(self.topSizer)
            self.topSizer.Fit(self)
            
            self.SetMinSize(self.GetSize())
            self.SetSize((-1, 300))


            self.ShowModal()


    def onOk(self, event):
        self.emailEd.saveChanges()
        self.Destroy()

       
