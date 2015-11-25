# SyslogSettings

## Synopsis

Used to set the 'Remote System Log' servers. 

## Requirements

* [Dell WSMan Client API Python](https://github.com/hbeatty/dell-wsman-client-api-python)
* wsmancli and libwsman1 from [OpenWSMAN](https://openwsman.github.io/)
  * I would like to get rid of this dependency (for various reasons) by enhancing the Dell WSMan Client API Python with a new transport.
  * I know it works with these versions of Openwsman. Success may vary with other versions.
    * wsmancli (2.3.2-54.5) from Openwsman
    * libwsman1 (2.4.15-148.1) from Openwsman

## Options

| parameter  | required | default | choices                   | comments                                                                           |
| ---------  | -------- | ------- | -------                   | --------                                                                           |
| username   | yes      |         |                           | A user that has admin access to the iDRAC                                          |
| password   | yes      |         |                           | Password of the above user                                                         |
| hostname   | yes      |         |                           | Hostname or IP of the iDRAC                                                        |
| command    | yes      |         |                           | This command is 'SyslogSettings'                                                   |
| servers    | yes      |         | Server1, Server2, Server3 | Dictionary of syslog servers. iDRAC limits to 3.                                   |
| enable     | no       | true    | true, false               | If you are calling this command I assume you want to turn on syslog.               |
| port       | no       |         |                           | If you don't specify a port this won't change what is set on the iDRAC.            |
| debug      | no       |         |                           | Turn on debug logging. This will also leave any xml files that might be generated. |

## Examples

```
- local_action: 
    module: idrac
    username: root
    password: password
    hostname: host.example.com
    command: 'SyslogSettings'
    servers:
      - 'Server1': '10.10.10.1'
      - 'Server2': '10.10.10.2'
      - 'Server3': '10.10.10.3'
    enable: true
    port: 514
    debug: True
  when: syslog_servers is defined
  tags:
    - idrac_syslog
```

## Role

* [idrac-alerts](https://github.com/hbeatty/idrac-roles/alerts)

