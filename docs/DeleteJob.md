```
- name: Delete the Job
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{ lom_hostname }} command="DeleteJob" jobid={{result.jobid}}
```
