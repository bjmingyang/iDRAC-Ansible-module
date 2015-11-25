# DeleteJob

## Synopsis

Deletes a singe job from the queue.

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
| command     | yes      |         |           | This command is 'DeleteJob'                   |
| jobid       | yes      |         |           | The ID of the job to delete                   |
| debug       | no       |         |           | Turn on debug logging. This will also leave any xml files that might be generated. |

## Examples

```
- name: Delete Job
  local_action: idrac username={{lom_user}} password={{lom_pass}}
    hostname={{ lom_hostname }} command="DeleteJob" jobid={{result.jobid}}
```
