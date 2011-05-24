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

"""Provides all metadata information about a DomainContact. E.g. supported attributes, 
labels to display a.s.o.
"""

# Use 'c' instead of DomainContact and self, where it has to be implemented by the 
# class that uses this information (see ContactDataTable as an example)
# [ (attributeName, attributeLabel, getterMethod, setterMethod, editable, visible) ]
_META_DATA_=[ ( "uid", "UID", "getUid()", None, False, False),
              ( "prefix", "Prefix", "c.getNamePrefix()", "c.setNamePrefix(value)", True, True),
              ( "family_name","Family Name", "c.getFamilyName()", "c.setFamilyName(value)", True, True),
              ( "given_name", "Given Name", "c.getGivenName()", "c.setGivenName(value)", True, True),
              ( "additional_name", "Additional Name", "c.getAdditionalName()", "c.setAdditionalName(value)", True, True),
              ( "suffix", "Suffix", "c.getNameSuffix()", "c.setNameSuffix(value)", True, True),
              ( "full_name", "Full Name", "c.getFullName()", "c.setFullName(value)", True, True),
              ( "email", "Email", "c.getEmail()", "c.setEmails(value)", True, True),
              ( "phone", "Phone", "c.getPhoneNumber(0)", "c.updatePhoneNumber(value)", True, False),
              ( "postal_address", "Address", "c.getPostalAddress()", "c.setPostalAddress(value)", True, True),
              ( "action", "Action", "c.getAction()", "c.setActionUpdate()", False, False)
            ]
              
IDX_ATTRIBUTE   = 0
IDX_LABEL       = 1
IDX_GETTER      = 2
IDX_SETTER      = 3
IDX_EDITABLE    = 4
IDX_VISIBLE     = 5


# For all get* it is important that when returning a list the order of
# _META_DATA_ must not be changed.
# XXX but still should be changed in the future... ;-)

def get_getter(attributeName = None, all=False):
    """If attributeName = None it returns a list of all getter in the order provided by _META_DATA_. 
    If 'all' is set to False just those with their visible flag set to True will be returned.
    If attributeName is set to an attribute the getter method will be returned depending on 
    the value of all.
    """
    if attributeName:
        for item in _META_DATA_:

            if item[IDX_ATTRIBUTE] is attributeName:
                if item[IDX_VISIBLE] or all:
                    return item[IDX_GETTER]
                else:
                    return None

        return None
                

    else:
        g = []
        if all is True:
            for item in _META_DATA_: g.append( item[IDX_GETTER] )
        elif all is False:
            for item in _META_DATA_:
                if item[IDX_VISIBLE] is True:
                    g.append( item[IDX_GETTER] )
            
        return g
    

def get_setter(attributeName = None, all=False):
    """If attributeName = None it returns a list of all setter in the order provided by _META_DATA_. 
    If 'all' is set to False just those with their visible flag set to True will be returned.
    If attributeName is set to an attribute the getter method will be returned depending on 
    the value of all.
    """
    if attributeName:
        for item in _META_DATA_:

            if item[IDX_ATTRIBUTE] is attributeName:
                if item[IDX_VISIBLE] or all:
                    return item[IDX_SETTER]
                else:
                    return None

        return None
                

    else:
        s = []
        if all is True:
            for item in _META_DATA_: s.append( item[IDX_SETTER] )
        elif all is False:
            for item in _META_DATA_:
                if item[IDX_VISIBLE] is True:
                    s.append( item[IDX_SETTER] )
            
        return s


def get_labels(all=False):
    """Returns a list of all labels in the order provided by _META_DATA_. 
    If 'all' is set to False just those with their visible flag set to True
    will be returned."""
    l=[]
    if all is True:
        for item in  _META_DATA_: l.append( item[IDX_LABEL] )
    elif all is False:
        for item in _META_DATA_:
            if item[IDX_VISIBLE] is True:
                l.append( item[IDX_LABEL] )
    return l

def get_col_idx(attname):
    """Returns the column index of the attribute in _META_DATA_. If it is not found
    -1 will be returned. Only items with visibility True are counted!
    """
    i = 0
    for item in _META_DATA_:
        if item[IDX_VISIBLE] is True:
            if item[IDX_ATTRIBUTE] is attname:
                return i
            i += 1
    return -1
            

from gdata.data import WORK_REL
from gdata.data import HOME_REL
from gdata.data import OTHER_REL

class _DICT(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
    def getKey(self, value):
        for k,v in self.iteritems():
            if v == value:
                return k

REL_LABEL = _DICT()
REL_LABEL[WORK_REL]="work" 
REL_LABEL[HOME_REL]="home"
REL_LABEL[OTHER_REL]="other"


from gdata.data import MAIL_BOTH
from gdata.data import MAIL_LETTERS
from gdata.data import MAIL_NEITHER
from gdata.data import MAIL_PARCELS

MAIL_CLASS = _DICT()
MAIL_CLASS[MAIL_BOTH]="both"
MAIL_CLASS[MAIL_LETTERS]="letters"
MAIL_CLASS[MAIL_PARCELS]="parcels"
MAIL_CLASS[MAIL_NEITHER]="neither"


from gdata.data import GENERAL_ADDRESS
from gdata.data import LOCAL_ADDRESS

MAIL_USAGE = _DICT()
MAIL_USAGE[GENERAL_ADDRESS]="genral"
MAIL_USAGE[LOCAL_ADDRESS]="local"


# Postal address meta information


class AddressMeta(object):
    def __init__(self, id, label, help):
        """id  ... unique identifier to be used throughout this dialogue
        label  ... label to be displayed
        help   ... description of the label
        """
        self.id = id
        self.label = label
        self.help = help

class AddressMetaList(list):
    def get(self, id):
        """Returns the AddressMeta object of passed id, else a BaseException
        will be raised.
        """
        for a in self:
            if a.id == id:
                return a
        raise BaseException("Unknown id %s" % id)

    def getLabel(self, id):
        """Returns the label of passed id, else a BaseExceptio will be raised.
        """
        return self.get(id).label

    def getGetter(self, id):
        """Returns the getter of passed id, else a BaseExceptio will be raised.
        """
        return self.get(id).getter

    def getHelp(self, id):
        """Returns the label of passed id, else a BaseExceptio will be raised.
        """
        return self.get(id).help

    def getIDs(self):
        """Returns all address ids.
        """
        ids = []
        for a in self:
            ids.append(a.id)
        return ids

AMI=AddressMetaList()

# as an id a two character abbreviation is used
AMI.append(AddressMeta(
                        "PA",
                        "Postal Address",
                        """The full, unstructured postal address."""
                        ))

AMI.append(AddressMeta(
                        "PR",
                        "Primary",
                        """Specifies the address as primary. Default value is false."""
                        ))

AMI.append(AddressMeta(
                        "ST",
                        "Street",
                        """Can be street, avenue, road, etc. This element also includes the
house number and room/apartment/flat/floor number."""
                        ))

AMI.append(AddressMeta(
                        "PC",
                        "Postal Code",
                        """Postal code. Usually country-wide, but sometimes specific to the
city (e.g. "2" in "Dublin 2, Ireland" addresses)."""
                        ))

AMI.append(AddressMeta(
                        "CI",
                        "City",
                        """Can be city, village, town, borough, etc. This is the postal town and
not necessarily the place of residence or place of business."""
                        ))

AMI.append(AddressMeta(
                        "CO",
                        "Country",
                        """The name or code of the country."""
                        ))

AMI.append(AddressMeta(
                        "TY",
                        "Type",
                        """Type of the address. Unless specified work type is assumed."""
                        ))

AMI.append(AddressMeta(
                        "LA",
                        "Label",
                        """Label"""
                        ))

AMI.append(AddressMeta(
                        "AG",
                        "Agent",
                        """The agent who actually receives the mail. Used in work addresses. 
Also for 'in care of' or 'c/o'."""
                        ))

AMI.append(AddressMeta(
                        "HN",
                        "House Name",
                        """Used in places where houses or buildings have names (and not
necessarily numbers), eg. "The Pillars"."""
                        ))


AMI.append(AddressMeta(
                        "MC",
                        "Mail Class",
                        """Classes of mail (letters, parcels) accepted at the address. Unless specified both is assumed."""
                        ))

AMI.append(AddressMeta(
                        "NH",
                        "Neighbourhood",
                        """This is used to disambiguate a street address when a city contains more
than one street with the same name, or to specify a small place whose
mail is routed through a larger postal town. In China it could be a
county or a minor city."""
                        ))

AMI.append(AddressMeta(
                        "PO",
                        "P.O. Box",
                        """Covers actual P.O. boxes, drawers, locked bags, etc. This is usually
but not always mutually exclusive with street."""
                        ))

AMI.append(AddressMeta(
                        "RE",
                        "Region",
                        """A state, province, county (in Ireland), Land (in Germany),
departement (in France), etc."""
                        ))

AMI.append(AddressMeta(
                        "SR",
                        "Subregion",
                        """Handles administrative districts such as U.S. or U.K. counties that are
not used for mail addressing purposes. Subregion is not intended for
delivery addresses."""
                        ))

AMI.append(AddressMeta(
                        "US",
                        "Usage",
                        """The context in which this address can be used. Local addresses may differ in 
layout from general addresses, and frequently use local script (as opposed to Latin script) 
as well, though local script is allowed in general addresses. Unless specified general usage is 
assumed."""
                        ))
