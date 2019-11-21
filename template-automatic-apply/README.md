# Automatic Template slection
#### automatic template selection based upon inventory fields


#### Authors:
- sergio.cricca@tomware.it

___
#### Features:
- apply templates based on model or hardware inventory
- alerts if no template has been found

#### How does it works:
This script reads host inventory field and check if there is a template named exactly like the field.
If it doesn't find one, it removes 1 char at a time from the field value, until if finds a suitable template, otherwise returns 0.

#### Usage:
1. copy automatic-template-selection.py into zabbix ```externalscripts``` folder   
2. import "Template App Automatic-Template-Selection" into zabbix  
3. apply template to hosts (or link it to already existing main templates)

___
### Version: 0.1
### Status: Work in progress
### TODO:



