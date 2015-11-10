# Introduction

This is used to detach the ISO image after a call of BootToISOImage has been completed.

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
  * Description: This command is 'DetachISOImage'
  * default: null
  * required: true
* debug:
  * Description: Turn on debug logging. This will also leave any xml files that might be generated.
  * default: false
  * required: false

# Playbook Example

```
- name: Detach ISO Image
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="DetachISOImage"
```
