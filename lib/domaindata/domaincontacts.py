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

import logging, sys

from domaincontact import ACTION
from domaincontact import DomainContact

import sfilter

class DomainContacts(list):
    """Container for all downloaded domain contacts.
    """
    def __init__(self, *args, **kw):
        list.__init__(self, *args, **kw)
        self.hiddenContacts = []

    def getContact(self, uid):
        """Returns the contact with the appropriate UID, else None
        """
        contact = None
        for contact in self:
            if contact.getUid() == uid:
                return contact
        
        # of = open("dump.txt","w+")
        # for contact in self:
            # of.write("Search uid = %d vs. getUid = %d\n " % (uid, contact.getUid()))
            
        return None
    
    def getActionSummary(self):
        """Returns a dictionary with the number of contacts to add, update and delete. 
        Each is represented as key=value pair.
        """
        s = { ACTION.ADD:0, ACTION.UPDATE:0, ACTION.DELETE:0 }
        for c in self:
            if (c.getAction() == ACTION.ADD) and (c.isEmpty() != True): s[ACTION.ADD] += 1
            elif c.getAction() == ACTION.UPDATE: s[ACTION.UPDATE] += 1
            elif c.getAction() == ACTION.DELETE: s[ACTION.DELETE] += 1

        return s
        
    def delete(self, c):
        """Removes the passed contact from the list."""
        logging.debug("Delete contact on index %d" % self.index(c))
        self.pop(self.index(c))
        logging.debug("Contact deleted....") 
        

    def getChangedContacts(self):
        """Returns a list of changed objects.
        """
        cc = []

        for c in self:
            if c.getAction():
                cc.append(c)

        return cc

    def getSearchHits(self, s):
        """Return indices of contacts that apply to the 
        search filter as list"""
        i = 0
        rl = []
        for c in self:
            if sfilter.contact_has_string(c, s) == False:
                rl.append(i)
            i += 1
        return rl

