# Introduction

Used to boot to a Network ISO image.

# Variables

* username:
  * Description: A user that has admin access to the iDRAC
  * default: null
  * required: true
* password:
  * Description: Password of the above user
  * default: null
  * required: true 
* hostname:
  * Description: Hostname or IP of the iDRAC
  * default: null
  * required: true
* command:
  * Description: This command is 'BootToNetworkISO'
  * default: null
  * required: true
* share_user:
  * Description: username for the share
  * default: null
  * required: true
* share_pass:
  * Description: password for the share_user
  * default: null
  * required: true
* share_ip:
  * Description: IP or hostname of the share
  * default: null
  * required: true
* share_name:
  * Description: Name of the share
  * default: null
  * required: false
* share_type:
  * Description: Name of the share
  * default: null
  * required: true
* debug:
  * Description: Turn on debug logging. This will also leave any xml files that might be generated.
  * default: false
  * required: false


# Playbook example

```
- name: Boot to network ISO
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="BootToNetworkISO"
    share_pass={{share_pass}} share_user={{share_user}}
    share_ip={{share_ip}} share_name={{share_name}}
    share_type={{share_type}} iso_image={{inventory_hostname}}.iso
```

# Return values

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

# Roles

* [idrac-iso](https://github.com/hbeatty/idrac-iso)
