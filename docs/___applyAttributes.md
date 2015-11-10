# Introduction

This is an internal function. 

# Variables

* username:
  * Description: A user that has admin access to the iDRAC
  * default: null
  * required: true
* password:
  * Description: Password of the above user
  * default: null
  * required: true 
* hostname:
  * Description: Hostname or IP of the iDRAC
  * default: null
  * required: true
* command:
  * Description: This command is '___applyAttributes'
  * default: null
  * required: true
* target:
  * Description: The target string of the iDRAC
  * default: iDRAC.Embedded.1
  * required: false
* debug:
  * Description: Turn on debug logging. This will also leave any xml files that might be generated.
  * default: false
  * required: false


