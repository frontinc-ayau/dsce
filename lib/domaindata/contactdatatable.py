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
"""PyGridTableBase implementation for DomainContacts
"""
import wx
import wx.grid
import metadata
import domaindata
import logging
import sys

from domaincontact import ACTION # need for label

import observer 
from observer import pmsg


class ContactDataTable(wx.grid.PyGridTableBase):
    """Uses Contacts found in DomainContacts and converts it into
     a PyGridTableBase object to be used within the Grid table.
    """
    def __init__(self, grid):
        """grid ... the owner grid of the ContactDataTable.
        """
        # This makes it convenient to send the necessary GRIDTABLE* events
        self.grid = grid
        wx.grid.PyGridTableBase.__init__(self)

        self.colLabels = metadata.get_labels()
        # as the order is guaranteed we can do the following
        self.getterMethods = metadata.get_getter()
        self.setterMethods = metadata.get_setter()

        self.dc = None
        self.rowLabels = []
        self.rowActionLabels = { ACTION.ADD:"Added", 
                                 ACTION.UPDATE:"Updated",
                                 ACTION.DELETE:"Deleted"
                               }

        logging.debug("Create ContactDataTable")
        logging.debug("Domain Contacts = %s" % self.dc)
        
        observer.subscribe(self._populateTable, pmsg.DATA_DOWNLOADED)

    def GetNumberRows(self):
        return len(self.rowLabels)

    def GetNumberCols(self):
        return len(self.colLabels)

    def IsEmptyCell(self, row, col):
        return False

    def getUidFromRow(self, row):
        """Wrapper to the fact that uid = row+1, at the moment
        """
        return self.dc[row].getUid()

    def getRowFromUid(self, uid):
        """Well, the oposit from above"""
        r = -1
        for c in self.dc:
            r += 1
            if c.getUid() == uid:
                return r
        return r

    def getContact(self, row):
        return self.dc.getContact(self.getUidFromRow(row))

    def GetValue(self, row, col):
        c = self.getContact(row)
        if c:
            rs = eval(self.getterMethods[col])
            if rs == None:
                return " "
            else:
                return rs
        else:
            return " "

    def SetValue(self, row, col, val):
        c = self.getContact(row)
        value = val
        if c:
            eval(self.setterMethods[col])
        

    def GetColLabelValue(self, col):
        return self.colLabels[col]
       
    def GetRowLabelValue(self, row):
        try:
            a = self.getContact(row).getAction()
        except Exception, e:
            logging.fatal("This should never happen %s" % str(e))
            sys.exit(200)
        
       
        if not a:
            return self.rowLabels[row]
        else:
            return self.rowActionLabels[a]

    def appendRow(self, c):
        """c ... DomainContact object"""
        self.rowLabels.append(c.getUid())
        return True

    def DeleteRows(self, row, numRows=1):
        self.rowLabels.pop(row)
        return True

    def DeleteCols(self, pos, numRows=1):
        return True

    def deleteRow(self, c):
        row = self.getRowFromUid(c.getUid())
        self.DeleteRows(row)
        logging.debug("GRIDTABLE_NOTIFY_ROWS_DELETED")
        msg = wx.grid.GridTableMessage(self,
                wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,row,1)
        self.grid.ProcessTableMessage(msg) 


    def rebuildTableIndex(self):
        logging.debug("Start to rebuild ContactDataTable index...")
        rowCount=0

        self.rowLabels=[]
        for c in self.dc:
            self.rowLabels.append(c.getUid())
            rowCount += 1
        logging.debug("Rebuild of %d rows done..." % rowCount)

        return rowCount


    def _populateTable(self, event):
        """Fills all necessary attributes by using the information 
        found in DomainContacts.
        """
        self.dc = domaindata.get_contacts()

        rowCount = self.rebuildTableIndex()

        if rowCount > 0:
            msg = wx.grid.GridTableMessage(self,
                    wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,rowCount)
            self.grid.ProcessTableMessage(msg) 
            self.grid.AutoSize()
        
