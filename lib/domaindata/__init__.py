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

"""The package domaindata is responsible to hold/define all necessary data used by dsce.
Further it provides interface methods to access the data itself.

NOTE:
    It is necessary to initialize the package by calling domaindata.init() before
    any other action on the data can be performed.
"""
import gdata.contacts.data
import gdata.contacts.client

import logging

from loginuser import *
from proxysettings import *
from domaincontactsclient import *
from domaincontact import DomainContact
from domaincontact import ACTION
from domaincontacts import DomainContacts
from dscegroups import *
from contactdatatable import *

import observer
from observer import pmsg

import storage

"""The following objects will be initialized by init()
"""

_domainContactsClient = None
_domainContacts = None
_loginUser = None
_proxySettings = None
_initialized = False # will be set to True at the end of the init() procedure.
_contactGroups = None

# Will be initialized during runtime as an existing wx.Grit is needed
_contactDataTable = None


def init():
    """Initializes all domaindata objects needed by the application.
    Each object can then be accessed direct or by using the provided 
    interface.
    """
    global _initialized, _loginUser, _domainContacts 

    if _initialized is True: return 

    if _loginUser is None: _loginUser = LoginUser()
    if _domainContacts is None: _domainContacts = DomainContacts()
    
    _initialized = True
    
def initialized():
    """Returns True if module has been initialized, else False
    """
    return _initialized

def set_proxy_environment(http_proxy = None, https_proxy = None, proxy_user = None, password = None):
    """Used to set the environment when being located behind an http proxy.
    """
    global _proxySettings
    _proxySettings = ProxySettings(http_proxy=http_proxy,
                                   https_proxy=https_proxy,
                                   proxy_user=proxy_user,
                                   password=password)


def set_login_credentials(email, password):
    global _loginUser, _domainContactsClient
    _loginUser.setFromEmail(email)
    _loginUser.password = password
    _domainContactsClient = DomainContactsClient(_loginUser)


def login():
    """Login at the google (apps) account with the provided credentials.
    """
    _domainContactsClient.loginAtSource()


def download_contacts():
    """Downloads all contacts found on google for gmail.com accounts and shared contacts
    for any other domain.
    """
    if _domainContactsClient:
        feedUrl = _domainContactsClient.GetFeedUri(contact_list=_loginUser.domain, 
                                         projection='full')
        while True:
            feed = _domainContactsClient.get_feed(uri=feedUrl,
                                                    auth_token=None,
                                                    desired_class=gdata.contacts.data.ContactsFeed)
            
            for entry in feed.entry:
                _domainContacts.append( DomainContact(entry) )
            
            next_link = feed.GetNextLink()
            # break
            if next_link is None:
                break
            else:
                feedUrl = next_link.href
          
        # XXX at the moment just for testing
        # import pickle
        # db = open("dsce.db","w+")
        # pickle.dump(_domainContacts, db)
        # db.close()


def download_groups():
    global _contactGroups, _domainContactsClient
    if _domainContactsClient:
        _contactGroups = _domainContactsClient.get_groups(desired_class=DSCEGroupsFeed)
        logging.debug("Groups downloaded. Group count: %d" % len(_contactGroups.entry))
    else:
        logging.debug("Not logged on!")

def reload_groups(delay=0):
    import time
    global _contactGroups
    logging.debug("Reload: delay: %d grops: %d" % (delay, len(_contactGroups.entry)))
    _contactGroups = None
    time.sleep(delay)
    download_groups()
    logging.debug("Groups reloaded. Group count: %d" % len(_contactGroups.entry))

def publish_group_changes():
    global _contactGroups, _domainContactsClient
    publish_added_groups()
    publish_deleted_groups()
    logging.debug("Groups published. Group count: %d" % len(_contactGroups.entry))
    reload_groups(delay=4) # XXX Need a better solution to handle the delay of the google backend

def publish_added_groups():
    global _contactGroups, _domainContactsClient
    for g in _contactGroups.ng:
        _domainContactsClient.CreateGroup(g)
    _contactGroups.ng = []

def publish_deleted_groups():
    global _contactGroups, _domainContactsClient
    for g in _contactGroups.dg:
        _domainContactsClient.Delete(g)
    _contactGroups.dg = []
        
def get_group_names():
    if not _contactGroups:
        return ([], [])
    else:
        return _contactGroups.getGroupNames()

def get_group_name(gid=None):
    global _contactGroups
    if _contactGroups and gid:
        return _contactGroups.getNameById(gid)
    else:
        return None

def get_group_id(name=None):
    global _contactGroups
    if _contactGroups and name:
        return _contactGroups.getGroupIDbyName(name)
    else:
        return None

def add_group(group):
    global _contactGroups
    if not _contactGroups:
        return
    logging.debug("Add group %s" %group.current)
    _contactGroups.addGroup(group.current)
    # make added groups immediate visible
    publish_added_groups()
    reload_groups(delay=4)

def del_group(group):
    global _contactGroups
    if not _contactGroups:
        return
    logging.debug("Delete group %s" % group.current)
    _contactGroups.delGroup(group.current)
    
def update_group(group):
    global _contactGroups
    logging.debug("Update group %s to %s" % (group.previous, group.current))
    _contactGroups.updateGroup(group.previous, group.current)

def load_contacts_store(): 
    _domainContacts = DomainContacts()
    for e in storage.get(storage.SID_CONTACTS):
        logging.debug(str(e))
        _domainContacts.append(e)
    logging.debug("Local loaded %d contacts" % len(_domainContacts))
    if _domainContacts == None:
        log.debug("Reset Contacts")
        _domainContacts = DomainContacts()
    
def add_contact(c=None):
    global _domainContacts, _contactDataTable
    logging.debug("In add_contact")
    if c == None:
        c = DomainContact()
    _domainContacts.append(c)
    _contactDataTable.appendRow(c)

def del_contact_from_row(row):
    """Deletes the contact which is in the passed row of the grid."""
    global _contactDataTable
    logging.debug("In del_contact")
    _contactDataTable.getContact(row).setActionDelete()

def get_contacts():
    """Used to return the current DomainContacts list.
    """
    return _domainContacts

def publish_changes():
    """Publish changes made to the contact
    """
    global _domainContacts, _contactDataTable 

    publish_group_changes()

    for c in _domainContacts.getChangedContacts():
        logging.debug("Contact changed: uid %d" % c.getUid())
        action = c.getAction()
        if action == ACTION.UPDATE:
            logging.debug("Updated contact %s" % c.getFamilyName())
            _domainContactsClient.updateContact(c)
            c.clearAction()
        elif action == ACTION.ADD:
            if c.isEmpty():
                logging.warning("Ignore empty contact when publishing %d" % c.getUid())
            else:
                logging.debug("Add contact %s" % c.getFamilyName())
                _domainContactsClient.addContact(c)
                c.clearAction()
        elif action == ACTION.DELETE:
            if c.isEmpty():
                logging.warning("Do not publish the deletion of an empty contact %d" % c.getUid())
            else:
                logging.debug("Delete contact %s" % c.getFamilyName())
                _domainContactsClient.deleteContact(c)
            
            _domainContacts.delete(c)
            _contactDataTable.deleteRow(c)
            del(c)
            logging.debug("deletion finished")
    # rebuild the table index is absolute necessary
    _contactDataTable.rebuildTableIndex()


def get_action_summary():
    global _contactGroups
    s = _domainContacts.getActionSummary() # contacts
    # append groups changes (add, update, delete)
    s.update(_contactGroups.getSumOfGroupChanges())
    return s


def get_grid_table(grid=None):
    """grid can be None as it makes the table requestable more than once"""
    global _contactDataTable
    if _contactDataTable == None:
        _contactDataTable = ContactDataTable(grid)
    return _contactDataTable

def do_search(sf):  # sf: search filter as string
    global _domainContacts
    if _domainContacts:
        cidx = _domainContacts.getSearchHits(sf)
        observer.send_message(pmsg.HIDE_ROWS, data=cidx)

    
def cancel_search(): # just for consitency it is done here
    observer.send_message(pmsg.UNHIDE_ROWS)
