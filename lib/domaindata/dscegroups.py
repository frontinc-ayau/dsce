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

"""This is the enhancement to the gdata.contacts.data.GroupsFeed class 
to adopt it for our needs and let it work as an interface to the dsce
application.
"""

import gdata.contacts.data
import atom.data

import observer
from observer import pmsg

# Index of the group lists tuple returned
# by DSCEGroupsFeed.getGroupNames()
SYSTEM_GROUPS = 0
PRIVATE_GROUPS = 1

class _GLOBAL_(object):
    pass
GRP = _GLOBAL_()
GRP.ADD = "a"
GRP.UPDATE = "u"
GRP.DELETE = "d"

class DSCEGroupsFeed(gdata.contacts.data.GroupsFeed):

    def __init__(self, *args, **kwargs):
        gdata.contacts.data.GroupsFeed.__init__(self, *args, **kwargs)
        self.ng = []
        self.dg = []
        self.ug = []

    def getGroupNames(self):
        sg = []
        pg = []
        for e in self.entry:
            if e.system_group:
                sg.append(e.system_group.id)
            else:
                pg.append(e.title.text)
        for e in self.ng+self.ug: # in case we already have added some groups
            pg.append(e.title.text)
        return (sg, pg)


    def getNameById(self,gid):
        for e in self.entry:
            if e.id.text == gid:
                if e.system_group:
                    return e.system_group.id
                else:
                    return e.title.text
        # XXX What about new groups...


    def getGroupIDbyName(self, name):
        for e in self.entry:
            if e.system_group:
                if e.system_group.id == name:
                    return e.id.text
            else:
                if e.title.text == name:
                    return e.id.text
        for e in self.ng+self.ug: # in case we already have added some groups
            if e.title.text == name:
                return e.id.text
            
    def addGroup(self, name):
        self.ng.append(gdata.contacts.data.GroupEntry(title=atom.data.Title(text=name)))

    def __delitionDone__(self, e):
        d={'id':e.id.text, 'name':e.title.text}
        observer.send_message(pmsg.GROUP_DELETION_DONE, data=d)

    def delGroup(self, name):
        for e in self.entry:
            if e.system_group:
                pass
            else:
                if e.title.text == name:
                    self.dg.append(e)
                    self.entry.remove(e)
                    self.__delitionDone__(e)
                    break

        for e in self.ng: # in case it is a new group
            if e.title.text == name:
               self.ng.remove(e)
               self.__delitionDone__(e)
               break
        # XXX what if group had been first updated and then deleted befor publishing?

    def updateGroup(self, oldname, newname):
        for e in self.entry:
            if e.system_group:
                pass
            else:
                if e.title.text == oldname:
                    e.title.text = newname
                    self.ug.append(e)
                    self.entry.remove(e)
                    break
        for e in self.ng: # in case it is a new group
            if e.title.text == oldname:
               e.title.text = newname
               break
        

    def getSumOfGroupChanges(self):
        """return (nrNew, nrUpdate, neDelete)"""
        s = {}
        s[GRP.ADD] = len(self.ng)
        s[GRP.UPDATE] = len(self.ug)
        s[GRP.DELETE] = len(self.dg)
        return s

