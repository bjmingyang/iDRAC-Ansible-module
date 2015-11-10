# Introduction

Used to set the Remote syslog server 

# Variables

* username:
  * Description: A user that has admin access to the iDRAC
  * type: string
  * default: null
  * required: true
* password:
  * Description: Password of the above user
  * type: string
  * default: null
  * required: true 
* hostname:
  * Description: Hostname or IP of the iDRAC
  * type: string
  * default: null
  * required: true
* command:
  * Description: This command is 'SyslogSettings'
  * type: string
  * default: null
  * required: true
* servers:
  * Description: Servers that receive syslog messages. Limit of 3
  * type: dict
  * default: null
  * required: true
* enable:
  * Description: Whether to enable or disable sending syslog messages
  * type: bool
  * default: true
  * required: false
* port:
  * Description: UDP port on the syslog server.
  * type: string
  * default: '514'
  * required: false
* debug:
  * Description: Turn on debug logging. This will also leave any xml files that might be generated.
  * type: bool
  * default: false
  * required: false

# Playbook Example

```
- local_action: 
    module: idrac
    username: root
    password: password
    hostname: host.example.com
    command: 'SyslogSettings'
    servers:
      - 'Server1': '10.10.10.1'
      - 10.10.10.2
    enable: true
    port: 514
    debug: True
  when: syslog_servers is defined
  tags:
    - idrac_syslog
```

# Return Values

# Role

* [idrac-alerts](https://github.com/hbeatty/idrac-alerts)

