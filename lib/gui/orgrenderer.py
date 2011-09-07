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
import wx.grid

import domaindata.orgf as orgf

import logging


class OrgCellRenderer(wx.grid.PyGridCellRenderer):
    def __init__(self):
        """Used to render orgainization data
        """
        wx.grid.PyGridCellRenderer.__init__(self)
        self._DELIMITER="|"

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        dc.SetClippingRect(rect)

        org = self.getValueAsString(grid, row, col)
        
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

        self.drawOrg(dc, rect, org)
        

    def drawOrg(self, dc, rect, org):

        dc.DrawRectangleRect(rect)
        w, h = dc.GetTextExtent(org)
        x = rect.x+1
        y = rect.y+1
        for a in org.split(self._DELIMITER):
            dc.DrawText(a, x, y)
            y = y+h+1

        dc.DestroyClippingRegion()


    def getValueAsString(self, grid, row, col):
        """Returns the requested value as usable unicode string. 
        Each entry is delimited by self._DELIMITER
        """
        org = u""

        o=grid.GetTable().GetValue(row,col)
        if type(o) == str: # empty
            return u" "

        for l in orgf.getOrgAsStringList(o):
            if l:   
                org +=  unicode(l).replace("\n"," ")+u" "
                org += self._DELIMITER

        logging.debug("org: %s" % str(org))
        return org

    def orgCount(self, grid, row, col):
        return len(orgf.getOrgAsStringList(grid.GetTable().GetValue(row, col)))

    def GetBestSize(self, grid, attr, dc, row, col):
        text = self.getValueAsString(grid, row, col)
        dc.SetFont(attr.GetFont())
        w,h = dc.GetTextExtent(text)
        # XXX 
        w = 300
        h = h*self.orgCount(grid, row, col)
        # logging.debug("XXXX height %d" % h)
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

