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
| debug      | no       |         |           | Turn on debug logging. This will also leave any xml files that might be generated. |

## Examples

```
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
      diagnostics:
        url: http://downloads.dell.com/FOLDER03115335M/1/Diagnostics_Application_MNYY2_WN64_4239A24_4239.32.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Diagnostics_Application_MNYY2_WN64_4239A24_4239.32.EXE;mountpoint={{share_name}}"
        target_version: 4239A24
      os_collector:
        url: http://downloads.dell.com/FOLDER02605944M/3/Diagnostics_Application_PWMC8_WN64_OSC_1.1_A00.EXE
        target_version: OSC_1.1
      driver_pack:
        url: http://downloads.dell.com/FOLDER03218446M/1/Drivers-for-OS-Deployment_Application_H1C80_WN64_15.07.07_A00.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Drivers-for-OS-Deployment_Application_H1C80_WN64_15.07.07_A00.EXE;mountpoint={{share_name}}"
        target_version: 15.07.07
      backplane:
        url: http://downloads.dell.com/FOLDER02998103M/1/Firmware_HMH10_WN64_3.03_A00-00.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Firmware_HMH10_WN64_3.03_A00-00.EXE;mountpoint={{share_name}}"
        target_version: 3.03
      backplane:
        url: http://downloads.dell.com/FOLDER02909023M/1/Firmware_635G9_WN64_2.23_A00-00.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Firmware_635G9_WN64_2.23_A00-00.EXE;mountpoint={{share_name}}"
        target_version: 2.23
      nic.1:
        url: http://downloads.dell.com/FOLDER02922813M/1/Network_Firmware_PX6V4_WN64_7.12.17.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Network_Firmware_PX6V4_WN64_7.12.17.EXE;mountpoint={{share_name}}"
        target_version: 7.12.17
        element_name: "Broadcom Gigabit Ethernet BCM5720"
        identity_info_value: "DCIM:firmware:14E4:165F:1028:1F5B"
      nic.2:
        url: "http://downloads.dell.com/FOLDER02861870M/2/Network_Firmware_6FD9P_WN64_16.5.20_A00.EXE"
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/firmware/Network_Firmware_6FD9P_WN64_16.5.20_A00.EXE;mountpoint={{share_name}}"
        target_version: "16.5.20"
        element_name: "Intel(R) Ethernet 10G 2P X520 Adapter"
        identity_info_value: "DCIM:firmware:8086:154D:8086:7B11"
        reboot: "True"
      psu:
        url: http://downloads.dell.com/FOLDER01901119M/1/Power_Firmware_DMRNY_WN64_04.07.23_A00.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/Power_Firmware_DMRNY_WN64_04.07.23_A00.EXE;mountpoint={{share_name}}"
        target_version: 04.07.23
      raid:
        url: http://downloads.dell.com/FOLDER03008731M/1/SAS-RAID_Firmware_WN0HC_WN64_25.3.0.0016_A04.EXE
        share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/SAS-RAID_Firmware_WN0HC_WN64_25.3.0.0016_A04.EXE;mountpoint={{share_name}}"
        target_version: 25.3.0.0016
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

The firmware variable above comes from the firmware.yml file and the 'SystemGeneration' index comes from the idrac-roles/facts.
