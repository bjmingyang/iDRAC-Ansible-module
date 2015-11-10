# Introduction

Currently this command only turns on syslog Events.

# Variables

* username - A user that has admin access to the iDRAC
* password - Password of the above user
* hostname - Hostname or IP of the iDRAC
* command - SetEventFiltersByInstanceIDs

# Playbook Example

```
- name: Turn on syslog notifications for iDRAC events
  local_action: idrac username={{lom_user}} password={{lom_pass}}
                hostname={{lom_hostname}} command="SetEventFiltersByInstanceIDs"
```

# Return Values

* changed - true or false
* failed - true or false
* msg - a dict of all the Event Filters and their values

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

