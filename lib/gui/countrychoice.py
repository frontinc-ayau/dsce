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

import wx

from domaindata import countrycodes

class CountryChoice(wx.Choice):
    def __init__(self, parent, id=1, size=(-1, -1), choices = countrycodes.get_country_list()):
        wx.Choice.__init__(self, parent, id, size, choices=choices)
        self.choices = choices
        
    def setValue(self, value):
        """Searches the value in a more or less intelligent way and sets the selection to this
        Value"""
        # XXX Needs of course a better algorithm...
        cs = None
        if len(value) == 2: # might be a country code
            cs = countrycodes.get_country(code=value)
        elif len(value) > 2: # might be a country
            cs = countrycodes.get_country(name=value)

        if cs:
            self.SetSelection(self.choices.index(unicode(cs)))

