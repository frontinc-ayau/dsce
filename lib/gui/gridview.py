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
"""Grid table interface to the contacts.
"""
import wx
import wx.grid

import domaindata 
from domaindata import metadata

import observer
from observer import *

from emaileditor import EmailEditDialog
from emailcellrenderer import EmailCellRenderer
from addresseditor import AddressEditDialog
from addressrenderer import AddressCellRenderer
from phonerenderer import PhoneCellRenderer
from phoneeditor import PhoneEditDialog

import logging


class GridView(wx.grid.Grid):
    def __init__(self, parent, id=-1):

        wx.grid.Grid.__init__(self,parent,id, wx.Point(0, 0), wx.DefaultSize,
                              wx.NO_BORDER | wx.WANTS_CHARS)
        self.table = domaindata.get_grid_table(self)
        self.SetTable(self.table, True)
        self.setRenderer()
        self.setEditors()
        self.bind()
        self.subscribe()


    def bind(self):
        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.gridEditorRequest, self)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.gridCellChanged, self)

    def subscribe(self):
        observer.subscribe(self.appendRow, pmsg.CONTACT_ADDED) # interested if contact added
        observer.subscribe(self.forceRefresh, pmsg.DATA_UPLOADED) # because of label changes
        
    def appendRow(self, event):
        self.ProcessTableMessage(wx.grid.GridTableMessage(self.table,
                                                         wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
                                )


    def gridCellChanged(self, evt):
        logging.debug("Cell changed")
        self.forceRefresh(None)

    def gridEditorRequest(self, evt):
        """Used when others than PyGridCellEditors have to be used.
        """
        c = evt.GetCol()
        if c == metadata.get_col_idx("email"):
            EmailEditDialog(self, -1, self.table, evt.GetRow(), c)
            evt.Veto()
        elif c == metadata.get_col_idx("postal_address"):
            AddressEditDialog(self, -1, self.table, evt.GetRow(), c)
            evt.Veto()
        elif c == metadata.get_col_idx("phone"):
            PhoneEditDialog(self, -1, self.table, evt.GetRow(), c)
            evt.Veto()
        evt.Skip()

    def forceRefresh(self, evt):
        logging.debug("Force Refresh()")
        self.ForceRefresh()

    def setRenderer(self):
        attr = wx.grid.GridCellAttr()
        attr.SetRenderer(EmailCellRenderer())
        self.SetColAttr(metadata.get_col_idx("email"), attr)
        
        attr = wx.grid.GridCellAttr()
        attr.SetRenderer(AddressCellRenderer())
        self.SetColAttr(metadata.get_col_idx("postal_address"), attr)
        
        attr = wx.grid.GridCellAttr()
        attr.SetRenderer(PhoneCellRenderer())
        self.SetColAttr(metadata.get_col_idx("phone"), attr)

    def setEditors(self):
        attr = wx.grid.GridCellAttr()
        # attr.SetEditor(wx.grid.GridCellAutoWrapStringEditor())
        # self.SetColAttr(metadata.get_col_idx("postal_address"), attr)

