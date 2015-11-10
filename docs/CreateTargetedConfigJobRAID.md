```
- name: Create Targeted Config Job RAID
  local_action: idrac username={{lom_user}} password={{lom_pass}}
   hostname={{lom_hostname}} command="CreateTargetedConfigJobRAID"
   reboot_type='1'
  register: result
```  
