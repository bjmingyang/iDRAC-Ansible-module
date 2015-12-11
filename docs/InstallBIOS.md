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
| name       | yes      |         |           | The name is 'InstallBIOS'                                       |
| firmware   | yes      |         |           | Dictionary of BIOS firmware.                                    |

firmware options:  

| parameter           | required | default | choices        | comments |
| ---------           | -------- | ------- | -------        | -------- |
| element_name        | no       | none    |                | ElementName from EnumerateSoftwareIdentity. |
| url                 | yes      | none    |                | The URL to download the firmware. Can be http, ftp, tftp, cifs, or nfs. If not specified the url will be used. |
| target_version      | yes      | none    |                | The version of software once upgraded. Used to check the installed version doesn't match the one to be installed before trying the install. |
| minimum_version     | no       | none    |                | If you run into a situation where an upgrade won't complete you may need to upgrade to a firmware version between the one installed and the one you are trying to upgrade to. |

## Examples

```
# The firmware var usually comes from the firmware.yml file which can be
# generated using GenerateFirmwareVars
- name: Install BIOS
  local_action:
    module: idrac
    username: "{{lom_user}}"
    password: "{{lom_pass}}"
    hostname: "{{lom_hostname}}"
    name: "InstallBIOS"
    firmware:
      "{{firmware[SystemGeneration].bios}}"
```

## Return Values


