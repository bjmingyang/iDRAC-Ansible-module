Deprecated. Use ScheduleFirmwareInstall instead.

```
- name: Upgrade NIC
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="UpgradeNIC"
    share_pass={{share_pass}} share_user={{share_user}}
    share_ip={{share_ip}} share_name={{share_name}}
    share_type={{share_type}} firmware={{ seven_thirty_xd.nic }}
  when: Model.find('730xd') != -1
```
