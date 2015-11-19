# CreateRebootJob

## Playbook Example

```
- name: Create Reboot job
  local_action: idrac username={{ lom_user }} password={{ lom_pass }}
    hostname={{ lom_hostname }} command="CreateRebootJob"
    jobid={{ result.jobid }}  reboot_type=1
  register: reboot_result
```
