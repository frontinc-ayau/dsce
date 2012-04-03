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
# Copyright (c) 2010, 2011, 2012 Klaus Melcher (melcher.kla@gmail.com)


#FI XXX: Try to use ArtProvider
import os, logging, sys
import wx

from configuration import *


_IMAGEDIR = config.wxImageDir if config.wxImageDir else os.path.join(os.path.abspath(
                                                                        os.path.dirname(sys.argv[0]).rstrip("bin")),
                                                                        "data/images")

# resource abstraction, so that we need not to call the file names
# for the resource in the program
R_LOGO = "TMTLogo.png"
R_EXIT = "exit.png"
R_ADD = "add.png"
R_DEL = "del.png"
R_GRP = "grp.png"
R_PUB = "pub.png"
R_GET = "get.png"
R_HELP = "help.png"

def resabspath(name):
    """Returns the absolute path of the resource passed 
    by name.
    """
    r = os.path.abspath(os.path.join(_IMAGEDIR,name))
    if not os.path.isfile(r):
        raise BaseException("Image %s does not exist" % r)
    else:
        return r


def getasbitmap(name):
    """Returns an alpha enabled bitmap for direct use in wx of the 
    underlying image
    """
    img = wx.Image(resabspath(name), wx.BITMAP_TYPE_PNG, True)
    # img.ConvertAlphaToMask(220)
    return img.ConvertToBitmap()

def getasimage(name, type=wx.BITMAP_TYPE_PNG):
    return wx.Image(resabspath(name), type, True)
    

def geticon(name):
    """Returns wx.Icon passed by name.
    """
    return wx.Icon(resabspath(name), wx.BITMAP_TYPE_ICO)
    
