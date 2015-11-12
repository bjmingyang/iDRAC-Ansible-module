# InstallIdrac

## Playbook Example

```
- name: Install iDRAC firmware
  local_action:
    module: idrac
    username: "{{lom_user}}"
    password: "{{lom_pass}}"
    hostname: "{{lom_hostname}}"
    command: "InstallIdracFirmware"
    debug: "True"
    firmware_info:
      "{{firmware[Model].idrac}}"
```
