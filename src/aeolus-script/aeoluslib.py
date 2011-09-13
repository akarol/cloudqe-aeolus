#!/usr/bin/env python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Description: aeolus install library functions 
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

import subprocess
import commands
import time
import sys
import os
import shutil
import re
import errno
import logging

AEOLUS_DIR_PATH = '/home/'
LOG_FILENAME = '/home/aeolus-script/output.log'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=LOG_FILENAME,
                    filemode='w')


#Execute command
def exec_command(cmdstring):
    v, o = commands.getstatusoutput(cmdstring)          
    if v:
        logging.debug(o)
        raise Exception("%s: FAILED" % cmdstring);
        logging.info("%s: v value" % v); 
    else:
        logging.info('SUCCESS')
      #  logging.info("%s: o value" % o);
    return (o)


#Aeolus cleanup
def aeolus_cleanup():
     check_exist = 'rpm -qa | grep aeolus'
     logging.info('Checking if old aeolus version is installed')
     logging.info('running: %s' % check_exist)
     v, o = commands.getstatusoutput(check_exist)
     logging.info('output:\n %s' % o)
     if o:
           aeolus_clean = 'sudo aeolus-cleanup'
           logging.info('running: %s' % aeolus_clean)
           exec_command(aeolus_clean)
           uninstl_aeolus = 'sudo yum -y remove  aeolus-all'
           logging.info('running: %s' % uninstl_aeolus)
           exec_command(uninstl_aeolus) 
     else:
          logging.info('No old verison installed')


#Add repo
def addrepo():
    addrepo = 'sudo wget -O /etc/yum.repos.d/fedora-aeolus.repo http://repos.fedorapeople.org/repos/aeolus/conductor/0.3.0/fedora-aeolus.repo'
    logging.info('running: %s' % addrepo)
    out = exec_command(addrepo)


#Install all the prerequisite aeolus packages
def instpkg():
    instpkg = 'sudo yum -y install aeolus-all'
    logging.info('running: %s' % instpkg)
    exec_command(instpkg)


#aeolus-configure
def aeolus_configure():
    ae_conf = 'sudo aeolus-configure'
    logging.info('running: %s' % ae_conf)
    exec_command(ae_conf)


#run check_services
def check_services():
    #os.chdir('/home/aeolus-script')
    chk_service = './checkServices.rb'
    logging.info('running: %s' % chk_service )
    out = exec_command(chk_service)
    logging.info('output:\n %s' % out)   

#Install the required development packages for conductor
def inst_dev_pkg():
    instdevpkg = 'sudo yum -y install classads-devel git rest-devel rpm-build ruby-devel zip '
    logging.info('running: %s' % instdevpkg)
    exec_command(instdevpkg)


#Install the required development packages for iwhd
def inst_dev_pkg_iwhd():
    instdevpkg = 'sudo yum -y install git jansson-devel.x86_64 libmicrohttpd-devel.x86_64 hail-devel.x86_64 gc-devel.x86_64 gperf mongodb-devel.x86_64 mongodb-server bison automake gettext-devel autoconf patch gcc gcc-c++ curl-devel uuid uuid-devel libuuid-devel libxml2-devel make boost-devel flex help2man libacl libacl-devel"classads-devel git rest-devel rpm-build ruby-devel zip'
    logging.info('running: %s' % instdevpkg)
    exec_command(instdevpkg)



rpmbuild_dir = '/root/rpmbuild/'
rpmpath = '/root/rpmbuild/RPMS/noarch'

clone_path = '/home/conductor' 
#Clone the Conductor git repository and compile
def pullsrc_compile_conductor():
    if os.path.exists(clone_path):
       logging.info('Removing existing cloned git repo that was detected...')
       shutil.rmtree(clone_path) 
    logging.info('Cloning the conductor git repositiry')
    #os.makedirs(AEOLUS_DIR_PATH)
    os.chdir(AEOLUS_DIR_PATH)
    clone = 'sudo git clone git://git.fedorahosted.org/git/aeolus/conductor.git'
    logging.info('running: %s' % clone)
    exec_command(clone)
    os.chdir(clone_path)
    mkrpms = 'make rpms'
    logging.info('running: %s' % mkrpms)
    exec_command(mkrpms)
 

#install conductor from source
def inst_frm_src_conductor():
    logging.info('Installing rpms from src')
    os.chdir(rpmpath)
    rpm_install = 'sudo yum -y localinstall aeolus* --nogpgcheck'  
    logging.info('running: %s' % rpm_install)
    exec_command(rpm_install)


clone_Oz_dir = '/home/oz'
#clone the Oz git repository and compile
def pullsrc_compile_Oz():
    if os.path.exists(clone_Oz_dir):
       logging.info('Removing existing cloned git repo that was detected...')
       shutil.rmtree(clone_Oz_dir)
    logging.info('Cloning the Oz git repositiry')
    os.chdir(AEOLUS_DIR_PATH)
    clone = 'sudo git clone git://github.com/clalancette/oz.git'
    logging.info('running: %s' % clone)
    exec_command(clone)
    if os.path.exists(rpmbuild_dir):
       logging.info('Removing existing rpmbuild dir that was detected...')
       os.system('rm -rf rpmbuild_dir')
    os.chdir(clone_Oz_dir)
    mkrpms = 'make rpm'
    logging.info('running: %s' % mkrpms)
    exec_command(mkrpms)

#install oz from source
def inst_frm_src_oz():
    logging.info('Installing rpms from src')
    os.chdir(rpmpath)
    rpm_install = 'sudo yum -y localinstall oz* --nogpgcheck'
    logging.info('running: %s' % rpm_install)
    exec_command(rpm_install)



clone_imgfact_dir = '/home/imagefactory'
#clone the image_factory git repository and compile
def pullsrc_compile_image_factory():
    if os.path.exists(clone_imgfact_dir):
       logging.info('Removing existing cloned git repo that was detected...')
       shutil.rmtree(clone_imgfact_dir)
    logging.info('Cloning the imagefactory git repositiry')
    os.chdir(AEOLUS_DIR_PATH)
    clone = 'sudo git clone https://github.com/aeolusproject/imagefactory'
    logging.info('running: %s' % clone)
    exec_command(clone)
    if os.path.exists(rpmbuild_dir):
       logging.info('Removing existing rpmbuild dir that was detected...')
       os.system('rm -rf rpmbuild_dir')
    os.chdir(clone_imgfact_dir)
    mkrpms = 'python setup.py bdist_rpm'
    logging.info('running: %s' % mkrpms)
    exec_command(mkrpms)



#install imagefactory from source
def inst_frm_src_image_factory():
    logging.info('Installing rpms from src')
    os.chdir(rpmpath)
    rpm_install = 'sudo yum -y localinstall *noarch.rpm --nogpgcheck'
    logging.info('running: %s' % rpm_install)
    exec_command(rpm_install)



clone_iwhd_dir = '/home/iwhd'
#clone the iwhd git repository and compile
def pullsrc_compile_iwhd():
    if os.path.exists(clone_iwhd_dir):
       logging.info('Removing existing cloned git repo that was detected...')
       shutil.rmtree(clone_iwhd_dir)
    logging.info('Cloning the iwhd git repositiry')
    os.chdir(AEOLUS_DIR_PATH)
    clone = 'sudo git clone git://git.fedorahosted.org/iwhd.git'
    logging.info('running: %s' % clone)
    exec_command(clone)
    if os.path.exists(rpmbuild_dir):
       logging.info('Removing existing rpmbuild dir that was detected...')
       os.system('rm -rf rpmbuild_dir')
    os.chdir(clone_iwhd_dir)
    mkrpms = 'make rpm'
    logging.info('running: %s' % mkrpms)
    exec_command(mkrpms)



#install iwhd from source
def inst_frm_src_iwhd():
    logging.info('Installing rpms from src')
    os.chdir(rpmpath)
    rpm_install = 'sudo yum -y localinstall iwhd* --nogpgcheck'
    logging.info('running: %s' % rpm_install)
    exec_command(rpm_install)



clone_audrey_dir = '/home/audrey'
config_path = '/home/audrey/configserver'
#clone the audery git repository and compile
def pullsrc_compile_audry():
    if os.path.exists(clone_audrey_dir):
       logging.info('Removing existing cloned git repo that was detected...')
       shutil.rmtree(clone_audrey_dir)
    logging.info('Cloning the audrey git repositiry')
    os.chdir(AEOLUS_DIR_PATH)
    clone = 'sudo git clone git://github.com/clalancette/audrey.git -b config-server'
    logging.info('running: %s' % clone)
    exec_command(clone)
    if os.path.exists(rpmbuild_dir):
       logging.info('Removing existing rpmbuild dir that was detected...')
       os.system('rm -rf rpmbuild_dir')
    os.chdir(config_path)
    mkrpms = 'rake rpm'
    logging.info('running: %s' % mkrpms)
    exec_command(mkrpms)


#install audery from source
def inst_frm_src_audry():
    logging.info('Installing rpms from src')
    os.chdir(rpmpath)
    rpm_install = 'sudo yum -y localinstall aeolus-config* --nogpgcheck'
    logging.info('running: %s' % rpm_install)
    exec_command(rpm_install)

