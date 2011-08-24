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
"""This is a wrapper around locating and loading of XRC files within the dsce.
"""
import wx
import wx.xrc as xrc

import os

_RESPATH_ = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "xrcs")

def _getXrcsAbsPath(fn):
    ap = os.path.join(_RESPATH_,fn)
    if not os.path.isfile(ap):
        raise BaseException("File %s does not exist" % ap)
    else:
        return ap

def loadPanel(parent, fn, n):
    """parent - parent to use
    fn - the XmlResouce file name. The file must be located in _RESPATH_.
    n - the resource name.
    """
    return xrc.XmlResource(_getXrcsAbsPath(fn)).LoadPanel(parent, n)

def getControl(rc, xmlid):
    """Returns the control from the resource (panel, dialog, etc) that correspond to its 
    xml id"""
    return xrc.XRCCTRL(rc, xmlid)
