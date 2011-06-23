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
# Copyright (c) 2011 Klaus Melcher (melcher.kla@gmail.com)
"""The package is going to be responsible for local storage handling,
e.g. to temporary store the downloaded contacts for a kind of offline 
modus, or to persist screen settings...
"""

import os, logging, pickle

try:
    from configuration import *
except:
    import sys
    sys.path.append(".")
    from configuration import *

# Storage identifiers will be used as unique key to access locally stored
# data.
SID_CONTACTS = 0

def get_contacts():
    logging.debug("Looking for db %s" % config.contactsDB)
    if os.path.isfile(config.contactsDB):
        logging.debug("Load contacts from contactsDB")
        return pickle.load(open(config.contactsDB,"r"))
    else:
        return None

def get(sid, **kwargs):
    if sid == SID_CONTACTS:
        return get_contacts()
    else:
        raise BaseException("Unknown SID %s" % str(sid))

if __name__ == "__main__":

    logging.basicConfig(format= config.logFormat,
                        datefmt = config.logDateFormat,
                        level=config.debugLevel)

    print get(SID_CONTACTS)
