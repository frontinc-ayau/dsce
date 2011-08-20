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
# Copyright (c) 2010, 2011 Klaus Melcher (melcher.kla@gmail.com)
import wx
import wx.grid

import domaindata.spaf as spaf

import logging


class AddressCellRenderer(wx.grid.PyGridCellRenderer):
    def __init__(self):
        """Used to render 0 to n structured postal addresses within a cell, 
        each address address is written in a separate row.
        """
        wx.grid.PyGridCellRenderer.__init__(self)
        self._DELIMITER="|"

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        dc.SetClippingRect(rect)

        addresses = self.getValueAsString(grid, row, col)
        
        hAlign, vAlign = attr.GetAlignment()
        dc.SetFont ( attr.GetFont() )

        if isSelected:
            bg = grid.GetSelectionBackground()
            fg = grid.GetSelectionForeground()
        else:
            bg = attr.GetBackgroundColour()
            fg = attr.GetTextColour()

        dc.SetTextBackground(bg)
        dc.SetTextForeground(fg)
        dc.SetBrush(wx.Brush(bg, wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)

        self.drawAddresses(dc, rect, addresses)
        

    def drawAddresses(self, dc, rect, addresses):
        dc.DrawRectangleRect(rect)

        w, h = dc.GetTextExtent(addresses)
        x = rect.x+1
        y = rect.y+1
        for a in addresses.split(self._DELIMITER):
            dc.DrawText(a, x, y)
            y = y+h+1

        dc.DestroyClippingRegion()


    def getValueAsString(self, grid, row, col):
        """Returns the requested value as usable unicode string. 
        Each entry is delimited by self._DELIMITER
        """
        addresses = u""

        for a in grid.GetTable().GetValue(row,col):
            a = spaf.getFirstString(a)
            if a:   
                addresses +=  unicode(a).replace("\n"," ")+u" "
                addresses += self._DELIMITER

        return addresses

    def addressCount(self, grid, row, col):
        return len(grid.GetTable().GetValue(row, col))

    def GetBestSize(self, grid, attr, dc, row, col):
        text = self.getValueAsString(grid, row, col)
        dc.SetFont(attr.GetFont())
        w,h = dc.GetTextExtent(text)
        # XXX 
        w = 300
        h = h*self.addressCount(grid, row, col)
        return wx.Size(w,h)

    def Clone(self):
        return EmailCellRenderer()


    def cleanup(self):
        """Cleanup that needs to be done at the end of editing
        """
        self._edc.Clear()
        self.startValue = None
        self.endValue = None

    def onKeyDown(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            self.onEnter()
            return
        evt.Skip()

    def Reset(self):
        self._edc.Clear()
        self.startValue = None

    def Clone(self):
        return AddresslCellRenderer()

