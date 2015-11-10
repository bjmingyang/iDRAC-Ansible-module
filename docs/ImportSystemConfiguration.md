```
- name: Import System Configuration
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="ImportSystemConfiguration"
    share_pass={{share_pass}} share_user={{share_user}}
    share_ip={{share_ip}} share_name={{share_name}}
    share_type={{share_type}} import_file=730xd_{{type}}_ImportSystemConfig.xml
  register: raid_result
  when: Model.find('730xd') != -1
```

See roles/idrac-storage/tasks/idrac-storage-setup.yml for a complete example of
how to use this command.

