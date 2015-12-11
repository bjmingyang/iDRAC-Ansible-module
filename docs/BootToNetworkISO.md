# BootToNetworkISO

## Synopsis

Used to boot to a Network ISO image.

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
| command    | yes      |         |           | This command is 'BootToNetworkISO'        |
| share_user | yes      |         |           | username for the share                    |
| share_pass | yes      |         |           | password for the share_user               |
| share_ip   | yes      |         |           | IP or hostname of the share               |
| share_name | yes      |         |           | Name of the share                         |
| share_type | yes      |         | cifs, nfs | Share type                                |
| iso_image  | yes      |         |           | The ISO image file                        |

## Examples

```
- name: Boot to network ISO
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="BootToNetworkISO"
    share_pass={{share_pass}} share_user={{share_user}}
    share_ip={{share_ip}} share_name={{share_name}}
    share_type={{share_type}} iso_image={{inventory_hostname}}.iso
```

## Return Values

  * changed:
    * Desciption: Whether or not changes were made.
    * Type: bool
    * Values: true/false
  * failed:
    * Description: Whether or not the job creation was successful
    * Type: bool
    * Values: true/false
  * msg:
    * Description: A hopefully helpful message
    * Type: string
  * ReturnValue:
    * Description: Return Value from the idrac
    * Values:
      * '2': An error occurred
      * '4096': Job Created
  * jobid:
    * Description: The jobid created by the iDRAC
    * Type: string
  * MessageID:
    * Description: The message ID returned by the iDRAC
    * Type: string
    * Values:
      * OSD1: The command was successful
      * OSD3: Lifecycle Controller is being used by another process
      * OSD9: Failed to reboot the system using IPMI command
      * OSD16: Mount network share failed - incorrect IP address or share name
      * OSD17: Exposing ISO image as interna device to the host system failed
      * OSD19: The fork() command for a child process to do the task failed
      * OSD21: Unable to boot to ISO image
      * OSD28: Hash verification on the ISO image failed
      * OSD30: Invalid value for ExposeDuration - must be 60-65535 seconds
      * OSD35: Lifecycle Controller is not enabled
      * OSD36: Boot to ISO Image has been cancelled by user using CTLR+E option on the server
      * OSD47: Inaccessible network share
      * OSD50: Lifecycle Controller is in field service mode
      * OSD51: Reboot the system to run pending Lifecycle Controller Tasks

## Notes

* [idrac-roles/os-install](https://github.com/hbeatty/idrac-roles/tree/master/os-install)
