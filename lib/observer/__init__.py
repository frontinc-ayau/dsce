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

""" A wrapper to the publisher. Mainly used as central place to define messages
"""

import wx
import wx.lib.pubsub.setuparg1
from wx.lib.pubsub import pub

Publisher = pub.Publisher()

import logging


class _PMSG(object):

    def register(self, msg):
        """ The attribute _PMSG.msg = msg will be created
        """
        if self.__dict__.has_key(msg):
            return
        else:
           self.__setattr__(msg, msg)
        logging.debug("%s registered" % msg)

pmsg = _PMSG()

"""Some common messages are registered at initialization so that it needs
not be done repeatedly.
"""
pmsg.register("EXIT_APP")
pmsg.register("ALERT")


# common data messages
pmsg.register("DATA_DOWNLOADED")
pmsg.register("DATA_UPLOADED")
pmsg.register("CONTACT_ADDED") 
pmsg.register("CONTACT_DELETED")
pmsg.register("GROUPS_DOWNLOADED")


def send_message(*args, **kwargs):
    Publisher.sendMessage(*args, **kwargs)

def subscribe(listener , topic):
    Publisher.subscribe(listener, topic)

def unsubscribe(listener, topic):
    Publisher.unsubscribe(listener, topic)
