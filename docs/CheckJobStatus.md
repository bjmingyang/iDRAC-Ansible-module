```
- name: Check Job Status
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="CheckJobStatus"
    jobid={{raid_result.jobid}}
  register: result
  retries: 50
  delay: 15
  until: result.PercentComplete == "100"
  failed_when: "'Failed' in result.JobStatus"
```
