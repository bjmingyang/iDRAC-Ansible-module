# InstallIdracFirmware

## Introduction

This causes an automatic reboot of the iDRAC because of the iDRAC not because of this module.

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
  * Description: This command is 'InstallIdracFirmware'
  * default: null
  * required: true
* debug:
  * Description: Turn on debug logging. This will also leave any xml files that might be generated.
  * default: false
  * required: false


## Playbook Example

```
- name: Install iDRAC firmware
  local_action:
    module: idrac
    username: "{{lom_user}}"
    password: "{{lom_pass}}"
    hostname: "{{lom_hostname}}"
    command: "InstallIdracFirmware"
    firmware:
      "{{firmware[Model].idrac}}"
```

The firmware variable above comes from the firmware.yml file and the 'Model' index comes from the idrac-roles/facts.