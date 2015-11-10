```
- name: Reset Default Password
  local_action: idrac username={{ lom_user }} new_pass={{ lom_pass }}
                hostname={{ lom_hostname }} user_to_change={{ lom_user }}
                password={{ drac_default_pass }} command=ResetPassword
```
