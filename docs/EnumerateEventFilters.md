# EnumerateEventFilters

## Synopsis

Used to get a lising of all the Event Filters

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter   | required | default | choices   | comments                                      |
| ---------   | -------- | ------- | -------   | --------                                      |
| username    | yes      |         |           | A user that has admin access to the iDRAC     |
| password    | yes      |         |           | Password of the above user                    |
| hostname    | yes      |         |           | Hostname or IP of the iDRAC                   |
| command     | yes      |         |           | This command is 'EnumerateEventFilters'       |
| debug       | no       |         |           | Turn on debug logging. This will also leave any xml files that might be generated. |

## Examples

```
- local_action: 
    module: idrac
    username: root
    password: password
    hostname: host.example.com
    command: 'EnumerateEventFilters'
    debug: true
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


