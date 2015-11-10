```
- name: Make sure iDrac is ready
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="GetRemoteServicesAPIStatus"
  register: result
  retries: 20
  delay: 20
  until: ((result.LCStatus == "0") and (result.Status == '0'))
```
