# UpgradeFirmware

## Synopsis

Upgrades all firmware except iDRAC and BIOS.  

If a the 'target_version' is less than the version installed this will still count as success.  

Gives an overall status of changed and failed. It is possible that some upgrades were successful and some were not. Check the status of the individual upgrades for more info (see example below).

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter   | required | default | choices   | comments                                                                                              |
| ---------   | -------- | ------- | -------   | --------                                                                                              |
| username    | yes      |         |           | A user that has admin access to the iDRAC                                                             |
| password    | yes      |         |           | Password of the above user                                                                            |
| hostname    | yes      |         |           | Hostname or IP of the iDRAC                                                                           |
| name        | yes      |         |           | This command is 'InstallFirmware'                                                                     |
| reboot_type | yes      | 2       | 1, 2, 3   | 1 = PowerCycle, 2 = Graceful Reboot without forced shutdown (You have to log in to the server and reboot), 3 = Graceful reboot with forced shutdown (iDRAC tries to reboot the server. On CentOS this requires additional software.) |
| firmware    | yes      |         |           | Dictionary of iDRAC firmware. See firmware.yml for details. 'share_uri' is optional. If 'share_uri' is not specified the 'url' value will be used to try to install the firmware. |

firmware options:  

| parameter           | required | default | choices        | comments |
| ---------           | -------- | ------- | -------        | -------- |
| element_name        | no       | none    |                | ElementName from EnumerateSoftwareIdentity. Created when firmware.yml is generated with GenerateFirmwareVars so that you'll have something to use when getting the url from Dell's website. |
| url                 | yes      | none    |                | Usually the URL to download from Dell. Can be used to download locally or if share_uri not specified will be passed to the iDRAC. |
| share_uri           | no       | none    |                | If specified this will be passed to the iDRAC. Can be http, ftp, tftp, cifs, or nfs. If not specified the url will be used. |
| target_version      | yes      | none    |                | The version of software once upgraded. Used to check the installed version doesn't match the one to be installed before trying the install. |
| minimum_version     | no       | none    |                | If you run into a situation where an upgrade won't complete you may need to upgrade to a firmware version between the one installed and the one you are trying to upgrade to. |
| reboot              | no       | "False" | "True"/"False" | This is a string not a bool. Do not try to use yes/no/1/0/true/false. |
| component_id        | no       | none    |                | If specified this will be used to match the 'ComponentID' from EnumerateSoftwareIdentity. |
| identity_info_value | no       | none    |                | If specified this will be used to match the 'IdentityInfoValue' from EnumerateSoftwareIdentity. |
| search              | no       | none    |                | Uses a regular expression search of the 'ElementName' from EnumerateSoftwareIdentity to find a match. This is a last resort and I recommend you use either the component_id or identity_info_value. |

Matching order:  
  1. key. idrac, bios, diagnostics, os_collector, and driver_pack should only match one.  
  2. component_id. if specified. Best used for disks, power supplies, RAID backplane, RAID enclosure  
  3. identity_info_value. if specified. Best used for NICs, RAID controller  
  4. search. if specified. Searches the 'ElementName' from EnumerateSoftwareIdentity. Last resort.  

## Examples

```
# The firmware variable comes from firmware.yml (see GenerateFirmwareVars) and the 'SystemGeneration' index comes from the idrac-roles/facts.
- name: Install Firmware
  local_action:
    module: idrac
    username: "{{lom_user}}"
    password: "{{lom_pass}}"
    hostname: "{{lom_hostname}}"
    name: "InstallFirmware"
    reboot_type: 1
    firmware:
      "{{firmware[SystemGeneration]}}"

- name: Install Firmware
  local_action:
    module: idrac
    username: some_user
    password: some_pass
    hostname: idrac01.example.com
    name: "InstallFirmware"
    reboot_type: 1
    firmware:
      "{{firmware[SystemGeneration]}}"

- name: Install Firmware
  local_action:
    module: idrac
    username: some_user
    password: some_pass
    hostname: host.example.com
    name: "InstallFirmware"
    reboot_type: 1
    firmware:
      os_collector:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Diagnostics_Application_5W2KP_WN64_OSC_1.1_X10-00.EXE;mountpoint={{share_name}}"
        target_version: "OSC_1.1"
        element_name: "OS COLLECTOR"
      diagnostics:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Diagnostics_Application_D5TM2_WN64_4247A1_4247.2.EXE;mountpoint={{share_name}}"
        target_version: "4247A1"
        element_name: "Dell 64 Bit uEFI Diagnostics"
      driver_pack:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Drivers-for-OS-Deployment_Application_3VP5C_WN64_15.07.07_A00.EXE;mountpoint={{share_name}}"
        target_version: "15.07.07"
        element_name: "Dell OS Driver Pack"
      raid_backplane.1:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Firmware_681JN_WN32_1.00_A00.EXE;mountpoint={{share_name}}"
        component_id: "26018"
        target_version: "1.00"
        element_name: "Backplane 1"
        reboot: "True"
      enclosure.1:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/ESM_Firmware_3GPH3_WN32_1.07_A00-00.EXE;mountpoint={{share_name}}"
        component_id: "15400735"
        target_version: "1.07"
        element_name: "BP12G+EXP 0:1"
        reboot: "True"
      nic.1:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Network_Firmware_PX6V4_WN64_7.12.17.EXE;mountpoint={{share_name}}"
        target_version: 7.12.17
        element_name: "Broadcom Gigabit Ethernet BCM5720"
        identity_info_value: "DCIM:firmware:14E4:165F:1028:1F5B"
        reboot: "True"
      nic.2:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Network_Firmware_6FD9P_WN64_16.5.20_A00.EXE;mountpoint={{share_name}}"
        target_version: "16.5.20"
        element_name: "Intel(R) Ethernet 10G 2P X520 Adapter"
        identity_info_value: "DCIM:firmware:8086:154D:8086:7B11"
        reboot: "True"
      psu.1:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Power_Firmware_62N6X_WN64_07.09.49_A00.EXE;mountpoint={{share_name}}"
        component_id: "26513"
        target_version: "07.09.49"
        element_name: "Power Supply"
        reboot: "True"
      raid:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/SAS-RAID_Firmware_WN0HC_WN64_25.3.0.0016_A04.EXE;mountpoint={{share_name}}"
        target_version: 25.3.0.0016
        reboot: "True"
        identity_info_value: "DCIM:firmware:1000:005B:1028:1F34"
      disk.1:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/SAS-Drive_Firmware_68NGY_WN64_LS0B_A00.EXE;mountpoint={{share_name}}"
        target_version: LS0B
        component_id: 30667
        reboot: "True"
      disk.2:
        url: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/SAS-Drive_Firmware_68NGY_WN64_LS0B_A00.EXE;mountpoint={{share_name}}"
        filename: SAS-Drive_Firmware_68NGY_WN64_LS0B_A00.EXE
        target_version: YS0C
        component_id: 25851
        reboot: "True"
```

## Return Values

| Name         | Values |
| ----         | ------ |
| ReturnValue  | This is the status of GetRemoteServicesAPIStatus not the status of the iDRAC/Server. Tells you if the call to the iDRAC completed successfully.  <ul><li>0 = Request was successfully executed</li><li>1 = Error occurred</li></ul> |
| Status       | The overall status of the Remote Services API. This tells you if the iDRAC is ready to receive commands.  <ul><li>0 = Ready</li><li>1 = Not Ready</li></ul> |
| LCStatus     | The Lifecycle Controller status that includes the Data Manager status.  <ul><li>0 = Ready</li><li>1 = Not Initialized</li><li>2 = Reloading Data</li><li>3 = Disabled</li><li>4 = In Recovery</li><li>5 = In Use</li></ul> |
| ServerStatus | The host system status.  <ul><li>0 = Powered Off</li><li>1 = In POST</li><li>2 = Out of POST</li><li>3 = Collecting System Inventory</li><li>4 = Automated Task Execution</li><li>5 = Lifecycle Controller Unified Server Configurator</li><li>6 = Server has halted at F1/F2 error prompt because of a POST error</li><li>7 = Server has halted at F1/F2/F11 prompt because there are no bootable devices available</li><li>8 = Server has entered F2 setup menu</li><li>9 = Serrver has entered F11 Boot Manager menu</li></ul> |
| RTStatus     | The RealTime Status.  <ul><li>0 = Ready</li><li>1 = Not Ready ( Also means NA where RT is not supported on current config )</li></ul> |
| msg          | Error Message in English corresponding to MessageID is returned if the method fails to execute                                |
| MessageID    | Error Message ID may be used to look-up in the Dell Message registry files. For more information, see Error Message Registry. |

Messages:  

| MessageID | msg |
| --------- | --- |
| LC060     | Lifecycle Controller Remote Services is not ready |
| LC061     | Lifecycle Controller Remote Services is ready |

Example Return:  

```
{
   "JobStatus": "Reboot Completed",
   "MessageID": "RED030",
   "Name": "Reboot1",
   "PercentComplete": "NA",
   "ReturnValue": 0,
   "ReturnValueString": "Success",
   "changed": true,
   "failed": false,
   "msg": "firmware install completed.",
   "rebootid": "RID_494227705984",
   "result": {
      "Diagnostics.Embedded.1:LC.Embedded.1": {
         "JobStatus": "Completed",
         "MessageID": "RED001",
         "Name": "update:DCIM:INSTALLED#802__Diagnostics.Embedded.1:LC.Embedded.1",
         "PercentComplete": "NA",
         "ReturnValue": 4096,
         "ReturnValueString": "Job Created",
         "VersionString": "4239A24",
         "changed": true,
         "current_version": "4239A14",
         "done": true,
         "failed": false,
         "jobid": "JID_494224628777",
         "minimum_version": "",
         "msg": "Job completed successfully.",
         "target_version": "4239A24"
      },
      "Disk.Bay.24:Enclosure.Internal.0-1:RAID.Integrated.1-1": {
         "JobStatus": "Completed",
         "MessageID": "PR19",
         "Name": "update:DCIM:INSTALLED#304_C_Disk.Bay.24:Enclosure.Internal.0-1:RAID.Integrated.1-1",
         "PercentComplete": "NA",
         "ReturnValue": 4096,
         "ReturnValueString": "Job Created",
         "VersionString": "DF09",
         "changed": true,
         "current_version": "DF04",
         "done": true,
         "failed": false,
         "jobid": "JID_494226381026",
         "minimum_version": "",
         "msg": "Job completed successfully.",
         "target_version": "DF09"
      },
      "Disk.Bay.3:Enclosure.Internal.0-1:RAID.Integrated.1-1": {
         "JobStatus": "Completed",
         "MessageID": "PR19",
         "Name": "update:DCIM:INSTALLED#304_C_Disk.Bay.3:Enclosure.Internal.0-1:RAID.Integrated.1-1",
         "PercentComplete": "NA",
         "ReturnValue": 4096,
         "ReturnValueString": "Job Created",
         "VersionString": "IS06",
         "changed": true,
         "current_version": "IS05",
         "done": true,
         "failed": false,
         "jobid": "JID_494224367025",
         "minimum_version": "",
         "msg": "Job completed successfully.",
         "target_version": "IS06"
      },
      "Enclosure.Internal.0-1:RAID.Integrated.1-1": {
         "JobStatus": "Completed",
         "MessageID": "PR19",
         "Name": "update:DCIM:INSTALLED#308_C_Enclosure.Internal.0-1:RAID.Integrated.1-1",
         "PercentComplete": "NA",
         "ReturnValue": 4096,
         "ReturnValueString": "Job Created",
         "VersionString": "3.03",
         "changed": true,
         "current_version": "1.07",
         "done": true,
         "failed": false,
         "jobid": "JID_494224797226",
         "minimum_version": "",
         "msg": "Job completed successfully.",
         "target_version": "3.03"
      },
      "NIC.Integrated.1-1-1": {
         "JobStatus": "Completed",
         "MessageID": "PR19",
         "Name": "update:DCIM:INSTALLED#701__NIC.Integrated.1-1-1",
         "PercentComplete": "NA",
         "ReturnValue": 4096,
         "ReturnValueString": "Job Created",
         "VersionString": "7.10.61",
         "changed": true,
         "current_version": "7.10.17",
         "done": true,
         "failed": false,
         "jobid": "JID_494226789853",
         "minimum_version": "",
         "msg": "Job completed successfully.",
         "target_version": "7.10.61"
      },
      "NIC.Slot.2-1-1": {
         "JobStatus": "Completed",
         "MessageID": "PR19",
         "Name": "update:DCIM:INSTALLED#701__NIC.Slot.2-1-1",
         "PercentComplete": "NA",
         "ReturnValue": 4096,
         "ReturnValueString": "Job Created",
         "VersionString": "16.5.20",
         "changed": true,
         "current_version": "16.0.22",
         "done": true,
         "failed": false,
         "jobid": "JID_494225231588",
         "minimum_version": "",
         "msg": "Job completed successfully.",
         "target_version": "16.5.20"
      },
      "OSCollector.Embedded.1": {
         "JobStatus": "Completed",
         "MessageID": "RED001",
         "Name": "update:DCIM:INSTALLED#802__OSCollector.Embedded.1",
         "PercentComplete": "NA",
         "ReturnValue": 4096,
         "ReturnValueString": "Job Created",
         "VersionString": "OSC_1.1",
         "changed": true,
         "current_version": "OSC_1.0",
         "done": true,
         "failed": false,
         "jobid": "JID_494227313304",
         "minimum_version": "",
         "msg": "Job completed successfully.",
         "target_version": "OSC_1.1"
      },
      "PSU.Slot.1": {
         "changed": false,
         "current_version": "04.07.23",
         "failed": false,
         "minimum_version": "",
         "msg": "Firmware is current",
         "target_version": "04.07.23"
      },
      "PSU.Slot.2": {
         "changed": false,
         "current_version": "00.24.6D",
         "failed": false,
         "minimum_version": "",
         "msg": "Firmware is current",
         "target_version": "00.24.6D"
      },
      "RAID.Backplane.Firmware.0": {
         "JobStatus": "Completed",
         "MessageID": "PR19",
         "Name": "update:DCIM:INSTALLED#314_C_RAID.Backplane.Firmware.0",
         "PercentComplete": "NA",
         "ReturnValue": 4096,
         "ReturnValueString": "Job Created",
         "VersionString": "2.23",
         "changed": true,
         "current_version": "2.20",
         "done": true,
         "failed": false,
         "jobid": "JID_494226005422",
         "minimum_version": "",
         "msg": "Job completed successfully.",
         "target_version": "2.23"
      },
      "RAID.Integrated.1-1": {
         "JobStatus": "Completed",
         "MessageID": "PR19",
         "Name": "update:DCIM:INSTALLED#301_C_RAID.Integrated.1-1",
         "PercentComplete": "NA",
         "ReturnValue": 4096,
         "ReturnValueString": "Job Created",
         "VersionString": "25.3.0.0016",
         "changed": true,
         "current_version": "25.2.2-0004",
         "done": true,
         "failed": false,
         "jobid": "JID_494225610307",
         "minimum_version": "",
         "msg": "Job completed successfully.",
         "target_version": "25.3.0.0016"
      }
   }
}

"Disk.Bay.22:Enclosure.Internal.0-1:RAID.Integrated.1-1": {
                "JobStatus": "Completed", 
                "Message": "Job completed successfully.", 
                "MessageID": "PR19", 
                "Name": "update:DCIM:INSTALLED#304_C_Disk.Bay.22:Enclosure.Internal.0-1:RAID.Integrated.1-1", 
                "PercentComplete": "NA", 
                "ReturnValue": 4096, 
                "ReturnValueString": "Job Created", 
                "VersionString": "LS0B", 
                "changed": true, 
                "current_version": "LS0A", 
                "done": true, 
                "failed": false, 
                "jobid": "JID_493489125555", 
                "minimum_version": "", 
                "msg": "iDRAC returned: Job Created", 
                "target_version": "LS0B"
}
```
