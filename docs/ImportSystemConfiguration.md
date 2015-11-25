# ImportSystemConfiguration

## Synopsis

Imports System Configuration. I usually use this to import the RAID configuration because looping through CreateVirtualDisks tends to stop working correctly after about the 4th iteration.

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter   | required | default | choices   | comments                                     |
| ---------   | -------- | ------- | -------   | --------                                     |
| username    | yes      |         |           | A user that has admin access to the iDRAC    |
| password    | yes      |         |           | Password of the above user                   |
| hostname    | yes      |         |           | Hostname or IP of the iDRAC                  |
| command     | yes      |         |           | This command is 'ImportSystemConfiguration'  |
| share_type  | yes      | cifs    | cifs, nfs | The type of share                            |
| share_user  | yes      |         |           | username for the share                       |
| share_pass  | yes      |         |           | password for the share_user                  |
| share_ip    | yes      |         |           | IP or hostname of the share server           |
| share_name  | no       |         |           | Name of the share. Used for cifs share type. |
| import_file | yes      |         |           | File to import. If you want/need to include a path the path will be relative to the root of the share. |
| debug       | no       |         |           | Turn on debug logging. This will also leave any xml files that might be generated. |

## Examples

```
- name: Import System Configuration
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="ImportSystemConfiguration"
    share_type={{share_type}} share_user={{share_user}}
    share_pass={{share_pass}} share_ip={{share_ip}} share_name={{share_name}}
    import_file=ImportSystemConfig.xml
  register: raid_result
  when: Model.find('730xd') != -1
```

