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

import gdata
import gdata.data

# XXX As in my gdata library the "class Country" comes with two different implementations
# (one with the 'code' attribute and one without) I decided to be shure that the 'code'
# attribute will be available anyway. 

class Country(gdata.data.Country):
    """Country name and 2 digit code."""
    code = 'code'

