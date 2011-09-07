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
# Copyright (c) 2011, 2011 Klaus Melcher (melcher.kla@gmail.com)
"""This module acts as an facade/filter to gdata.data.Organization().

It depends on the phone number related definitions made in metadata. 
Throughout the whole module the parameter/variable 'o' refers to 
a gdata.data.Organization() object and 'v' is a value.
"""

import gdata
import gdata.data
import logging


# what is needed for type
from domaindata.metadata import WORK_REL
from domaindata.metadata import OTHER_REL
from domaindata.metadata import REL_LABEL


def setLabel(o, v):
    o.label = v

def setDepartment(o, v):
    o.department = gdata.data.OrgDepartment(text=v)

def setDescription(o, v):
    o.job_description = gdata.data.OrgJobDescription(text=v)

def setName(o, v):
    o.name = gdata.data.OrgName(text=v)

def setSymbol(o, v):
    o.symbol = gdata.data.OrgSymbol(text=v)

def setTitle(o, v):
    o.title = gdata.data.OrgTitle(text=v)

def setPrimary(o, v=False):
    if v == True or v == "true" or v == "yes":
        o.primary = "true"

def setType(o, v):
    o.rel=REL_LABEL.getKey(v)

def setWhere(o, v):
    o.where = gdata.data.Where(text=v) 


def getLabel(o):
    if o.label:
        return o.label
    else:
        return None

def getDepartment(o):
    if o.department:
        return o.department.text
    else:
        return None

def getDescription(o):
    if o.job_description:
        return o.job_description.text
    else:
        return None

def getName(o):
    if o.name:
        return o.name.text
    else:
        return None

def getSymbol(o):
    if o.symbol:
        return o.symbol.text
    else:
        return None

def getTitle(o):
    if o.title:
        return o.title.text
    else:
        return None

def getPrimary(o):
    if o.primary:
        if o.primary == "true":
            return True
        else:
            return False
    else:
        return False

def getType(o):
    if o.rel:
        return REL_LABEL[o.rel]
    else:
        None

def getWhere(o):
    # XXX not direct supported in my gdata version
    try:
        if o.where:
            return o.where.text
        else:
            return None
    except:
        return None

def isOrganization(o):
    return (type(o) == gdata.data.Organization)


def getOrganization(label=None, department=None, description=None, name=None,
                    symbol=None, title=None, primary=None, typel=None, where=None):
    """Returns an gdata.data.Organization object with all not None values set 
    correctly. Prame 'typel' is the type/rel label!!
    """
    o = gdata.data.Organization()
    if label:       setLabel(o, label)
    if department:  setDepartment(o, department)
    if description: setDescription(o, description)
    if name:        setName(o, name)
    if symbol:      setSymbol(o, symbol)
    if title:       setTitle(o, title)
    if primary:     setPrimary(o, primary)
    if typel:       setType(o, typel)
    if where:       setWhere(o, where)
    return o

def getOrgAsStringList(o):
    """Used to return organization data as a list of string values. The list
    will not contain null values"""
    d=[]
    if type(o) != gdata.data.Organization:
        return d
    v=getName(o)
    if v: d.append(v)
    v=getDepartment(o)
    if v: d.append(v)
    v=getTitle(o)
    if v: d.append(v)
    v=getDescription(o)
    if v: d.append(v)
    v=getLabel(o)
    if v: d.append(v)
    v=getType(o)
    if v: d.append(v)
    v=getSymbol(o)
    if v: d.append(v)
    v=getPrimary(o)
    if v: d.append("Primary")
    v=getWhere(o)
    if v: d.append(v)
    return d


def hasWhere(o=None):
    """This needs to be done because of a kind of lack in the gdata 
    python implementation of google (see issue 28 for details)"""
    if not o:
        o = gdata.data.Organization()
    try:
        o.where
        return True
    except AttributeError, e:
        logging.warning("Your Google library does not support where: %s" % str(e))
        return False
    
