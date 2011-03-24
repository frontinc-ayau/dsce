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

class LoginUser(object):
    """Represents all user information needed to connect to your google account
    """
    def __init__(self, name=None, password=None, email=None, domain=None):
        self.name = name
        self.password = password
        self.email = email
        self.account_type = None # will be set by _setDomain()
        self.domain = self._setDomain(domain)
        

    def _setDomain(self, domain):
        """If the domain is gmail.com, domain will be set to None.
        Also the account_type will be set, depending on the rules"""
        # XXX Let the user decide where feasible
        if domain == "gmail.com":
            self.domain = None
        else:
            self.domain = domain
        self._setAddountType()

    def _setAddountType(self):
        """If self.domain is None it is not a google apps account and
        therefore the account_type has to be set to GOOGLE, else to 
        HOSTED"""
        if self.domain:
            self.account_type = "HOSTED"
        else:
            self.account_type = "GOOGLE"


    def setFromEmail(self, email=None):
        """Used to set name and domain by extracting the information
        from the passed email address. Also self.email will be stet to 
        the passed email.
        Everything before '@' will be the name, anything after '@'
        will be the domain.
        if email = None then the value found in self.email will be used.
        """

        if not email:
            if not self.email:
                raise BaseException("Missing email address")
            else: 
                email = self.email

        r = email.split('@')
        
        self.name = r[0]
        self._setDomain(r[1])
        self.email = email

        return self # just to be able to initiate it within one line
        


if __name__ == "__main__":

    import logging, sys

    sys.exit(0)
    
