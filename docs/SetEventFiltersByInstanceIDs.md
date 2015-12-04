# SetEventFiltersByInstanceIDs

## Synopsis

Currently this command only turns on the 'Remote System Log' event Notifications.

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter  | required | default | choices   | comments                                       |
| ---------  | -------- | ------- | -------   | --------                                       |
| username   | yes      |         |           | A user that has admin access to the iDRAC      |
| password   | yes      |         |           | Password of the above user                     |
| hostname   | yes      |         |           | Hostname or IP of the iDRAC                    |
| command    | yes      |         |           | This command is 'SetEventFiltersByInstanceIDs' |

## Examples

```
- name: Turn on syslog notifications for iDRAC events
  local_action: idrac username={{lom_user}} password={{lom_pass}}
                hostname={{lom_hostname}} command="SetEventFiltersByInstanceIDs"
```

## Return Values

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

