#!/usr/bin/python

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Description: aeolus installation in two ways
# Option 1:Install all the rpms from the last released repo and then pull all the src and compile
# Option 2:Only pull the src and compile
#
# Author: Aziza Karol <akarol@redhat.com>
# Copyright (C) 2011  Red Hat
# see file 'COPYING' for use and warranty information
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 only
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from optparse import OptionParser
import subprocess as sub
import os
import shutil
import aeoluslib
import logging

parser = OptionParser(usage="usage: %prog [options]\n ex: ./install.py -o --oz -p --base_dir '/home'", version="%prog 1.0")
parser.add_option("-r", "--repo", action="store_true", dest="repo",   default=False, help="Install conductor from repo(does not require base dir)")
parser.add_option("-s", "--src", action="store_true", dest="src",   default=False, help="Install conductor from src")
parser.add_option("-u", "--all", action="store_true", dest="all",   default=False, help="Update all components from src")
parser.add_option("-c", "--conductor", action="store_true", dest="conductor",   default=False, help="update conductor")
parser.add_option("-o", "--oz", action="store_true", dest="oz",   default=False, help="update oz")
parser.add_option("-f", "--factory", action="store_true", dest="factory",   default=False, help="update factory")
parser.add_option("-i", "--iwhd", action="store_true", dest="iwhd", default=False, help="update iwhd")
parser.add_option("-a", "--audrey", action="store_true", dest="audrey", default=False, help="update audrey")
parser.add_option("-z", "--configure", action="store_true", dest="configure", default=False, help="update audrey")
parser.add_option('-p','--base_dir', type='string',dest='dir',help='base dir of checkout')
parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="print debug output",)
(options, args) = parser.parse_args()
base_dir = str(options.dir)


LOG_FILENAME = 'output.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=LOG_FILENAME,
                    filemode='w')

logging.info('base_dir='+base_dir)
os.system("mkdir "+base_dir)

if options.repo:
        print("installing from repo")
        try:
         aeoluslib.aeolus_cleanup()
        except:
         print("could not uninstall")
        aeoluslib.addrepo()
        aeoluslib.instpkg()
        aeoluslib.aeolus_configure()
        aeoluslib.check_services()
        #aeoluslib.inst_dev_pkg()
        #aeoluslib.pullsrc_compile()

if options.src and options.dir:
        
        aeoluslib.aeolus_cleanup()
        aeoluslib.addrepo()
        aeoluslib.instpkg()
        aeoluslib.inst_dev_pkg()
        aeoluslib.pullsrc_compile_conductor(base_dir)
        aeoluslib.inst_frm_src_conductor()
        aeoluslib.aeolus_configure()
        aeoluslib.check_services()


if options.conductor and options.dir:
        
        aeoluslib.cleanup_aeolus()
        aeoluslib.inst_dev_pkg()
        aeoluslib.pullsrc_compile_conductor(base_dir)
        aeoluslib.inst_frm_src_conductor()
        aeoluslib.aeolus_configure()
        aeoluslib.check_services()


if options.oz and options.dir:
          
        aeoluslib.pullsrc_compile_Oz(base_dir)
        aeoluslib.inst_frm_src_oz()


if options.factory and options.dir:
        
        aeoluslib.pullsrc_compile_image_factory(base_dir)
        aeoluslib.inst_frm_src_image_factory()
       
if options.configure and options.dir:
        aeoluslib.pullsrc_compile_Configure(base_dir)
        aeoluslib.inst_frm_src_configure()

if options.iwhd and options.dir:
        
        aeoluslib.inst_dev_pkg_iwhd()
        aeoluslib.pullsrc_compile_iwhd(base_dir)
        aeoluslib.inst_frm_src_iwhd()


if options.audrey and options.dir:
        
        aeoluslib.pullsrc_compile_audry(base_dir)
        aeoluslib.inst_frm_src_audry()


if options.all and options.dir:
       
       aeoluslib.cleanup_aeolus()
       aeoluslib.inst_dev_pkg()
       aeoluslib.pullsrc_compile_conductor(basedir)
       aeoluslib.inst_frm_src_conductor()
       aeoluslib.aeolus_configure()
       aeoluslib.check_services()
       aeoluslib.pullsrc_compile_Oz(base_dir)
       aeoluslib.inst_frm_src_oz()
       aeoluslib.pullsrc_compile_image_factory(base_dir)
       aeoluslib.inst_frm_src_image_factory()
       aeoluslib.inst_dev_pkg_iwhd()
       aeoluslib.pullsrc_compile_iwhd(base_dir)
       aeoluslib.inst_frm_src_iwhd()
       aeoluslib.pullsrc_compile_audry(base_dir)
       aeoluslib.inst_frm_src_audry()

