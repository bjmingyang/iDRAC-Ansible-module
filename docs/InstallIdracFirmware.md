# InstallIdracFirmware

## Synopsis

This causes an automatic reboot of the iDRAC because of the iDRAC not because of this module.

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
| command    | yes      |         |           | This command is 'InstallIdracFirmware'    |
| firmware   | yes      |         |           | Dictionary of iDRAC firmware. See firmware.yml for details. 'share_uri' is optional. If 'share_uri' is not specified the 'url' value will be used to try to install the firmware. |
| debug      | no       |         |           | Turn on debug logging. This will also leave any xml files that might be generated. |

## Examples

```
- name: Install iDRAC firmware
  local_action:
    module: idrac
    username: "{{lom_user}}"
    password: "{{lom_pass}}"
    hostname: "{{lom_hostname}}"
    command: "InstallIdracFirmware"
    firmware:
      "{{firmware[SystemGeneration].idrac}}"

- name: Install iDRAC firmware
  local_action:
    module: idrac
    username: root
    password: password
    hostname: host.example.com
    command: InstallIdracFirmware
    firmware:
      - url: http://downloads.dell.com/FOLDER03046131M/1/iDRAC-with-Lifecycle-Controller_Firmware_1WJT4_WN64_2.15.10.10_A00.EXE
      - share_uri: "{{share_type}}://{{share_user}}:{{share_pass}}@{{share_ip}}/{{remote_share_path}}/iDRAC-with-Lifecycle-Controller_Firmware_1WJT4_WN64_2.15.10.10_A00.EXE;mountpoint={{share_name}}"
      - target_version: 2.15.10.10
      - search: none
      - minimum_version: none

- name: Install iDRAC firmware
  local_action:
    module: idrac
    username: root
    password: password
    hostname: host.example.com
    command: InstallIdracFirmware
    firmware:
      - url: http://downloads.dell.com/FOLDER03046131M/1/iDRAC-with-Lifecycle-Controller_Firmware_1WJT4_WN64_2.15.10.10_A00.EXE
      - share_uri: "cifs://some_user:some_pass@host1.example.com/firmware/iDRAC-with-Lifecycle-Controller_Firmware_1WJT4_WN64_2.15.10.10_A00.EXE;mountpoint=public"
      - target_version: 2.15.10.10
      - search: none
      - minimum_version: none

- name: Install iDRAC firmware
  local_action:
    module: idrac
    username: root
    password: password
    hostname: host.example.com
    command: InstallIdracFirmware
    firmware:
      - url: http://downloads.dell.com/FOLDER03046131M/1/iDRAC-with-Lifecycle-Controller_Firmware_1WJT4_WN64_2.15.10.10_A00.EXE
      - target_version: 2.15.10.10
      - search: none
      - minimum_version: none
```

The firmware variable above comes from the firmware.yml file and the 'Model' index comes from the idrac-roles/facts.
