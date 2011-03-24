# This file is part of the DomainSharedContactsEditor (DSCE) appliction.
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
# 
"""Filter for supported configuration file types
"""
import json, os

class ConfigFileFilter(object):
    """Derive each filter and implement it's methods
    """
    def __init__(self, path):
        """As 'path' the absolute filename path includint the file
        of the configuration file is expected.
        """
        raise NotImplementedError("Method not implemented!")

    def getAllAsDict(self):
        """Returns all key=val out of the configuration file as a
        dictionary.
        """
        raise NotImplementedError("Method not implemented!")



class JSONConfigFileFilter(ConfigFileFilter):
    def __init__(self, path):
        self.opts = self._getAllOpts(path)

    def _getAllOpts(self, path):
        o = {}
        jo = json.load(open(path))

        for section in jo.keys():
            for k,v in jo[section].iteritems():
                o.__setitem__(k,v)         
        return o

    def getAllAsDict(self):
        return self.opts


        
        
