# GetRemoteServicesAPIStatus

## Synopsis

Gets the status of the iDRAC, LC, and Server.

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter  | required | default | choices   | comments                                      |
| ---------  | -------- | ------- | -------   | --------                                      |
| username   | yes      |         |           | A user that has admin access to the iDRAC     |
| password   | yes      |         |           | Password of the above user                    |
| hostname   | yes      |         |           | Hostname or IP of the iDRAC                   |
| name       | yes      |         |           | The name is 'GetRemoteServicesAPIStatus'      |

## Examples

```
- name: Make sure iDrac is ready
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="GetRemoteServicesAPIStatus"
  register: result
  retries: 20
  delay: 20
  until: ((result.LCStatus == "0") and (result.Status == '0'))
```

## Return Values

| Name         | Values |
| ----         | ------ |
| ReturnValue  | This is the status of GetRemoteServicesAPIStatus not the status of the iDRAC/Server. Tells you if the call to the iDRAC completed successfully.  <ul><li>0 = Request was successfully executed</li><li>1 = Error occurred</li></ul> |
| Status       | The overall status of the Remote Services API. This tells you if the iDRAC is ready to receive commands.  <ul><li>0 = Ready</li><li>1 = Not Ready</li></ul> |
| LCStatus     | The Lifecycle Controller status that includes the Data Manager status.  <ul><li>0 = Ready</li><li>1 = Not Initialized</li><li>2 = Reloading Data</li><li>3 = Disabled</li><li>4 = In Recovery</li><li>5 = In Use</li></ul> |
| ServerStatus | The host system status.  <ul><li>0 = Powered Off</li><li>1 = In POST</li><li>2 = Out of POST</li><li>3 = Collecting System Inventory</li><li>4 = Automated Task Execution</li><li>5 = Lifecycle Controller Unified Server Configurator</li><li>6 = Server has halted at F1/F2 error prompt because of a POST error</li><li>7 = Server has halted at F1/F2/F11 prompt because there are no bootable devices available</li><li>8 = Server has entered F2 setup menu</li><li>9 = Serrver has entered F11 Boot Manager menu</li></ul> |
| RTStatus     | The RealTime Status.  <ul><li>0 = Ready</li><li>1 = Not Ready ( Also means NA where RT is not supported on current config )</li></ul> |
| msg          | Error Message in English corresponding to MessageID is returned if the method fails to execute                                |
| MessageID    | Error Message ID may be used to look-up in the Dell Message registry files. For more information, see Error Message Registry. |

Messages:  

| MessageID | msg |
| --------- | --- |
| LC060     | Lifecycle Controller Remote Services is not ready |
| LC061     | Lifecycle Controller Remote Services is ready |

