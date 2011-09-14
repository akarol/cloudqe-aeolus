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
import pdb



LOG_FILENAME = 'output.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=LOG_FILENAME,
                    filemode='w')
rpmbuild_dir = os.path.expanduser(os.path.join('~','rpmbuild/'))
rpmpath = os.path.expanduser(os.path.join('~','rpmbuild/RPMS/noarch/'))

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
     #pdb.set_trace()
     v, o = commands.getstatusoutput(check_exist)
     logging.info('output:\n %s' % o)
     logging.info('output:\n %s' % v)
     if o:
           aeolus_clean = 'aeolus-cleanup -v'
           logging.info('running: %s' % aeolus_clean)
           out = exec_command(aeolus_clean)
           logging.info('output:\n %s' % out)  
           uninstl_aeolus = ' yum -y remove  aeolus-all'
           logging.info('running: %s' % uninstl_aeolus)
           exec_command(uninstl_aeolus) 
     else:
          logging.info('No old verison installed')

#cleanup
def  cleanup_aeolus():
     logging.info('Checking which old aeolus version is installed')
     check_exist = 'rpm -qa | grep aeolus'
     logging.info('running: %s' % check_exist)
     v, o = commands.getstatusoutput(check_exist)
     logging.info('The aeolus version installed:\n %s' % o)
     aeolus_clean = ' aeolus-cleanup'
     logging.info('running: %s' % aeolus_clean)
     exec_command(aeolus_clean)


#Add repo
def addrepo():
    print("adding repo")
    addrepo = ' wget -O /etc/yum.repos.d/fedora-aeolus-testing.repo http://repos.fedorapeople.org/repos/aeolus/conductor/testing/fedora-aeolus-testing.repo' 
    logging.info('running: %s' % addrepo)
    out = exec_command(addrepo)


#Install all the prerequisite aeolus packages
def instpkg():
    instpkg = ' yum -y install aeolus-all'
    logging.info('running: %s' % instpkg)
    exec_command(instpkg)


#aeolus-configure
def aeolus_configure():
    print("running configure")
    ae_conf = ' aeolus-configure'
    logging.info('running: %s' % ae_conf)
    out = exec_command(ae_conf)
    logging.info("wes")
    logging.info('output:\n %s' % out)  
    
    


#run check_services
def check_services():
    #os.chdir('/home/aeolus-script')
    chk_service = '/usr/bin/aeolus-check-services'
    logging.info('running: %s' % chk_service )
    out = exec_command(chk_service)
    logging.info('output:\n %s' % out)   

#Install the required development packages for conductor
def inst_dev_pkg():
    instdevpkg = ' yum -y install classads-devel git rest-devel rpm-build ruby-devel zip '
    logging.info('running: %s' % instdevpkg)
    exec_command(instdevpkg)


#Install the required development packages for iwhd
def inst_dev_pkg_iwhd():
    instdevpkg = ' yum install jansson-devel libmicrohttpd-devel hail-devel gc-devel git gperf mongodb-devel help2man mongodb-server'
    logging.info('running: %s' % instdevpkg)
    exec_command(instdevpkg)
    





component_cond = 'conductor' 
#Clone the Conductor git repository and compile
def pullsrc_compile_conductor(base_dir):
    clone_cond_dir = os.path.join(base_dir,component_cond)
    if os.path.exists(clone_cond_dir):
       logging.info('Removing existing cloned git repo that was detected...')
       shutil.rmtree(clone_cond_dir) 
    logging.info('Cloning the conductor git repositiry')
    #os.makedirs(base_dir)
    os.chdir(base_dir)
    clone = ' git clone git://git.fedorahosted.org/git/aeolus/conductor.git'
    logging.info('running: %s' % clone)
    exec_command(clone)
    if os.path.exists(rpmbuild_dir):
       logging.info('Removing existing rpmbuild dir that was detected...')
       shutil.rmtree(rpmbuild_dir)   
    os.chdir(clone_cond_dir)
    mkrpms = 'make rpms'
    logging.info('running: %s' % mkrpms)
    exec_command(mkrpms)
 

#install conductor from source
def inst_frm_src_conductor():
    logging.info('Installing rpms from src')
    os.chdir(rpmpath)
    rpm_install = ' yum -y localinstall aeolus* --nogpgcheck'  
    logging.info('running: %s' % rpm_install)
    exec_command(rpm_install)
    check_exist = 'rpm -qa | grep aeolus'
    logging.info('running: %s' % check_exist)
    v, o = commands.getstatusoutput(check_exist)
    logging.info('The aeolus version installed:\n %s' % o)





component_oz = 'oz'
#clone the Oz git repository and compile
def pullsrc_compile_Oz(base_dir):
    print('base_dir= '+base_dir)
    clone_Oz_dir = os.path.join(base_dir,component_oz)
    if os.path.exists(clone_Oz_dir):
       logging.info('Removing existing cloned git repo that was detected...')
       shutil.rmtree(clone_Oz_dir)
    logging.info('Cloning the Oz git repositiry')
    os.chdir(base_dir)
    clone = ' git clone git://github.com/clalancette/oz.git'
    logging.info('running: %s' % clone)
    exec_command(clone)
    if os.path.exists(rpmbuild_dir):
       logging.info('Removing existing rpmbuild dir that was detected...')
       shutil.rmtree(rpmbuild_dir)  
    print clone_Oz_dir
    os.chdir(clone_Oz_dir)
    mkrpms = 'make rpm'
    logging.info('running: %s' % mkrpms)
    exec_command(mkrpms)

#pull and build configure 
component_configure = 'configure'
def pullsrc_compile_Configure(base_dir):
    require_rpms ='rubygem-rspec.noarch rpm-build'
    logging.info('installing required rpms '+require_rpms)
    exec_command('yum -y install '+require_rpms)
    clone_Configure_dir = os.path.join(base_dir,component_configure)
    if os.path.exists(clone_Configure_dir):
        logging.info('Removing existing cloned git repo')
        shutil.rmtree(clone_Configure_dir)
    logging.info('Cloning aeolus configure repoistory')
    os.chdir(base_dir)
    clone = 'git clone git://git.fedorahosted.org/aeolus/configure.git'
    logging.info('running: '+ clone)
    exec_command(clone)
    if os.path.exists(rpmbuild_dir):
       logging.info('Removing existing rpmbuild dir that was detected...')
       shutil.rmtree(rpmbuild_dir)  
    print clone_Configure_dir
    os.chdir(clone_Configure_dir)
    mkrpms = 'rake rpms'
    logging.info('running: %s' % mkrpms)
    exec_command(mkrpms)

    
    

#install oz from source
def inst_frm_src_oz():
    check_oz = 'rpm -qa | grep oz'
    logging.info('running: %s' % check_oz)
    v, o = commands.getstatusoutput(check_oz)
    logging.info('The oz version installed before updating:\n %s' % o)
    logging.info('Installing rpms from src')
    os.chdir(rpmpath)
    rpm_install = ' yum -y localinstall oz* --nogpgcheck'
    logging.info('running: %s' % rpm_install)
    exec_command(rpm_install)
    v, o = commands.getstatusoutput(check_oz)
    logging.info('The updated oz version installed:\n %s' % o)




component_factory = 'imagefactory'
#clone the image_factory git repository and compile
def pullsrc_compile_image_factory(base_dir):
    clone_imgfact_dir = os.path.join(base_dir,component_factory)
    if os.path.exists(clone_imgfact_dir):
       logging.info('Removing existing cloned git repo that was detected...')
       shutil.rmtree(clone_imgfact_dir)
    logging.info('Cloning the imagefactory git repositiry')
    os.chdir(base_dir)
    clone = ' git clone https://github.com/aeolusproject/imagefactory'
    logging.info('running: %s' % clone)
    exec_command(clone)
    if os.path.exists(rpmbuild_dir):
       logging.info('Removing existing rpmbuild dir that was detected...')
       shutil.rmtree(rpmbuild_dir) 
    os.chdir(clone_imgfact_dir)
    mkrpms = 'make rpm'
    logging.info('running: %s' % mkrpms)
    exec_command(mkrpms)

#install imagefactory from source
def inst_frm_src_image_factory():
    check_factory = 'rpm -qa | grep imagefactory'
    logging.info('running: %s' % check_factory)
    v, o = commands.getstatusoutput(check_factory)
    logging.info('The imagefactory version installed before updating:\n %s' % o)
    logging.info('Installing rpms from src')
    os.chdir(rpmpath)
    rpm_install = ' yum -y localinstall *noarch.rpm --nogpgcheck'
    logging.info('running: %s' % rpm_install)
    exec_command(rpm_install)
    v, o = commands.getstatusoutput(check_factory)
    logging.info('The updated imagefactory version installed:\n %s' % o)
    logging.info('Restarting Imagefactory  service...')
    chk_status = '/etc/init.d/imagefactory  restart'
    logging.info('running: %s' % chk_status)
    exec_command(chk_status)
  

component_iwhd = 'iwhd'
iwhd_rpmpath = '~/rpmbuild/RPMS/x86_64'
#clone the iwhd git repository and compile
def pullsrc_compile_iwhd(base_dir):
    clone_iwhd_dir = os.path.join(base_dir,component_iwhd) 
    if os.path.exists(clone_iwhd_dir):
       logging.info('Removing existing cloned git repo that was detected...')
       shutil.rmtree(clone_iwhd_dir)
    logging.info('Cloning the iwhd git repositiry')
    os.chdir(base_dir)
    clone = ' git clone git://git.fedorahosted.org/iwhd.git'
    logging.info('running: %s' % clone)
    exec_command(clone)
    if os.path.exists(rpmbuild_dir):
       logging.info('Removing existing rpmbuild dir that was detected...')
       shutil.rmtree(rpmbuild_dir)
        #os.system('rm -rf rpmbuild_dir')
    os.chdir(clone_iwhd_dir)
    btstrap = './bootstrap'
    logging.info('running: %s' % btstrap)
    exec_command(btstrap)
    configure = './configure --quiet'
    logging.info('running: %s' % configure)
    exec_command(configure)
    mkrpms = 'make rpm'
    logging.info('running: %s' % mkrpms)
    exec_command(mkrpms)



#install iwhd from source
def inst_frm_src_iwhd():
    check_iwhd = 'rpm -qa | grep iwhd'
    logging.info('running: %s' % check_iwhd)
    v, o = commands.getstatusoutput(check_iwhd)
    logging.info('The iwhd version installed before updating:\n %s' % o)
    logging.info('Installing rpms from src')
    os.chdir(iwhd_rpmpath)
    rpm_install = ' yum -y localinstall iwhd* --nogpgcheck'
    logging.info('running: %s' % rpm_install)
    exec_command(rpm_install)
    v, o = commands.getstatusoutput(check_iwhd)
    logging.info('The updated iwhd version installed:\n %s' % o)
    logging.info('Restarting mongodb server dependency...')
    chk_status = '/etc/init.d/mongod  restart'
    logging.info('running: %s' % chk_status)
    exec_command(chk_status)
    logging.info('Restarting iwhd  service...')
    chk_status = '/etc/init.d/iwhd  restart'
    logging.info('running: %s' % chk_status)
    exec_command(chk_status)


component_aud = 'audrey'
#clone the audery git repository and compile
def pullsrc_compile_audry(base_dir):
    clone_audrey_dir = os.path.join(base_dir,component_aud)
    config_path = clone_audrey_dir + 'configserver'
    if os.path.exists(clone_audrey_dir):
       logging.info('Removing existing cloned git repo that was detected...')
       shutil.rmtree(clone_audrey_dir)
    logging.info('Cloning the audrey git repositiry')
    os.chdir(base_dir)
    clone = ' git clone git://github.com/clalancette/audrey.git -b config-server'
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
    rpm_install = ' yum -y localinstall aeolus-config* --nogpgcheck'
    logging.info('running: %s' % rpm_install)
    exec_command(rpm_install)

