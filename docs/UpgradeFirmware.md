# UpgradeFirmware

## Synopsis

Upgrades all firmware except iDRAC and BIOS.

If a the 'target_version' is less than the version installed this will still count as success.

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter  | required | default | choices   | comments                                  |
| ---------  | -------- | ------- | -------   | --------                                  |
| username   | yes      |         |           | A user that has admin access to the iDRAC |
| password   | yes      |         |           | Password of the above user                |
| hostname   | yes      |         |           | Hostname or IP of the iDRAC               |
| name       | yes      |         |           | This command is 'InstallFirmware'         |
| firmware   | yes      |         |           | Dictionary of iDRAC firmware. See firmware.yml for details. 'share_uri' is optional. If 'share_uri' is not specified the 'url' value will be used to try to install the firmware. |



firmware options:  
   element_name:  
     - optional  
     - ElementName from EnumerateSoftwareIdentity. Created when firmware.yml is generated with GenerateFirmwareVars so that you'll have something to use when getting the url from Dell's website.  
   url:  
     - required  
     - Usually the URL to download from Dell. Can be used to download locally or if share_uri not specified will be passed to the iDRAC.  
   share_uri:  
     - optional  
     - if specified this will be passed to the iDRAC. Can be http, ftp, tftp, cifs, or nfs. If not specified the url will be used.  
   target_version:  
     - required  
     - The version of software to be installed. Used to check the installed version doesn't match the one to be installed before trying the install.  
   minimum_version:  
     - optional  
     - If you run into a situation where an install won't complete you may need to install a firmware version between the one installed and the one you are trying to install.  
   reboot:  
     - optional  
     - defaults to False  
   component_id:  
     - optional  
     - If specified this will be used to match the 'ComponentID' from EnumerateSoftwareIdentity.  
   identity_info_value:  
     - optional  
     - If specified this will be used to match the 'IdentityInfoValue' from EnumerateSoftwareIdentity.  
   search:  
     - optional  
     - Uses a regular expression search of the 'ElementName' from EnumerateSoftwareIdentity to find a match. This is a last resort and I recommend you use either the component_id or identity_info_value.  

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
    firmware:
      "{{firmware[SystemGeneration]}}"

- name: Install Firmware
  local_action:
    module: idrac
    username: some_user
    password: some_pass
    hostname: idrac01.example.com
    name: "InstallFirmware"
    firmware:
      "{{firmware[SystemGeneration]}}"

- name: Install Firmware
  local_action:
    module: idrac
    username: some_user
    password: some_pass
    hostname: host.example.com
    name: "InstallFirmware"
    firmware:
      os_collector:
        url: "http://downloads.dell.com/FOLDER02775623M/1/Diagnostics_Application_5W2KP_WN64_OSC_1.1_X10-00.EXE"
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/firmware/Diagnostics_Application_5W2KP_WN64_OSC_1.1_X10-00.EXE;mountpoint={{share_name}}"
        target_version: "OSC_1.1"
        element_name: "OS COLLECTOR"
      diagnostics:
        url: "http://downloads.dell.com/FOLDER03035031M/1/Diagnostics_Application_D5TM2_WN64_4247A1_4247.2.EXE"
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/firmware/Diagnostics_Application_D5TM2_WN64_4247A1_4247.2.EXE;mountpoint={{share_name}}"
        target_version: "4247A1"
        element_name: "Dell 64 Bit uEFI Diagnostics"
      driver_pack:
        url: "http://downloads.dell.com/FOLDER03181143M/1/Drivers-for-OS-Deployment_Application_3VP5C_WN64_15.07.07_A00.EXE"
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/firmware/Drivers-for-OS-Deployment_Application_3VP5C_WN64_15.07.07_A00.EXE;mountpoint={{share_name}}"
        target_version: "15.07.07"
        element_name: "Dell OS Driver Pack"
      raid_backplane.1:
        url: "http://downloads.dell.com/FOLDER00232516M/9/Firmware_681JN_WN32_1.00_A00.EXE"
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/firmware/Firmware_681JN_WN32_1.00_A00.EXE;mountpoint={{share_name}}"
        component_id: "26018"
        target_version: "1.00"
        element_name: "Backplane 1"
        reboot: "True"
      enclosure.1:
        url: "http://downloads.dell.com/FOLDER00307374M/6/ESM_Firmware_3GPH3_WN32_1.07_A00-00.EXE"
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/firmware/ESM_Firmware_3GPH3_WN32_1.07_A00-00.EXE;mountpoint={{share_name}}"
        component_id: "15400735"
        target_version: "1.07"
        element_name: "BP12G+EXP 0:1"
        reboot: "True"
      nic.1:
        url: http://downloads.dell.com/FOLDER02922813M/1/Network_Firmware_PX6V4_WN64_7.12.17.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Network_Firmware_PX6V4_WN64_7.12.17.EXE;mountpoint={{share_name}}"
        target_version: 7.12.17
        element_name: "Broadcom Gigabit Ethernet BCM5720"
        identity_info_value: "DCIM:firmware:14E4:165F:1028:1F5B"
        reboot: "True"
      nic.2:
        url: "http://downloads.dell.com/FOLDER02861870M/2/Network_Firmware_6FD9P_WN64_16.5.20_A00.EXE"
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/firmware/Network_Firmware_6FD9P_WN64_16.5.20_A00.EXE;mountpoint={{share_name}}"
        target_version: "16.5.20"
        element_name: "Intel(R) Ethernet 10G 2P X520 Adapter"
        identity_info_value: "DCIM:firmware:8086:154D:8086:7B11"
        reboot: "True"
      psu.1:
        url: "http://downloads.dell.com/FOLDER01901391M/1/Power_Firmware_62N6X_WN64_07.09.49_A00.EXE"
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/firmware/Power_Firmware_62N6X_WN64_07.09.49_A00.EXE;mountpoint={{share_name}}"
        component_id: "26513"
        target_version: "07.09.49"
        element_name: "Power Supply"
        reboot: "True"
      raid:
        url: http://downloads.dell.com/FOLDER03008731M/1/SAS-RAID_Firmware_WN0HC_WN64_25.3.0.0016_A04.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/SAS-RAID_Firmware_WN0HC_WN64_25.3.0.0016_A04.EXE;mountpoint={{share_name}}"
        target_version: 25.3.0.0016
        reboot: "True"
        identity_info_value: "DCIM:firmware:1000:005B:1028:1F34"
      # According to Dell's website disks do not require a reboot
      disk.1:
        url: http://downloads.dell.com/FOLDER03122098M/1/SAS-Drive_Firmware_68NGY_WN64_LS0B_A00.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/SAS-Drive_Firmware_68NGY_WN64_LS0B_A00.EXE;mountpoint={{share_name}}"
        target_version: LS0B
        component_id: 30667
      disk.2:
        url: http://downloads.dell.com/FOLDER02347714M/2/SAS-Drive_Firmware_57G3N_WN64_YS0C_A08.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/SAS-Drive_Firmware_68NGY_WN64_LS0B_A00.EXE;mountpoint={{share_name}}"
        filename: SAS-Drive_Firmware_68NGY_WN64_LS0B_A00.EXE
        target_version: YS0C
        component_id: 25851
```


