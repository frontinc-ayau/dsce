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

import wx, gui, domaindata, configuration, logging
from domaindata.domaincontact import ACTION 

import observer
from observer import pmsg 

class Controller(object):
    """Controls activities between views, business logic and user input
    """

    def __init__(self, app):
        self.app = app
        self.retisterMessages() 
        self.enterApp()
        
    def retisterMessages(self):
        pmsg.register("SET_PROXY")
        

    def enterApp(self):
        observer.subscribe(self.app.doExit, pmsg.EXIT_APP)
        observer.subscribe(self.setProxy, pmsg.SET_PROXY)
        observer.subscribe(self.alert, pmsg.ALERT)

        self.login()
        self.downloadContacts()
        self.downloadGroups()

        observer.subscribe(self.pubContacts, pmsg.PUB_CONTACT)
        observer.subscribe(self.addContact, pmsg.ADD_CONTACT)
        observer.subscribe(self.delContact, pmsg.DEL_CONTACT)


    def login(self):
        """Get login information and logon at the account
        """
        dlg = self.app.displayDialog(gui.LoginView)
        if dlg.ShowModal() == wx.ID_OK:
            logging.debug("Login requested")
            if not self.performLogin( dlg.getEmail(), dlg.getPassword() ):
                self.login() # start over on error
        else: 
            logging.debug("Login canceled")
            # domaindata.load_contacts_store()
            # observer.send_message(pmsg.DATA_DOWNLOADED)

        dlg.Destroy()

    def setProxy(self, event):
        """In case you are located behind a web proxy, this 
        dialog is used to set the os.environment to use it.
        For how settings are loaded in an automatic way refer to
        gui.SetProxyView.
        """
        dlg = self.app.displayDialog(gui.SetProxyView)
        if dlg.ShowModal() == wx.ID_OK:
            logging.debug("Set proxy")
            http = None
            https = None
            usr = None
            pas = None

            if not dlg.http_t.IsEmpty():
                http = dlg.http_t.GetValue()
                logging.debug("set http-proxy to %s" % http)
            else:
                logging.fatal("Missing http-proxy")
                return

            if not dlg.https_t.IsEmpty():
                https = dlg.https_t.GetValue()
                logging.debug("set https-proxy to %s" % https)

            if not dlg.proxyuser_t.IsEmpty():
                usr = dlg.proxyuser_t.GetValue()
                logging.debug("set proxy-username to %s" % usr)

            if not dlg.proxypass_t.IsEmpty():
                pas = dlg.proxypass_t.GetValue()
                logging.debug("set proxy-password to %s" % pas)

            domaindata.set_proxy_environment(http, https, usr, pas)


        else:
            logging.debug("Setting of proxy canceled")

        dlg.Destroy()

    def performLogin(self, user, password):
        logging.debug("Login invoked....")
        logging.debug("Email: %s password: %s" % (user, "*"*len(password) ))

        dlg = None

        try:
            dlg = self.app.inProgressDialog("Login...")

            domaindata.set_login_credentials(user, password) # user == email
            domaindata.login()
            
            dlg.Destroy() # login successful
        except Exception, e:
            dlg.Destroy()
            self.alert(str(e), title="Login Error")
            return False

        return True

    def loadLocalContacts(self):
        logging.debug("Try to load local stored contacts")
        dlg = None
        try:
            dlg = self.app.inProgressDialog("Try to load local stored contacts")

            domaindata.load_contacts_store()
            
            dlg.Destroy() 
        except Exception, e:
            dlg.Destroy()
            self.alert(str(e), title="Local loading error.")
            return False

        return True

    def downloadContacts(self):
        try:
            dlg = self.app.inProgressDialog("Download contacts...")
 
            domaindata.download_contacts()
            observer.send_message(pmsg.DATA_DOWNLOADED)
 
            dlg.Destroy() # contacts downloaded
        except Exception, e:
            dlg.Destroy()
            self.alert(str(e), title="Download Error")
            return False

    def downloadGroups(self):
        try:
            dlg = self.app.inProgressDialog("Download groups...")
 
            domaindata.download_groups()
            observer.send_message(pmsg.GROUPS_DOWNLOADED)
 
            dlg.Destroy() 
        except Exception, e:
            dlg.Destroy()
            self.alert(str(e), title="Download Error")
            return False

    def alert(self, msg, title=None):

        logging.debug("Alert %s" % str(msg))

        if title:
            self.app.displayAlert(title, str(msg))
        else:
            self.app.displayAlert("Error", str(msg))

    def doSearch(self, event):
        logging.debug("Controller: Search for %s" % unicode(event.data))

    def addContact(self, event):
        logging.debug("Controller: Add contact")
        domaindata.add_contact()
        observer.send_message(pmsg.CONTACT_ADDED)
        
    def delContact(self, msg):
        logging.debug("Controller: Delete contact %s" % str(msg))
        for row in msg.data:
            if row >= 0:
                logging.debug("Mark row %d as deleted" % row)
                domaindata.del_contact_from_row(row)
        observer.send_message(pmsg.CONTACT_DELETED)


    def pubContacts(self, event):
        s = domaindata.get_action_summary()
        txt = "Do you really want to %s %d, %s %d and %s %d contacts?" % ( 
                        ACTION.ADD, s[ACTION.ADD], 
                        ACTION.UPDATE, s[ACTION.UPDATE], 
                        ACTION.DELETE, s[ACTION.DELETE] 
                        )

        dlg = self.app.displayDialog(wx.MessageDialog, txt, 'Question?', wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            logging.debug("Publish changes")
            dlg.Destroy()

            dlg = self.app.inProgressDialog("Publish changes made to contacts...")
            try:
                domaindata.publish_changes()
                dlg.Destroy()
            except BaseException, e:
                dlg.Destroy()
                self.alert(str(e), title="Publish Error")
            
            observer.send_message(pmsg.DATA_UPLOADED) # do it anyway because of possible partial upload

            
        else:
            logging.debug("Cancel the publishing of changes")
            dlg.Destroy()



