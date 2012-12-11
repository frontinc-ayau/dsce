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

"""One contact entry used by DomainSharedContactsEditor."""


import gdata.contacts.data
import gdata.data
import logging

import observer
from observer import pmsg

class _GOBAL_(object):
    pass


ACTION = _GOBAL_()
ACTION.ADD = "add"
ACTION.UPDATE = "update"
ACTION.DELETE = "delete"


class UID(object):
    """Implements a unique id for each contact.
    To get a unique id just call UID().getId()
    """
    _id = 0
    _instance = None
    def __init__(self):
        if UID._instance is None:
            UID._instance = self
    def getId(self):
        UID._id += 1
        return UID._id


class DomainContact(object):
    """This class is responsible to interface gdata.contacts.data.ContactEntry
    and all its related attributes. Therefore it is the core data source of this
    application.

    """
    
    def __init__(self, entry=None):
        # attributes without a representation of gdata
        self.uid = UID().getId() # Unique ID within this application
        self.action = None # can be one of the ACTION_STRING attributes
        if entry:
            self.entry = entry
        else: # must be a new contact
            self.entry = gdata.contacts.data.ContactEntry()
            self.setActionAdd()
        self.__subscirbeEvents__()

    def __subscirbeEvents__(self):
        observer.subscribe(self.onGroupDeletEvent, pmsg.GROUP_DELETION_DONE)

    def isEmpty(self):
        """It is assumed that at least one of the following attributes has to be set 
        to be accepted as a contact entry.
            - at least one part of the name or, except prefix and suffix
            - an email address
        As at the moment I do not know any other main identification- or reference point
        of a contact no further tests are implemented until someone comes up with other
        possibilities. 
        """
        if len(self.getEmail()) > 0:
            logging.debug("Email %d" % len(self.getEmail()))
            return False
        elif self.getGivenName() or self.getFamilyName() or self.getAdditionalName():
            logging.debug("Found a name")
            return False
        else:
            return True

    def getEntry(self):
        return self.entry

    def setEntry(self, entry):
        self.entry = entry

    def setNamePrefix(self, text):
        self.setName(prefix=text)

    def setGivenName(self, text):
        self.setName(given_name=text)

    def setFamilyName(self, text):
        self.setName(family_name=text)

    def setAdditionalName(self, text):
        self.setName(additional_name=text)

    def setNameSuffix(self, text):
        self.setName(suffix = text)

    def setFullName(self, text):
        import logging
        logging.debug("Set full name %s " % text)
        self.setName(full_name = text)

    def getNamePrefix(self):
        if self.entry.name and self.entry.name.name_prefix:
            return self.entry.name.name_prefix.text
        else:
            return unicode("")

    def getGivenName(self):
        if self.entry.name and self.entry.name.given_name:
            return self.entry.name.given_name.text
        else:
            return unicode("")

    def getFamilyName(self):
        if self.entry.name and self.entry.name.family_name:
            return self.entry.name.family_name.text
        else:
            return unicode("")

    def getFullName(self):
        if self.entry.name and self.entry.name.full_name:
            return self.entry.name.full_name.text
        else:
            return unicode("")

    def getGroups(self):
        return self.entry.group_membership_info

    def setGroups(self, groups=[]):
        self.entry.group_membership_info = []
        for i in groups:
            mi=gdata.contacts.data.GroupMembershipInfo()
            mi.href=i
            self.entry.group_membership_info.append(mi) 
        self.setActionUpdate()

    def onGroupDeletEvent(self, event):
        for mi in self.getGroups():
            if mi.href == event.data['id']:
                self.entry.group_membership_info.remove(mi)
                logging.debug("Removed group %s from %s" % (self.getFamilyName(), event.data['name']))
                del(mi)
                break
        

    def getAdditionalName(self):
        if self.entry.name and self.entry.name.additional_name:
            return self.entry.name.additional_name.text
        else:
            return unicode("")

    def getNameSuffix(self):
        if self.entry.name and self.entry.name.name_suffix:
            return self.entry.name.name_suffix.text
        else:
            return unicode("")

    def setName(self, prefix=None, given_name=None, family_name=None,  
                additional_name=None, suffix=None, full_name=None):
        """Can be used to set the name attribute of a ContactEntry. 
        
        Even no Name-attribute is passed to this method the name attribute itself will
        be initialized anyway.
        """
        if not self.entry.name:
            self.entry.name = gdata.data.Name()
        
        if prefix:
            self.entry.name.name_prefix = gdata.data.NamePrefix(text=prefix)

        if family_name:
            self.entry.name.family_name = gdata.data.FamilyName(text=family_name)

        if given_name:
            self.entry.name.given_name = gdata.data.GivenName(text=given_name)
   
        if additional_name:
            self.entry.name.additional_name = gdata.data.AdditionalName(text=additional_name)

        if suffix:
            self.entry.name.name_suffix = gdata.data.NameSuffix(suffix)

        if full_name:
            self.entry.name.full_name = gdata.data.FullName(text=full_name)

        self.setActionUpdate()

    def getName(self):
        """Returns a list of the following order 
                [ prefix, given_name, family_name, additional_name, suffix ]. 
        If one value is not set it will be replaced by None. E.g. if the contact entry has no
        suffix set, the list will contain a None value on the position where suffix is to be 
        expected. (Worst case [ None, None, None, None, None ]) 
        """
        n = []
        n.append(self.getNamePrefix())
        n.append(self.getGivenName())
        n.append(self.getFamilyName())
        n.append(self.getAdditionalName())
        n.append(self.getNameSuffix())

        return n

    def setPostalAddress(self, value, idx=-1):
        if idx >= 0:
            self.entry.structured_postal_address[idx]=value
        else:
            self.entry.structured_postal_address = value
        self.setActionUpdate()
 

    def getPostalAddress(self, idx=-1):
        """Returns either the address at the position of idx or 
        default the entry.structured_postal_address array.
        """
        if idx >= 0:
            try:
                return self.entry.structured_postal_address[idx]
            except:
                return None
        else:
            return self.entry.structured_postal_address
        

    def getUid(self):
        return self.uid

    def setActionAdd(self):
        if not self.action:
            self.action = ACTION.ADD

    def setActionDelete(self):
        self.action = ACTION.DELETE

    def setActionUpdate(self):
        # makes only sense if it has not been added or set for deletion:
        if not self.action: 
            self.action = ACTION.UPDATE

    def clearAction(self):
        self.action = None

    def getAction(self):
        return self.action

    def addEmail(self, email, primary="false", rel=gdata.data.WORK_REL, label=None):
        """Appends an email address to the contact.
        """
        self.entry.email.append(gdata.data.Email(address=email, 
                                                 primary=primary, 
                                                 rel=rel,
                                                 label=label))
        self.setActionUpdate()

    def deleteEmail(self, email):
        """Deletes any Email entry that is associated with the passed email
        address. 
        It returns the number of deleted entries.
        """
        deleteCount=0
        emails = self.entry.email[:]

        for e in emails:
            if e.address == email:
                self.entry.email.remove(e)
                deleteCount += 1
        
        self.setActionUpdate()
        return deleteCount

    def emailExist(self, email):
        emails = self.entry.email[:]
        for e in emails:
            if e.address == email:
                return True
                
        return False

    def updateEmail(self, old, new):
        """replaces the old Email.address string with the new email string. If old does not
        exist, an BaseException will be raised. If number of emails is 0
        the new email will just be added.
        """
        nrOfEmails = len(self.entry.email)
        updateCount = 0

        if nrOfEmails == 0:
            raise BaseException("There exist no email address that can be updated" % nrOfEmails)

        i=0
        while i < nrOfEmails:
            if self.entry.email[i].address == old:
                self.entry.email[i].address = new
                updateCount += 1
            i += 1

        if updateCount == 0:
            raise BaseException("Email address %s does not exist" % old)
        else:
            self.setActionUpdate()
            return updateCount

    def getEmail(self, idx=-1):
        """Returns either the email at the position of idx or 
        default the entry.email array.
        """
        if idx >= 0:
            try:
                return self.entry.email[idx].address
            except:
                return None
        else:
            return self.entry.email

    def getEmailAddresses(self):
        """Returns all found email addresses as a list of strings or an empty
        list.
        """
        emails = []
        for email in self.getEmail():
            emails.append(email.address)
        return emails


    def setEmails(self, emails):
        """The current self.entry.email[] will be replaced by a list of gd.data.Email 
        objects created of the addresses provided by the following matrix:
        emails = [ [address, type, label, primary], ... ]
        """ 
        self.entry.email = []

        import logging
        logging.debug(emails)
        
        for e in emails:
            self.addEmail(email   = e[0], 
                          rel     = e[1],
                          label   = e[2],
                          primary = e[3])
        self.setActionUpdate()



    def getPhoneNumber(self,idx=-1):
        """Returns either the phone number at the position of idx or default
        the entry.phone_number list.
        """
        if idx >= 0:
            try:
                return self.entry.phone_number[idx]
            except:
                return None
        else:
            return self.entry.phone_number

    def setPhoneNumber(self, value, idx=-1):
        if idx >= 0:
            self.entry.phone_number[idx]=value
        else:
            self.entry.phone_number = value
        self.setActionUpdate()

    def getOrganization(self):
        return self.entry.organization

    def setOrganization(self, org):
        """@param: org = gdata.data.Organization"""
        self.entry.organization = org
        self.setActionUpdate()


# Tests
if __name__ == "__main__":

    import unittest
    class TestDomainContact(unittest.TestCase):
        def setUp(self):
            self.dc = DomainContact()

        def testSetGetAction(self):
            self.dc.setActionAdd()
            self.assertEqual(self.dc.getAction(), ACTION.ADD, msg="Wrong action value after setActionAdd()")

