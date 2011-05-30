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

import json, os, os.path
import logging
from configfilefilter import *

class Configuration(object):
    """Main class to handle application configuration data.

    Example usage:
        conf = Configuration()
        conf.set("key1", value1)
        conf.set("key2", value2)
        ...
        # example usage
        a = conf.key1

    """
    def set(self, key, value):
        self.__setattr__(key, value)

    def getAll(self):
        """Write configuration to stdout
        """
        return self.__dict__


    def hasKey(self, key):
        return self.__dict__.has_key(key)
        

class DSCEConfiguation(Configuration):
    """DSCE specific configuration. The main purpose is to load 
    INSTALLDIR/etc/dsce.json where INSTALLDIR is __file__/../../.
    Also, per accident ;-), INSTALLDIR will be provided as installDir option.
    If the configuration file does not exist, an IOError will be raised.
    """
    def __init__(self):
        Configuration.__init__(self)
        
        installDir = os.path.dirname(os.path.abspath(__file__))
        self.set("installDir", os.path.abspath(os.path.join(installDir, "../../")) )

        self.loadConfigFile(os.path.join(self.installDir,"etc","dsce.json"))
        self._correctValues()


    def _correctValues(self):
        """Correct missing values with default values, where possible.
        """
        if self.hasKey("debugLevel"):
            self.set("debugLevel", eval("logging.%s" % self.debugLevel))
        else:
            self.set("debugLevel", logging.INFO)
        

    def loadConfigFile(self, filename):
        """Depending on the file extention the settings are loaded by
        """

        if not os.path.isfile(filename):
            raise IOError("File %s does not exist or is not a regular file!" % os.path.abspath(filename))

        co = None

        if filename.endswith("json"):
            co = JSONConfigFileFilter(filename)
        else:
            raise BaseException("Configuration file type %s not supported!" %
                                os.path.basename(filename))
        

        for k,v in co.getAllAsDict().iteritems():
            self.set(k, v)
        
