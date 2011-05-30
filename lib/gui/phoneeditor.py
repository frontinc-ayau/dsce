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
import  wx.lib.mixins.listctrl  as  listmix
import wx.lib.rcsizer  as rcsizer
import logging as log
import sys 

from gdata.data import OTHER_REL

from domaindata.metadata import PID_NUMBER 
from domaindata.metadata import PID_TYPE   
from domaindata.metadata import PID_LABEL  
from domaindata.metadata import PID_PRIMARY
from domaindata.metadata import PID_URI    
from domaindata.metadata import PMI
from domaindata.metadata import PHONE_TYPE


import gdata.data


class PhoneListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.LIST_AUTOSIZE):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        # Attribute index is used to keep track of what column holds what 
        # postal address information.
        # key = AddressMeta.id, value = column index
        self.attridx={} 

        self._insertHeader()
        
    def _insertHeader(self):
        idx=0
        for ai in PMI:
            self.InsertColumn(idx, ai.label)
            self.attridx[ai.id] = idx
            idx+=1

    def getColId(self, ci):
        """Returns the id of the column on position ci (column index).
        """
        for id , i in self.attridx.iteritems():
            if i == ci:
                return id
        raise BaseException("Columng indes %d does not exist!" % ci)


    def _getPhoneMeataId(self, colidx):
        """Gets the PhoneMeta.id on passed column index. 
        If the colidx is not found and BaseException is raised"""
        for id, idx in self.attridx.iteritems():
            if idx == colidx:
                return id
        raise BaseException("Unable to find index %d in address list control" % colidx)


    def appendRow(self, address):
        pass

    def updateRow(self, idx, ad):
        """idx ... row index
        ad  ... address dictionary {ID:VAL}"""
        pass

    def addRow(self, ad):
        pass


    def deleteRow(self, idx):
        pass

    def getColumnText(self, idx, col):
        pass

    def getAsDict(self, idx):
        pass

    def setColumnValue(self, idx, id, val):
        pass
        


class PhoneForm(wx.Panel):
    def __init__(self, *args, **kwargs):

        wx.Panel.__init__(self, *args, **kwargs)

        self.updateLabel = {"add":"Add", "update":"Update"}
        self.types = PHONE_TYPE.values()

        self.addCtrls()


    def addCtrls(self, type=PHONE_TYPE[OTHER_REL], label="", primary=False):
        nr = wx.StaticText(self, -1, PMI.getLabel(PID_NUMBER))
        self.nr = wx.TextCtrl(self, -1, size=(150, -1))
        self.nr.SetToolTipString(PMI.getHelp(PID_NUMBER))
        
        la = wx.StaticText(self, -1, PMI.getLabel(PID_LABEL))
        self.la = wx.TextCtrl(self, -1, size=(150, -1))
        self.la.SetToolTipString(PMI.getHelp(PID_LABEL))

        ur = wx.StaticText(self, -1, PMI.getLabel(PID_URI))
        self.ur = wx.TextCtrl(self, -1, size=(150, -1))
        self.ur.SetToolTipString(PMI.getHelp(PID_URI))

        pr = wx.StaticText(self, -1, PMI.getLabel(PID_PRIMARY))
        self.pr = wx.CheckBox(self, -1 )
        self.pr.SetToolTipString(PMI.getHelp(PID_PRIMARY))

        ty = wx.StaticText(self, -1, PMI.getLabel(PID_TYPE))
        self.ty = wx.Choice(self, -1, (-1, -1), choices = self.types)
        self.ty.SetToolTipString(PMI.getHelp(PID_TYPE))

        self.updateB = wx.Button(self, 10, self.updateLabel["add"], (50, -1))
        self.deleteB = wx.Button(self, 20, "Delete", (50, -1))
        self.disableDeleteButton()
        
        # formSizer = wx.FlexGridSizer(rows=3, cols=5, vgap=6, hgap=6)
        formSizer = rcsizer.RowColSizer()
        formSizer.Add(nr,           row=0, col=0, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.nr,      row=0, col=1, flag=wx.EXPAND)
        formSizer.Add(ty,           row=0, col=2, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.ty,      row=0, col=3)
        formSizer.Add(self.updateB, row=0, col=4, flag= wx.ALIGN_RIGHT)

        formSizer.Add(la,           row=1, col=0, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.la,      row=1, col=1, flag=wx.EXPAND)
        formSizer.Add(pr,           row=1, col=2, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.pr,      row=1, col=3, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.deleteB, row=1, col=4, flag= wx.ALIGN_LEFT)

        formSizer.Add(ur,           row=2, col=0, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.ur,      row=2, col=1, flag=wx.EXPAND)
        formSizer.AddSpacer(6,6,    row=2, col=2)
        formSizer.AddSpacer(6,6,    row=2, col=3)
        formSizer.AddSpacer(6,6,    row=2, col=4)

        self.SetSizer(formSizer)


    def setValue(self, id, v):
        """Sets the gui control identified by id (metadata.AddressMeta.id)
        to the passed value v.
        """
        pass
        if id == "PA": self.pa.SetValue(unicode(v))
        # elif id == "ST": self.st.SetValue(unicode(v))
        # elif id == "PC": self.pc.SetValue(unicode(v))
        # elif id == "CI": self.ci.SetValue(unicode(v))
        # elif id == "PR":
        #     if (v and (v == "true" or v == "yes") ):
        #         self.pr.SetValue(True)
        #     else:
        #         self.pr.SetValue(False)
        # elif id == "TY": 
        #     try:
        #         self.ty.SetSelection(self.types.index(v))
        #     except:
        #         self.ty.SetSelection(-1)
        # elif id == "MC":
        #     try:
        #         self.mc.SetSelection(self.mailClasses.index(v))
        #     except:
        #         self.mc.SetSelection(-1)
        # elif id == "US": 
        #     try:
        #         self.us.SetSelection(self.mailUsage.index(v))
        #     except:
        #         self.us.SetSelection(-1)
        # else: 
        #     raise BaseException("Id %s unknown!" % id)

    def getValues(self):
        """Returns its values as dict {ID:VAL, ...}. Unset Values will not be 
        included in the dictionary"""
        # d = {}
        # d["PA"] = self.pa.GetValue()
        # d["ST"] = self.st.GetValue()
        # d["PC"] = self.pc.GetValue()
        # d["CI"] = self.ci.GetValue()
        # d["LA"] = self.la.GetValue()
        # d["AG"] = self.ag.GetValue()
        # d["HN"] = self.hn.GetValue()
        # d["NH"] = self.nh.GetValue()
        # d["PO"] = self.po.GetValue()
        # d["RE"] = self.re.GetValue()
        # d["SR"] = self.sr.GetValue()
        # if self.co.GetCurrentSelection() >= 0:
        #     d["CO"] = self.co.getValue(self.co.GetCurrentSelection())
        # if self.ty.GetCurrentSelection() >= 0:
        #     d["TY"] = self.types[self.ty.GetCurrentSelection()]
        # if self.pr.GetValue():
        #     d["PR"] = "yes"
        # else:
        #     d["PR"] = ""
        # if self.mc.GetCurrentSelection() >= 0:
        #     d["MC"] = self.mailClasses[self.mc.GetCurrentSelection()]
        # if self.us.GetCurrentSelection() >= 0:
        #     d["US"] = self.mailUsage[self.us.GetCurrentSelection()]
        # return d
        pass

    def setButtonLabelAdd(self):
        """Sets the label if idx refers to an existing entry or not
        """
        self.updateB.SetLabel(self.updateLabel["add"])

    def setButtonLabelUpdate(self):
        """Sets the label if idx refers to an existing entry or not
        """
        self.updateB.SetLabel(self.updateLabel["update"])

    def enableDeleteButton(self):
        self.deleteB.Enable()

    def disableDeleteButton(self):
        self.deleteB.Disable()

    def getTypeString(self, idx):
        if idx < 0:
            return unicode("")
        else:
            return unicode(self.types[idx])

    def reset(self):
        """Just to make it more readable or understandable
        """
        pass

        

class PhoneEditor(wx.Panel):
    """Responsible to initialize and display the forms UI components and manages
    the work flow and control of the dialog (what to display when and what to call
    when etc.). 
    """
    def __init__(self, parent, id, table, row, col, style=0 ):
        wx.Panel.__init__(self, parent, id, style=style)



        self.gridTable = table
        self.row = row
        self.col = col
        self.hasChanged = False # set to true if add, update or delete has been invoked

        # Safes the index of the current selected list item or -1 if
        # none is selected
        self.idx = -1 

        self.sizer = wx.FlexGridSizer(rows = 2, vgap=6, hgap=6)

        self.listCtrl = None
        self.addListCtrl()
        # self.populate()

        self.form = None
        self.addForm()

        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0)
        self.SetSizer(self.sizer)

        # self.bindEvents()


    def bindEvents(self):
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected, self.listCtrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeselected, self.listCtrl)
        self.Bind(wx.EVT_BUTTON, self.onAddOrUpdate, self.form.updateB)
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.form.deleteB)


    def addListCtrl(self, id=-1):
        self.listCtrl = PhoneListCtrl(self, id,
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
        self.sizer.Add(self.listCtrl, 1, wx.EXPAND)

        

    def addForm(self, address="", type="other", label="", primary=False):
        self.form = PhoneForm(self, -1)
        self.sizer.Add( self.form , 1, wx.ALIGN_LEFT)



    def populate(self):
        log.debug("In populate()")
        for e in self.gridTable.GetValue(self.row, self.col):
            self.listCtrl.appendRow( address=e )
 
    def onItemSelected(self, event):
        self.idx = event.GetIndex()
        for ci in range( 0, (self.listCtrl.GetColumnCount()) ):
            self.form.setValue( self.listCtrl.getColId(ci), 
                                       self.listCtrl.getColumnText(self.idx, ci))

        self.form.setButtonLabelUpdate()
        self.form.enableDeleteButton()

    def applyEditRules(self, d):
        """Check and apply rules that needs to be followed before updating or adding
        an entry"""
        item = -1
        if d.has_key("PR"):
            if d["PR"] == 'yes':
                while True:
                    item = self.listCtrl.GetNextItem(item, wx.LIST_NEXT_ALL)
                    if item != -1:
                        self.listCtrl.setColumnValue(item, "PR", "")
                    else:
                        break

    def onAddOrUpdate(self, event):
        """Adds a new entry or updates an existing one
        """
        d = self.form.getValues()
        log.debug("form: %s" % str(d))

        self.applyEditRules(d)

        if self.idx < 0:
            log.debug("Add new entry")
            self.listCtrl.addRow(d)
            self.form.reset()
        else:
            log.debug("Update existing entry")
            self.listCtrl.updateRow(self.idx, d)
        self.hasChanged = True

    def onItemDeselected(self, event):
        self.idx=-1
        self.form.reset()
        self.form.setButtonLabelAdd()
        self.form.disableDeleteButton()

    def onDelete(self, event):
        self.listCtrl.deleteRow(self.idx)
        self.form.reset()
        self.idx=-1
        self.hasChanged = True

    def getSPAfromListItem(self, item):
        """Converts a address list item into a StructurePostalAddress object
        and returns it."""
        log.debug("Item passed %s" % str(item))
        self.listCtrl.getAsDict(item)
        return spaf.getSPAfromDict( self.listCtrl.getAsDict(item) )

    def saveChanges(self):
        """Saves changes made to postal_addresses.
        """
        addresses = []
        item = -1

        if self.hasChanged:

            while True:
                item = self.listCtrl.GetNextItem(item, wx.LIST_NEXT_ALL)
                if item != -1:
                    addresses.append( self.getSPAfromListItem(item) )
                else:
                    break

            self.gridTable.SetValue(self.row, self.col, addresses)
            


class PhoneEditDialog(wx.Dialog):

    def __init__(self, parent, ID, table, row, col, title="Edit Postal Addresses"):

            wx.Dialog.__init__(self, parent, ID, title, 
                               style=wx.DEFAULT_DIALOG_STYLE
                                      | wx.RESIZE_BORDER
                                )

            self.editor = PhoneEditor(self, -1, table, row, col)

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
            self.topSizer.Add(self.editor, 1, wx.EXPAND, space)
            self.topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND| wx.ALL, space)
            self.topSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT, space)

            self.SetSizer(self.topSizer)
            self.topSizer.Fit(self)
            
            self.SetMinSize(self.GetSize())
            self.SetSize((-1, 300))


            self.ShowModal()


    def onOk(self, event):
        self.editor.saveChanges()
        self.Destroy()

       
