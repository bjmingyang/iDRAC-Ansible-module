# CheckReadyState

## Synopsis

Checks to see if the iDRAC is ready to accept commands. Does not check the status of the server. See [GetRemoteServicesAPIStatus](GetRemoteServicesAPIStatus.md) for server status.

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
| command    | yes      |         |           | This command is 'CheckReadyState'         |

## Examples

```
- name: Make sure iDrac is ready
  local_action: idrac username={{lom_user}} password={{lom_pass}}
                hostname={{lom_hostname}} command="CheckReadyState"
```
