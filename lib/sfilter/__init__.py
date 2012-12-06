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
    if contact.getFamilyName().upper().find(S) >= 0:
        return True
    elif contact.getGivenName().upper().find(S) >= 0:
        return True
    elif contact.getFullName().upper().find(S) >= 0:
        return True
    elif contact.getNamePrefix().upper().find(S) >= 0:
        return True
    elif contact.getNameSuffix().upper().find(S) >= 0:
        return True
    elif contact.getAdditionalName().upper().find(S) >= 0:
        return True
    else:
        return False
    # def getEmailAddresses(self):
    # def getGroups(self):
    # def getPostalAddress(self, idx=-1):
    # def getPhoneNumber(self,idx=-1):
    # def getOrganization(self):
