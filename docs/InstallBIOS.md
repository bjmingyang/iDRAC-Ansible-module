# InstallBIOS

## Synopsis

Used to install the BIOS. Needs to be run seperately from other firmware installs.

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter  | required | default | choices   | comments                                                        |
| ---------  | -------- | ------- | -------   | --------                                                        |
| username   | yes      |         |           | A user that has admin access to the iDRAC                       |
| password   | yes      |         |           | Password of the above user                                      |
| hostname   | yes      |         |           | Hostname or IP of the iDRAC                                     |
| command    | yes      |         |           | This command is 'InstallBIOS'                                   |
| firmware   | yes      |         |           | Dictionary of BIOS firmware. See [firmware.yml](https://github.com/hbeatty/idrac-roles/tree/master/firmware.yml) for details. 'share_uri' is optional. If 'share_uri' is not specified the 'url' value will be used to try to install the firmware. |
| debug      | no       |         |           | Turn on debug logging. This will also leave any xml files that might be generated. |

## Examples

```
- name: Install BIOS
  local_action:
    module: idrac
    username: "{{lom_user}}"
    password: "{{lom_pass}}"
    hostname: "{{lom_hostname}}"
    command: "InstallBIOS"
    firmware:
      "{{firmware[SystemGeneration].bios}}"
```

The firmware variable above comes from the [firmware.yml](https://github.com/hbeatty/idrac-roles/tree/master/firmware.yml) file and the 'SystemGeneration' index comes from the idrac-roles/facts.

## Return Values


