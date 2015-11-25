# GetSystemInventory

## Synopsis

Gets the system inventory and stores in ansible_facts.

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter  | required | default | choices   | comments                                  |
| ---------  | -------- | ------- | -------   | --------                                  |
| username   | yes      |         |           | A user that has admin access to the iDRAC |
| password   | yes      |         |           | Password of the above user                |
| hostname   | yes      |         |           | Hostname or IP of the iDRAC               |
| command    | yes      |         |           | This command is 'GetSystemInventory'      |
| debug      | no       |         |           | Turn on debug logging. This will also leave any xml files that might be generated. |

## Examples

```
- name: Get System Inventory
  local_action: idrac username={{ lom_user }} password={{ lom_pass }}
                hostname={{ lom_hostname }} command=GetSystemInventory
```

## Return Values

```
{
    "ansible_facts": {
        "AssetTag": "", 
        "BIOSReleaseDate": "01/28/2015", 
        "BIOSVersionString": "2.5.2", 
        "BaseBoardChassisSlot": "NA", 
        "BatteryRollupStatus": "1", 
        "BladeGeometry": "255", 
        "BoardPartNumber": "046V88A00", 
        "BoardSerialNumber": "CN7016325P00CI", 
        "CMCIP": "", 
        "CPLDVersion": "1.0.3", 
        "CPURollupStatus": "1", 
        "ChassisModel": "", 
        "ChassisName": "Main System Chassis", 
        "ChassisServiceTag": "4WXBQV1", 
        "ChassisSystemHeight": "2", 
        "DeviceDescription": "System", 
        "EstimatedExhaustTemperature": "25", 
        "EstimatedSystemAirflow": "255", 
        "ExpressServiceCode": "10698022333", 
        "FQDD": "System.Embedded.1", 
        "FanRollupStatus": "1", 
        "HostName": "host.example.com", 
        "IDSDMRollupStatus": "1", 
        "InstanceID": "System.Embedded.1", 
        "IntrusionRollupStatus": "1", 
        "LastSystemInventoryTime": "20151104213659.000000+000", 
        "LastUpdateTime": "20151008002936.000000+000", 
        "LicensingRollupStatus": "1", 
        "LifecycleControllerVersion": "2.20.20.20", 
        "Manufacturer": "Dell Inc.", 
        "MaxCPUSockets": "2", 
        "MaxDIMMSlots": "24", 
        "MaxPCIeSlots": "6", 
        "MemoryOperationMode": "OptimizerMode", 
        "Model": "PowerEdge_R720", 
        "NodeID": "4WXBQV1", 
        "PSRollupStatus": "1", 
        "PlatformGUID": "3156514f-c0b4-4280-5810-00574c4c4544", 
        "PopulatedCPUSockets": "2", 
        "PopulatedDIMMSlots": "16", 
        "PopulatedPCIeSlots": "2", 
        "PowerCap": "483", 
        "PowerCapEnabledState": "3", 
        "PowerState": "2", 
        "PrimaryStatus": "1", 
        "RollupStatus": "1", 
        "ServerAllocation": "", 
        "ServiceTag": "4WXBQV1", 
        "StorageRollupStatus": "1", 
        "SysMemErrorMethodology": "6", 
        "SysMemFailOverState": "NotInUse", 
        "SysMemLocation": "3", 
        "SysMemMaxCapacitySize": "1572864", 
        "SysMemPrimaryStatus": "1", 
        "SysMemTotalSize": "131072", 
        "SystemGeneration": "12G_Monolithic", 
        "SystemID": "1164", 
        "SystemRevision": "0", 
        "TempRollupStatus": "1", 
        "UUID": "4c4c4544-0057-5810-8042-b4c04f515631", 
        "VoltRollupStatus": "1", 
        "smbiosGUID": "44454c4c-5700-1058-8042-b4c04f515631"
    }, 
    "changed": false, 
    "failed": false, 
    "msg": "System Inventory success."
}
```

