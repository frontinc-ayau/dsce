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
import cellrootrenderer as crr

import logging


class OrgCellRenderer(crr.CellRootRenderer):
    def __init__(self):
        """Used to render orgainization data
        """
        crr.CellRootRenderer.__init__(self)


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

        return org


    def Clone(self):
        return OrgCellRenderer()

