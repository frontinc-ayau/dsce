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

"""Just to make release packages using one command.
"""
import os, sys, getopt, subprocess, json, shutil, tarfile, platform

from distutils.core import *
import py2exe
import distutils.archive_util

import logging
logging.basicConfig(format="%(asctime)s %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.DEBUG)
log = logging

# defaults
_PNAME_ = "dsce"
_PREFIX_ = "%s-" % _PNAME_
# the format of the json should be a list of tuples where each tuple
# has the following format:
# (filename, src, exe)
# path/to/file relative to the the package base directory
# src = true/false depending, if it should be included to the src package
# exe = true/false depending, if it should be included to the executable package
#
# Mapping of indeces
I_FN=0
I_SRC=1
I_EXE=2

_MANIFEST_ = "manifest.json"

_USAGE__TXT ="""release.py - Create release packages
Used to build release packages of the DomainSharedContactsEditor.

Usage: release.py [options] 

Options
 mandatory:
    -v version  # what version should be applied to the created packages
    -p prefix   # what should be used as before the version number [%s]
    -m manifest # manifest file to use [%s]
    -e          # build windows exe 
    -s          # build src tar 
 optional:
    -h          # this screen
""" % (_PREFIX_, _MANIFEST_)

_MK_SRC_ = False
_MK_EXE_ = False

def usage():
    print(_USAGE__TXT)


def exit_on_error(msg, rc=1):
    log.fatal("%s" % msg)
    sys.exit(rc)

def get_file_records(mf):
    """Returns all file records found in the manifest"""
    return json.load(open(mf,"r"))

def _get_file_list(mf, ridx):
    """ridx is either I_SRC or I_EXE
    """
    fl = []
    for record in get_file_records(mf):
        log.debug("%s" % str(record))
        if record[ridx]:
            fl.append(record[I_FN])
    return fl

def get_src_file_list(mf):
    """Returns a list of files that has to be distributed in the
    source package.
    """
    return _get_file_list(mf, I_SRC)

def get_exe_file_list(mf):
    """Returns a list of files that has to be distributed in the
    execution package.
    """
    return _get_file_list(mf, I_EXE)

def get_pkg_root(pf, vn):
    return "%s%s" % (pf,vn)

def create_package_dirs(pr, fl):
    """Creates the needed package directory structure 
    depending on the package root directory (pr) and list of files.
    """
    rp = os.path.abspath(pr)
    for f in fl:
        d = os.path.dirname(f)
        fp = os.path.join(rp,d)
        if not os.path.isdir(fp):
            log.info("Create directory %s" % fp)
            os.makedirs(fp)
    
def cp_files(pr, fl):
    """Copies files found in the file list to th package root (pr)
    """
    rp = os.path.abspath(pr)
    for src in fl:
        s = os.path.abspath(src)
        d = os.path.abspath(os.path.join(rp,src))
        log.info("Copy %s to %s" % (s,d))
        shutil.copy2(s,d)
        

def remove_dirs(directory):
    d = os.path.abspath(directory)
    if os.path.exists(d) and os.path.isdir(d):
        log.info("Remove directory %s" %d )
        shutil.rmtree(d)
    elif os.path.exists(d) and os.path.isfile(d):
        raise BaseException("%s is not a directory" %d)


def create_src_tar(pr):
    """Expects the root dir and creates a pr.tar.gz 
    archive including the content of pr.
    """
    tfn = "%s.tar.gz" % pr
    log.info("Open %s" % tfn)
    t = tarfile.open(name=tfn, mode='w:gz')
    log.info("Add %s to archive" % pr)
    t.add(pr)
    log.info("Close %s" % tfn)
    t.close()

def configure_pkg(pr):
    """In principle this ensures that the application is executable
    without additional configuration after extracting. 
    """
    log.info("Configure package")
    defcfg = os.path.abspath(os.path.join(pr,"etc/dsce.json"))
    srccfg = os.path.abspath(os.path.join(pr,"etc/noproxy.dsce.json.example"))
    log.info("Generate %s" % defcfg)
    log.info("Use %s" % srccfg)
    shutil.copy2(srccfg,defcfg)
    
    

def build_src_package(pf,vn, mf):
    # pf ... prefix
    # vn ... version number
    # mf ... manifest file
    log.info("Create src package")
    log.info("Use manifest file %s" % mf)

    log.info("Retrieve source file list")
    fl = get_src_file_list(mf)

    pr = get_pkg_root(pf, vn)
    
    log.info("Cleanup old directories")
    remove_dirs(pr)
    
    log.info("Create package directory structure in %s" % pr)
    create_package_dirs(pr, fl)

    log.info("Copy src files to %s" % pr)
    cp_files(pr, fl)

    configure_pkg(pr)

    log.info("Create tar file archive")
    create_src_tar(pr)

    log.info("Cleanup temporary directories")
    remove_dirs(pr)
    log.info("Src package created successful")

def compile():
    sys.path.append("./lib")

    sys.argv = []
    sys.argv.append(__file__)
    sys.argv.append("py2exe")

    rs = """setup(
        console=['bin/DomainSharedContactsEditor.py'],
        options={
            "py2exe":{ 
                "packages": ['wx.lib.pubsub', 'gdata']
                
            }
        }
    )"""
    exec(rs)

    
    
def build_exe_package(pf, vn, mf):
    # pf ... prefix
    # vn ... version number
    # mf ... manifest file
    OS = platform.system()
    if OS != "Windows":
        exit_on_error("Cannot build executable on %s" % OS)

    ARCH = platform.architecture()[0]
    log.info("Create %s executable for %s" % (ARCH, OS))

    pr = get_pkg_root(pf, vn)
    pr = "%s-Win%s" % (pr, ARCH)
    log.info("pkg name %s" % pr)

    log.info("Remove old directories")
    remove_dirs(pr)
    remove_dirs("build")
    remove_dirs("dist")

    log.info("Compile dsce")
    compile()

    log.info("Rename dist to %s" % pr)
    os.rename("dist", pr)
    
    log.info("Get additional package file list")
    fl = get_exe_file_list(mf)

    log.info("Create package directory structure in %s" % pr)
    create_package_dirs(pr, fl)

    log.info("Copy files to %s" % pr)
    cp_files(pr, fl)

    configure_pkg(pr)

    log.info("Archive to %s.zip" % pr)
    distutils.archive_util.make_zipfile(pr, pr)

    log.info("Cleanup temporary directories")
    remove_dirs(pr)
    remove_dirs("build")
    log.info("Executable package created successful")
    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        exit_on_error("Too view arguments!")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv:p:m:es")
    except getopt.GetoptError, err:
        usage()
        exit_on_error(str(err))
        
    vn = None
    pf = _PREFIX_
    mf = os.path.abspath(_MANIFEST_)

    for o,a in opts:
        if o == "-v":
            vn = a
        elif o == "-p":
            pf = a
        elif o == "-m":
            mf = os.path.abspath(a)
        elif o == "-e":
            _MK_EXE_ = True
        elif o == "-s":
            _MK_SRC_ = True
        elif o == "-h":
            usage()
            sys.exit(0)
        else:
            usage()
            exit_on_error("Not handled option %s" % o)
        

    if not _MK_SRC_  and not _MK_EXE_:
        usage()
        exit_on_error("Either '-e' or '-s' is mandatory!")
    if not vn:
        usage()
        exit_on_error("'-v version' is mandatory!")

    if not os.path.isfile(mf): exit_on_error("File %s does not exist" % mf)


    if _MK_SRC_:
        log.info("Build source release packages for %s" % get_pkg_root(pf,vn))
        build_src_package(pf, vn, mf)

    if _MK_EXE_:
        log.info("Build exe release packages for %s" % get_pkg_root(pf,vn))
        build_exe_package(pf, vn, mf)
        


    sys.exit(0)

