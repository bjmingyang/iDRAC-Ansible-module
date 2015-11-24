# CreateRebootJob

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter   | required | default | choices   | comments                                  |
| ---------   | -------- | ------- | -------   | --------                                  |
| username    | yes      |         |           | A user that has admin access to the iDRAC |
| password    | yes      |         |           | Password of the above user                |
| hostname    | yes      |         |           | Hostname or IP of the iDRAC               |
| command     | yes      |         |           | This command is 'CreateRebootJob'         |
| reboot_type | yes      | 2       | 1, 2, 3   | 1 = PowerCycle, 2 = Graceful Reboot without forced shutdown, 3 = Graceful reboot with forced shutdown |
| debug       | no       |         |           | Turn on debug logging. This will also leave any xml files that might be generated. |

## Examples

```
- name: Create Reboot job
  local_action: idrac username={{ lom_user }} password={{ lom_pass }}
    hostname={{ lom_hostname }} command="CreateRebootJob" reboot_type=1
  register: reboot_result
```
