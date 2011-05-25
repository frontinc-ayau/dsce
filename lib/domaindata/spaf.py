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
# Copyright (c) 2010, 2011 Klaus Melcher (melcher.kla@gmail.com)
"""This module acts as an facade to gdata.data.StructuredPostalAddress.
"""

import gdata
import gdata.data
import logging

from domaindata.metadata import AMI
from domaindata.metadata import REL_LABEL
from domaindata.metadata import MAIL_CLASS
from domaindata.metadata import MAIL_USAGE
import country



def getPA(spa):
    if spa.formatted_address:
        return spa.formatted_address.text
    return None

def getPR(spa):
    if spa.primary:
        return spa.primary
    return None

def getST(spa):
    if spa.street:
        return spa.street.text
    return None

def getPC(spa):
    if spa.postcode:
        return spa.postcode.text
    return None

def getCI(spa):
    if spa.city:
        return spa.city.text
    return None

def getCO(spa):
    if spa.country:
        return spa.country.text
    return None

def getTY(spa):
    if spa.rel:
        return REL_LABEL[spa.rel] # Do not change
    return None

def getLA(spa):
    if spa.label:
        return spa.label
    return None

def getAG(spa):
    if spa.agent:
        return spa.agent.text
    return None

def getHN(spa):
    if spa.house_name:
        return spa.house_name.text
    return None

def getMC(spa):
    if spa.mail_class:
        return MAIL_CLASS[spa.mail_class] # Do not change
    return None

def getNH(spa):
    if spa.neighborhood:
        return spa.neighborhood.text
    return None

def getPO(spa):
    if spa.po_box:
        return spa.po_box.text
    return None

def getRE(spa):
    if spa.region:
        return spa.region.text
    return None

def getSR(spa):
    if spa.subregion:
        return spa.subregion.text
    return None

def getUS(spa):
    if spa.usage:
        return MAIL_USAGE[spa.usage] # Do not change
    return None

def setPA(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.formatted_address = gdata.data.FormattedAddress(text=v)

def setPR(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    if v == True or v == "true" or v == "yes":
        spa.primary = "true"

def setST(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.street = gdata.data.Street(text=v)

def setPC(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.postcode = gdata.data.Postcode(text=v)

def setCI(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.city = gdata.data.City(text=v)

def setCO(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    v = v.split()
    if len(v) == 2:
        spa.country = country.Country(text=v[1])
        spa.country.code = v[0]
    else:
        spa.country = country.Country(text=v[0])

def setTY(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.rel=REL_LABEL.getKey(v)

def setLA(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.label=v

def setAG(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.agent = gdata.data.Agent(text=v)

def setHN(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.house_name = gdata.data.HouseName(text=v)

def setMC(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.mail_class = MAIL_CLASS.getKey(v)

def setNH(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.neighborhood = gdata.data.Neighborhood(text=v)

def setPO(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.po_box = gdata.data.PoBox(text=v)

def setRE(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.region = gdata.data.Region(text=v)

def setSR(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.subregion = gdata.data.Subregion(text=v)

def setUS(spa, v):
    """spa = StructuredPostalAddress(), v = value"""
    spa.usage = MAIL_USAGE.getKey(v)

def getValue( spa, id ):
    """Returns the value of the spa attribute that corresponds to id.
    e.g. CI returns spa.city.text value or None if no city is defined.
    It does not return the value of the city attribute but its real
    value like Vienna, Milano, London...
    
    Implementation note: It is assumed that for each AddressMeta.id (ID) an 
    getID(spa) function exists!
    """
    return eval("get%s(spa)" % id)

def setValue( spa, id, v):
    """The sets the value of the passed id to the StructuredPostalAddress"""
    eval("set%s(spa, v)" % id)

def getSPAdict( spa ):
    """Returns the StructuredPostalAddress as dictionary where the 
    keys are the metadata.AddressMeta.id with the corresponding value
    found in the passed StructuredPostalAddress (spa). 
    If one id has no corresponding value it will not be present in the
    returned dictionary.
    """
    d = {}
    for a in AMI:
        v = getValue(spa, a.id)
        if v:
            d[a.id] = unicode(v)
    return d

def getSPAfromDict(d):
    spa = gdata.data.StructuredPostalAddress()
    for id, v in d.iteritems():
        setValue(spa, id, v)
    return spa


def getFirstString( spa ):
    """Returns either formatted address or street.
    This string is ment to be displayed in the grid.
    If neither nor exists we return an empty string
    """
    # XXX Street and postal code etc would also be nice...
    if getPA(spa):  
        return getPA(spa)
    else:
        return getST(spa)
    
