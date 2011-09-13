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

#copy the folder in /home and  execute
import getopt, sys
import aeoluslib

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h:i:s:u:v", ["help", "rpms","src","conductor","oz","factory","iwhd","audrey"])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	output = None
	verbose = False
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-i", "--repo"):
                        aeoluslib.aeolus_cleanup()
                        aeoluslib.addrepo()
                        aeoluslib.instpkg()
                        aeoluslib.aeolus_configure()
                        aeoluslib.check_services()
                        aeoluslib.inst_dev_pkg()
                        aeoluslib.pullsrc_compile()     
                elif o in ("-s", "--src"):
                        aeoluslib.aeolus_cleanup()
                        aeoluslib.inst_dev_pkg()
                        aeoluslib.pullsrc_compile_conductor()
                        aeoluslib.inst_frm_src_conductor()
                        aeoluslib.check_services()
                elif o in ("-u"):
                        if a == "--conductor":
                              aeoluslib.inst_dev_pkg()
                              aeoluslib.pullsrc_compile_conductor()
                              aeoluslib.inst_frm_src_conductor()
                        if a == "--oz":
                              aeoluslib.pullsrc_compile_Oz()
                              aeoluslib.inst_frm_src_oz()
                        if a == "--factory":
                              aeoluslib.pullsrc_compile_image_factory()
                              aeoluslib.inst_frm_src_image_factory() 
                        if a == "--iwhd":
                              aeoluslib.inst_dev_pkg_iwhd()
                              aeoluslib.pullsrc_compile_iwhd()
                              aeoluslib.inst_frm_src_iwhd()
	                if a == "--audrey":
                              aeoluslib.pullsrc_compile_audry()
                              aeoluslib.inst_frm_src_audry()
                        if a == "--all": 
                              aeoluslib.inst_dev_pkg()
                              aeoluslib.pullsrc_compile_conductor()
                              aeoluslib.inst_frm_src_conductor()
                              aeoluslib.pullsrc_compile_Oz()
                              aeoluslib.inst_frm_src_oz()
                              aeoluslib.pullsrc_compile_image_factory()
                              aeoluslib.inst_frm_src_image_factory()
                              aeoluslib.inst_dev_pkg_iwhd()
                              aeoluslib.pullsrc_compile_iwhd()
                              aeoluslib.inst_frm_src_iwhd()
                              aeoluslib.pullsrc_compile_audry()
                              aeoluslib.inst_frm_src_audry()
                else:
			assert False, "unhandled option"


def usage():
    usage = """
    -h --help                 Prints help
    -i --repo                 Install conductor from repo
    -s --src                  Install conductor from src
    -s --srcall               Install rpms,install and update all components from src
    -u --all                  Update all components
    -u --conductor            Update Conductor
    -u --oz                   Update Oz 
    -u --factory              Update factory 
    -u --iwhd                 Update iwhd
    -u --audrey               Update Audrey
    """
    print usage


if __name__ == "__main__":
	main()
