# InstallBIOS

## Introduction

Used to install the BIOS. Needs to be run seperately from other firmware installs.

## Variables

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
  * Description: This command is 'InstallBIOS'
  * default: null
  * required: true
* debug:
  * Description: Turn on debug logging. This will also leave any xml files that might be generated.
  * default: false
  * required: false

## Playbook Example

```
- name: Install Firmware
  local_action:
    module: idrac
    username: "{{lom_user}}"
    password: "{{lom_pass}}"
    hostname: "{{lom_hostname}}"
    command: "InstallFirmware"
    firmware:
      "{{firmware[Model].bios}}"
```

The firmware variable above comes from the firmware.yml file and the 'Model' index comes from the idrac-roles/facts.
