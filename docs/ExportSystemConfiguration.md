```
- name: Export System Configuation
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="ExportSystemConfiguration"
    share_pass={{share_pass}} share_user={{share_user}}
    share_ip={{share_ip}} share_name={{share_name}}
    share_type={{share_type}}
```

optional: workgroup={{workgroup}}
