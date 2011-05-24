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
import  wx.lib.mixins.listctrl  as  listmix
import wx.lib.rcsizer  as rcsizer
import logging as log
import sys 

from domaindata import spaf
from domaindata.metadata import WORK_REL
from domaindata.metadata import HOME_REL
from domaindata.metadata import OTHER_REL
from domaindata.metadata import REL_LABEL

from domaindata.metadata import MAIL_BOTH
from domaindata.metadata import MAIL_LETTERS
from domaindata.metadata import MAIL_NEITHER
from domaindata.metadata import MAIL_PARCELS
from domaindata.metadata import MAIL_CLASS

from domaindata.metadata import GENERAL_ADDRESS
from domaindata.metadata import LOCAL_ADDRESS
from domaindata.metadata import MAIL_USAGE

from domaindata.metadata import AMI


from gui.countrychoice import CountryChoice



class AddressListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.LIST_AUTOSIZE):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        # Attribute index is used to keep track of what column holds what 
        # postal address information.
        # key = AddressMeta.id, value = column index
        self.attridx={} # key = AddressMeta.id, value = column index

        self._insertHeader()
        
    def _insertHeader(self):
        idx=0
        for ai in AMI:
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

    def _setPrimary(self, idx, primary):
        """This method takes also care that only one primary address
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

    def _getAddressMeataId(self, colidx):
        """Gets the AddressMeta.id on passed column index. 
        If the colidx is not found and BaseException is raised"""
        for id, idx in self.attridx.iteritems():
            if idx == colidx:
                return id
        raise BaseException("Unable to find index %d in address list control" % colidx)


    def appendRow(self, address):
        """address is one gdata.data.StructuredPostalAddress.
        """
        id0 = self._getAddressMeataId(0)

        address= spaf.getSPAdict(address)

        idx = self.InsertStringItem(sys.maxint,"" )
        for i, v in address.iteritems():
            self.SetStringItem(idx, self.attridx[i], address[i])


    def updateRow(self, idx, address):
        self.SetStringItem(idx, COLIDX_ADDRESS, address)


    def deleteRow(self, idx):
        self.DeleteItem(idx)

    def getColumnText(self, idx, col):
        item = self.GetItem(idx, col)
        return item.GetText()

class AddressForm(wx.Panel):
    def __init__(self, *args, **kwargs):

        wx.Panel.__init__(self, *args, **kwargs)

        # Safes the index of the current selected list item or -1 if
        # none is selected
        self.idx = -1 
        self.types = REL_LABEL.values()
        self.mailClasses = MAIL_CLASS.values()
        self.mailUsage = MAIL_USAGE.values()
        self.updateLabel = {"add":"Add", "update":"Update"}

        self.addCtrls()


    def addCtrls(self, type=REL_LABEL[OTHER_REL], label="", primary=False):
        pa = wx.StaticText(self, -1, AMI.getLabel("PA"))
        self.pa = wx.TextCtrl(self, -1, size=(200, -1), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER) 
        self.pa.SetToolTipString(AMI.getHelp("PA"))

        ty = wx.StaticText(self, -1, AMI.getLabel("TY"))
        self.ty = wx.Choice(self, -1, (-1, -1), choices = self.types)
        self.ty.SetToolTipString(AMI.getHelp("TY"))

        pr = wx.StaticText(self, -1, AMI.getLabel("PR"))
        self.pr = wx.CheckBox(self, -1 )
        self.pr.SetToolTipString(AMI.getHelp("PR"))

        ag = wx.StaticText(self, -1, AMI.getLabel("AG"))
        self.ag = wx.TextCtrl(self, -1, "", size=(170, -1))
        self.ag.SetToolTipString(AMI.getHelp("AG"))

        st = wx.StaticText(self, -1, AMI.getLabel("ST"))
        self.st = wx.TextCtrl(self, -1, "", size=(-1, -1))
        self.st.SetToolTipString(AMI.getHelp("ST"))

        po = wx.StaticText(self, -1, AMI.getLabel("PO"))
        self.po = wx.TextCtrl(self, -1, "", size=(-1, -1))
        self.po.SetToolTipString(AMI.getHelp("PO"))

        mc = wx.StaticText(self, -1, AMI.getLabel("MC"))
        self.mc = wx.Choice(self, -1, (-1, -1), choices = self.mailClasses)
        self.mc.SetToolTipString(AMI.getHelp("MC"))

        hn = wx.StaticText(self, -1, AMI.getLabel("HN"))
        self.hn = wx.TextCtrl(self, -1, "", size=(170, -1))
        self.hn.SetToolTipString(AMI.getHelp("HN"))

        nh = wx.StaticText(self, -1, AMI.getLabel("NH"))
        self.nh = wx.TextCtrl(self, -1, "", size=(170, -1))
        self.nh.SetToolTipString(AMI.getHelp("NH"))

        re = wx.StaticText(self, -1, AMI.getLabel("RE"))
        self.re = wx.TextCtrl(self, -1, "", size=(170, -1))
        self.re.SetToolTipString(AMI.getHelp("RE"))

        pc = wx.StaticText(self, -1, AMI.getLabel("PC"))
        self.pc = wx.TextCtrl(self, -1, "", size=(-1, -1))
        self.pc.SetToolTipString(AMI.getHelp("PC"))

        ci = wx.StaticText(self, -1, AMI.getLabel("CI"))
        self.ci = wx.TextCtrl(self, -1, "", size=(-1, -1))
        self.ci.SetToolTipString(AMI.getHelp("CI"))

        sr = wx.StaticText(self, -1, AMI.getLabel("SR"))
        self.sr = wx.TextCtrl(self, -1, "", size=(170, -1))
        self.sr.SetToolTipString(AMI.getHelp("SR"))

        co = wx.StaticText(self, -1, AMI.getLabel("CO"))
        self.co = CountryChoice(self)
        self.co.SetToolTipString(AMI.getHelp("CO"))

        la = wx.StaticText(self, -1, AMI.getLabel("LA"))
        self.la = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.la.SetToolTipString(AMI.getHelp("LA"))

        us = wx.StaticText(self, -1, AMI.getLabel("US"))
        self.us = wx.Choice(self, -1, (-1, -1), choices = self.mailUsage)
        self.us.SetToolTipString(AMI.getHelp("US"))

        self.updateB = wx.Button(self, 10, self.updateLabel["add"], (50, -1))
        self.deleteB = wx.Button(self, 20, "Delete", (50, -1))
        self.disableDeleteButton()

        # On my system the GridBagSizer did not run stable so I switched to 
        # the RowColSizer.
        formSizer = rcsizer.RowColSizer()

        formSizer.Add(pa,        row=0, col=1, flag=wx.ALIGN_LEFT)
        formSizer.Add(la,        row=4, col=1, flag=wx.ALIGN_LEFT )

        formSizer.AddSpacer(6,6, row=1, col=2)

        formSizer.Add(self.pa,   row=0, col=3, rowspan=4, flag=wx.EXPAND)
        formSizer.Add(self.la,   row=4, col=3, flag=wx.ALL)

        formSizer.AddSpacer(6,6, row=2, col=4)

        formSizer.Add(st,        row=0, col=5, flag=wx.ALIGN_LEFT)
        formSizer.Add(pc,        row=1, col=5, flag=wx.ALIGN_LEFT)
        formSizer.Add(po,        row=2, col=5, flag=wx.ALIGN_LEFT)
        formSizer.Add(ty,        row=3, col=5, flag=wx.ALIGN_LEFT)
        formSizer.Add(mc,        row=4, col=5, flag=wx.ALIGN_LEFT)

        formSizer.AddSpacer(6,6, row=2, col=6)

        formSizer.Add(self.st,   row=0, col=7, colspan=5, flag=wx.EXPAND)
        formSizer.Add(self.pc,   row=1, col=7, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.po,   row=2, col=7, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.ty,   row=3, col=7, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.mc,   row=4, col=7, flag=wx.ALIGN_LEFT)

        formSizer.AddSpacer(6,6, row=2, col=8)

        formSizer.Add(ci,        row=1, col=9, flag=wx.ALIGN_LEFT)
        formSizer.Add(co,        row=2, col=9, flag=wx.ALIGN_LEFT)
        formSizer.Add(us,        row=3, col=9, flag=wx.ALIGN_LEFT)
        formSizer.Add(pr,        row=4, col=9, flag=wx.ALIGN_LEFT)

        formSizer.AddSpacer(6,6, row=2, col=10)

        formSizer.Add(self.ci,   row=1, col=11, flag=wx.EXPAND)
        formSizer.Add(self.co,   row=2, col=11, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.us,   row=3, col=11, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.pr,   row=4, col=11, flag=wx.ALIGN_LEFT)

        formSizer.AddSpacer(6,6, row=1, col=12)

        formSizer.Add(hn,        row=0, col=13, flag=wx.ALIGN_LEFT)
        formSizer.Add(nh,        row=1, col=13, flag=wx.ALIGN_LEFT)
        formSizer.Add(re,        row=2, col=13, flag=wx.ALIGN_LEFT)
        formSizer.Add(sr,        row=3, col=13, flag=wx.ALIGN_LEFT)
        formSizer.Add(ag,        row=4, col=13, flag=wx.ALIGN_LEFT)

        formSizer.AddSpacer(6,6, row=1, col=14)

        formSizer.Add(self.hn,   row=0, col=15, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.nh,   row=1, col=15, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.re,   row=2, col=15, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.sr,   row=3, col=15, flag=wx.ALIGN_LEFT)
        formSizer.Add(self.ag,   row=4, col=15, flag=wx.ALIGN_LEFT)

        bBox = wx.BoxSizer(wx.HORIZONTAL)
        bBox.Add(self.deleteB)
        bBox.Add(self.updateB)

        formSizer.Add(bBox, row=5, col=15, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(formSizer)


    def setValue(self, id, v):
        """Sets the gui control identified by id (metadata.AddressMeta.id)
        to the passed value v.
        """
        if id == "PA": self.pa.SetValue(unicode(v))
        elif id == "ST": self.st.SetValue(unicode(v))
        elif id == "PC": self.pc.SetValue(unicode(v))
        elif id == "CI": self.ci.SetValue(unicode(v))
        elif id == "LA": self.la.SetValue(unicode(v))
        elif id == "AG": self.ag.SetValue(unicode(v))
        elif id == "HN": self.hn.SetValue(unicode(v))
        elif id == "NH": self.nh.SetValue(unicode(v))
        elif id == "PO": self.po.SetValue(unicode(v))
        elif id == "RE": self.re.SetValue(unicode(v))
        elif id == "SR": self.sr.SetValue(unicode(v))
        elif id == "CO": self.co.setValue(v)
        elif id == "PR":
            if (v and v == "true"):
                self.pr.SetValue(True)
            else:
                self.pr.SetValue(False)
        elif id == "TY": 
            try:
                self.ty.SetSelection(self.types.index(v))
            except:
                self.ty.SetSelection(-1)
        elif id == "MC":
            try:
                self.mc.SetSelection(self.mailClasses.index(v))
            except:
                self.mc.SetSelection(-1)
        elif id == "US": 
            try:
                self.us.SetSelection(self.mailUsage.index(v))
            except:
                self.us.SetSelection(-1)
        else: 
            raise BaseException("Id %s unknown!" % id)


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
        for id in AMI.getIDs():
            self.setValue(id, "")

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

    def onAddOrUpdate(self, event):
        """Adds a new entry or updates an existing one
        """

        if self.idx < 0:
            log.debug("Add new entry")
            self.addEntry()
            self.reset()
        else:
            log.debug("Update existing entry")
            self.updateEntry()

    def onDelete(self, event):
        if self.idx >= 0:
            self.emailListCtrl.deleteRow(self.idx)
            self.reset()
        

class AddressEditor(wx.Panel):
    """Responsible to initialize and display the forms UI components and manages
    the work flow and control of the dialog (what to display when and what to call
    when etc.). 
    """
    def __init__(self, parent, id, table, row, col, style=0 ):
        wx.Panel.__init__(self, parent, id, style=style)



        self.gridTable = table
        self.row = row
        self.col = col

        # Safes the index of the current selected list item or -1 if
        # none is selected

        self.sizer = wx.FlexGridSizer(rows = 2, vgap=6, hgap=6)

        self.addressListCtrl = None
        self.addressForm = None

        self.addAddressListCtrl()
        self.populate()
        self.addAddressForm()

        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0)
        self.SetSizer(self.sizer)

        self.bindEvents()


    def bindEvents(self):
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected, self.addressListCtrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeselected, self.addressListCtrl)
        # self.Bind(wx.EVT_BUTTON, self.onAddOrUpdate, self.updateB)
        # self.Bind(wx.EVT_BUTTON, self.onDelete, self.deleteB)


    def addAddressListCtrl(self, id=-1):
        self.addressListCtrl = AddressListCtrl(self, id,
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
        self.sizer.Add(self.addressListCtrl, 1, wx.EXPAND)

        

    def addAddressForm(self, address="", type="other", label="", primary=False):
        self.addressForm = AddressForm(self, -1)
        self.sizer.Add( self.addressForm , 1, wx.ALIGN_LEFT)



    def populate(self):
        log.debug("In populate()")
        for e in self.gridTable.GetValue(self.row, self.col):
            self.addressListCtrl.appendRow( address=e )
 
    def onItemSelected(self, event):
        item = event.GetItem()
        idx = event.GetIndex()
        log.debug("Selected Item  - %s" % item.GetText())
        log.debug("Item Attribute - %s" % item.GetAttributes())
        log.debug("Number of cols - %d" % self.addressListCtrl.GetColumnCount())
        for ci in range( 0, (self.addressListCtrl.GetColumnCount()) ):
            log.debug("Select %s - %s " % (
                            self.addressListCtrl.getColId(ci), 
                            self.addressListCtrl.getColumnText(idx, ci)))
            self.addressForm.setValue( self.addressListCtrl.getColId(ci), 
                                       self.addressListCtrl.getColumnText(idx, ci))

        self.addressForm.setButtonLabelUpdate()
        self.addressForm.enableDeleteButton()

    def onItemDeselected(self, event):
        self.addressForm.reset()
        self.addressForm.setButtonLabelAdd()
        self.addressForm.disableDeleteButton()


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
            

class AddressEditDialog(wx.Dialog):

    def __init__(self, parent, ID, table, row, col, title="Edit Postal Addresses"):

            wx.Dialog.__init__(self, parent, ID, title, 
                               style=wx.DEFAULT_DIALOG_STYLE
                                      | wx.RESIZE_BORDER
                                )

            self.addressEd = AddressEditor(self, -1, table, row, col)

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
            self.topSizer.Add(self.addressEd, 1, wx.EXPAND, space)
            self.topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND| wx.ALL, space)
            self.topSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT, space)

            self.SetSizer(self.topSizer)
            self.topSizer.Fit(self)
            
            self.SetMinSize(self.GetSize())
            self.SetSize((-1, 300))


            self.ShowModal()


    def onOk(self, event):
        # self.addressEd.saveChanges()
        self.Destroy()

       
