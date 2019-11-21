#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
automatic-template-selection.py
finds the most suitable templates starting from inventory field provided
"""


from pyzabbix import ZabbixAPI
import logging
import getopt
import os, sys, re

SWVERSION = 0.1
log_level = "INFO" # CRITICAL, ERROR, WARNING, INFO, DEBUG
logshowerror = False
skipmodules=["pyzabbix", "urllib3"]



ZBXURI = ""
ZBXUSER = ""
ZBXPASS = ""
ZBXTEMPLATE_PREFIX="Template Printers "


class ZabbixAPI(ZabbixAPI):
    logging.getLogger(__name__)
    def __init__(self, *args, **kwargs):
        try:
            return super(ZabbixAPI, self).__init__(*args, **kwargs)
        except Exception as e:
            logging.critical(str(e))
            raise
        
    def get_host_inventory_field(self, hostname, inventory_field):
        try:
            h = self.host.get(output="extend", filter={"host": hostname}, selectInventory=[inventory_field.lower()])
            logging.info(
                f"working on {hostname}:\n"
                f"Name is {h[0]['name']}\n"
                f"Model is {h[0]['inventory'][inventory_field.lower()]}")
            return h[0]['inventory'][inventory_field.lower()]
        except Exception as e:
            logging.critical(str(e), exc_info = logshowerror)
            pass
        
    
    def match_template_list(self, name):
        inventoryid = None
        templates = self.template.get(output="extend")
        while inventoryid == None and len(name)>0:
            for t in templates:
                template_name = t['host'].replace(ZBXTEMPLATE_PREFIX,'')
                logging.debug(
                    f"checking {template_name} against {name}"
                )
                if name == template_name:
                    logging.info(f"found {t['host']} that matches {name}. Returning ID#{t['templateid']} ")
                    inventoryid = t['templateid']
                    break
            name = name[:-1]
        if inventoryid is not None:
            return inventoryid
        else:
            return 0
        
    def get_host_templates(self, hostname):
        try:
            return self.host.get(output="hostid", filter={"host": hostname}, selectParentTemplates=["templateid", "name"])
        except Exception as e:
            logging.critical(str(e))
            raise
        

    def cicle_inventory_value(self, hostname, inventory_field):
        fieldvalue = self.get_host_inventory_field(hostname, inventory_field)
        h = self.get_host_templates(hostname)
        templateid_new = str(self.match_template_list(fieldvalue)).lower()
        if templateid_new != "0":
            logging.info(f"templateid to add is {templateid_new}")
            host_templateids = []
            for ht in h[0]['parentTemplates']:
                logging.debug(
                    f"{ht['templateid']} {ht['name']}"
                )
                host_templateids.append(ht['templateid'].lower())
            logging.info(host_templateids)    
            
            if templateid_new in host_templateids:
                logging.info(f"{templateid_new} is already linked to host")
            else:
                logging.info(f"{templateid_new} need to be linked to host")
                host_templateids.append(templateid_new)
                templatelist = []
                for templateid in host_templateids:
                    templatelist.append({"templateid": templateid})
                self.host.update(output="extend", hostid=h[0]['hostid'], templates=templatelist)
                
def helpArgs():
    print (
        "\n"
        f"{os.path.basename(__file__)} - automatic template selection v{SWVERSION}\n"
        "Arguments:\n"
        "\t-s|--source <hostname to manage>\n"
        "\t-f|--field <inventory field name to check>\n"
        f"eg: {os.path.basename(__file__)} -s 'Linux Host' -f 'Model'"
    )
    

def main(argv):
    logging.basicConfig(format='%(asctime)s:%(process)d:[%(levelname)s](%(name)s):%(message)s', level=log_level)
    for module in skipmodules:
        logging.getLogger(module).setLevel(logging.ERROR)


    try:
        opts, args = getopt.getopt(argv,"hs:f:",["help","source=","field="])
    except getopt.GetoptError:
        helpArgs()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            helpArgs()
            sys.exit()
        elif opt in ("-s","--source"):
            hostname = arg
        elif opt in ("-f","--field"):
            fieldname = arg

    zapi = ZabbixAPI(ZBXURI)
    zapi.login(ZBXUSER,ZBXPASS)
    logging.info("Connected to Zabbix API %s Version %s" % (ZBXURI,zapi.api_version()))
    zapi.cicle_inventory_value(hostname=hostname, inventory_field=fieldname)

if __name__ == "__main__":
    main(sys.argv[1:])
