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
"""Derive your renderer from this class and implement the 
needed methods and functions.
"""
import wx
import wx.grid

import logging


class CellRootRenderer(wx.grid.PyGridCellRenderer):
    def __init__(self):
        wx.grid.PyGridCellRenderer.__init__(self)
        self._DELIMITER="|"

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        dc.SetClippingRect(rect)

        
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

        content = self.getValueAsString(grid, row, col)

        self.drawOrg(grid, row, col, dc, rect, content)
        
    def getRowHeight(self, content, h):
        """Provides a unifified calculation of the 
        heigth needed for the row"""
        rh = 0
        nrOfLines = len(content.split(self._DELIMITER))-1
        rh = nrOfLines*(h+1)
        return rh+2

    def drawOrg(self, grid, row, col, dc, rect, content):

        x = rect.x+1
        y = rect.y+1

        dc.DrawRectangleRect(rect)
        ss = grid.GetCellValue(row, col)
        w, h = dc.GetTextExtent(u" ")

        sh = grid.GetRowSize(row) # current height
        eh = self.getRowHeight(content, h) # expected height


        for a in content.split(self._DELIMITER):
            dc.DrawText(a, x, y)
            y = y+h+1

        
        dc.DestroyClippingRegion()

        if eh > sh:
            grid.SetRowSize(row, eh)
            grid.ForceRefresh()


    def getValueAsString(self, grid, row, col):
        """Returns the requested value as usable unicode string. 
        Each entry is delimited by self._DELIMITER
        """
        # content = u""
        raise NotImplementedError

    def Clone(self):
        """return a new instance of the itself. E.g. if your derived class is named
        MyCellRenderer return MyCellRenderer()."""
        raise NotImplementedError


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

