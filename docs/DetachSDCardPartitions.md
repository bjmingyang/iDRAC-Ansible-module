```
- name: Detach all SD Card Partitions
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="DetachSDCardPartitions"
```
