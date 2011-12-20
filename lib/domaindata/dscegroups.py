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

# Index of the group lists tuple returned
# by DSCEGroupsFeed.getGroupNames()
SYSTEM_GROUPS = 0
PRIVATE_GROUPS = 1

class DSCEGroupsFeed(gdata.contacts.data.GroupsFeed):

    def __init__(self, *args, **kwargs):
        gdata.contacts.data.GroupsFeed.__init__(self, *args, **kwargs)

    def getGroupNames(self):
        sg = []
        pg = []
        for e in self.entry:
            if e.system_group:
                sg.append(e.system_group.id)
            else:
                pg.append(e.title.text)
        return (sg, pg)

    def getNameById(self,gid):
        for e in self.entry:
            if e.id.text == gid:
                if e.system_group:
                    return e.system_group.id
                else:
                    return e.title.text

        raise BaseException("No group with id %s found!" % gid)
