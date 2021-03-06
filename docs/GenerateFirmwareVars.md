# GenerateFirmwareVars

## Synopsis

Used to generate <tmp_dir><hostname>.firmware.yml files for merging with [MergeFirmwareVars](MergeFirmwareVars.md).

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter     | required | default | choices   | comments                                  |
| ---------     | -------- | ------- | -------   | --------                                  |
| username      | yes      | none    |           | A user that has admin access to the iDRAC |
| password      | yes      | none    |           | Password of the above user                |
| hostname      | yes      | none    |           | Hostname or IP of the iDRAC               |
| name          | yes      | none    |           | The name is 'GenerateFirmwareVars'        |
| tmp_dir       | no       | ./      |           | Temporary directory. Must end with a /    |

## Examples

```
---
# file: generateFirmwareVars.yml
- hosts: all
  gather_facts: False
  become: yes

  tasks:

  - name: Generate Firmware Files
    local_action:
      module: idrac
      username: "{{lom_user}}"
      password: "{{lom_pass}}"
      hostname: "{{lom_hostname}}"
      name: "GenerateFirmwareVars"
      tmp_dir: "{{idrac_tmp_dir}}"

- hosts: localhost
  gather_facts: False
  become: yes

  tasks:

  - name: Merge Firmware files
    local_action:
      module: idrac
      name: "MergeFirmwareVars"
      tmp_dir: "{{idrac_tmp_dir}}"
      firmware_file: group_vars/all/firmware.yml
    tags: merge_firmware
```

## Return Values

* changed:
  * Desciption: Whether or not changes were made.
  * Type: bool
  * Values: true/false
* failed:
  * Description: Whether or not the firmware.yml was created.
  * Type: bool
  * Values: true/false
* msg:
  * Description: A hopefully helpful message
  * Type: string

## Notes

