### Share Types

Most commands do not support all share types. This is not a limitation of the
module but a limitation of the iDRAC. Check the commands to see which share
types that command supports.

Note: I primarily use samba. So if the documentation says that a command
supports a 'type' and it isn't working properly that is probably a bug.
Please open an issue.

type: cifs, smb, samba  
required: share_ip, share_user, share_pass, share_name  
optional: workgroup

type: nfs  
required: share_ip, share_user, share_pass

type: ftp  
required: share_ip

type: tftp  
required:  share_ip

type: http  
required: share_ip
