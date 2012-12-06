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
from observer import *

class LoginView(wx.Dialog):

    def __init__(self, parent, id=-1, title="Login"):
        wx.Dialog.__init__(self, parent, id, title)
        self.parent = parent

        # register messages to be used with our observer
        self.registerMessages()

        self.drawControls()
        self.bindEvents()


    def drawControls(self):

        ttext = "Login at your account"
        title = wx.StaticText(self, -1, ttext, (20, 120))
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL)
        title.SetFont(font)

        self.luname = wx.StaticText(self, wx.ID_ANY, 'Email:')
        self.email = wx.TextCtrl(self, wx.ID_ANY , size=(250, -1) )
        self.lpass = wx.StaticText(self, wx.ID_ANY, 'Password:')
        self.password = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PASSWORD, size=(250, -1))

        space = 6

        # text inputs
        fgs = wx.FlexGridSizer(2, 2, space, space)
        fgs.Add(self.luname, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.email, 0, wx.EXPAND)
        fgs.Add(self.lpass, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.password, 0, wx.EXPAND)
        fgs.AddGrowableCol(1) # make col 1 expandable

        inputPasswordSizer  = wx.BoxSizer(wx.HORIZONTAL)
        inputPasswordSizer.Add(self.lpass, 0, wx.ALL, space)
        inputPasswordSizer.Add(self.password, 0, wx.ALL|wx.EXPAND, space)


        # buttons
        self.login_button = wx.Button(self, wx.ID_OK, "Login")
        self.login_button.SetDefault()
        self.cancel_button = wx.Button(self, wx.ID_CANCEL)
        self.proxy_button = wx.Button(self, wx.ID_APPLY, label="Set Proxy")


        btns = wx.StdDialogButtonSizer()
        btns.AddButton(self.proxy_button)
        btns.AddButton(self.login_button)
        btns.AddButton(self.cancel_button)
        btns.Realize()



        # layout all
        topSizer        = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(title, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, space)
        topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, space)
        topSizer.Add(fgs, 0, wx.EXPAND | wx.ALL, space)
        topSizer.Add(btns, 0, wx.EXPAND | wx.ALL, space)

        self.SetSizer(topSizer)
        topSizer.Fit(self)


    def bindEvents(self):
        self.Bind(wx.EVT_BUTTON, self.publish, self.proxy_button)


    def getEmail(self):
        return self.email.GetValue()


    def getPassword(self):
        return self.password.GetValue()


    def registerMessages(self):
        pmsg.register("LOGIN")
        pmsg.register("EXPAND")
        pmsg.register("SET_PROXY")


    def publish(self, event):

        eid = event.GetId()
        if eid == wx.ID_APPLY:
            Publisher.sendMessage(pmsg.SET_PROXY, event)

        else:
            raise BaseException("Unknown event during event. Please inform the developer!")
            

