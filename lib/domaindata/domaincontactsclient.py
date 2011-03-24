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
        pass

    def updateContact(self, contact):
        import logging
        entry = contact.getEntry()
        logging.debug("Update contact %s" % contact.getFamilyName())
        self.Update(entry)


    def deleteContact(self, contact):
        pass


if __name__ == "__main__":

    import logging, sys

    sys.exit(0)
    
