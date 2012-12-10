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
# Copyright (c) 2012 Klaus Melcher (melcher.kla@gmail.com)
"""This package provides supporting functions that are used 
in searching.""" 
import logging

def contact_has_string(contact, s):
    """Returns True, if any contact data contains
    the passed string s. This function works NOT case
    sensitive."""
    S=s.upper()
    if (S in contact.getFamilyName().upper()) ||
       (S in contact.getGivenName().upper()) ||
       (S in contact.getFullName().upper()) ||
       (S in contact.getNamePrefix().upper()) ||
       (S in contact.getNameSuffix().upper()) ||
       (S in contact.getAdditionalName().upper()) ||
       (S in str(c.getEmailAddresses()).upper()):
        return True
    else:
        return False
#   if S in contact.getFamilyName().upper():
#       return True
#   elif S in contact.getGivenName().upper():
#       return True
#   elif S in contact.getFullName().upper():
#       return True
#   elif S in contact.getNamePrefix().upper():
#       return True
#   elif S in contact.getNameSuffix().upper():
#       return True
#   elif S in contact.getAdditionalName().upper():
#       return True
#   elif find_string_in_emails(contact, S): 
#       return True
#   else:
#       return False
    # def getGroups(self):
    # def getPostalAddress(self, idx=-1):
    # def getPhoneNumber(self,idx=-1):
    # def getOrganization(self):

