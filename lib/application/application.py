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
# 
import wx, gui, domaindata, controller, sys, configuration, resources
from observer import *

class App(wx.App):
    def OnInit(self):
        self.Bind(wx.EVT_QUERY_END_SESSION, self.onQueryEndSession)
        return True

    def onQueryEndSession(self, event):
        """Avoid blocking from shutdown windows.
        """
        pass


class Application(object):
    """This class is responsible to initializes the whole application and the MainLoop()
    Workflow: o-> init wx.App 
               -> setup domain data objects 
               -> load configuration settings
               -> init main frame
               -> init controller
               -> hand over application control to controller
               -> enter MainLoop().

    Also it provides procedures to access tasks that should be performed on 
    application level, like e.g. doExit() or displaying messages.
    """
    def __init__(self, args=None, **kwargs):
        self.app = None
        self.mainFrame = None
        self.initApplication()
        


    def initApplication(self):
        self.app = App(redirect=False)
        self.initDomainData()
        self.loadConfigurationSettings() # must be after initDomainData()
        self.initMainFrame()
        self.initController()


    def initMainFrame(self):
        self.mainFrame = gui.MainFrame(None, -1, ico=resources.geticon("logo.ico"))
        self.app.SetTopWindow(self.mainFrame)


    def initDomainData(self):
        domaindata.init()


    def initController(self):
        if self.app and domaindata.initialized() and self.mainFrame:
            controller.init(self)

    def loadConfigurationSettings(self):
        conf = configuration.getConfiguration()
        http = https = user = pas = None
        if conf.hasKey("httpProxy"):
            http = conf.httpProxy
            if conf.hasKey("httpsProxy"): https = conf.httpsProxy
            if conf.hasKey("proxyUser"): user = conf.proxyUser
            if conf.hasKey("proxyPassword"): pas = conf.proxyPassword
            domaindata.set_proxy_environment(http, https, user, pas)
        

    def displayDialog(self, dialog, *args, **kwargs):
        return dialog(self.mainFrame, *args, **kwargs)

    def inProgressDialog(self, txt):
        return gui.InProgressDialog(txt, parent=self.mainFrame)

    def run(self):
        self.mainFrame.Show()
        self.app.MainLoop()


    def doExit(self, event):
        self.mainFrame.Destroy()
        sys.exit(0)


    def displayAlert(self, title, text):
        alert = wx.MessageDialog(self.mainFrame, text, title, wx.OK | wx.ICON_ERROR)
        alert.ShowModal()
        alert.Destroy()


