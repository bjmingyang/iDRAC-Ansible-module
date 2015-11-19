# iDRAC-Ansible-module
Ansible module to manage the Dell iDRAC

## Install

* In your 'library' directory run

```
$ git clone git@github.com/hbeatty/iDRAC-Ansible-module.git idrac
```

OR  

```
$ git submodule add https://github.com/hbeatty/iDRAC-Ansible-module.git idrac
```

You should be able to copy this right into any standard Ansible layout.

# Requirements:  

https://github.com/hbeatty/dell-wsman-client-api-python

I know it works with these versions of wsman. Success may vary with other versions.  
wsmancli (2.3.2-54.5) from Openwsman  
libwsman1 (2.4.15-148.1) from Openwsman

# Documentation

[Docs](https://github.com/hbeatty/iDRAC-Ansible-module/tree/master/docs)

## Notes
 
More info on git submodules: [Git Book](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
