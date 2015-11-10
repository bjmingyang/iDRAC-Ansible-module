```
- name: Do the reboot
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="SetupJobQueue"
    rebootid={{result.rebootid}}
```

This is going to be moved to a "private" function
