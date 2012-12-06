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
"""This module acts as an facade/filter to gdata.data.PhoneNumber().

It depends on the phone number related definitions made in metadata. 
Throughout the whole module the parameter/variable 'p' refers to 
a gdata.data.PhoneNumber() object and 'd' to a python dicionary of the
format {PID:VALUE}. 'PID' or 'pid' refers always to one of the PID_ definitions 
made in the metadata module (see import below).
"""

import gdata
import gdata.data
import logging

from domaindata.metadata import PID_NUMBER
from domaindata.metadata import PID_TYPE
from domaindata.metadata import PID_LABEL
from domaindata.metadata import PID_PRIMARY
from domaindata.metadata import PID_URI

from domaindata.metadata import PHONE_TYPE



def getPhoneNumber(p):
    if p.text: 
        return p.text
    return None

def setPhoneNumber(p, v):
    p.text = v

def getType(p):
    if p.rel: 
        return PHONE_TYPE[p.rel]
    return None

def setType(p, v):
    """spa = StructuredPostalAddress(), v = value"""
    p.rel=PHONE_TYPE.getKey(v)

def getLabel(p):
    if p.label: 
        return p.label
    return None

def setLabel(p, v):
    p.label = v

def getPrimary(p):
    if p.primary:
        if p.primary == "true":
            return "yes"
        else:
            return ""
    return None

def setPrimary(p, v):
    if v == True or v == "true" or v == "yes":
        p.primary = "true"

def getUri(p):
    if p.uri: 
        return p.uri
    return None

def setUri(p, v):
    p.uri = v

def getValue( p, pid ):
    return _GETTER[pid](p)

def setValue( p, pid, v):
    _SETTER[pid](p, v)


# map the PIDs to it's getter and setter functions
_GETTER = {}
_GETTER[PID_NUMBER] = getPhoneNumber
_GETTER[PID_TYPE] = getType
_GETTER[PID_LABEL] = getLabel
_GETTER[PID_PRIMARY] = getPrimary
_GETTER[PID_URI] = getUri

_SETTER = {}
_SETTER[PID_NUMBER] = setPhoneNumber
_SETTER[PID_TYPE] = setType
_SETTER[PID_LABEL] = setLabel
_SETTER[PID_PRIMARY] = setPrimary
_SETTER[PID_URI] = setUri


def getAsDict(p):
    """Returns 'p' as dictionary 'd'.
    If one pid has no corresponding value it will not be present in the
    returned dictionary.
    """
    d = {}
    for id, gf in _GETTER.iteritems():
        v = gf(p)
        if v:
            d[id] = v
    return d

def getPNfromDict(d):
    pn = gdata.data.PhoneNumber()
    for id, v in d.iteritems():
        setValue(pn, id, v)
    return pn
