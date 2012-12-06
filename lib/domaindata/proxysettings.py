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
import os

class ProxySettings(object):
    """Used to set os environment to be able to run this program behind
    a web proxy.
    """
    def __init__(self, http_proxy = None, https_proxy = None, proxy_user = None, password = None):
        self.httpProxy = http_proxy
        self.httpsProxy = https_proxy
        self.proxyUser = proxy_user
        self.password = password
        self._env_set_()
        
    def _env_set_(self):
        if self.httpProxy: os.environ['http_proxy'] = self.httpProxy
        if self.httpsProxy: os.environ['https_proxy'] = self.httpsProxy
        if self.proxyUser: os.environ['proxy-username'] = self.proxyUser
        if self.password: os.environ['proxy-password'] = self.password
        

if __name__ == "__main__":

    import sys

    sys.exit(0)
    
