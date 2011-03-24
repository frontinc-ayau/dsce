#!env python

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

_version_="0.0.0"

import sys
import os
import logging
import wx



p=os.path.abspath(os.path.dirname(sys.argv[0])).replace("bin","lib")
if os.path.isdir(p):
    sys.path.append(p)
else:
    logging.fatal("Libraries directory %s does not exist" % p)
    sys.exit(1)


import configuration

config = configuration.getConfiguration()
logging.basicConfig(format= config.logFormat,
                    datefmt = config.logDateFormat,
                    level= config.debugLevel)

import application 


if __name__ == "__main__":

    logging.debug("Start DomainSharedContactsEditor version %s" % _version_)

    app = application.Application(sys.argv)
    app.run()

    logging.debug("DomainSharedContactsEditor closed")
    sys.exit(0)
