Deprecated. Use ScheduleFirmwareInstall instead.

```
- name: Perc upgrade
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="UpgradePerc"
    share_pass={{share_pass}} share_user={{share_user}}
    share_ip={{share_ip}} share_name={{share_name}}
    share_type={{share_type}} firmware={{ seven_thirty_xd.perc }}
  when: Model.find('730xd') != -1
```

Notes:
Strictly speaking this isn't an upgrade. You could use this to install any version of the software (including the same version).
