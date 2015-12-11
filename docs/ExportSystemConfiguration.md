# ExportSystemConfiguration

## Synopsis

Exports the system configuration to a remote share.

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter  | required | default | choices   | comments                                    |
| ---------  | -------- | ------- | -------   | --------                                    |
| username   | yes      |         |           | A user that has admin access to the iDRAC   |
| password   | yes      |         |           | Password of the above user                  |
| hostname   | yes      |         |           | Hostname or IP of the iDRAC                 |
| command    | yes      |         |           | This command is 'ExportSystemConfiguration' |
| share_user | yes      |         |           | username for the share                      |
| share_pass | yes      |         |           | password for the share_user                 |
| share_ip   | yes      |         |           | IP or hostname of the share                 |
| share_name | yes      |         |           | Name of the share                           |
| share_type | yes      |         | cifs, nfs | Share type                                  |
| workgroup  | no       |         |           | The workgroup for the share                 |

## Examples

```
- name: Export System Configuation
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="ExportSystemConfiguration"
    share_pass={{share_pass}} share_user={{share_user}}
    share_ip={{share_ip}} share_name={{share_name}}
    share_type={{share_type}}
```

optional: workgroup={{workgroup}}
