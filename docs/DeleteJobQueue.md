# DeleteJobQueue

## Playbook Example

```
- name: Delete the Job Queue
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{ lom_hostname }} command="DeleteJobQueue"
```
