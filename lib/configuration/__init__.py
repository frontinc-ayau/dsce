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
"""The package configuration provides application configuration functionality
(including default values) to dsce.
"""

import os, logging

from configuration import *

config = DSCEConfiguation()


def set(key, value):
    """Used to set an attribute (key) to the value in the
    config object"""
    global config
    config.set(key, value)


def getConfiguration():
    global config
    return config

if __name__ == "__main__":

    logging.basicConfig(format= config.logFormat,
                        datefmt = config.logDateFormat,
                        level=config.debugLevel)


    for k, v in config.__dict__.iteritems():
        logging.debug("%-15s = %s" %(str(k), str(v)))

