# CreateVirtualDisk

## Synopsis

Creates a Virtual Disk on the RAID controller.

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter         | required | default | choices     | comments                                  |
| ---------         | -------- | ------- | -------     | --------                                  |
| username          | yes      |         |             | A user that has admin access to the iDRAC |
| password          | yes      |         |             | Password of the above user                |
| hostname          | yes      |         |             | Hostname or IP of the iDRAC               |
| command           | yes      |         |             | This command is 'CheckJobStatus'          |
| target_controller | yes      |         |             | This parameter is the FQDD of the DCIM_ControllerView. example: RAID.Integrated.1-1 |
| physical_disks    | yes      |         |             | This parameter is the list of physical disk FQDDs that will be used to create a virtual Disk. example: { 'Disk.Bay.24:Enclosure.Internal.0-1:RAID.Integrated.1-1', 'Disk.Bay.25:Enclosure.Internal.0-1:RAID.Integrated.1-1' } |
| raid_level        | yes      |         | <ul><li>2</li><li>4</li><li>64</li><li>128</li><li>2048</li><li>8192</li><li>16384</li></ul> | <ul><li>2 = RAID 0</li><li>4 = RAID 1</li><li>64 = RAID 5</li><li>128 = RAID 6</li><li>2048 = RAID 10</li><li>8192 = RAID 50</li><li>16384 = RAID 60 |
| span_length       | yes      |         |             | Number of Physical Disks to be used per span. Minimum requirements for given RAID Level must be met. |
| virtual_disk_name | yes      |         |             | Name of the virtual disk. (1-15 character range) |
| size              | no       | Full size of physical disks selected. | | Size of the virtual disk specified in MB. If not specified, default will use full size of physical disks selected. |
| span_depth        | no       |         |             | If not specified, default is single span which is used for RAID 0, 1, 5 and 6. Raid 10, 50 and 60 require a spandepth of at least 2. |
| stripe_size       | no       | 0       | <ul><li>0</li><li>1</li><li>2</li><li>4</li><li>8</li><li>16</li><li>32</li><li>64</li><li>128</li><li>256</li><li>512</li><li>1024</li><li>2048</li><li>4096</li><li>8192</li><li>16384</li><li>32768</li></ul>  | <ul><li>0 = Default</li><li>1 = 512 Bytes</li><li>2 = 1 KB</li><li>4 = 2 KB</li><li>8 = 4 KB</li><li>16 = 8 KB</li><li>32 = 16 KB</li><li>64 = 32 KB</li><li>128 = 64 KB</li><li>256 = 128 KB</li><li>512 = 256 KB</li><li>1024 = 512 KB</li><li>2048 = 1 MB</li><li>4096 = 2 MB</li><li>8192 = 4 MB</li><li>16384 = 8 MB</li><li>32768 = 16 MB</li></ul> This varies depending on your RAID controller. |
| read_policy       | no       | Value set in RAID controller. |             |                                           |
| write_policy      | no       | Value set in RAID controller. |             |                                           |
| disk_cache_policy | no       | Value set in RAID controller. |             |                                           |
| remove_xml        | no       | yes     | <ul><li>true</li><li>false</li></ul> |                                        |

## Examples

```
- name: Create Virtual Disk
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{lom_hostname}} command="CreateVirtualDisk"
```
