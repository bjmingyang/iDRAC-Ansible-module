# MergeFirmwareVars

## Synopsis

Used to merge the files in <tmp_dir> with <firmware_file>.

Use with [GenerateFirmwareVars](GenerateFirmwareVars.md).

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter     | required | default | choices        | comments                                                                                     |
| ---------     | -------- | ------- | -------        | --------                                                                                     |
| name          | yes      | none    |                | The name is 'MergeFirmwareVars'                                                              |
| tmp_dir       | no       | ./      |                | Temporary directory. Must end with a /. If not specified uses the directory of the playbook. |
| firmware_file | no       | ''      |                | Current firmware.yml. Usuaally group_vars/all/firmware.yml                                   |
| debug         | no       | "False" | "True"/"False" |

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

