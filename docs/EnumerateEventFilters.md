# Introduction

Used to get a lising of all the Event Filters

# Variables

* username:
  * Description: A user that has admin access to the iDRAC
  * default: null
  * required: true
* password:
  * Description: Password of the above user
  * default: null
  * required: true 
* hostname:
  * Description: Hostname or IP of the iDRAC
  * default: null
  * required: true
* command:
  * Description: This command is 'EnumerateEventFilters'
  * default: null
  * required: true
* debug:
  * Description: Turn on debug logging. This will also leave any xml files that might be generated.
  * default: false
  * required: false

# Playbook Example

```
- local_action: 
    module: idrac
    username: root
    password: password
    hostname: host.example.com
    command: 'EnumerateEventFilters'
    debug: True
```

# Return Values

* changed:
  * Description: Whether or not changes were made
  * Type: bool
  * Values: false
* failed:
  * Description: Whether or not enumeration failed
  * Type: bool
  * Values: true/false
* msg:
  * Description: A dict of Event Filters with their settings
  * Type: dict
  * sample:
  ```
  {
     "iDRAC.Embedded.1#RACEvtFilterCfgRoot#AMP_1_1": {
        "Action": [
           "0"
        ], 
        "Category": [
            "System Health"
        ], 
        "Notification": [
            "2", 
            "7"
        ], 
        "PossibleActionDescriptions": [
            "None", 
            "Reboot", 
            "Power Off", 
            "Power Cycle"
        ], 
        "PossibleActions": [
            "0", 
            "1", 
            "2", 
            "3"
        ], 
        "PossibleNotificationDescriptions": [
            "None", 
            "IPMI Alert", 
            "SNMP Trap", 
            "Email Alert", 
            "OS Log", 
            "WS-Eventing", 
            "Remote System Log"
        ], 
        "PossibleNotifications": [
            "0", 
            "1", 
            "2", 
            "3", 
            "5", 
            "6", 
            "7"
        ], 
        "Severity": [
            "Critical"
        ], 
        "SubCategory": [
            "AMP"
        ], 
        "SubCategoryDescription": [
            "Amperage"
        ]
     }, 
     "iDRAC.Embedded.1#RACEvtFilterCfgRoot#AMP_1_2": {
         "Action": [
             "0"
         ], 
         "Category": [
             "System Health"
         ], 
         "Notification": [
             "2", 
             "7"
         ], 
         "PossibleActionDescriptions": [
             "None", 
             "Reboot", 
             "Power Off", 
             "Power Cycle"
         ], 
         "PossibleActions": [
             "0", 
             "1", 
             "2", 
             "3"
         ], 
         "PossibleNotificationDescriptions": [
             "None", 
             "IPMI Alert", 
             "SNMP Trap", 
             "Email Alert", 
             "OS Log", 
             "WS-Eventing", 
             "Remote System Log"
         ], 
         "PossibleNotifications": [
             "0", 
             "1", 
             "2", 
             "3", 
             "5", 
             "6", 
             "7"
         ], 
         "Severity": [
             "Warning"
         ], 
         "SubCategory": [
             "AMP"
         ], 
         "SubCategoryDescription": [
             "Amperage"
         ]
     },
     {
     ...
  } 

  ```

# Role

Would be used with the [idrac-alerts](https://github.com/hbeatty/idrac-alerts) role but, there is not an example in this role.


