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

"""Model (domain data) that are used by the DomainSharedContactsEditor."""

import gdata.contacts.data
import gdata.contacts.client


class DomainContactsClient(gdata.contacts.client.ContactsClient):

    def __init__(self, user, source = "getSharedContacts", *args, **kwargs):
        """Expects a LoginUser object as parameter.
        """
        self.user = user
        self.source = source
        
        gdata.contacts.client.ContactsClient.__init__(self, *args, **kwargs)

    def loginAtSource(self):

        self.client_login(email=self.user.email, 
                      password=self.user.password, 
                      source=self.source, 
                      account_type=self.user.account_type)

    def addContact(self, contact):
        entry = contact.getEntry()
        entry = self.CreateContact(entry)
        contact.setEntry(entry)

    def updateContact(self, contact):
        entry = contact.getEntry()
        entry = self.Update(entry)
        contact.setEntry(entry)

    def deleteContact(self, contact):
        entry = contact.getEntry()
        self.Delete(entry)


if __name__ == "__main__":

    import logging, sys
    from loginuser import *
    import pydoc
    from dscegroups import *

    loginUser = LoginUser()
    # loginUser.setFromEmail("melcher.kla@gmail.com")
    loginUser.setFromEmail("klaus@themobileterminal.com")
    dc = DomainContactsClient(loginUser)
    print "Login at google..."
    dc.loginAtSource()
    print "Get groups"
    gf = dc.get_groups(desired_class=DSCEGroupsFeed)
    print type(gf)
    print type(gf.entry)
    for entry in gf.entry:
        print 'Atom Id: %s' % entry.id.text
        print 'Group Name: %s' % entry.title.text
        print 'Last Updated: %s' % entry.updated.text

        print "Name got by id: %s" % gf.getNameById(entry.id.text)

        print 'Extended Properties:'
        for extended_property in entry.extended_property:
            if extended_property.value:
                value = extended_property.value
            else:
                value = extended_property.GetXmlBlob()
                print '  %s = %s' % (extended_property.name, value)
        print 'Self Link: %s' % entry.GetSelfLink().href
        if not entry.system_group:
            print 'Edit Link: %s' % entry.GetEditLink().href
            print 'ETag: %s' % entry.etag
        else:
            print 'System Group Id: %s' % entry.system_group.id

    gs = gf.getGroupNames()
    
    for gn in gs[SYSTEM_GROUPS]:
        print ("Group: %s (sys)" % gn)
    for gn in gs[PRIVATE_GROUPS]:
        print ("Group: %s (priv)"% gn)

    sys.exit(0)
    
