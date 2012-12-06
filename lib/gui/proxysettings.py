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

import domaindata
from observer import *


class SetProxyView(wx.Dialog):
    def __init__(self, parent, id=-1, title="Proxy Settings"):
        wx.Dialog.__init__(self, parent, id, title)

        self.title = self.getRichText(18, title)
        self.hint = self.getRichText(12, "If you have any questions, please ask your administrator.")


        self.http_l = wx.StaticText(self, -1, "http-proxy:")
        self.https_l = wx.StaticText(self, -1, "https-proxy:")
        self.proxyuser_l = wx.StaticText(self, -1, "proxy-username:")
        self.proxypass_l = wx.StaticText(self, -1, "proxy-password:")

        self.http_t = wx.TextCtrl(self, wx.ID_ANY)
        self.https_t = wx.TextCtrl(self, wx.ID_ANY)
        self.proxyuser_t = wx.TextCtrl(self, wx.ID_ANY)
        self.proxypass_t = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PASSWORD)
        
        if domaindata.initialized and domaindata._proxySettings:
            ps =  domaindata._proxySettings
            self.http_t.SetValue( unicode(ps.httpProxy))
            self.https_t.SetValue( unicode(ps.httpsProxy))
            self.proxyuser_t.SetValue( unicode(ps.proxyUser))
            self.proxypass_t.SetValue( unicode(ps.password))
 
        self.button_set = wx.Button(self, wx.ID_OK, "Set")
        self.button_set.SetDefault()
        self.button_cancel = wx.Button(self, wx.ID_CANCEL)

        # Layout
        space = 6
        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(self.title, 0, wx.ALL, space)
        topSizer.Add(self.hint, 0, wx.ALL, space)
        topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, space)

        fgs = wx.FlexGridSizer(4, 2, space, space)
        fgs.Add(self.http_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.http_t, 0, wx.EXPAND)
        fgs.Add(self.https_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.https_t, 0, wx.EXPAND)
        fgs.Add(self.proxyuser_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.proxyuser_t, 0, wx.EXPAND)
        fgs.Add(self.proxypass_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.proxypass_t, 0, wx.EXPAND)
        fgs.AddGrowableCol(1) # make col 1 expandable

        topSizer.Add(fgs, 0, wx.EXPAND | wx.ALL, space)
        
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(self.button_set)
        btns.AddButton(self.button_cancel)
        btns.Realize()

        topSizer.Add(btns, 0, wx.EXPAND | wx.ALL, space)

        self.SetSizer(topSizer)
        topSizer.Fit(self)


    def getRichText(self, size, text):
        title = wx.StaticText(self, -1, text, (20, 120 ))
        font = wx.Font(size, wx.SWISS, wx.NORMAL, wx.NORMAL)
        title.SetFont(font)
        return title
        
