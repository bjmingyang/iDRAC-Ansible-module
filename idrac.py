#!/usr/bin/env python
#
# (c) 2015 by Hank Beatty
#
# This file is part of the iDRAC Ansible Module (a.k.a. idrac-ansible-module).
#
# iDrac Ansible Module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# iDrac Ansible Module is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License
# along with iDRAC Ansible Module.  If not, see <http://www.gnu.org/licenses/>.
#
# Dell, iDRAC are copyrights of Dell.
#
# Ansible is copyright of Ansible, Inc.

DOCUMENTATION = '''
---
module: idrac
short_description: Module to configure to Dell iDRAC
description:
   - Use this module to configure Dell iDRAC.
version: 0.0.3
options:
   hostname:
      description:
         - The IP address or hostname of the iDRAC to be configured
      default: null
      required: true
      relevant functions: all
   username:
      description:
         - The username to allow commands to be run on the iDRAC
      default: null
      required: true
      relevant functions: all
   password:
      description:
         - The password of the user specified in username
      default: null
      required: true
      relevant functions: all
   command:
      description:
         - The command to be run on the iDRAC. Examples of all the available
           commands have been given in the EXAMPLES section.
      default: null
      required: true
      relevant functions: all
   jobid:
      description:
         - The job ID from the list of IDs in the Job Queue of the iDRAC.
      default: '' or 'JID_CLEARALL'
      required: false
      relevant functions: ___checkJobStatus, ___deleteJobQueue, setupJobQueue
   target_controller:
      description:
         - RAID controller to be queried or modified.
      default: null
      required: false
      relevant functions: ___createVirtualDisk
   physical_disks:
      description:
         - List of physical disks to be configured in a RAID.
      default: null
      required: false
      relevant functions: ___createVirtualDisk
   raid_level:
      description:
         - RAID level to be configured in a RAID.
            RAID 0 = 2
            RAID 1 = 4
            RAID 5 = 64
            RAID 6 = 128
            RAID 10 = 2048
            RAID 50 = 8192
            RAID 60 = 16384
      default: null
      required: false
      relevant functions: ___createVirtualDisk
   span_length:
      description:
         - How many disks the RAID will span. Minimum requirements for given
            RAID Level must be met.
      default: null
      required: false
      relevant functions: ___createVirtualDisk
   virtual_disk_name:
      description:
         - The name of the virtual disk being created.
      default: null
      required: false
      relevant functions: ___createVirtualDisk
   size:
      description:
         - Size in MB of the virtual disk. When not specifed it will use all
            disk space available.
      default: ''
      required: false
      relevant functions: ___createVirtualDisk
   span_depth:
      description:
         - If not specified, default is single span which is used for RAID 0,
            1, 5 and 6. Raid 10, 50 and 60 require a spandepth of at least 2.
      default: ''
      required: false
      relevant functions: ___createVirtualDisk
   stripe_size:
      description:
         - The stripe size of the virtual disk being created.
            16   = 8KB
            32   = 16KB
            64   = 32KB
            128  = 64KB
            256  = 128KB
            512  = 256KB
            1024 = 512KB
            2048 = 1MB
      default: ''
      required: false
      relevant functions: ___createVirtualDisk
   read_policy:
      description:
         - The read policy for the virtual disk being created.
            16  No Read Ahead
            32  Read Ahead
            64  Adaptive Read Ahead
      default: ''
      required: false
      relevant functions: ___createVirtualDisk
   write_policy:
      description:
      default: ''
      required:
      relevant functions:
   disk_cache_policy:
      description:
      default: ''
      required:
      relevant functions:
   share_user:
      description:
         - Username for the share the iDRAC is connecting.
      default: ''
      required: false
      relevant functions: ___bootToNetworkISO, ___exportSystemConfiguration,
         ___installFromURI, ___importSystemConfiguration
   share_pass:
      description:
         - Password for the share the iDRAC is connecting.
      default: ''
      required: false
      relevant functions: ___bootToNetworkISO, ___exportSystemConfiguration,
         ___installFromURI, ___importSystemConfiguration
   share_name:
      description:
         - Share Name for the share the iDRAC is connecting.
      default: ''
      required: false
      relevant functions: ___bootToNetworkISO, ___exportSystemConfiguration,
         ___installFromURI, ___importSystemConfiguration
   workgroup:
      description:
         - Workgroup for the share the iDRAC is connecting.
      default: ''
      required: false
      relevant functions: ___bootToNetworkISO, ___exportSystemConfiguration,
         ___installFromURI, ___importSystemConfiguration
   share_type:
      description:
         - Type of share
      default: 'nfs'
      required: false
      relevant functions: ___bootToNetworkISO, ___exportSystemConfiguration,
         ___installFromURI, ___importSystemConfiguration
   share_ip:
      description:
      default:
      required:
      relevant functions:

requirements:
 - wsmancli
 - dell-wsman-client-api-python
   https://github.com/hbeatty/dell-wsman-client-api-python
author: Hank Beatty
updates: [ 'Steve Malenfant', '' ]
'''

EXAMPLES = '''
These examples assume you are using inventory and group vars. See the Ansible
documentation.

CheckJobStatus

  - name: Check Job Status
    local_action: idrac username={{drac_username}} password={{drac_password}}
      hostname={{drac_hostname}} command="CheckJobStatus" jobid={{ jobid }}
    register: result
    retries: 50
    delay: 15
    until: result.PercentComplete == "100"

GetRemoteServicesAPIStatus returns values for:

  ReturnValue:
    0 = Ready
    1 = Not Ready

  Status:
    0 = Ready
    1 = Not Ready

  LCStatus:
    0 = Ready
    1 = Not Initialized
    2 = Reloading Data
    3 = Disabled
    4 = In Recovery
    5 = In Use

  Server Status:
    0 = Powered Off
    1 = In POST
    2 = Out of POST
    3 = Collecting System Inventory
    4 = Automated Task Execution
    5 = Lifecycle Controller Unified Server Configurator
    7 = Waiting for OS to be installed? Or maybe no available boot media?
        This status wasn't documented in the Dell documentation

  - name: Make sure iDRAC/LC is ready
    local_action: idrac username={{username}} password={{password}}
      hostname={{drac_hostname}} command="GetRemoteServicesAPIStatus"
    register: result
    retries: 20
    delay: 20
    until: result.LCStatus == "0"

Delete all the jobs in the Job Queue

   # To only delete a single job include jobid={{<jobid>}}

  - name: Delete the Job Queue
    local_action: idrac username={{username}} password={{password}}
      hostname={{hostname}} command="DeleteJobQueue"

Clear config from a RAID controller

  - name: Reset RAID Config
    local_action: idrac username={{username}} password={{password}}
      hostname={{hostname}} command="ResetConfig"

  - name: Apply Config
    local_action: idrac username={{username}} password={{password}}
      hostname={{drac_hostname}} command="CreateTargetedConfigJobRAID"

  ## Wait until the iDrac is ready
  - name: Check iDrac status
    local_action: idrac username={{username}} password={{password}}
      hostname={{hostname}} command="GetRemoteServicesAPIStatus"
    register: result
    retries: 20
    delay: 20
    until: result.LCStatus == "0"

  - name: Create RAID1 boot disk
    local_action: idrac username={{username}} password={{password}}
      hostname={{hostname}} command="CreateVirtualDisk"
      virtual_disk_name={{boot_disk_name}} target_controller={{target_RAID}}
      physical_disks={{boot_disks}} raid_level={{boot_RAID_level}}
      span_length={{ boot_span_length }}

  - name: Create Cache Disks
    local_action: idrac username={{username}} password={{password}}
      hostname={{hostname}} command="CreateVirtualDisk"
      virtual_disk_name={{item.name}} target_controller={{target_RAID}}
      physical_disks={{item.physical_disk}} raid_level={{cache_RAID_level}}
      span_length={{cache_span_length}}
    with_items: cache_disks

  - name: Apply Config
    local_action: idrac username={{username}} password={{password}}
      hostname={{hostname}} command="CreateTargetedConfigJobRAID"

  - name: Waiting until server is ready
    local_action: idrac username={{username}} password={{password}}
      hostname={{hostname}} command="CheckJobStatus" jobid={{jobid}}
    register: result
    retries: 50
    delay: 15
    until: result.PercentComplete == "100"

Install OS from network share

  - name: Install OS
    local_action: idrac username={{username}} password={{password}}
      hostname={{hostname}} command="BootToNetworkISO" share_user={{share_user}}
      share_pass={{share_pass}} share_name={{share_name}}
      share_type={{share_type}} share_ip={{share_ip}} workgroup={{workgroup}}
      iso_image={{iso_image}}

'''

import sys
import json
import os
import os.path
import datetime
import time
import re # regular expressions
import tempfile
import string
import random
import logging

from distutils.version import LooseVersion, StrictVersion

try:
   import xml.etree.cElementTree as ET
except ImportError:
   import xml.etree.ElementTree as ET

try:
   from wsman import WSMan
   from wsman.provider.remote import Remote
   from wsman.transport.process import Subprocess
   from wsman.response.reference import Reference
   from wsman.response.fault import Fault
   from wsman.format.command import OutputFormatter
   from wsman.loghandlers.HTMLHandler import HTMLHandler

   HAS_WSMAN = True
except ImportError:
   HAS_WSMAN = False


class switch(object):
   def __init__(self, value):
      self.value = value
      self.fall = False

   def __iter__(self):
      """Return the match method once, then stop"""
      yield self.match
      raise StopIteration

   def match(self, *args):
      """Indicate whether or not to enter a case suite"""
      if self.fall or not args:
         return True
      elif self.value in args: # changed for v1.5, see below
         self.fall = True
         return True
      else:
         return False

debug = False
check_mode = False
fmt = ''
fHandle = ''
html = ''
log = ''
wsman = ''

# Boot to a network ISO image. Reboot appears to be immediate.
#
# remote:
#    - ip, username, password passed to Remote() of WSMan
# share_user: username for the share
#    - default: ''
# share_pass: password for the share
#    - default: ''
# share_name: name of the share
#    - default: ''
# share_type: Type of share
#    - default: 'nfs'
#    - possible values: nfs, smb, samba, cifs, 0, 2
# workgroup: Workgroup for the share
#    - default: ''
# iso_image: Path to ISO image relative to the share
#    - default: ''
#
def bootToNetworkISO(remote,share_info,iso_image):
   msg = { 'ansible_facts': {} }
   properties = {};

   # wsman invoke -a BootToNetworkISO \
   # http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_OSDeploymentService?CreationClassName=DCIM_OSDeploymentService&Name=DCIM:OSDeploymentService&SystemCreationClassName=DCIM_ComputerSystem&SystemName=DCIM:ComputerSystem \
   # -k IPAddress="<share_ip>" -k ImageName="<iso image>" -k Password="<pass>" \
   # -k ShareName="/homes" -k ShareType="2" -k Username="<user>" -k \
   # Workgroup="WORKGROUP" -h <host> -P 443 -u <idrac-user> -p <idrac-pass> -V \
   # -v -c dummy.cert -j utf-8 -y basic

   r = Reference("DCIM_OSDeploymentService")

   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_OSDeploymentService")

   r.set("CreationClassName","DCIM_OSDeploymentService")
   r.set("Name","DCIM:OSDeploymentService")
   r.set("SystemCreationClassName","DCIM_ComputerSystem")
   r.set("SystemName","DCIM:ComputerSystem")

   properties['Username'] = share_info['user']
   properties['Password'] = share_info['pass']
   properties['ShareName'] = share_info['name']
   if ((share_info['type'] == 'samba') or (share_info['type'] == 'cifs')
      or (share_info['type'] == 'smb')):
      share_info['type'] = '2'
   elif share_info['type'] == 'nfs':
      share_info['type'] = '0'
   properties['ShareType'] = share_info['type']
   properties['IPAddress'] = share_info['ip']
   if share_info['workgroup'] != '':
      properties['Workgroup'] = share_info['workgroup']
   properties['ImageName'] = iso_image

   res = wsman.invoke(r, 'BootToNetworkISO', properties, remote)
   if type(res) is Fault:
      #print 'There was an error!'
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res,msg)

   if msg['failed']:
      msg['changed'] = False
   else:
      msg['changed'] = True

   return msg

# Checks the job Status of the given Job ID.
#
def checkJobStatus (remote,jobid):

   msg = ___checkJobStatus(remote,jobid)

   # return the jobid so that we can check it again.
   msg['jobid'] = jobid
   #if hasattr(msg, 'JobStatus') == False:
   #   msg['JobStatus'] = 'Downloading'
   msg['changed'] = False
   return msg

# Checks to see if the iDRAC/LC and server are ready to accept commands.
#
# Steve doesn't want the serverStatus to returned failed
def checkReadyState(remote):
   msg = {}
   msg['msg'] = ''
   msg['failed'] = False

   res = ___getRemoteServicesAPIStatus(remote)
   if res['failed']:
      return res
   else:
      msg['LCStatusString'] = res['LCStatusString']
      msg['LCStatus'] = res['LCStatus']
      msg['StatusString'] = res['StatusString']
      msg['Status'] = res['Status']
      msg['ServerStatusString'] = res['ServerStatusString']
      msg['ServerStatus'] = res['ServerStatus']

      if res['Status'] != '0':
         msg['msg'] = "Overall Status of server is not ready"
         msg['failed'] = True

      if res['LCStatus'] != '0':

         if msg['failed']:
            msg['msg'] = msg['msg']+" and Lifecycle Controller is not ready"
         else:
            msg['msg'] = "Lifecycle Controller is not ready"
            msg['failed'] = True


      #if ((res['ServerStatus'] != '0') and (res['ServerStatus'] != '2')):
      #   if msg['failed']:
      #      msg['msg'] = msg['msg']+" and Server is not ready"
      #      msg['ServerStatusString'] = res['ServerStatusString']
      #   else:
      #      msg['msg'] = "Server is not ready"
      #      msg['failed'] = False
      #      msg['ServerStatusString'] = res['ServerStatusString']

   if not msg['failed']:
      msg['msg'] = "iDRAC is ready. Who knows if the server is because we "
      msg['msg'] = msg['msg']+"didn't check."

   msg['changed'] = False
   return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
# reboot_type:
#    - 1 = PowerCycle
#    - 2 = Graceful Reboot without forced shutdown
#    - 3 = Graceful reboot with forced shutdown
def createRebootJob (remote,hostname,reboot_type):
   msg = { }

   msg = ___createRebootJob(remote,hostname,reboot_type)

   if msg['failed']:
      msg['changed'] = False
   else:
      msg['changed'] = True

   return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
#
def createTargetedConfigJobRAID(remote,hostname,remove_xml,reboot_type):
   # TODO ansible_facts doesn't need to be here
   msg = { 'ansible_facts': { } }

   # wsman invoke -a CreateTargetedConfigJob http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_RAIDService?SystemCreationClassName=DCIM_ComputerSystem,CreationClassName=DCIM_RAIDService,SystemName=DCIM:ComputerSystem,Name=DCIM:RAIDService -h $IPADDRESS -V -v -c dummy.cert -P 443 -u $USERNAME -p $PASSWORD -J CreateTargetedConfigJob_RAID.xml -j utf-8 -y basic
   r = Reference("DCIM_RAIDService")

   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_RAIDService")

   r.set("SystemCreationClassName","DCIM_ComputerSystem")
   r.set("CreationClassName","DCIM_RAIDService")
   r.set("SystemName","DCIM:ComputerSystem")
   r.set("Name","DCIM:RAIDService")

   # ddddddddhhmmss.mmmmmm
   future = "00000000001000.000000"

   sffx = "_"+hostname+"_CreateTargetedConfigJobRAID.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:CreateTargetedConfigJob_INPUT xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_RAIDService">\n')
   fh.write('<p:Target>RAID.Integrated.1-1</p:Target>\n') # TODO should be var
   fh.write('<p:RebootJobType>'+reboot_type+'</p:RebootJobType>\n')
   # TODO schedule
   fh.write('<p:ScheduledStartTime>TIME_NOW</p:ScheduledStartTime>\n')
   # TODO fixme: try until this time
   #fh.write('<p:UntilTime>'+future+'</p:UntilTime>\n')
   fh.write('</p:CreateTargetedConfigJob_INPUT>\n')

   fh.close()

   res = wsman.invoke(r, "CreateTargetedConfigJob", fh.name, remote, False)
   if remove_xml:
      os.remove(fh.name)
   if type(res) is Fault:
      #print 'There was an error!'
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res, msg)

   return msg

# wsman:
#    - provided by module
# remote:
#    - ip, username, password passed to Remote() of WSMan
# jobid:
#    - default: JID_CLEARALL
#
# wsman invoke -a DeleteJobQueue \
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_JobService?SystemCreationClassName=DCIM_ComputerSystem&CreationClassName=DCIM_JobService&SystemName=Idrac&Name=JobService \
# -h <hostname> -V -v -c dummy.cert -P 443 -u <username> -p <password> \
# -k JobID="<jobid>" -j utf-8 -y basic
#
def deleteJobQueue(remote,jobid):
   msg = {}
   properties = {}
   properties['JobID'] = jobid

   # Check the Job Queue to make sure there are no pending jobs
   res = ___listJobs(remote,'',{})
   for k in res:
      if (k == 'JID_CLEARALL') and (res[k]['JobStatus'] == 'Pending'):
         continue
      if (hasattr(res[k], 'JobStatus')) and (res[k]['JobStatus'] == 'Pending'):
         msg['failed'] = True
         msg['changed'] = False
         msg['msg'] = 'Could not complete because there are pending Jobs.'
         msg['msg'] = msg['msg']+' Pending Job: '+k+'. Please clear the Job'
         msg['msg'] = msg['msg']+' Queue and reset the iDRAC.'
         return msg

   r = Reference("DCIM_JobService")

   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_JobService")

   r.set("SystemCreationClassName","DCIM_ComputerSystem")
   r.set("CreationClassName","DCIM_JobService")
   r.set("SystemName","Idrac")
   r.set("Name","JobService")

   res = wsman.invoke(r, 'DeleteJobQueue', properties, remote)
   if type(res) is Fault:
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res, msg)

   return msg

# wsman invoke -a DetachISOImage \
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_OSDeploymentService?CreationClassName=DCIM_OSDeploymentService&Name=DCIM:OSDeploymentService&SystemCreationClassName=DCIM_ComputerSystem&SystemName=DCIM:ComputerSystem" \
# -u <username> -p <password> -h <hostname> -V -v -c dummy.cert -P 443 \
# -j utf-8 -y basic
#
def detachISOImage(remote):

   if check_mode:
      msg['check_mode'] = "Running in check mode."
      msg['msg'] = "Would have attempted detach of ISO image"
      msg['changed'] = False
      msg['failed'] = False
      return msg

   r = Reference("DCIM_JobService")

   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_OSDeploymentService")

   r.set("SystemCreationClassName","DCIM_ComputerSystem")
   r.set("CreationClassName","DCIM_OSDeploymentService")
   r.set("SystemName","DCIM:ComputerSystem")
   r.set("Name","DCIM:OSDeploymentService")

   res = wsman.invoke(r, 'DetachISOImage', '', remote)
   if type(res) is Fault:
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res)

   if msg['failed']:
      msg['changed'] = False
   else:
      msg['changed'] = True

   return msg

def detachSDCardPartitions(remote,hostname):
   msg = {}

   # Get SD Card Partitions
   res = ___listSDCardPartitions(remote)
   if res['failed']:
      return res

   found = 0
   # TODO need to keep track of the ones that were successfully detached and the
   # ones that failed
   for k in res:
      # this k != 'failed' is needed! failed is True or False and python blows
      # up if you try to iterate a bool object!
      if k != 'failed': 
         for l in res[k]:
            if debug:
               print k+": "+l+": "+res[k][l]

            if ((l == 'AttachedState') and (res[k][l] == 'Attach')):
               found = 1
               if debug:
                  print "found a match"
                  msg['msg'] = "Would have detached at lease one SD Partition."
               if not check_mode:
                  result = ___detachSDCardPartition(remote,hostname,k)
                  if result['failed']:
                     msg['msg'] = "Could not detach partition: "+k+" Named: "+res[k]['Name']
                     msg['changed'] = False
                     msg['failed'] = True
                     return msg

                  # Waits 3 minutes or until the download completes
                  for x in range(1, 90):
                     jobStatus_res = ___checkJobStatus(remote,result['jobid'])
                     if jobStatus_res['JobStatus'] == 'Completed':
                        break
                     if jobStatus_res['JobStatus'] == 'Failed':
                        break

                     time.sleep(2)

                  if debug:
                     print "JobStatus in detachSDCardPartitions(): "+jobStatus_res['JobStatus']
                  if jobStatus_res['JobStatus'] != 'Completed':
                     msg['msg'] = "Could not detach partition: "+k+" Named: "+res[k]['Name']
                     msg['changed'] = False
                     msg['failed'] = True
                     return msg

   if check_mode:
      msg['check_mode'] = "Running in check mode."

   if found and check_mode:
      msg['changed'] = False
      msg['msg'] = "Found some partitions to detach but, none detached."
   elif found:
      msg['changed'] = True
      msg['msg'] = "All partitions have been detached."
   else:
      msg['changed'] = False
      msg['msg'] = "No partitions found to detach."
   msg['failed'] = False
   return msg

#
def enumerateEventFilters(remote):
   msg = { 'msg': {} }

   res = ___enumerateEventFilters(remote)
   if res['failed']:
      msg['failed'] = True
      msg['changed'] = False
      return msg

   for k in res:
      # this k != 'failed' is needed! failed is True or False and python blows
      # up if you try to iterate a bool object!
      if k != 'failed':
         msg['msg'][k] = res[k]

   msg['changed'] = False
   return msg

# Puts the return values from ___enumerateSoftwareIdentity() into ansible_facts
# 
def enumerateSoftwareIdentity(remote):
   msg = { 'ansible_facts': { 'software_identity': {} } }

   res = ___enumerateSoftwareIdentity(remote)
   if res['failed']:
      res['changed'] = False
      return res

   for k in res:
      # this k != 'failed' is needed! failed is True or False and python blows
      # up if you try to iterate a bool object!
      if k != 'failed':
         msg['ansible_facts']['software_identity'][k] = res[k]

   if debug:
      tmp = json.dumps(msg, indent=3, separators=(',', ': '))
      log.debug(tmp)

   msg['changed'] = False
   msg['failed'] = False
   return msg

# This function does not modify the iDRAC. The iDRAC deletes the file from the
# share before putting it back.
#
# remote:
#    - ip, username, password passed to Remote() of WSMan
# share_user:
# share_pass:
# share_name:
# share_type:
#    - default: 'nfs'
#    - possible values: nfs, smb, samba, cifs
# share_ip:
# workgroup:
# local_path:
#    - default: "/tmp"
#
def exportSystemConfiguration(remote,share_info,hostname,local_path,
                                 remove_xml=True):

   ret = { 'ansible_facts': {} }
   ret['failed'] = False

   # TODO use ___checkShareInfo()
   if share_info['user'] == '':
      ret['failed'] = True
      ret['msg'] = "share_user must be defined"
   if share_info['pass'] == '':
      ret['failed'] = True
      ret['msg'] = "share_pass must be defined"
   if share_info['name'] == '':
      ret['failed'] = True
      ret['msg'] = "share_name must be defined"
   if share_info['type'] == '':
      ret['failed'] = True
      ret['msg'] = "share_type must be defined"
   if share_info['ip'] == '':
      ret['failed'] = True
      ret['msg'] = "share_ip must be defined"

   if ret['failed'] == True:
      return ret

   if (share_info['type'] == 'samba') or (share_info['type'] == 'cifs') or (share_info['type'] == 'smb'):
      share_info['type'] = '2'
   elif share_info['type'] == 'nfs':
      share_info['type'] = '0'
   else:
      ret['failed'] = True
      ret['msg'] = 'share_type not recognized.'

   # wsman invoke -a ExportSystemConfiguration http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService?SystemCreationClassName=DCIM_ComputerSystem,CreationClassName=DCIM_LCService,SystemName=DCIM:ComputerSystem,Name=DCIM:LCService -h $IPADDRESS -V -v -c dummy.cert -P 443 -u $USERNAME -p $PASSWORD -j utf-8 -y basic
   ref = Reference("DCIM_LCService")

   ref.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService")

   ref.set("SystemCreationClassName","DCIM_ComputerSystem")
   ref.set("CreationClassName","DCIM_LCService")
   ref.set("SystemName","DCIM:ComputerSystem")
   ref.set("Name","DCIM:LCService")

   sffx = "_"+hostname+"_ExportSystemConfiguration.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:ExportSystemConfiguration_INPUT ')
   fh.write('xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService">\n')
   fh.write('   <p:IPAddress>'+share_info['ip']+'</p:IPAddress>\n')
   fh.write('   <p:ShareName>'+share_info['name']+'</p:ShareName>\n')
   fh.write('   <p:FileName>'+hostname+'SystemConfig.xml</p:FileName>\n')
   fh.write('   <p:ShareType>'+share_info['type']+'</p:ShareType>\n')
   fh.write('   <p:Username>'+share_info['user']+'</p:Username>\n')
   fh.write('   <p:Password>'+share_info['pass']+'</p:Password>\n')
   if share_info['workgroup'] != '':
      fh.write('   <p:Workgroup>'+share_info['workgroup']+'</p:Workgroup>')
   fh.write('</p:ExportSystemConfiguration_INPUT>\n')

   fh.close()

   res = wsman.invoke(ref, 'ExportSystemConfiguration', fh.name, remote)
   if remove_xml:
      os.remove(fh.name)
   if type(res) is Fault:
      ret['failed'] = True
      ret['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return ret

   ret = ___checkReturnValues(res, ret)

   if ret['failed']:
      ret['changed'] = False
      return ret

   # TODO instead of looping use checkJobStatus for completion.  Will also give
   # better return.

   # if everything checks out up to this point we should get the system
   # configuration in the local path. It takes a moment for the iDRAC
   # to send it. We'll loop for 10 tries with a 3 second pause

   if re.match('~', local_path):
      #print "matched ~"
      home_dir = os.path.expanduser("~")
      sys_config_file = hostname+'SystemConfig.xml'
      sys_config_file = os.path.join(home_dir, sys_config_file)
   elif re.search('/$', local_path):
      #print "matched trailing /"
      sys_config_file = local_path+hostname+'SystemConfig.xml'
   else:
      #print "no trailing /"
      sys_config_file = local_path+'/'+hostname+'SystemConfig.xml'

   cnt = 0
   test = os.path.isfile(sys_config_file)
   while test is False:
      test = os.path.isfile(sys_config_file)
      cnt += 1
      if cnt == 15:
         ret['failed'] = True
         ret['msg'] = 'Could not find file: '+sys_config_file
         return ret
      time.sleep(5)

   fh_in = open(sys_config_file, 'r')
   filedata = fh_in.read()
   fh_in.close()

   # TODO leave the comments in and add this to the elem2json() as comments

   #filedata = filedata.replace('<!-- ', '')
   #filedata = filedata.replace(' -->', '')
   #filedata = filedata.replace('\n-->\n', '\n')
   #filedata = filedata.replace('\n', '')

   fh_out = open(sys_config_file, 'w')
   fh_out.write(filedata)
   fh_out.close()

   #print filedata

   sys_config = ET.parse(sys_config_file)
   #print type(sys_config)
   # I'm not happy with this but, it was the only thing I could find to test
   # if the xml parse worked
   if sys_config is None:
      ret['failed'] = True
      ret['msg'] = sys_config_file+' is not XML?'
      return ret
   #os.remove(sys_config_file)

   sys_config = ___elem2json(sys_config)

   ret[hostname] = sys_config

   #iter_ = sys_config.getiterator()
   #for elem in iter_:
   #   print elem.tag, elem.attrib

   #sys_config.write(sys.stdout)

   ret['changed'] = False
   return ret

# This is just a wrapper function. Will be removed once no playbooks are calling
# it directly.
#
def getRemoteServicesAPIStatus (remote):

   msg = ___getRemoteServicesAPIStatus(remote)

   msg['changed'] = False
   return msg

def getSystemInventory(remote):

   msg = { 'ansible_facts': {} }

   # wsman enumerate \
   # "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_SystemView" \
   #  -h <hostname> -V -v -c dummy.cert -P 443 -u <user> -p <pass> -j utf-8 \
   #  -y basic
   r = Reference("DCIM_SystemView")
   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_SystemView")
   res = wsman.enumerate(r, 'root/dcim', remote)
   if type(res) is Fault:
      #print 'There was an error!'
      msg['failed'] = True
      msg['result'] = "no system inventory"
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   for instance in res:
      tmp = ''
      for k,v in instance.items:
         tmp = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
         if re.match('Model', k) != None:
            print "matched Model"
            tmp = tmp.replace(" ", "_")
         if debug:
            print "key: "+k+" value: "+tmp
         msg['ansible_facts'][k] = tmp

   msg['changed'] = False
   msg['failed'] = False
   msg['msg'] = 'System Inventory success.'
   return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
# share_info:
#    - share_user, share_pass, share_name, share_type, share_ip
# hostname:
#    - This is used to make the generated XML file unique
# import_file:
#    import_file is relative to the share
# remove_xml:
#    - boolean: True or False
#    - default: True
#       Removes the generated XML file
#
def importSystemConfiguration(remote,share_info,hostname,import_file,
                              remove_xml):
   # wsman invoke -a ImportSystemConfiguration 
   # "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService?SystemCreationClassName=DCIM_ComputerSystem&CreationClassName=DCIM_LCService&SystemName=DCIM:ComputerSystem&Name=DCIM:LCService"
   # -h <hostname> -V -v -c dummy.cert -P 443 -u <username> -p <password>
   # -J ImportSystemConfiguration.xml -j utf-8 -y basic

   msg = { 'ansible_facts': { } }
   msg['failed'] = False

   msg = ___checkShareInfo(share_info)
   if msg['failed']:
      return msg

   if import_file == '':
      msg['failed'] = True
      msg['msg'] = "import_file must be defined"

   if msg['failed']:
      return msg

   if (share_info['type'] == 'samba') or (share_info['type'] == 'cifs') or (share_info['type'] == 'smb'):
      share_info['type'] = '2'
   elif share_info['type'] == 'nfs':
      share_info['type'] = '0'

   ref = Reference("DCIM_LCService")

   ref.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService")

   ref.set("SystemCreationClassName","DCIM_ComputerSystem")
   ref.set("CreationClassName","DCIM_LCService")
   ref.set("SystemName","DCIM:ComputerSystem")
   ref.set("Name","DCIM:LCService")

   sffx = "_"+hostname+"_ImportSystemConfiguration.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:ImportSystemConfiguration_INPUT ')
   fh.write('xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService">\n')
   fh.write('<p:IPAddress>'+share_info['ip']+'</p:IPAddress>\n')
   fh.write('<p:ShareName>'+share_info['name']+'</p:ShareName>\n')
   fh.write('<p:FileName>'+import_file+'</p:FileName>\n')
   fh.write('<p:ShareType>'+share_info['type']+'</p:ShareType>\n')
   fh.write('<p:Username>'+share_info['user']+'</p:Username>\n')
   fh.write('<p:Password>'+share_info['pass']+'</p:Password>\n')
   fh.write('</p:ImportSystemConfiguration_INPUT>\n')

   fh.close()

   res = wsman.invoke(ref, 'ImportSystemConfiguration', fh.name, remote)
   if remove_xml:
      os.remove(fh.name)
   if type(res) is Fault:
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res, msg)

   if msg['failed']:
      msg['changed'] = False
   else:
      msg['changed'] = True

   return msg

# Install iDRAC Firmware
# Checks current installed version, compares to version
# that is being installed and if different performs an install.
#
# The iDRAC firmware is unique in that it causes an automatic reboot of the
# iDRAC. The scheduleFirmwareInstall() will not perform an iDRAC install.
#
def installIdracFirmware(remote,firmware):
   msg = { }

   if not firmware:
      msg['changed'] = False
      msg['failed'] = True
      msg['msg'] = "firmware must be defined."
      return msg

   if debug:
      for k in firmware:
         log.debug ("firmware key: %s value: %s",k,firmware[k])

   if 'share_uri' in firmware:
      uri = firmware['share_uri']
   else:
      uri = firmware['url']

   if debug:
      log.debug("uri: %s",uri)

   # Check the Job Queue to make sure there are no pending jobs
   res = ___listJobs(remote,'',{})
   #print "___listJobs"
   if res['failed']:
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = 'iDRAC not accepting commands. wsman returned: '+res['msg']
      return msg

   for k in res:
      #print k+": "+str(res[k])
      if (k == 'JID_CLEARALL') and (res[k]['JobStatus'] == 'Pending'):
         continue
      if (hasattr(res[k], 'JobStatus')) and (res[k]['JobStatus'] == 'Pending'):
         msg['failed'] = True
         msg['changed'] = False
         msg['msg'] = 'Could not complete because there are pending Jobs.'
         msg['msg'] = msg['msg']+' Pending Job: '+k+'. Please clear the Job'
         msg['msg'] = msg['msg']+' Queue and reset the iDRAC.'
         return msg

   # Check to make sure the iDRAC is ready to accept commands
   res = ___getRemoteServicesAPIStatus(remote)
   for k in res:
      #print "key: "+k+" value: "+str(res[k])
      if (res['LCStatus'] != '0') and (res['Status'] != '0'):
         msg['failed'] = True
         msg['changed'] = False
         msg['msg'] = 'iDRAC is not ready. Please check the iDRAC. It may need to be reset.'
         return msg

   res = ___enumerateSoftwareIdentity(remote)
   if debug:
      #print "Calling ___enumerateSoftwareIdentity() from upgradeIdrac()"
      log.debug("Calling ___enumerateSoftwareIdentity() from upgradeIdrac()")
   if res['failed']:
      return res

   # check to see if version trying to be installed is the same
   for k in res:
      #print k
      if re.search('iDRAC', k):
         if res[k]['Status'] == 'Installed':
            cur_version = res[k]['VersionString']
            instanceID = k

   new_version = firmware['target_version']

   if LooseVersion(new_version) != LooseVersion(cur_version):
      msg = ___installFromURI(remote,uri,instanceID)
      if msg['failed']:
         msg['changed'] = False
         return msg

      # Waits 3 minutes or until the download completes
      wait_time = 60 * 3
      end_time = time.clock() + wait_time
      while time.clock() < end_time:
         res = ___checkJobStatus(remote,msg['jobid'])
         if res['JobStatus'] == 'Completed':
            break
         if res['JobStatus'] == 'Failed':
            break

         time.sleep(2)

      if res['JobStatus'] != 'Completed':
         msg['failed'] = True
         msg['changed'] = True
         msg['idrac_msg'] = res['Message']
         msg['msg'] = 'Download started but, not completed.'
         return msg

      # Once the download is complete the iDRAC will install the firmware
      # automatically. Wait until the iDRAC is ready again

      # Waits 15 minutes or until the iDRAC is ready
      wait_time = 60 * 15
      end_time = time.clock() + wait_time
      while time.clock() < end_time:
         res = ___getRemoteServicesAPIStatus(remote)
         if re.search('Internal Server Error', res['msg']) != None:
            continue

         if (res['LCStatus'] == '0') and (res['Status'] == '0'):
            break

         time.sleep(10)

      if (res['LCStatus'] != '0') and (res['Status'] != '0'):
         msg['failed'] = True
         msg['changed'] = True
         msg['msg'] = 'Timeout during upgrade. Verify iDrac.'
      else:
         msg['failed'] = False
         msg['changed'] = True
         msg['msg'] = 'iDRAC firmware upgrade successfully completed.'

   elif LooseVersion(new_version) == LooseVersion(cur_version):
      msg['msg'] = "Installed version "+cur_version+" same as version to be"
      msg['msg'] = msg['msg']+" installed."
      msg['failed'] = False
      msg['changed'] = False
   else:
      msg['msg'] = "Was unable to compare versions. Installed version: "
      msg['msg'] = msg['msg']+cur_version+". New version: "+new_version
      msg['failed'] = True
      msg['changed'] = False

   msg['ansible_facts'] = {}
   msg['ansible_facts']['LifecycleControllerVersion'] = new_version

   return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
# hostname:
#    - This is used to make the generated XML file unique
# user_to_change:
#    - the username that we are changing the password for
# new_pass:
#    - the new password
#
def resetPassword(remote,hostname,user_to_change,new_pass):
   msg = {}

   if not user_to_change:
      msg['failed'] = True
      msg['msg'] = 'user_to_change must be defined'
      return msg

   if not new_pass:
      msg['failed'] = True
      msg['msg'] = 'new_pass must be defined'
      return msg

   #print new_pass

   res = ___enumerateIdracCardString(remote)
   if res['failed']:
      return res

   # TODO Could make this loop slightly faster if went directly to the users
   # instead of looping thru the whole dictionary
   found = 0
   for k in res:
      #print k
      if k != 'failed':
         # used for debugging
         #for l in res[k]:
         #   print k+": "+l+": "+res[k][l]

         tmp = k.split("#")
         if tmp[2] == 'UserName':
            if re.match('^'+res[k]['CurrentValue']+'$', user_to_change):
               #print "found a match"
               found = 1
               target = tmp[0]
               #print 'target: '+target
               attribute_name = tmp[1]+'#Password'
               attributes = {}
               attributes[attribute_name] = new_pass
               result = ___applyAttributes(remote,target,attributes)
               if result['failed']:
                  return result

   if not found:
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = 'Could not find user'
      return msg

   msg['failed'] = False
   msg['changed'] = True
   msg['msg'] = 'Password has been changed.'
   return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
#
def resetRAIDConfig(remote,hostname,remove_xml):
   msg = {}

   # wsman invoke -a ResetConfig http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_RAIDService?SystemCreationClassName=DCIM_ComputerSystem&CreationClassName=DCIM_RAIDService&SystemName=DCIM:ComputerSystem&Name=DCIM:RAIDService -h 10.22.252.15 -V -v -c Dummy -P 443 -u root -p <password> -J /tmp/resetConfig.xml -j utf-8 -y basic
   # wsman invoke " http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_RAIDService?CreationClassName="DCIM_RAIDService"&SystemName="DCIM:ComputerSystem"&Name="DCIM:RAIDService"&SystemCreationClassName="DCIM_ComputerSystem"" -a "ResetConfig" -u <username> -p <password> -h <hostname> -P 443 -j utf-8 -y basic -V -v -c Dummy --input="/tmp/resetConfig.xml"
   r = Reference("DCIM_RAIDService")

   r.set_resource_uri('http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_RAIDService')

   r.set("SystemCreationClassName","DCIM_ComputerSystem")
   r.set("CreationClassName","DCIM_RAIDService")
   r.set("SystemName","DCIM:ComputerSystem")
   r.set("Name","DCIM:RAIDService")

   sffx = "_"+hostname+"_resetRAIDConfig.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:ResetConfig_INPUT xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_RAIDService">')
   fh.write('<p:Target>RAID.Integrated.1-1</p:Target>') # TODO: this needs to be a var
   fh.write('</p:ResetConfig_INPUT>')

   fh.close()

   res = wsman.invoke(r, 'ResetConfig', fh.name, remote)
   if remove_xml:
      os.remove(fh.name)
   if type(res) is Fault:
      #print 'There was an error!'
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res, msg)

   if msg['failed']:
      msg['changed'] = False
   else:
      msg['changed'] = True

   return msg

# Schedule Firmware Install
#
# Will not install iDRAC firmware. If you want to up/downgrade the iDRAC use
# installIdracFirmware()
# 
# Returns the jobid of ___installFromURI() which can then be passed to 
# setupJobQueue() with the rebootid returned from ___createRebootJob()
#
def scheduleFirmwareInstall(remote,firmware):
   msg = { 'ansible_facts': { } }
   msg['failed'] = False

   if debug:
      #print "scheduleFirmwareUpdate() Calling ___checkShareInfo()"
      log.debug("scheduleFirmwareUpdate() Calling ___checkShareInfo()")

   if not firmware:
      msg['changed'] = False
      msg['failed'] = True
      msg['msg'] = "firmware must be defined."
      return msg

   if instanceID == '':
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = "instanceID must be defined."
      return msg
   elif debug:
      print "scheduleFirmwareUpdate() instanceID: "+instanceID

   if check_mode:
      # TODO maybe put in what type of firmware.
      msg['msg'] = "Firmware update would have been attempted."
      msg['changed'] = True
      msg['failed'] = False
      return msg

   # Check the Job Queue to make sure there are no pending jobs
   if debug:
      log.debug( "scheduleFirmwareUpdate() calling ___listJobs()")
   res = ___listJobs(remote,'',{})
   if res['failed']:
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = 'iDRAC not accepting commands. wsman returned: '+res['msg']
      return msg

   for k in res:
      #print k+": "+str(res[k])
      if (k == 'JID_CLEARALL') and (res[k]['JobStatus'] == 'Pending'):
         if debug:
            print "scheduleFirmwareUpdate() this server has a JID_CLEARALL pending"
         continue
      if (hasattr(res[k], 'JobStatus')) and (res[k]['JobStatus'] == 'Pending'):
         if debug:
            print "scheduleFirmwareUpdate() this server has a job pending"
         msg['failed'] = True
         msg['changed'] = False
         msg['msg'] = "Could not complete because there are pending Jobs."
         msg['msg'] = msg['msg']+" Pending Job: "+k+". Please clear the Job"
         msg['msg'] = msg['msg']+" Queue and reset the iDRAC."
         return msg
   #### End of Checking Job Queue

   # Check to make sure the iDRAC is ready to accept commands
   if debug:
      print "scheduleFirmwareUpdate() calling ___getRemoteServicesAPIStatus()"
   res = ___getRemoteServicesAPIStatus(remote)
   for k in res:
      #print "key: "+k+" value: "+str(res[k])
      if (res['LCStatus'] != '0') and (res['Status'] != '0'):
         if debug:
            print "scheduleFirmwareUpdate() finished ___getRemoteServicesAPIStatus and iDRAC isn't ready"
         msg['failed'] = True
         msg['changed'] = True
         msg['msg'] = "iDRAC is not ready. Please check the iDRAC. It may need to be reset."
         return msg
   #### End of checking for iDRAC is ready

   if debug:
      print "scheduleFirmwareUpdate() calling ___installFromURI()"
   installURI_res = ___installFromURI(remote,uri,firmware,instanceID)
   if installURI_res['failed']:
      msg['failed'] = True
      msg['changed'] = True
      msg['idrac_msg'] = installURI_res['Message']
      msg['msg'] = "Download started but, not completed."

   if not msg['failed']:
      msg['ansible_facts']['jobid'] = installURI_res['jobid']

      # Waits 3 minutes or until the download completes
      if debug:
         print "scheduleFirmwareUpdate() checking JobStatus"
      for x in range(1, 90):
         res = ___checkJobStatus(remote,installURI_res['jobid'])
         if res['JobStatus'] == 'Downloaded':
            break
         if res['JobStatus'] == 'Failed':
            break
   
         time.sleep(2)
   
      if res['JobStatus'] != 'Downloaded':
         msg['failed'] = True
         msg['changed'] = True
         msg['idrac_msg'] = res['Message']
         msg['msg'] = "Download started but, not completed."

   if msg['failed']:
      return msg
   else:
      msg['changed'] = True
      msg['failed'] = False
      msg['msg'] = "Succesfully scheduled firmware update."
      return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
#
# check_mode is working
#def setEventFilters(remote,enable_event,enable_service,disable_event,disable_service):
def setEventFiltersByInstanceIDs(remote):
   msg = { 'msg': {} }
   msg['changed'] = False
   targets = {}
   event_instances = {}

   res = ___enumerateEventFilters(remote)
   if res['failed']:
      res['changed'] = False
      return res

   for k in res:
      if k != "failed":
         print "key: ",k
         #msg['msg'].update(res[k])
         # check to see if this alert supports "Remote System Log"
         if "Remote System Log" in res[k]['PossibleNotificationDescriptions']:
            #print "index: ", res[k]['PossibleNotificationDescriptions'].index('Remote System Log')
            idx = res[k]['PossibleNotificationDescriptions'].index('Remote System Log')
            #print "PossibleNotifications: ",res[k]['PossibleNotifications'][idx]
            rsyslog_dec = res[k]['PossibleNotifications'][idx]
            if rsyslog_dec not in res[k]['Notification']:
               # add it to res because we are going to change it and return res
               res[k]['Notification'].append(rsyslog_dec)

               if '0' in res[k]['Notification']:
                  res[k]['Notification'].remove('0')

               if not check_mode:
                  # Set the Event Filter
                  tmp = dict(res[k])
                  tmp['InstanceID'] = k
                  set_ef_res = ___setEventFilterByInstanceID(remote,tmp)
                  if set_ef_res['failed']:
                     return set_ef_res

               # Set changed because a change has been made
               msg['changed'] = True

         # add this Event Filter for return whether changed or not
         msg['msg'][k] = res[k]

   if debug:
      tmp = json.dumps(msg, indent=3, separators=(',', ': '))
      log.debug("hostname: %s, msg: %s",remote.ip,tmp)

   msg['failed'] = False
   return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
# jobs:
#    - array of jobs to be executed.
#
# TODO: this can actually handle multile jobs. Change the jobid and rebootid to
#   jobs and remove the combining of them in the function. Need to know how to
#   handle arrays in passing into module.
def setupJobQueue(remote,hostname,jobid,rebootid):
   msg = { }
   jobs = []

   if jobid is not '':
      jobs.append(jobid)
   if rebootid is not '':
      jobs.append(rebootid)

   msg = ___setupJobQueue(remote,hostname,jobs)

   if msg['failed']:
      msg['changed'] = False
   else:
      msg['changed'] = True

   return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
# servers:
#    - dicionary of servers - iDRAC limit of 3
#
# check_mode is working
def syslogSettings(remote,servers,enable,port):
   msg = {}
   attributes = {}
   msg['changed'] = False

   if not servers:
      msg['failed'] = True
      msg['msg'] = 'servers must be defined'
      if debug:
         log.debug ("hostname: %s, servers not defined in syslogSettings", remote.ip)
      return msg

   res = ___enumerateIdracCardString(remote)
   if res['failed']:
      return res

   target = "iDRAC.Embedded.1"
   if ('Server1' in servers) and (res['iDRAC.Embedded.1#SysLog.1#Server1']['CurrentValue'] != servers['Server1']):
      msg['changed'] = True
      attributes['SysLog.1#Server1'] = servers['Server1']
   elif ('Server1' not in servers) and (res['iDRAC.Embedded.1#SysLog.1#Server1']['CurrentValue'] != ''):
      msg['changed'] = True
      attributes['SysLog.1#Server1'] = ''


   if ('Server2' in servers) and (res['iDRAC.Embedded.1#SysLog.1#Server2']['CurrentValue'] != servers['Server2']):
      msg['changed'] = True
      attributes['SysLog.1#Server2'] = servers['Server2']
   elif ('Server2' not in servers) and (res['iDRAC.Embedded.1#SysLog.1#Server2']['CurrentValue'] != ''):
      msg['changed'] = True
      attributes['SysLog.1#Server2'] = ''

   if ('Server3' in servers) and (res['iDRAC.Embedded.1#SysLog.1#Server3']['CurrentValue'] != servers['Server3']):
      msg['changed'] = True
      attributes['SysLog.1#Server3'] = servers['Server3']
   elif ('Server3' not in servers) and (res['iDRAC.Embedded.1#SysLog.1#Server3']['CurrentValue'] != ''):
      msg['changed'] = True
      attributes['SysLog.1#Server3'] = ''

   # According Dell's documentation this should give all the iDRAC settings 
   # (Integer and String) but, it doesn't.
   res = ___enumerateIdracCard(remote)
   if res['failed']:
      return res

   if enable and (res['iDRAC.Embedded.1#SysLog.1#SysLogEnable']['CurrentValue'] != 'Enabled'):
      log.debug ("hostname: %s, syslog not enabled. Enabling.", remote.ip)
      msg['changed'] = True
      attributes['SysLog.1#SysLogEnable'] = 'Enabled'
   elif (not enable) and (res['iDRAC.Embedded.1#SysLog.1#SysLogEnable']['CurrentValue'] == 'Enabled'):
      log.debug ("hostname: %s, syslog enabled. Disabling.", remote.ip)
      msg['changed'] = True
      attributes['SysLog.1#SysLogEnable'] = 'Disabled'

   # For syslog to work both syslog and ipmi have to be enabled
   if enable and (res['iDRAC.Embedded.1#IPMILan.1#AlertEnable']['CurrentValue'] != 'Enabled'):
      log.debug ("hostname: %s, IPMI alerting over lan not enabled. Enabling.", remote.ip)
      msg['changed'] = True
      attributes['IPMILan.1#AlertEnable'] = 'Enabled'
   elif (not enable) and (res['iDRAC.Embedded.1#IPMILan.1#AlertEnable']['CurrentValue'] == 'Enabled'):
      log.debug ("hostname: %s, IPMI alerting over lan enabled. Disabling.", remote.ip)
      msg['changed'] = True
      attributes['IPMILan.1#AlertEnable'] = 'Disabled'

   res = ___enumerateIdracCardInteger(remote)
   if res['failed']:
      return res

   if port != int(res['iDRAC.Embedded.1#SysLog.1#Port']['CurrentValue']):
      log.debug ("hostname: %s, syslog port doesn't match setting to %s. Enabling.",
                 remote.ip, res['iDRAC.Embedded.1#SysLog.1#Port']['CurrentValue'])
      msg['changed'] = True
      attributes['SysLog.1#Port'] = res['iDRAC.Embedded.1#SysLog.1#Port']['CurrentValue']

   if not check_mode:
      if msg['changed']:
         result = ___applyAttributes(remote,target,attributes)
         if result['failed']:
            return result

   msg['failed'] = False
   msg['msg'] = 'Syslog Servers Set'
   return msg

# Upgrade BIOS
# Checks current installed version and compares to version
# that is being installed.
#
# remote:
#   - ip, username, password passed to Remote() of WSMan
# hostname:
#   - hostname of the iDRAC being upgraded
#
# This function is deprecated. TODO remove
# Use installBIOS() instead
#
def upgradeBIOS(remote,hostname,share_info,firmware):
   msg = { }
   jobs = []

   res = ___checkShareInfo(share_info)
   if res['failed']:
      return res

   if firmware == '':
      msg['changed'] = False
      msg['failed'] = True
      msg['msg'] = "firmware must be defined."
      return msg

   # Check the Job Queue to make sure there are no pending jobs
   res = ___listJobs(remote,'',{})
   #print "___listJobs"
   if res['failed']:
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = 'iDRAC not accepting commands. wsman returned: '+res['msg']
      return msg

   for k in res:
      #print k+": "+str(res[k])
      if (k == 'JID_CLEARALL') and (res[k]['JobStatus'] == 'Pending'):
         continue
      if (hasattr(res[k], 'JobStatus')) and (res[k]['JobStatus'] == 'Pending'):
         msg['failed'] = True
         msg['changed'] = False
         msg['msg'] = 'Could not complete because there are pending Jobs.'
         msg['msg'] = msg['msg']+' Pending Job: '+k+'. Please clear the Job'
         msg['msg'] = msg['msg']+' Queue and reset the iDRAC.'
         return msg
   #### End of Checking Job Queue

   # Check to make sure the iDRAC is ready to accept commands
   res = ___getRemoteServicesAPIStatus(remote)
   for k in res:
      #print "key: "+k+" value: "+str(res[k])
      if (res['LCStatus'] != '0') and (res['Status'] != '0'):
         msg['failed'] = True
         msg['changed'] = False
         msg['msg'] = 'iDRAC is not ready. Please check the iDRAC. It may need to be reset.'
         return msg
   #### End of checking for iDRAC is ready

   res = ___enumerateSoftwareIdentity(remote)
   if res['failed'] == True:
      return res

   # check to see if version trying to be installed is newer or same
   # if not install
   for k in res:
      if re.search('BIOS', k):
         if res[k]['Status'] == 'Installed':
            cur_version = res[k]['VersionString']
            instanceID = k

   tmp = re.split('/', firmware)
   tmp = tmp[-1]
   tmp = re.split('\.', tmp)
   new_version = tmp[0]+'.'+tmp[1]+'.'+tmp[2]

   if StrictVersion(new_version) > StrictVersion(cur_version):
      if check_mode:
         msg['msg'] = "BIOS upgrade would have been attempted."
         msg['changed'] = False
         msg['failed'] = False
      else:
         installURI_res = ___installFromURI(remote,hostname,share_info,firmware,
                                            instanceID)
         if installURI_res['failed']:
            msg['failed'] = True
            msg['changed'] = False
            msg['idrac_msg'] = installURI_res['Message']
            msg['msg'] = "Download started but, not completed."
            return msg

         jobs.append(installURI_res['jobid'])

         # Waits 3 minutes or until the download completes
         for x in range(1, 90):
            res = ___checkJobStatus(remote,installURI_res['jobid'])
            if res['JobStatus'] == 'Downloaded':
               break
            if res['JobStatus'] == 'Failed':
               break

            time.sleep(2)

         if res['JobStatus'] != 'Downloaded':
            msg['failed'] = True
            msg['changed'] = True
            msg['idrac_msg'] = res['Message']
            msg['msg'] = "Download started but, not completed."
            return msg

         # Create a reboot job
         rebootJob_res = ___createRebootJob(remote,hostname,1)
         if rebootJob_res['failed']:
            msg['failed'] = True
            msg['changed'] = True
            msg['msg'] = "Download completed but, could not create reboot job."
            return msg

         jobs.append(rebootJob_res['rebootid'])

         jobQueue_res = ___setupJobQueue(remote,hostname,jobs)
         if jobQueue_res['failed']:
            msg['failed'] = True
            msg['changed'] = True
            msg['msg'] = "Download completed and reboot job created but, could"
            msg['msg'] = msg['msg']+" not execute reboot."
            return msg

         # Waits 6 minutes or until the bios upgrade completes
         for x in range(1, 1800):
            res = ___checkJobStatus(remote,installURI_res['jobid'])
            if res['JobStatus'] == 'Completed':
               break
            if res['JobStatus'] == 'Failed':
               break

            time.sleep(2)

         if res['JobStatus'] != 'Completed':
            msg['failed'] = True
            msg['changed'] = True
            msg['msg'] = "BIOS upgrade failed."
            return msg

         # Waits 15 minutes or until the iDRAC is ready
         for x in range(1, 90) :
            res = ___getRemoteServicesAPIStatus(remote)
            if ((res['LCStatus'] == '0') and (res['Status'] == '0')
                and res['ServerStatus'] == '2'):
               break

            time.sleep(10)

         if (res['LCStatus'] != '0') and (res['Status'] != '0'):
            msg['failed'] = True
            msg['changed'] = True
            msg['msg'] = "iDRAC never came back after BIOS upgrade."
         else:
            msg['failed'] = False
            msg['changed'] = True
            msg['msg'] = "BIOS upgrade successfully completed."

   elif StrictVersion(new_version) == StrictVersion(cur_version):
      msg['msg'] = "Installed version same as version to be installed."
      msg['failed'] = False
      msg['changed'] = False
   else:
      msg['msg'] = "Installed version newer than version to be installed."
      msg['failed'] = False
      msg['changed'] = False

   if check_mode:
      msg['check_mode'] = "Running in check mode."

   return msg

# Upgrade iDRAC
# Checks current installed version and compares to version
# that is being installed.
#
def upgradeIdrac(remote,hostname,share_info,firmware):
   msg = { }
   msg['ansible_facts'] = {}

   res = ___checkShareInfo(share_info)
   if res['failed']:
      return res

   if firmware == '':
      msg['changed'] = False
      msg['failed'] = True
      msg['msg'] = "firmware must be defined."
      return msg

   # Check the Job Queue to make sure there are no pending jobs
   res = ___listJobs(remote,'',{})
   #print "___listJobs"
   if res['failed']:
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = 'iDRAC not accepting commands. wsman returned: '+res['msg']
      return msg

   for k in res:
      #print k+": "+str(res[k])
      if (k == 'JID_CLEARALL') and (res[k]['JobStatus'] == 'Pending'):
         continue
      if (hasattr(res[k], 'JobStatus')) and (res[k]['JobStatus'] == 'Pending'):
         msg['failed'] = True
         msg['changed'] = False
         msg['msg'] = 'Could not complete because there are pending Jobs.'
         msg['msg'] = msg['msg']+' Pending Job: '+k+'. Please clear the Job'
         msg['msg'] = msg['msg']+' Queue and reset the iDRAC.'
         return msg

   # Check to make sure the iDRAC is ready to accept commands
   res = ___getRemoteServicesAPIStatus(remote)
   for k in res:
      #print "key: "+k+" value: "+str(res[k])
      if (res['LCStatus'] != '0') and (res['Status'] != '0'):
         msg['failed'] = True
         msg['changed'] = False
         msg['msg'] = 'iDRAC is not ready. Please check the iDRAC. It may need to be reset.'
         return msg

   res = ___enumerateSoftwareIdentity(remote)
   if debug:
      print "Calling ___enumerateSoftwareIdentity() from upgradeIdrac()"
   if res['failed']:
      return res

   # check to see if version trying to be installed is newer
   for k in res:
      #print k
      if re.search('iDRAC', k):
         if res[k]['Status'] == 'Installed':
            cur_version = res[k]['VersionString']
            instanceID = k

   tmp = re.split('/', firmware)
   tmp = tmp[-1]
   tmp = re.split('\.', tmp)
   new_version = tmp[0]+'.'+tmp[1]+'.'+tmp[2]+'.'+tmp[3]

   if LooseVersion(new_version) > LooseVersion(cur_version):
      msg = ___installFromURI(remote,hostname,share_info,firmware,instanceID)
      if msg['failed']:
         msg['changed'] = False
         return msg

      # Waits 3 minutes or until the download completes
      for x in range(1, 90):
         res = ___checkJobStatus(remote,msg['jobid'])
         if res['JobStatus'] == 'Completed':
            break
         if res['JobStatus'] == 'Failed':
            break

         time.sleep(2)

      if res['JobStatus'] != 'Completed':
         msg['failed'] = True
         msg['changed'] = True
         msg['idrac_msg'] = res['Message']
         msg['msg'] = 'Download started but, not completed.'
         return msg

      # Once the download is complete the iDRAC will install the firmware
      # automatically. Wait until the iDRAC is ready again

      # STEVE: Setting the upgrade timer to 20 minutes, variable should be global?
      wait_time = 60 * 20
      end_time = time.clock() + wait_time
      while time.clock() < end_time:
         res = ___getRemoteServicesAPIStatus(remote)
         if re.search('Internal Server Error', res['msg']) != None:
            msg['idrac_msg'] = res['msg']
            continue

         if (res['LCStatus'] == '0') and (res['Status'] == '0'):
            msg['failed'] = False
            msg['changed'] = True
            msg['msg'] = 'iDRAC firmware upgrade successfully completed.'
            msg['ansible_facts']['LifecycleControllerVersion'] = new_version
            return msg

         time.sleep(10)

      if (res['LCStatus'] != '0') and (res['Status'] != '0'):
         msg['failed'] = True
         msg['changed'] = True
         msg['msg'] = 'Timeout during upgrade. Verify iDrac.'

   elif LooseVersion(new_version) == LooseVersion(cur_version):
      msg['msg'] = "Installed version "+cur_version+" same as version to be"
      msg['msg'] = msg['msg']+" installed."
      msg['failed'] = False
      msg['changed'] = False
   else:
      msg['msg'] = "Installed version: "+cur_version+" newer than version:"
      msg['msg'] = msg['msg']+" "+new_version+" to be installed."
      msg['failed'] = False
      msg['changed'] = False

   # Steve: If it got here, software didn't change.
   # msg['ansible_facts']['LifecycleControllerVersion'] = new_version

   return msg

# DCIM:INSTALLED:PCI:14E4:1639:0237:1028
# It is installed firmware on a PCI device.
# VID (Vendor ID)= 14E4
# DID (Device ID) = 1636
# SSID (Subsystem ID) = 0237
# SVID (Subvendor ID) = 1028
# This refers to a Broadcom NetXtreme II BCM5709 network adaptor7.
def upgradeNIC(remote,hostname,share_info,firmware):
   if debug:
      print "upgrading NIC"

#
#
def upgradePerc(remote,hostname,share_info,firmware):
   msg = {}
   msg['failed'] = False
   instanceID = ''

   res = ___enumerateSoftwareIdentity(remote)
   if debug:
      print "Calling ___enumerateSoftwareIdentity() from upgradePerc()"
   if res['failed']:
      return res

   for k in res:
      if ((k != 'failed') and (k != 'changed')):
         if re.search('PERC', res[k]['ElementName']):
            if res[k]['Status'] == 'Installed':
               instanceID = k

   if instanceID is not '':
      if check_mode:
         msg['msg'] = "Found: "+InstanceID+" would have tried to install firmware"
      else:
         if debug:
            print "Calling ___upgradeFirmware() from upgradePerc()"
         res = ___upgradeFirmware(remote,hostname,share_info,firmware,instanceID)
         if res['failed']:
            return res
   else:
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = "Unable to find Perc to install firmware."


   if msg['failed'] or check_mode:
      msg['changed'] = False
   else:
      msg['changed'] = True

   return msg

# Currently used to reset password
#
# wsman invoke -a ApplyAttributes \
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_iDRACCardService?SystemCreationClassName=DCIM_ComputerSystem&CreationClassName=DCIM_iDRACCardService&SystemName=DCIM:ComputerSystem&Name=DCIM:iDRACCardService" \
# -h <hostname> -V -v -c dummy.cert -P 443 \
# -u <user> -p <pass> -j utf-8 -y basic -J <file>
#
def ___applyAttributes(remote,target,attributes,remove_xml=True):
   ret = {}

   ref = Reference("DCIM_OSDeploymentService")

   ref.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_iDRACCardService")

   ref.set("SystemCreationClassName", "DCIM_ComputerSystem")
   ref.set("CreationClassName", "DCIM_iDRACCardService")
   ref.set("SystemName", "DCIM:ComputerSystem")
   ref.set("Name","DCIM:iDRACCardService")

   sffx = "_"+remote.ip+"_Attributes.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:ApplyAttributes_INPUT ')
   fh.write('xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_iDRACCardService">\n')
   fh.write('<p:Target>'+target+'</p:Target>\n')
   for k in attributes:
      fh.write('<p:AttributeName>'+k+'</p:AttributeName>\n')
      fh.write('<p:AttributeValue>'+attributes[k]+'</p:AttributeValue>\n')
   fh.write('</p:ApplyAttributes_INPUT>\n')

   fh.close()

   res = wsman.invoke(ref, 'ApplyAttributes', fh.name, remote)
   if remove_xml:
      os.remove(fh.name)

   if type(res) is Fault:
      ret['failed'] = True
      ret['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return ret

   ret = ___checkReturnValues(res, ret)

   if ret['failed']:
      ret['changed'] = False
   else:
      ret['changed'] = True

   return ret

# Checks the job Status of the given Job ID.
#
# remote:
#    - ip, username, password passed to Remote() of WSMan
# jobid:
#    - passed in by Ansible.
#
def ___checkJobStatus (remote,jobid):
   msg = {}

   # wsman get http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LifecycleJob?InstanceID=<job id> -h <ip or hostname> -V -v -c dummy.cert -P 443 -u <user> -p <pass> -j utf-8 -y basic

   r = Reference("DCIM_LifecycleJob")
   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LifecycleJob")
   r.set("InstanceID",jobid)

   res = wsman.get(r, 'root/dcim', remote)
   if type(res) is Fault:
      #print 'There was an error!'
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res)

   return msg

# This function will set the failure status but, it is up to the calling
# function to set changed
#
def ___checkReturnValues(res, msg = {}):
   found = 0

   for p in res.keys:
      if debug:
         print p, res.get(p)
      if re.match('ReturnValue', p) != None:
         # This is the only place (so far) where we set found. This is the only
         # place where we really need to set 'failed'.
         found = 1
         tmp = res.get(p).__str__() # convert to a string
         #print "tmp: "+tmp
         if re.search("\[u'4096'\]", tmp) != None:
            msg['failed'] = False
            msg['ReturnValue'] = 4096
            msg['ReturnValueString'] = "Job Created"
            msg['msg'] = "iDRAC returned: Job Created"
         elif re.search("\[u'0'\]", tmp) != None:
            msg['failed'] = False
            msg['ReturnValue'] = 0
            msg['ReturnValueString'] = "Success"
            msg['msg'] = "iDRAC returned: Success"
         elif re.search("\[u'1'\]", tmp) != None:
            msg['failed'] = True
            msg['ReturnValue'] = 1
            msg['ReturnValueString'] = "Not Supported"
            msg['msg'] = "iDRAC returned: Not Supported"
         elif re.search("\[u'2'\]", tmp) != None:
            msg['failed'] = True
            msg['ReturnValue'] = 2
            msg['ReturnValueString'] = "Failed"
            msg['msg'] = "iDRAC returned: Failed"
         else:
            msg['failed'] = True
            msg['msg'] = "should not reach here. Matched ReturnValue but not the actual value"

      if re.match('JobStatus', p) != None:
         found = 1
         tmp = res.get(p).__str__() # convert to a string
         tmp = tmp.split("'")
         #print tmp[1]
         msg['JobStatus'] = str(tmp[1])

      if re.match('Name', p) != None:
         found = 1
         tmp = res.get(p).__str__() # convert to a string
         tmp = tmp.split("'")
         #print tmp[1]
         msg['Name'] = tmp[1]

      if re.match('Message$', p):
         tmp = res.get(p).__str__()
         tmp = re.split("'", tmp)
         #print tmp[1]
         msg['Message'] = tmp[1]

      if re.match('MessageID', p):
         tmp = res.get(p).__str__()
         tmp = re.split("'", tmp)
         #print tmp[1]
         msg['MessageID'] = tmp[1]

      if re.match('Job', p) != None:
         tmp = res.get(p).__str__() # convert to a string
         tmp = re.split('"', tmp)
         for i in tmp:
            if re.match('JID', i):
               msg['jobid'] = i
               #msg['ansible_facts']['jobid'] = i
               #print "job id: "+jobid
            elif re.match('RID', i):
               msg['rebootid'] = i
            elif re.match('DCIM', i):
               msg['jobid'] = i

      if re.match('RebootJobID', p) != None:
         tmp = res.get(p).__str__() # convert to a string
         tmp = re.split('"', tmp)
         for i in tmp:
            if re.match('RID', i):
               msg['rebootid'] = i

      if re.match('Status', p) != None:
         tmp = res.get(p).__str__() # convert to string
         tmp = re.split("'", tmp)
         msg['Status'] = tmp[1]
         #msg['ansible_facts']['Status'] = tmp[1]
         for case in switch(tmp[1]):
            if case('0'):
               msg['StatusString'] = "Ready"
               break
            if case('1'):
               msg['StatusString'] = "Not Ready"
               break
            if case():
               msg['StatusString'] = "Unknown Status Returned"

      if re.match('LCStatus', p) != None:
         tmp = res.get(p).__str__() # convert to string
         tmp = re.split("'", tmp)
         msg['LCStatus'] = tmp[1]
         #msg['ansible_facts']['LCStatus'] = tmp[1]
         for case in switch(tmp[1]):
            if case('0'):
               msg['LCStatusString'] = "Ready"
               break
            if case('1'):
               msg['LCStatusString'] = "Not Initialized"
               break
            if case('2'):
               msg['LCStatusString'] = "Reloading Data"
               break
            if case('3'):
               msg['LCStatusString'] = "Disabled"
               break
            if case('4'):
               msg['LCStatusString'] = "In Recovery"
               break
            if case('5'):
               msg['LCStatusString'] = "In Use"
               break
            if case():
               msg['LCStatusString'] = "Unknown Status Returned"

      if re.match('ServerStatus', p) != None:
         tmp = res.get(p).__str__() # convert to string
         tmp = re.split("'", tmp)
         msg['ServerStatus'] = tmp[1]
         #msg['ansible_facts']['ServerStatus'] = tmp[1]
         for case in switch(tmp[1]):
            if case('0'):
               msg['ServerStatusString'] = "Powered Off"
               break
            if case('1'):
               msg['ServerStatusString'] = "In POST"
               break
            if case('2'):
               msg['ServerStatusString'] = "Out of POST"
               break
            if case('3'):
               msg['ServerStatusString'] = "Collecting System Inventory"
               break
            if case('4'):
               msg['ServerStatusString'] = "Automated Task Execution"
               break
            if case('5'):
               msg['ServerStatusString'] = "Lifecycle Controller Unified Server Configurator"
               break
            if case('7'):
               msg['ServerStatusString'] = "UNDOCUMENTED! Waiting for OS to be installed?"
               break
            if case():
               msg['ServerStatusString'] = "Unknown Status Returned"

      if re.match('PercentComplete', p) != None:
         tmp = res.get(p).__str__() # convert to a string
         tmp = tmp.split("'")
         #print tmp[1]
         msg['PercentComplete'] = str(tmp[1])

   if not found:
      msg['failed'] = True
      msg['msg'] = 'iDRAC did not return proper values'

   return msg

def ___checkShareInfo(share_info):
   msg = {}
   msg['failed'] = False
   msg['msg'] = "share_info looks good."

   if share_info['ip'] == '':
      msg['failed'] = True
      msg['msg'] = "share_ip must be defined"

   if share_info['type'] == '':
      msg['failed'] = True
      msg['msg'] = "share_type must be defined"

   if ((share_info['type'] == 'samba') 
      or (share_info['type'] == 'cifs') 
      or (share_info['type'] == 'smb')):
      if debug:
         print "___checkShareInfo() share_type is smb"

      if share_info['user'] == '':
         msg['failed'] = True
         msg['msg'] = "share_user must be defined"
      if share_info['pass'] == '':
         msg['failed'] = True
         msg['msg'] = "share_pass must be defined"
      if share_info['name'] == '':
         msg['failed'] = True
         msg['msg'] = "share_name must be defined"
   elif (share_info['type'] == 'nfs'):
      if debug:
         print "___checkShareInfo() share_type is nfs"
      if share_info['user'] == '':
         msg['failed'] = True
         msg['msg'] = "share_user must be defined"
      if share_info['pass'] == '':
         msg['failed'] = True
         msg['msg'] = "share_pass must be defined"
   elif (share_info['type'] == 'http'):
      if debug:
         print "___checkShareInfo() share_type is http"
   elif (share_info['type'] == 'ftp'):
      if debug:
         print "___checkShareInfo() share_type is ftp"
   elif (share_info['type'] == 'tftp'):
      if debug:
         print "___checkShareInfo() share_type is tftp"
   else:
      msg['failed'] = True
      msg['msg'] = "unrecognized share_type"

   return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
# reboot_type:
#    - 1 = PowerCycle, 2 = Graceful Reboot without forced shutdown, 3 = Graceful reboot with forced shutdown
#
# Does not return a changed status. That is up to the calling function.
#
# TODO: hostname is not needed in this function. Use remote.ip instead
def ___createRebootJob (remote,hostname,reboot_type):
   msg = { }

   # wsman invoke -a CreateRebootJob \
   # "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_SoftwareInstallationService?CreationClassName=DCIM_SoftwareInstallationService&SystemCreationClassName=DCIM_ComputerSystem&SystemName=IDRAC:ID&Name=SoftwareUpdate" \
   # -h <hostname> -V -v -c dummy.cert -P 443 -u <user> -p <pass> -J \
   # <file> -j utf-8 -y basic
   r = Reference("DCIM_SoftwareInstallationService")
   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_SoftwareInstallationService")
   r.set("CreationClassName","DCIM_SoftwareInstallationService")
   r.set("SystemCreationClassName","DCIM_ComputerSystem")
   r.set("SystemName","IDRAC:ID")
   r.set("Name","SoftwareUpdate")

   sffx = "_"+hostname+"_CreateRebootJob.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:CreateRebootJob_INPUT ')
   fh.write('xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_SoftwareInstallationService">')
   fh.write('<p:RebootJobType>'+str(reboot_type)+'</p:RebootJobType>')
   fh.write('</p:CreateRebootJob_INPUT>')

   fh.close()

   res = wsman.invoke(r, 'CreateRebootJob', fh.name, remote)
   if debug is not True:
      os.remove(fh.name)

   if type(res) is Fault:
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res,msg)

   return msg

# This function works for creating one or two virtual disks in a row. I tried
# creating 24 disks in a loop and it started giving interesting results around
# disk 6. If you need to create a lot of virtual disks or are doing initial
# setup see ___exportSystemConfiguration and ___importSystemConfiguration().
#
# remote:
#    - ip, username, password passed to Remote() of WSMan
# target: This parameter is the FQDD of the DCIM_ControllerView
#     example: RAID.Integrated.1-1
#
# disks: This parameter is the list of physical disk FQDDs that will be used to
#     create a virtual Disk.
#     example: { 'Disk.Bay.24:Enclosure.Internal.0-1:RAID.Integrated.1-1', 'Disk.Bay.25:Enclosure.Internal.0-1:RAID.Integrated.1-1' }
#
# raid_level:
#     RAID 0 = 2
#     RAID 1 = 4
#     RAID 5 = 64
#     RAID 6 = 128
#     RAID 10 = 2048
#     RAID 50 = 8192
#     RAID 60 = 16384
#
# span_length: Number of Physical Disks to be used per span. Minimum
#     requirements for given RAID Level must be met.
#
# virtual_disk_name: Name of the virtual disk (1-15 character range)
#
# size: Size of the virtual disk specified in MB. If not specified,
#     default will use full size of physical disks selected.
#
# span_depth: If not specified, default is single span which is used
#     for RAID 0, 1, 5 and 6. Raid 10, 50 and 60 require a spandepth of at least 2.
#
# stripe_size:
#     8KB = 16
#     16KB = 32
#     32KB = 64
#     64KB = 128
#     128KB = 256
#     256KB = 512
#     512KB = 1024
#     1MB = 2048
#
# read_policy:
#     No Read Ahead = 16
#     Read Ahead = 32
#     Adaptive Read Ahead = 64
#
# write_policy: Optional.
#     Write Through = 1
#     Write Back = 2
#     Write Back Force = 4
#
# disk_cache_policy: Optional.
#     Enabled = 512
#     Disabled = 1024
#
def ___createVirtualDisk(remote,target,disks,raid_level,span_length,
                         virtual_disk_name,size,span_depth,stripe_size,
                         read_policy,write_policy,disk_cache_policy,remove_xml):
   msg = { 'ansible_facts': {} }
   # wsman invoke -a CreateVirtualDisk \
   # http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_RAIDService?SystemCreationClassName=DCIM_ComputerSystem,CreationClassName=DCIM_RAIDService,SystemName=DCIM:ComputerSystem,Name=DCIM:RAIDService \
   # -h <idrac hostname> -P 443 -u <idrac user> -p <idrac pass> -V -v -c \
   # dummy.cert -j utf-8 -y basic -J <filename>
   r = Reference("DCIM_RAIDService")

   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_RAIDService")

   r.set("SystemCreationClassName","DCIM_ComputerSystem")
   r.set("CreationClassName","DCIM_RAIDService")
   r.set("SystemName","DCIM:ComputerSystem")
   r.set("Name","DCIM:RAIDService")

   sffx = "_"+hostname+"_CreateVirtualDisk.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:CreateVirtualDisk_INPUT xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_RAIDService">\n')
   fh.write('<p:Target>'+target+'</p:Target>\n')
   disks = re.split ('!!!', disks)
   for disk in disks:
      fh.write('<p:PDArray>'+disk+'</p:PDArray>\n')
   fh.write('<p:VDPropNameArray>RAIDLevel</p:VDPropNameArray>\n')
   fh.write('<p:VDPropNameArray>SpanLength</p:VDPropNameArray>\n')
   fh.write('<p:VDPropNameArray>VirtualDiskName</p:VDPropNameArray>\n')
   if size != '':
      fh.write('<p:VDPropNameArray>Size</p:VDPropNameArray>\n')
   if span_depth != '':
      fh.write('<p:VDPropNameArray>SpanDepth</p:VDPropNameArray>\n')
   if stripe_size != '':
      fh.write('<p:VDPropNameArray>StripeSize</p:VDPropNameArray>\n')
   if read_policy != '':
      fh.write('<p:VDPropNameArray>ReadPolicy</p:VDPropNameArray>\n')
   if write_policy != '':
      fh.write('<p:VDPropNameArray>WritePolicy</p:VDPropNameArray>\n')
   if disk_cache_policy != '':
      fh.write('<p:VDPropNameArray>DiskCachePolicy</p:VDPropNameArray>\n')
   fh.write('<p:VDPropValueArray>'+raid_level+'</p:VDPropValueArray>\n')
   fh.write('<p:VDPropValueArray>'+span_length+'</p:VDPropValueArray>\n')
   fh.write('<p:VDPropValueArray>'+virtual_disk_name+'</p:VDPropValueArray>\n')
   if size != '':
      fh.write('<p:VDPropValueArray>'+str(size)+'</p:VDPropValueArray>\n')
   if span_depth != '':
      fh.write('<p:VDPropValueArray>'+str(span_depth)+'</p:VDPropValueArray>\n')
   if stripe_size != '':
      fh.write('<p:VDPropValueArray>'+str(stripe_size)+'</p:VDPropValueArray>\n')
   if read_policy != '':
      fh.write('<p:VDPropValueArray>'+str(read_policy)+'</p:VDPropValueArray>\n')
   if write_policy != '':
      fh.write('<p:VDPropValueArray>'+str(write_policy)+'</p:VDPropValueArray>\n')
   if disk_cache_policy != '':
      fh.write('<p:VDPropValueArray>'+str(disk_cache_policy)+'</p:VDPropValueArray>\n')
   fh.write('</p:CreateVirtualDisk_INPUT>')

   fh.close()

   res = wsman.invoke(r, "CreateVirtualDisk", fh.name, remote)
   if remove_xml:
      os.remove(fh.name)
   if type(res) is Fault:
      #print 'There was an error!'
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res, msg)

   if msg['failed']:
      msg['changed'] = False
   else:
      msg['changed'] = True

   return msg

def ___detachSDCardPartition(remote,hostname,partition_ndx,msg={}):

   # wsman invoke -a DetachPartition \
   # "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_PersistentStorageService?SystemCreationClassName=DCIM_ComputerSystem&CreationClassName=DCIM_PersistentStorageService&SystemName=DCIM:ComputerSystem&Name=DCIM:PersistentStorageService" \
   # -h <hostname> -V -v -c dummy.cert -P 443 -u <username> -p <password> \
   # -J DetachPartition.xml -j utf-8 -y basic

   r = Reference("DCIM_PersistentStorageService")
   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_PersistentStorageService")
   r.set("CreationClassName","DCIM_PersistentStorageService")
   r.set("SystemCreationClassName","DCIM_ComputerSystem")
   r.set("SystemName","DCIM:ComputerSystem")
   r.set("Name","DCIM:PersistentStorageService")

   sffx = "_"+hostname+"_DetachPartition.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:DetachPartition_INPUT ')
   fh.write('xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_PersistentStorageService">\n')
   fh.write('   <p:PartitionIndex>'+partition_ndx+'</p:PartitionIndex>\n')
   fh.write('</p:DetachPartition_INPUT>')

   fh.close()

   res = wsman.invoke(r, 'DetachPartition', fh.name, remote)
   if debug is not True:
      os.remove(fh.name)

   if type(res) is Fault:
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res,msg)

   if msg['failed']:
      msg['changed'] = False
   else:
      msg['changed'] = True

   return msg

def ___elem2json(elem, strip_ns=0, strip=1):

   """Convert an ElementTree or Element into a JSON string."""

   if hasattr(elem, 'getroot'):
      elem = elem.getroot()

   #return json.dumps(___elem_to_internal(elem, strip_ns=strip_ns, strip=strip), sort_keys=True, indent=4, separators=(',', ': '))
   #return json.dumps(___elem_to_internal(elem, strip_ns=strip_ns, strip=strip))
   # leave in json
   return ___elem_to_internal(elem, strip_ns=strip_ns, strip=strip)

def ___elem_to_internal(elem, strip_ns=1, strip=1):
   """Convert an Element into an internal dictionary (not JSON!)."""
   d = {}
   elem_tag = elem.tag
   if strip_ns:
      elem_tag = ___strip_tag(elem.tag)
   else:
      for key, value in list(elem.attrib.items()):
         d['@' + key] = value

   # loop over subelements to merge them
   for subelem in elem:
      v = ___elem_to_internal(subelem, strip_ns=strip_ns, strip=strip)

      tag = subelem.tag
      if strip_ns:
         tag = ___strip_tag(subelem.tag)

      value = v[tag]

      try:
         # add to existing list for this tag
         d[tag].append(value)
      except AttributeError:
         # turn existing entry into a list
         d[tag] = [d[tag], value]
      except KeyError:
         # add a new non-list entry
         d[tag] = value

   text = elem.text
   tail = elem.tail
   if strip:
      # ignore leading and trailing whitespace
      if text:
         text = text.strip()
      if tail:
         tail = tail.strip()

   if tail:
      d['#tail'] = tail

   if d:
      # use #text element if other attributes exist
      if text:
         d["#text"] = text
   else:
      # text is the value if no attributes
      d = text or None
   return {elem_tag: d}

#
# wsman enumerate \
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EventFilter" \
# -h <hostname> -V -v -c dummy.cert -P 443 -u <username> -p <password> -j utf-8 \
# -y basic
#
def ___enumerateEventFilters(remote):
   ret = {}

   r = Reference("DCIM_EventFilter")

   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EventFilter")

   # provides raw XML output
   #res = wsman.enumerate(r, 'root/dcim', remote, True)
   #print res
   res = wsman.enumerate(r, 'root/dcim', remote)
   if type(res) is Fault:
      ret['failed'] = True
      ret['result'] = "Could not enumerate Event Filters"
      ret['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return ret

   for instance in res:
      tmp = ''
      for k,v in instance.items:
         if k == 'InstanceID':
            tmp = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))

      ret[tmp] = {}
      for k,v in instance.items:
         if k != 'InstanceID':
            ret[tmp][k] = v

   ret['failed'] = False
   return ret

# TODO consider making part of fact gathering
#
# wsman enumerate \
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_iDRACCardEnumeration" \
# -h <hostname> -V -v -c dummy.cert -P 443 -u <username> -p <password> -j utf-8 \
# -y basic
#
def ___enumerateIdracCard(remote):
   ret = {}

   r = Reference("DCIM_iDRACCardEnumeration")

   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_iDRACCardEnumeration")

   res = wsman.enumerate(r, 'root/dcim', remote)
   if type(res) is Fault:
      ret['failed'] = True
      ret['result'] = "Could not enumerate iDRAC Card"
      ret['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return ret

   for instance in res:
      tmp = ''
      for k,v in instance.items:
         if k == 'InstanceID':
            tmp = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
            #ret['InstanceID'] = tmp
            #print tmp

      ret[tmp] = {}
      for k,v in instance.items:
         if k != 'InstanceID':
            value = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
            ret[tmp][k] = value.__str__()
         #if k == 'AttributeName':
         #   print k+": "+value.__str__()

   ret['failed'] = False
   ret['changed'] = False
   return ret

# TODO consider making a part of fact gathering
#
# wsman enumerate \
# http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_iDRACCardInteger \
# -h <hostname> -V -v -c dummy.cert -P 443 -u <username> -p <password> \
# -j utf-8 -y basic
#
def ___enumerateIdracCardInteger(remote):
   ret = {}

   ref = Reference("DCIM_iDRACCardInteger")

   ref.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_iDRACCardInteger")

   res = wsman.enumerate(ref, 'root/dcim', remote)
   if type(res) is Fault:
      ret['failed'] = True
      ret['changed'] = False
      ret['result'] = 'Could not enumerate iDRAC Card Integer'
      ret['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return ret

   for instance in res:
      tmp = ''
      for k,v in instance.items:
         if k == 'InstanceID':
            tmp = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
            #msg['InstanceID'] = tmp
            tmp = tmp.__str__()

      ret[tmp] = {}
      for k,v in instance.items:
         if k != 'InstanceID':
            value = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
            k = k.__str__()
            ret[tmp][k] = value.__str__()

   ret['failed'] = False
   return ret

# TODO consider making a part of fact gathering
#
# wsman enumerate \
# http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_iDRACCardString \
# -h <idrac hostname> -V -v -c dummy.cert -P 443 -u <idrac user> -p \
# <idrac pass> -j utf-8 -y basic
#
def ___enumerateIdracCardString(remote):
   ret = {}

   ref = Reference("DCIM_iDRACCardString")

   ref.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_iDRACCardString")

   res = wsman.enumerate(ref, 'root/dcim', remote)
   if type(res) is Fault:
      ret['failed'] = True
      ret['changed'] = False
      ret['result'] = 'Could not enumerate iDRAC Card String'
      ret['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return ret

   for instance in res:
      tmp = ''
      for k,v in instance.items:
         if k == 'InstanceID':
            tmp = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
            #msg['InstanceID'] = tmp
            tmp = tmp.__str__()

      ret[tmp] = {}
      for k,v in instance.items:
         if k != 'InstanceID':
            value = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
            k = k.__str__()
            ret[tmp][k] = value.__str__()

   ret['failed'] = False
   return ret

# wsman enumerate \
# http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_SoftwareIdentity \
# -h <hostname> -V -v -c dummy.cert -P 443 -u <username> -p <password>
# -j utf-8 -y basic
#
def ___enumerateSoftwareIdentity(remote):
   ret = {}

   r = Reference("DCIM_SoftwareIdentity")

   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_SoftwareIdentity")

   res = wsman.enumerate(r, 'root/dcim', remote)
   if type(res) is Fault:
      ret['failed'] = True
      ret['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return ret

   for instance in res:
      tmp = ''
      for k,v in instance.items:
         if k == 'InstanceID':
            tmp = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
            #msg['InstanceID'] = tmp

      ret[tmp] = {}
      for k,v in instance.items:
         if k != 'InstanceID':
            value = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
            ret[tmp][k] = value

   if debug:
      tmp = json.dumps(ret, indent=3, separators=(',', ': '))
      log.debug (tmp)

   ret['failed'] = False
   return ret

# remote:
#    - ip, username, password passed to Remote() of WSMan
#
# wsman invoke -a GetRemoteServicesAPIStatus
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService?SystemCreationClassName=DCIM_ComputerSystem&CreationClassName=DCIM_LCService&SystemName=DCIM:ComputerSystem&Name=DCIM:LCService
# -h <hostname> -V -v -c dummy.cert -P 443 -u <username> -p <password>
# -j utf-8 -y basic
#
def ___getRemoteServicesAPIStatus (remote):
   msg = {}
   msg['ServerStatus'] = ''
   msg['LCStatus'] = ''
   msg['Status'] = ''
   msg['ReturnValue'] = ''

   r = Reference("DCIM_LCService")

   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LCService")

   r.set("SystemCreationClassName","DCIM_ComputerSystem")
   r.set("CreationClassName","DCIM_LCService")
   r.set("SystemName","DCIM:ComputerSystem")
   r.set("Name","DCIM:LCService")

   res = wsman.invoke(r, 'GetRemoteServicesAPIStatus', '', remote)
   if type(res) is Fault:
      #print 'There was an error!'
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res, msg)

   return msg

def ___info(object, spacing=10, collapse=1):
   """Print methods and doc strings.

   Takes module, class, list, dictionary, or string."""
   methodList = [method for method in dir(object) if callable(getattr(object, method))]
   processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
   print "\n".join(["%s %s" %
                     (method.ljust(spacing),
                      processFunc(str(getattr(object, method).__doc__)))
                    for method in methodList])

# remote:
#    - ip, username, password passed to Remote() of WSMan
# share_info: Consists of the below
#    user:
#    pass:
#    name:
#    type:
#    ip:
#    workgroup:
# firmware:
#    - default: ''
# instanceID: The firmware instance to be changed
#
# wsman invoke -a InstallFromURI
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_SoftwareInstallationService?CreationClassName=DCIM_SoftwareInstallationService&SystemCreationClassName=DCIM_ComputerSystem&SystemName=IDRAC:ID&Name=SoftwareUpdate"
# -h <hostname> -V -v -c dummy.cert -P 443 -u <username> -p <password>
# -J InstallFromURI.xml -j utf-8 -y basic
#
def ___installFromURI(remote,hostname,share_info,firmware,instanceID):

   msg = { 'ansible_facts': { } }
   msg['failed'] = False
   msg['jobid'] = ''

   # TODO share_info should be checked in calling function

   if share_info['ip'] == '':
      msg['failed'] = True
      msg['msg'] = "share_ip must be defined"
   if share_info['type'] == '':
      msg['failed'] = True
      msg['msg'] = "share_type must be defined"

   #cifs://WORKGROUP_NAME\[USERNAME]:[PASSWORD]@[URI-IP-ADDRESS]/[FILE.exe];mountpoint=[DIRECTORYNAME]
   if (share_info['type'] == 'samba') or (share_info['type'] == 'cifs') or (share_info['type'] == 'smb'):
      if share_info['user'] == '':
         msg['failed'] = True
         msg['msg'] = "share_user must be defined"
      if share_info['pass'] == '':
         msg['failed'] = True
         msg['msg'] = "share_pass must be defined"
      if share_info['name'] == '':
         msg['failed'] = True
         msg['msg'] = "share_name must be defined"

      uri = "cifs://"
      if share_info['workgroup'] != '':
         uri = uri+share_info['workgoup']+'\\'
      uri = uri+share_info['user']+":"+share_info['pass']+"@"+share_info['ip']
      uri = uri+"/"+firmware+";mountpoint="+share_info['name']

   elif share_info['type'] == 'http':
      uri = 'http://'+share_info['ip']+'/'+firmware
   elif share_info['type'] == 'ftp':
      uri = 'ftp://'+share_info['ip']+'/'+firmware
   elif share_info['type'] == 'tftp':
      uri = 'tftp://'+share_info['ip']+'/'+firmware
   else:
      msg['failed'] = True
      msg['msg'] = "share_type did not match one of the available options"

   if msg['failed'] == True:
      return msg

   sffx = "_"+hostname+"_InstallFromURI.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:InstallFromURI_INPUT ')
   fh.write('xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_SoftwareInstallationService">\n')
   fh.write('   <p:URI>'+uri+'</p:URI>\n')
   fh.write('   <p:Target xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd">\n')
   fh.write('      <a:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>\n')
   fh.write('      <a:ReferenceParameters>\n')
   fh.write('         <w:ResourceURI>http://schemas.dell.com/wbem/wscim/1/cim-schema/2/DCIM_SoftwareIdentity</w:ResourceURI>\n')
   fh.write('         <w:SelectorSet>\n')
   fh.write('            <w:Selector Name="InstanceID">'+instanceID+'</w:Selector>\n')
   fh.write('         </w:SelectorSet>\n')
   fh.write('      </a:ReferenceParameters>\n')
   fh.write('   </p:Target>\n')
   fh.write('</p:InstallFromURI_INPUT>\n')

   fh.close()

   ref = Reference("DCIM_SoftwareInstallationService")

   ref.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_SoftwareInstallationService")

   ref.set("SystemCreationClassName","DCIM_ComputerSystem")
   ref.set("CreationClassName","DCIM_SoftwareInstallationService")
   ref.set("SystemName","IDRAC:ID")
   ref.set("Name","SoftwareUpdate")

   res = wsman.invoke(ref, 'InstallFromURI', fh.name, remote, False)
   if not debug:
      os.remove(fh.name)
   if type(res) is Fault:
      #print 'There was an error!'
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res, msg)

   return msg

"""Convert an internal dictionary (not JSON!) into an Element.
Whatever Element implementation we could import will be
used by default; if you want to use something else, pass the
Element class as the factory parameter.
"""
def ___internal_to_elem(pfsh, factory=ET.Element):


   attribs = {}
   text = None
   tail = None
   sublist = []
   tag = list(pfsh.keys())
   if len(tag) != 1:
      raise ValueError("Illegal structure with multiple tags: %s" % tag)
   tag = tag[0]
   value = pfsh[tag]
   if isinstance(value, dict):
      for k, v in list(value.items()):
         if k[:1] == "@":
            attribs[k[1:]] = v
         elif k == "#text":
            text = v
         elif k == "#tail":
            tail = v
         elif isinstance(v, list):
            for v2 in v:
               sublist.append(___internal_to_elem({k: v2}, factory=factory))
         else:
            sublist.append(___internal_to_elem({k: v}, factory=factory))
   else:
      text = value
   e = factory(tag, attribs)
   for sub in sublist:
      e.append(sub)
   e.text = text
   e.tail = tail
   return e

# Convert a JSON string into an Element.
# Whatever Element implementation we could import will be used by
# default; if you want to use something else, pass the Element class
# as the factory parameter.
#
def ___json2elem(json_data, factory=ET.Element):

   return ___internal_to_elem(json.loads(json_data), factory)

# Covers these two commands:
# wsman get http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LifecycleJob?InstanceID=JobID -h <drac_hostname> -V -v -c dummy.cert -P 443 -u <drac_username> -p <drac_password> -j utf-8 -y basic
# wsman enumerate http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LifecycleJob -h <drac_hostname> -V -v -c dummy.cert -P 443 -u <drac_username> -p <drac_password> -j utf-8 -y basic
#
def ___listJobs(remote,jobid='',msg={}):

   ref = Reference("DCIM_LifecycleJob")
   ref.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_LifecycleJob")

   if jobid is not '':
      ref.set("InstanceID",jobid)
      res = wsman.get(ref, 'root/dcim', remote)
   else:
      res = wsman.enumerate(ref, 'root/dcim', remote)

   if type(res) is Fault:
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
   else:
      msg['failed'] = False
      for instance in res:
         tmp = ''
         for k,v in instance.items:
            if k == 'InstanceID':
               tmp = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
               #ret['InstanceID'] = tmp
               #print tmp

         msg[tmp] = {}
         for k,v in instance.items:
            if k != 'InstanceID':
               value = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
               msg[tmp][k] = value.__str__()

   return msg

def ___listSDCardPartitions(remote, msg={}):
   ref = Reference("DCIM_OpaqueManagementData")
   ref.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_OpaqueManagementData")

   res = wsman.enumerate(ref, 'root/dcim', remote)

   if type(res) is Fault:
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
   else:
      msg['failed'] = False
      for instance in res:
         tmp = ''
         for k,v in instance.items:
            if k == 'PartitionIndex':
               tmp = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
               #ret['InstanceID'] = tmp
               #print tmp

         msg[tmp] = {}
         for k,v in instance.items:
            if k != 'PartitionIndex':
               value = ("%s" % ("".join(map(lambda x: x if x else "" ,v)) ))
               msg[tmp][k] = value.__str__()

   return msg

# wsman invoke -a SetEventFilterByCategory \
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EFConfigurationServcie?SystemCreationClassName=DCIM_SPComputerSystem&CreationClassName=DCIM_EFConfigurationServcie&SystemName=systemmc&Name=DCIM:EFConfigurationService" \
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EFConfigurationService?SystemCreationClassName=DCIM_SPComputerSystem&CreationClassName=DCIM_EFConfigurationService&SystemName=systemmc&Name=DCIM:EFConfigurationService"
# -h <hostname> -P 443 -u <username> -p <password> -V -v -c dummy.cert \
# -j utf-8 -y basic -k "Category=Storage" -k "SubCategory=BAT" \
# -k "Severity=Warning" -k "RequestedAction=0" \
# -k "RequestedNotification=2,3,5,6,7"
#
def ___setEventFilterByCategory(remote,event_instance):
   msg = {}

   return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
# eventInstance:
#    - dict of a single Event Filter by InstanceID
#      {
#          "InstanceID": "iDRAC.Embedded.1#RACEvtFilterCfgRoot#BAT_2_2"
#          "Actions": ['0','1','2','3']
#          "Notifications": ['1','2','3','4','5','6','7']
#      }
#
# See the docs/mofs/DCIM_EventFilter.mof for information on the above Actions
# and Notifications
#
# This command sets one Notification at a time and turns the others off. Not
# real useful IMO but, put here for completeness
#
# wsman invoke -a SetEventFilterByInstanceIDs \
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EFConfigurationService?Name=DCIM:EFConfigurationService&CreationClassName=DCIM_EFConfigurationService&SystemName=systemmc&SystemCreationClassName=DCIM_SPComputerSystem" \
# -h <hostname> -P 443 -u <username> -p <password> -V -v -c dummy.cert \
# -j utf-8 -y basic \
# -k "InstanceID=iDRAC.Embedded.1#RACEvtFilterCfgRoot#BAT_2_2" \
# -k "RequestedAction=0" -k "RequestedNotification=5"
#
# This command uses an XML file to set multiple notifications but, can only set
# one Event Filter at a time. I have put in a request will Dell to enhance the 
# iDRAC so that multiple Event Filters can be set at a time.
#
# wsman invoke -a SetEventFilterByInstanceIDs \
# "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EFConfigurationService?Name=DCIM:EFConfigurationService&CreationClassName=DCIM_EFConfigurationService&SystemName=systemmc&SystemCreationClassName=DCIM_SPComputerSystem" \
# -h <hostname> -P 443 -u <username> -p <password> -V -v -c dummy.cert \
# -j utf-8 -y basic -J <file.xml>
#
# <p:SetEventFilterByInstanceIDs_INPUT xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EFConfigurationService">
#    <p:InstanceID>iDRAC.Embedded.1#RACEvtFilterCfgRoot#BAT_2_2</p:InstanceID>
#    <p:RequestedAction>0</p:RequestedAction>
#    <p:RequestedNotification>2</p:RequestedNotification>
#    <p:RequestedNotification>3</p:RequestedNotification>
#    <p:RequestedNotification>5</p:RequestedNotification>
#    <p:RequestedNotification>6</p:RequestedNotification>
#    <p:RequestedNotification>7</p:RequestedNotification>
# </p:SetEventFilterByInstanceIDs_INPUT>
#
def ___setEventFilterByInstanceID(remote,event_instance):
   msg = {}

   ref = Reference ("DCIM_EFConfigurationService")

   ref.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EFConfigurationService")

   ref.set("SystemCreationClassName","DCIM_SPComputerSystem")
   ref.set("CreationClassName","DCIM_EFConfigurationService")
   ref.set("SystemName","systemmc")
   ref.set("Name","DCIM:EFConfigurationService")

   sffx = "_"+remote.ip+"_EventFilterByInstanceIDInput.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:SetEventFilterByInstanceIDs_INPUT ')
   fh.write('xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_EFConfigurationService">\n')
   fh.write('<p:InstanceID>'+event_instance['InstanceID']+'</p:InstanceID>\n')
   for k in event_instance['Action']:
      fh.write('<p:RequestedAction>'+k+'</p:RequestedAction>\n')
   for k in event_instance['Notification']:
      fh.write('<p:RequestedNotification>'+k+'</p:RequestedNotification>\n')
   fh.write('</p:SetEventFilterByInstanceIDs_INPUT>\n')

   fh.close()

   res = wsman.invoke(ref, 'SetEventFilterByInstanceIDs', fh.name, remote)
   if not debug:
      os.remove(fh.name)

   if type(res) is Fault:
      #print 'There was an error!'
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res,msg)

   msg['failed'] = False
   return msg

# remote:
#    - ip, username, password passed to Remote() of WSMan
# jobs:
#    - list of jobs to be executed.
#
# This function does not return changed status. It is up to the calling function.
#
# wsman invoke -a SetupJobQueue \
# http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_JobService?SystemCreationClassName=DCIM_ComputerSystem&CreationClassName=DCIM_JobService&SystemName=Idrac&Name=JobService \
# -h <hostname> -V -v -c dummy.cert -P 443 -u <username> -p <password> \
# -J SetupJobQueue.xml -j utf-8 -y basic
#
def ___setupJobQueue(remote,hostname,jobs):
   msg = { }

   r = Reference ("DCIM_JobService")

   r.set_resource_uri("http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_JobService")

   r.set("SystemCreationClassName","DCIM_ComputerSystem")
   r.set("CreationClassName","DCIM_JobService")
   r.set("SystemName","Idrac")
   r.set("Name","JobService")

   now = datetime.datetime.now()
   future = now + datetime.timedelta(minutes = 10)
   future = datetime.datetime.strftime(future, '%Y%m%d%H%M%S')
   #print future

   # ddddddddhhmmss.mmmmmm
   future = "00000000001000.000000"

   sffx = "_"+hostname+"_SetupJobQueue.xml"

   fh = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=sffx)

   fh.write('<p:SetupJobQueue_INPUT xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/root/dcim/DCIM_JobService">\n')
   for i in jobs:
      fh.write('\t<p:JobArray>'+i+'</p:JobArray>\n')
   fh.write('\t<p:StartTimeInterval>TIME_NOW</p:StartTimeInterval>\n')
   #fh.write('<p:UntilTime>'+future+'</p:UntilTime>')
   fh.write('</p:SetupJobQueue_INPUT>\n')

   fh.close()

   res = wsman.invoke(r, 'SetupJobQueue', fh.name, remote)
   if not debug:
      os.remove(fh.name)

   if type(res) is Fault:
      msg['failed'] = True
      msg['msg'] = "Code: "+res.code+", Reason: "+res.reason+", Detail: "+res.detail
      return msg

   msg = ___checkReturnValues(res, msg)

   return msg

def ___strip_tag(tag):
   strip_ns_tag = tag
   split_array = tag.split('}')
   if len(split_array) > 1:
      strip_ns_tag = split_array[1]
      tag = strip_ns_tag
   return tag

# Upgrade firmware
#
# This function will return 'changed' because based on how far it gets
# it could have made changes to the iDRAC.
#
# TODO I think you can combine upgrading all firmware. Investigate.
def ___upgradeFirmware(remote,hostname,share_info,firmware,instanceID):
   msg = { }
   jobs = [] # passed to ___setupJobQueue
   msg['failed'] = False

   if debug:
      print "Calling ___checkShareInfo() from upgradeFirmware()"
   res = ___checkShareInfo(share_info)
   if res['failed']:
      res['changed'] = False
      return res

   if firmware == '':
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = "firmware must be defined."
      return msg

   if instanceID == '':
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = "instanceID must be defined."
      return msg
   elif debug:
      print "___upgradeFirmware() instanceID: "+instanceID

   if check_mode:
      # TODO maybe put in what type of firmware.
      msg['msg'] = "Firmware upgrade would have been attempted."
      msg['changed'] = False
      msg['failed'] = False
      return msg

   # Check the Job Queue to make sure there are no pending jobs
   if debug:
      print "in upgradeFirmware() calling ___listJobs()"
   res = ___listJobs(remote,'',{})
   if res['failed']:
      msg['failed'] = True
      msg['changed'] = False
      msg['msg'] = 'iDRAC not accepting commands. wsman returned: '+res['msg']
      return msg

   for k in res:
      #print k+": "+str(res[k])
      if (k == 'JID_CLEARALL') and (res[k]['JobStatus'] == 'Pending'):
         if debug:
            print "in upgradeFirmware() this server has a JID_CLEARALL pending"
         continue
      if (hasattr(res[k], 'JobStatus')) and (res[k]['JobStatus'] == 'Pending'):
         if debug:
            print "in upgradeFirmware() this server has a job pending"
         msg['failed'] = True
         msg['changed'] = False
         msg['msg'] = "Could not complete because there are pending Jobs."
         msg['msg'] = msg['msg']+" Pending Job: "+k+". Please clear the Job"
         msg['msg'] = msg['msg']+" Queue and reset the iDRAC."
         return msg
   #### End of Checking Job Queue

   # Check to make sure the iDRAC is ready to accept commands
   if debug:
      print "in upgradeFirmware() calling ___getRemoteServicesAPIStatus()"
   res = ___getRemoteServicesAPIStatus(remote)
   for k in res:
      #print "key: "+k+" value: "+str(res[k])
      if (res['LCStatus'] != '0') and (res['Status'] != '0'):
         if debug:
            print "in upgradeFirmware() finished ___getRemoteServicesAPIStatus and iDRAC isn't ready"
         msg['failed'] = True
         msg['changed'] = True
         msg['msg'] = "iDRAC is not ready. Please check the iDRAC. It may need to be reset."
         return msg
   #### End of checking for iDRAC is ready

   if debug:
      print "in upgradeFirmware() calling ___installFromURI()"
   installURI_res = ___installFromURI(remote,hostname,share_info,firmware,instanceID)
   if installURI_res['failed']:
      msg['failed'] = True
      msg['changed'] = True
      msg['idrac_msg'] = installURI_res['Message']
      msg['msg'] = "Download started but, not completed."

   if not msg['failed']:
      jobs.append(installURI_res['jobid'])

      # Waits 3 minutes or until the download completes
      if debug:
         print "in upgradeFirmware() checking JobStatus"
      for x in range(1, 90):
         res = ___checkJobStatus(remote,installURI_res['jobid'])
         if res['JobStatus'] == 'Downloaded':
            break
         if res['JobStatus'] == 'Failed':
            break

         time.sleep(2)

      if res['JobStatus'] != 'Downloaded':
         msg['failed'] = True
         msg['changed'] = True
         msg['idrac_msg'] = res['Message']
         msg['msg'] = "Download started but, not completed."

   if not msg['failed']:
      # TODO this reboot job type should be a var.
      # Create a reboot job
      if debug:
         print "in upgradeFirmware() calling ___createRebootJob()"
      rebootJob_res = ___createRebootJob(remote,hostname,1)
      if rebootJob_res['failed']:
         msg['failed'] = True
         msg['changed'] = True
         msg['msg'] = "Download completed but, could not create reboot job."

   if not msg['failed']:
      jobs.append(rebootJob_res['rebootid'])

      if debug:
         print "in upgradeFirmware() calling ___setupJobQueue() to execute reboot job"
      jobQueue_res = ___setupJobQueue(remote,hostname,jobs)
      if jobQueue_res['failed']:
         msg['failed'] = True
         msg['changed'] = True
         msg['msg'] = "Download completed and reboot job created but, could"
         msg['msg'] = msg['msg']+" not execute reboot."

   if not msg['failed']:
      # Waits 6 minutes or until the firmware upgrade completes
      if debug:
         print "in upgradeFirmware() checking JobStatus"
      for x in range(1, 1800):
         res = ___checkJobStatus(remote,installURI_res['jobid'])
         if res['JobStatus'] == 'Completed':
            break
         if res['JobStatus'] == 'Failed':
            break

         time.sleep(2)

      if res['JobStatus'] != 'Completed':
         msg['failed'] = True
         msg['changed'] = True
         msg['msg'] = "Firmware upgrade failed."

   if not msg['failed']:
      # Waits 15 minutes or until the iDRAC is ready
      if debug:
         print "in upgradeFirmware() waiting 15 minutes for the iDRAC to go back to ready"
      for x in range(1, 90) :
         res = ___getRemoteServicesAPIStatus(remote)
         if ((res['LCStatus'] == '0') and (res['Status'] == '0')
             and res['ServerStatus'] == '2'):
            break

         time.sleep(10)

      if (res['LCStatus'] != '0') and (res['Status'] != '0'):
         msg['failed'] = True
         msg['changed'] = True
         msg['msg'] = "iDRAC never came back after Firmware upgrade."
      else:
         msg['failed'] = False
         msg['changed'] = True
         msg['msg'] = "Firmware upgrade successfully completed."

   return msg

def main():
   global debug,check_mode,fmt,fHandle,html,log,wsman

   module = AnsibleModule(
      argument_spec = dict(
         attributes        = dict(type='list'),
         command           = dict(required=True),
         debug             = dict(default='False',type='bool'),
         disk_cache_policy = dict(default=''),
         enable            = dict(type='bool',default='True'),
         firmware          = dict(default=''),
         hostname          = dict(required=True),
         import_file       = dict(default=''),
         instanceID        = dict(default=''),
         iso_image         = dict(),
         jobid             = dict(default=''),
         local_path        = dict(default='~'),
         new_pass          = dict(),
         old_pass          = dict(),
         partition_ndx     = dict(),
         password          = dict(required=True),
         physical_disks    = dict(default=''),
         port              = dict(type='int',default=514),
         raid_level        = dict(default=''),
         read_policy       = dict(default=''),
         rebootid          = dict(),
         reboot_type       = dict(default='2'),
         remove_xml        = dict(default=True),
         servers           = dict(type='dict'),
         share_ip          = dict(default=''),
         share_name        = dict(default=''),
         share_pass        = dict(default=''),
         share_type        = dict(default=''),
         share_user        = dict(default=''),
         size              = dict(default=''),
         span_depth        = dict(default=''),
         span_length       = dict(default=''),
         stripe_size       = dict(default=''),
         target            = dict(default='iDRAC.Embedded.1'),
         target_controller = dict(default=''),
         user_to_change    = dict(default=''),
         username          = dict(required=True),
         virtual_disk_name = dict(default=''),
         workgroup         = dict(default=''),
         write_policy      = dict(default='')
      ),
      supports_check_mode=True
   )

   attributes        = module.params['attributes']
   command           = module.params['command']
   debug             = module.params['debug']
   disk_cache_policy = module.params['disk_cache_policy']
   enable            = module.params['enable']
   firmware          = module.params['firmware']
   hostname          = module.params['hostname']
   import_file       = module.params['import_file']
   instanceID        = module.params['instanceID']
   iso_image         = module.params['iso_image']
   jobid             = module.params['jobid']
   local_path        = module.params['local_path']
   new_pass          = module.params['new_pass']
   old_pass          = module.params['old_pass']
   partition_ndx     = module.params['partition_ndx']
   password          = module.params['password']
   physical_disks    = module.params['physical_disks']
   port              = module.params['port']
   raid_level        = module.params['raid_level']
   read_policy       = module.params['read_policy']
   reboot_type       = module.params['reboot_type']
   rebootid          = module.params['rebootid']
   remove_xml        = module.params['remove_xml']
   servers           = module.params['servers']
   share_ip          = module.params['share_ip']
   share_name        = module.params['share_name']
   share_pass        = module.params['share_pass']
   share_type        = module.params['share_type']
   share_user        = module.params['share_user']
   size              = module.params['size']
   span_length       = module.params['span_length']
   span_depth        = module.params['span_depth']
   stripe_size       = module.params['stripe_size']
   target            = module.params['target']
   target_controller = module.params['target_controller']
   user_to_change    = module.params['user_to_change']
   username          = module.params['username']
   virtual_disk_name = module.params['virtual_disk_name']
   workgroup         = module.params['workgroup']
   write_policy      = module.params['write_policy']

   check_mode        = module.check_mode

   if not HAS_WSMAN:
      module.fail_json(msg='dell-wsman-client-api-python is required for this module http://github.com/hbeatty/dell-wsman-client-api-python')

   wsman = WSMan(transport=Subprocess())

   # Set up the text log
   fmt = OutputFormatter('%(asctime)s %(levelname)s %(name)s %(message)s %(command)s %(output)s %(duration)fs', pretty=False)
   fHandle = logging.FileHandler("test_raw.txt", mode="w")
   fHandle.setFormatter(fmt)

   # Set up the HTML log
   html = HTMLHandler("test_raw.html", pretty=False)
   log = logging.getLogger("")
   log.setLevel(logging.DEBUG)
   log.addHandler(fHandle)
   log.addHandler(html)

   if debug:
      #debug = True
      logging.basicConfig(level=logging.DEBUG,
                          format='%(asctime)s %(levelname)-8s %(message)s',
                          datefmt='%a, %d %b %Y %H:%M:%S')
      log.debug ("Entering debug mode")

   if debug and check_mode:
      log.debug ("Entering check mode")

   # this gets passed to all wsman commands
   remote = Remote(hostname, username, password)
   changed = False

   share_info = {
      'user': share_user,
      'pass': share_pass,
      'name': share_name,
      'type': share_type,
      'ip': share_ip,
      'workgroup': workgroup
   }

   if command == "BootToNetworkISO":
      res = bootToNetworkISO(remote,share_info,iso_image)
      module.exit_json(**res)

   elif command == "CheckJobStatus":
      res = checkJobStatus(remote,jobid)
      module.exit_json(**res)

   elif command == "CheckReadyState":
      res = checkReadyState(remote)
      module.exit_json(**res)

   elif command == "CreateRebootJob":
      res = createRebootJob(remote,hostname,reboot_type)
      module.exit_json(**res)

   elif command == "CreateTargetedConfigJobRAID":
      res = createTargetedConfigJobRAID(remote,hostname,remove_xml,reboot_type)
      module.exit_json(**res)

   elif command == "DeleteJob":
      res = deleteJobQueue(remote,jobid)
      module.exit_json(**res)

   elif command == "DeleteJobQueue":
      jobid = 'JID_CLEARALL'
      res = deleteJobQueue(remote,jobid)
      module.exit_json(**res)

   elif command == "DetachISOImage":
      res = detachISOImage(remote)
      module.exit_json(**res)

   elif command == "DetachSDCardPartitions":
      res = detachSDCardPartitions(remote,hostname)
      module.exit_json(**res)

   elif command == "EnumerateEventFilters":
      res = enumerateEventFilters(remote)
      module.exit_json(**res)

   # The return value is in ansible_facts
   elif command == "EnumerateSoftwareIdentity":
      res = enumerateSoftwareIdentity(remote)
      module.exit_json(**res)

   elif command == "ExportSystemConfiguration":
      res = exportSystemConfiguration(remote,share_info,hostname,local_path,
                                         remove_xml)
      module.exit_json(**res)

   elif command == "GetSystemInventory":
      res = getSystemInventory(remote)
      module.exit_json(**res)

   elif command == "GetRemoteServicesAPIStatus":
      res = getRemoteServicesAPIStatus(remote)
      module.exit_json(**res)

   elif command == "ImportSystemConfiguration":
      res = importSystemConfiguration(remote,share_info,hostname,import_file,
                                      remove_xml)
      module.exit_json(**res)

   elif command == "InstallIdracFirmware":
      res = installIdracFirmware(remote,firmware)
      module.exit_json(**res)

   elif command == "ResetPassword":
      res = resetPassword(remote,hostname,user_to_change,new_pass)
      module.exit_json(**res)

   elif command == "ResetRAIDConfig":
      res = resetRAIDConfig(remote,hostname,remove_xml)
      module.exit_json(**res)

   elif command == "SetEventFiltersByInstanceIDs":
      res = setEventFiltersByInstanceIDs(remote)
      module.exit_json(**res)

   elif command == "SyslogSettings":
      res = syslogSettings(remote,servers,enable,port)
      module.exit_json(**res)

   elif command == "SetupJobQueue":
      res = setupJobQueue(remote,hostname,jobid,rebootid)
      module.exit_json(**res)

   elif command == "UpgradeBIOS":
      res = upgradeBIOS(remote,hostname,share_info,firmware)
      module.exit_json(**res)

   elif command == "UpgradeFirmware":
      res = ___upgradeFirmware(remote,hostname,share_info,firmware,instanceID)
      module.exit_json(**res)

   elif command == "UpgradeIdrac":
      res = upgradeIdrac(remote,hostname,share_info,firmware)
      module.exit_json(**res)

   elif command == "UpgradePerc":
      res = upgradePerc(remote,hostname,share_info,firmware)
      module.exit_json(**res)

   elif command == "CreateVirtualDisk":
      res = ___createVirtualDisk(remote,target_controller,physical_disks,
                                 raid_level,span_length,virtual_disk_name,size,
                                 span_depth,stripe_size,read_policy,
                                 write_policy,disk_cache_policy,remove_xml)
      module.exit_json(**res)

   # The below commands are considered "private" for the module. One should not
   # have to call any of them directly. They are in this section for testing
   # purposes.

   elif command == "___applyAttributes":
      res = ___applyAttributes(remote,target,attributes)
      module.exit_json(**res)

   elif command == "___checkJobStatus":
      res = ___checkJobStatus(remote,jobid)
      module.exit_json(**res)

   elif command == "___detachSDCardPartition":
      res = ___detachSDCardPartition(remote,hostname,partition_ndx)
      module.exit_json(**res)

   elif command == "___enumerateEventFilters":
      res = ___enumerateEventFilters(remote)
      module.exit_json(**res)

   elif command == "___enumerateIdracCard":
      res = ___enumerateIdracCard(remote)
      module.exit_json(**res)

   elif command == "___enumerateIdracCardInteger(remote)":
      res = ___enumerateIdracCardInteger(remote)
      module.exit_json(**res)

   elif command == "___enumerateIdracCardString":
      res = ___enumerateIdracCardString(remote)
      module.exit_json(**res)

   # The return value isn't in ansible_facts
   elif command == "___enumerateSoftwareIdentity":
      res = ___enumerateSoftwareIdentity(remote)
      module.exit_json(**res)

   elif command == "___installFromURI":
      res = ___installFromURI(remote,hostname,share_info,firmware)
      module.exit_json(**res)

   elif command == "___listJobs":
      res = ___listJobs(remote,jobid,{})
      module.exit_json(**res)

   elif command == "___listSDCardPartitions":
      res = ___listSDCardPartitions(remote)
      module.exit_json(**res)

   else:
      # Catch no matching command
      module.fail_json(changed=False, msg="command did not match")
      #print json.dumps({
      #   "msg" : "command did not match",
      #   "changed" : False
      #})

from ansible.module_utils.basic import *
from ansible.module_utils.facts import *
main()
