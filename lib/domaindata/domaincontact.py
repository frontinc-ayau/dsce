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

    def getEntry(self):
        return self.entry

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

    def setPostalAddress(self, text, idx=0):
        if len(self.entry.postal_address) == 0:
            pa = gdata.data.StructuredPostalAddress(text)
            self.entry.structured_postal_address.append(pa)
        else:
            self.entry.postal_address[idx].structured_postal_address.formatted_address.text = text
            self.setActionUpdate()
 
    def getPostalAddress(self, idx=-1):
        """Returns either the email at the position of idx or 
        default the entry.email array.
        """
        if idx >= 0:
            try:
                return self.entry.structured_postal_address[idx].formatted_address.text
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


    def addPhoneNumber(self, number, primary="false", rel=gdata.data.WORK_REL):
        self.entry.phone_number.append(gdata.data.PhoneNumber(text=number.strip(),
                                                              primary=primary, 
                                                              rel=rel))
        self.setActionUpdate()


    def getPhoneNumber(self,idx=-1):
        """Returns either the email at the position of idx or default
        the entry.phone_number list.
        """
        if idx >= 0:
            try:
                return self.entry.phone_number[idx].text
            except:
                return None
        else:
            return self.entry.phone_number

    def deletePhoneNumber(self, number):
        """Deletes any phone number entry that is associated with the passed 
        phone number. 
        It returns the number of deleted entries.
        """
        deleteCount=0
        p_numbers = self.entry.phone_number[:]
        p_number = number.strip()

        for p in p_numbers:
            if p.text == p_number:
                self.entry.phone_number.remove(p)
                deleteCount += 1
        
        self.setActionUpdate()
        return deleteCount

    def updatePhoneNumber(self, old, new):
        """Replaces the old PhoneNumber.text string with the new phone string. If 'old' does not
        exist, an BaseException will be raised.
        """
        nrOfPhoneNumbers = len(self.entry.phone_number)
        updateCount = 0
        old = old.strip()
        new = new.strip()
        

        if nrOfPhoneNumbers == 0:
            raise BaseException("There are no phone numbers that can be updated")

        i=0
        while i < nrOfPhoneNumbers:
            if self.entry.phone_number[i].text == old:
                self.entry.phone_number[i].text = new
                updateCount += 1
            i += 1

        if updateCount == 0:
            raise BaseException("Phone number %s does not exist" % old)
        else:
            self.setActionUpdate()
            return updateCount


# Tests
if __name__ == "__main__":

    import unittest
    class TestDomainContact(unittest.TestCase):
        def setUp(self):
            self.dc = DomainContact()

        def testSetGetAction(self):
            self.dc.setActionAdd()
            self.assertEqual(self.dc.getAction(), ACTION.ADD, msg="Wrong action value after setActionAdd()")

            self.dc.setActionUpdate()
            self.assertEqual(self.dc.getAction(), ACTION.UPDATE, msg="Wrong action value after setActionUpdate()")

            self.dc.setActionDelete()
            self.assertEqual(self.dc.getAction(), ACTION.DELETE, msg="Wrong action value after setActionDelete()")

        def testGetUid(self):
            id = self.dc.getUid()
            self.assertEqual(id, 3, msg="Wrong UID, expected 1 got %d" % id)
            c1 = DomainContact()
            id = c1.getUid()
            self.assertEqual(id, 4, msg="Wrong UID, expected 2 got %d" % id)

        def testSetGetNamePrefix(self):
            self.dc.setNamePrefix("Prefix")
            self.assertEqual(self.dc.getNamePrefix(),  "Prefix", msg="Wrong prefix after setNamePrefix()")

        def testSetGetGivenName(self):
            self.dc.setGivenName("GivenName")
            self.assertEqual(self.dc.getGivenName(), "GivenName", msg="Wrong given name after setGivenName()")

        def testSetGetFamilyName(self):
            self.dc.setFamilyName("FamilyName")
            self.assertEqual(self.dc.getFamilyName(), "FamilyName", msg="Wrong family name after setFamilyName()")

        def testSetGetAdditionalName(self):
            self.dc.setAdditionalName("AdditionalName")
            self.assertEqual(self.dc.getAdditionalName(), "AdditionalName", msg="Wrong family name after setAdditionalName()")

        def testSetGetNameSuffix(self):
            self.dc.setNameSuffix("NameSuffix")
            self.assertEqual(self.dc.getNameSuffix(), "NameSuffix", msg="Wrong family name after setNameSuffix()")

        def testSetGetSetName(self):
            self.dc.setName(prefix="A", given_name="B", family_name="C",  
                            additional_name="D", suffix="E")

            res=["A", "B", "C", "D", "E"]
            self.assertEqual(self.dc.getName(), res, msg="Wrong name-array after set/getName()")


        def testAddDeleteEmail(self):
            self.dc.addEmail("test@test.com", primary="true")
            expected='<ns0:email address="test@test.com" primary="true" rel="http://schemas.google.com/g/2005#work" xmlns:ns0="http://schemas.google.com/g/2005" />'
            self.assertEqual(str(self.dc.getEmail(idx=0)), expected, msg="error in the addEmail()" )
            self.assertEqual(self.dc.deleteEmail("test@test.com"), 1, msg="wrong number of deleted emails")
            self.assertEqual(len(self.dc.getEmail()), 0, msg="wrong amount of emails left in entry")
            self.assertEqual(self.dc.deleteEmail("test@test.com"), 0, msg="wrong number of deleted emails")

            self.dc.addEmail("test@test.com", primary="true")
            self.dc.addEmail("test@test.com" )
            self.dc.addEmail("test@test.com" )
            deletedEmails=self.dc.deleteEmail("test@test.com")
            self.assertEqual(deletedEmails, 3, msg="wrong number of deleted emails %d (3)" % deletedEmails)
            self.assertEqual(len(self.dc.getEmail()), 0, msg="wrong amount of emails after the deletion of 3")
            
        def testUpdateEmail(self):
            self.assertRaises(BaseException, self.dc.updateEmail,"test@test.com", "new@test.com")
            self.dc.addEmail("test@test.com", primary="true")
            self.assertRaises(BaseException, self.dc.updateEmail,"notExist@test.com", "new@test.com")

            nu=self.dc.updateEmail("test@test.com", "new@test.com")
            self.assertEqual(nu, 1, msg="update email returns wrong update count. Expect 1 got %d" % nu)
            expected='<ns0:email address="new@test.com" primary="true" rel="http://schemas.google.com/g/2005#work" xmlns:ns0="http://schemas.google.com/g/2005" />'
            self.assertEqual(str(self.dc.getEmail(idx=0)), expected, msg="error in the updateEmail() result" )
            self.dc.addEmail("test@test.com" )
            self.dc.addEmail("test@test.com" )
            nu=self.dc.updateEmail("test@test.com", "new@test.com")
            self.assertEqual(nu, 2, msg="update email returns wrong update count. Expect 2 got %d" % nu)

        def testAddDeletePhoneNumber(self):
            self.dc.addPhoneNumber("+39 000 333 444")
            self.assertEqual(self.dc.getPhoneNumber(0).text, "+39 000 333 444" , 
                             msg="error in addPhoneNumber()")

            self.assertEqual(self.dc.deletePhoneNumber("+39 000 333 444"), 1, 
                             msg="wrong number of deleted phone numbers (1)") 

            self.assertEqual(len(self.dc.getPhoneNumber()), 0, 
                             msg="wrong amount of phone numbers left in entry (len(0))")

            self.assertEqual(self.dc.deletePhoneNumber("+39 000 333 444"), 0, 
                             msg="wrong number of deleted phone numbers (0)")
            
            self.dc.addPhoneNumber("+39 000 333 444")
            self.dc.addPhoneNumber("+39 000 333 222")
            self.dc.addPhoneNumber("+39 000 333 444 ")
            self.assertEqual(len(self.dc.getPhoneNumber()), 3, 
                             msg="wrong amount of phone numbers left in entry (len(3))")
            self.assertEqual(self.dc.deletePhoneNumber("+39 000 333 444"), 2, 
                             msg="wrong number of deleted phone numbers (2)")
            self.dc.addPhoneNumber("+39 000 333 444 ")
            self.dc.addPhoneNumber("+39 000 333 444 ")

            self.assertRaises(BaseException, self.dc.updatePhoneNumber,"+39 000 333 WWW","+39 000 333 444")
            nu= self.dc.updatePhoneNumber("+39 000 333 222 "," +39 000 333 444")
            self.assertEqual(nu, 1, msg="update phone_number returns the wrong number (1) %d" % nu)
            self.assertEqual(self.dc.getPhoneNumber(0).text, "+39 000 333 444", msg="wrong phone number on postion 0")
            

    unittest.main(argv = unittest.sys.argv + ['--verbose'])
    # unittest.main()
    sys.exit(0)
    
