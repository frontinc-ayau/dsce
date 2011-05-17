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


class AddressMeta(object):
    def __init__(self, id, label, help):
        """id ... unique identifier to be used throughout this dialogue
        label ... label to be displayed
        help  ... description of the label
        """
        self.id = id
        self.label = label
        self.help = help

class AddressMetaList(list):
    def getLabel(self, id):
        """Returns the label of passed id, else a BaseExceptio will be raised.
        """
        for a in self:
            if a.id == id:
                return a.label
        raise BaseException("Unknown id %s" % id)

metaInfo=AddressMetaList()

# as id a two character abbreviation is used
metaInfo.append(AddressMeta(
                        "PA",
                        "Postal Address",
                        """The full, unstructured postal address."""
                        ))

metaInfo.append(AddressMeta(
                        "PR",
                        "Primary",
                        """Specifies the address as primary. Default value is false."""
                        ))

metaInfo.append(AddressMeta(
                        "ST",
                        "Street",
                        """Can be street, avenue, road, etc. This element also includes the
house number and room/apartment/flat/floor number."""
                        ))

metaInfo.append(AddressMeta(
                        "PC",
                        "Postal Code",
                        """Postal code. Usually country-wide, but sometimes specific to the
city (e.g. "2" in "Dublin 2, Ireland" addresses)."""
                        ))

metaInfo.append(AddressMeta(
                        "CI",
                        "City",
                        """Can be city, village, town, borough, etc. This is the postal town and
not necessarily the place of residence or place of business."""
                        ))

metaInfo.append(AddressMeta(
                        "CO",
                        "Country",
                        """The name or code of the country."""
                        ))

metaInfo.append(AddressMeta(
                        "TY",
                        "Type",
                        """Type of the address. Unless specified work type is assumed."""
                        ))

metaInfo.append(AddressMeta(
                        "LA",
                        "Label",
                        """Label"""
                        ))

metaInfo.append(AddressMeta(
                        "AG",
                        "Agent",
                        """The agent who actually receives the mail. Used in work addresses. 
Also for 'in care of' or 'c/o'."""
                        ))

metaInfo.append(AddressMeta(
                        "HN",
                        "House Name",
                        """Used in places where houses or buildings have names (and not
necessarily numbers), eg. "The Pillars"."""
                        ))


metaInfo.append(AddressMeta(
                        "MC",
                        "Mail Class",
                        """Classes of mail (letters, parcels) accepted at the address. Unless specified both is assumed."""
                        ))

metaInfo.append(AddressMeta(
                        "NH",
                        "Neighbourhood",
                        """This is used to disambiguate a street address when a city contains more
than one street with the same name, or to specify a small place whose
mail is routed through a larger postal town. In China it could be a
county or a minor city."""
                        ))

metaInfo.append(AddressMeta(
                        "PO",
                        "P.O. Box",
                        """Covers actual P.O. boxes, drawers, locked bags, etc. This is usually
but not always mutually exclusive with street."""
                        ))

metaInfo.append(AddressMeta(
                        "RE",
                        "Region",
                        """A state, province, county (in Ireland), Land (in Germany),
departement (in France), etc."""
                        ))

metaInfo.append(AddressMeta(
                        "SR",
                        "Subregion",
                        """Handles administrative districts such as U.S. or U.K. counties that are
not used for mail addressing purposes. Subregion is not intended for
delivery addresses."""
                        ))

metaInfo.append(AddressMeta(
                        "US",
                        "Usage",
                        """The context in which this address can be used. Local addresses may differ in 
layout from general addresses, and frequently use local script (as opposed to Latin script) 
as well, though local script is allowed in general addresses. Unless specified general usage is 
assumed."""
                        ))

class AddressListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.LIST_AUTOSIZE):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self._insertHeader()
        
    def _insertHeader(self):
        idx=0
        for ai in metaInfo:
            self.InsertColumn(idx, ai.label)
            idx+=1

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

    def appendRow(self, address=""):
        idx = self.InsertStringItem(sys.maxint, address)


    def updateRow(self, idx, address):
        self.SetStringItem(idx, COLIDX_ADDRESS, address)


    def deleteRow(self, idx):
        self.DeleteItem(idx)

    def getColumnText(self, idx, col):
        item = self.GetItem(idx, col)
        return item.GetText()


class AddressEditor(wx.Panel):
    def __init__(self, parent, id, table, row, col, style=0 ):
        wx.Panel.__init__(self, parent, id, style=style)

        self.types = [ REL_LABEL[OTHER_REL], 
                       REL_LABEL[HOME_REL], 
                       REL_LABEL[WORK_REL]
                     ]

        self.mailClasses = [ MAIL_CLASS[MAIL_BOTH],
                             MAIL_CLASS[MAIL_LETTERS],
                             MAIL_CLASS[MAIL_PARCELS],
                             MAIL_CLASS[MAIL_NEITHER]
                        ]

        self.mailUsage = [ MAIL_USAGE[GENERAL_ADDRESS],
                           MAIL_USAGE[LOCAL_ADDRESS]
                        ] 

        self.updateLabel = {"add":"Add", "update":"Update"}

        self.gridTable = table
        self.row = row
        self.col = col

        # Safes the index of the current selected list item or -1 if
        # none is selected
        self.idx = -1 

        self.sizer = wx.FlexGridSizer(rows = 2, vgap=6, hgap=6)

        self.addAddressListCtrl()
        # self.populate()
        self.addAddressForm()

        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0)
        self.SetSizer(self.sizer)

        # self.binEvents()


    def binEvents(self):
        pass
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected, self.emailListCtrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeselected, self.emailListCtrl)
        self.Bind(wx.EVT_BUTTON, self.onAddOrUpdate, self.updateB)
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.deleteB)

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
        
        pa = wx.StaticText(self, -1, metaInfo.getLabel("PA"))
        self.pa = wx.TextCtrl(self, -1, size=(200, -1), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER) 
        ty = wx.StaticText(self, -1, metaInfo.getLabel("TY"))
        self.ty = wx.Choice(self, -1, (-1, -1), choices = self.types)
        pr = wx.StaticText(self, -1, metaInfo.getLabel("PR"))
        self.pr = wx.CheckBox(self, -1 )
        ag = wx.StaticText(self, -1, metaInfo.getLabel("AG"))
        self.ag = wx.TextCtrl(self, -1, address, size=(170, -1))

        st = wx.StaticText(self, -1, metaInfo.getLabel("ST"))
        self.st = wx.TextCtrl(self, -1, address, size=(-1, -1))
        po = wx.StaticText(self, -1, metaInfo.getLabel("PO"))
        self.po = wx.TextCtrl(self, -1, address, size=(-1, -1))
        mc = wx.StaticText(self, -1, metaInfo.getLabel("MC"))
        self.mc = wx.Choice(self, -1, (-1, -1), choices = self.mailClasses)

        hn = wx.StaticText(self, -1, metaInfo.getLabel("HN"))
        self.hn = wx.TextCtrl(self, -1, address, size=(170, -1))
        nh = wx.StaticText(self, -1, metaInfo.getLabel("NH"))
        self.nh = wx.TextCtrl(self, -1, address, size=(170, -1))
        re = wx.StaticText(self, -1, metaInfo.getLabel("RE"))
        self.re = wx.TextCtrl(self, -1, address, size=(170, -1))

        pc = wx.StaticText(self, -1, metaInfo.getLabel("PC"))
        self.pc = wx.TextCtrl(self, -1, address, size=(-1, -1))
        ci = wx.StaticText(self, -1, metaInfo.getLabel("CI"))
        self.ci = wx.TextCtrl(self, -1, address, size=(170, -1))
        sr = wx.StaticText(self, -1, metaInfo.getLabel("SR"))
        self.sr = wx.TextCtrl(self, -1, address, size=(170, -1))

        co = wx.StaticText(self, -1, metaInfo.getLabel("CO"))
        self.co = wx.TextCtrl(self, -1, address, size=(170, -1))
        la = wx.StaticText(self, -1, metaInfo.getLabel("LA"))
        self.la = wx.TextCtrl(self, -1, address, size=(200, -1))
        us = wx.StaticText(self, -1, metaInfo.getLabel("US"))
        self.us = wx.Choice(self, -1, (-1, -1), choices = self.mailUsage)

        self.updateB = wx.Button(self, 10, self.updateLabel["add"], (50, -1))
        # self._setButtonLabel()
        self.deleteB = wx.Button(self, 20, "Delete", (50, -1))
        # self._setDeleteButton()

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

        formSizer.Add(self.ci,   row=1, col=11, flag=wx.ALIGN_LEFT)
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

        self.sizer.Add(formSizer, 1, wx.ALIGN_LEFT)


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

       
