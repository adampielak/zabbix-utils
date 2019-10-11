#!/usr/bin/python

# running by threads on systemd
# if empty Hostname, set hostname with inventory.name
# Author: sergio.cricca@tomware.it - 2018


from pyzabbix import ZabbixAPI, ZabbixAPIException
import sys, string, glob, getopt, logging, threading, time

logging.basicConfig(level="INFO")

class threadManagement():
    
    threads = []

    def logMsg(self, message, logtype="info"):
        if logtype == "info":
            logging.info(message)
        elif logtype == "warning":
            logging.warning(message)
        elif logtype == "error":
            logging.error(message)
        elif logtype == "debug":
            logging.debug(message)
        else:
            logging.debug(message)
    
    def randomInt(self, start=0, stop=60):
        return random.randint(start, stop )

    def threadRemove(self, threadList):
        if len(threadList) > 0:
            for t in threadList:
                if not t.is_alive():
                    threadList.remove(t)
                    self.logMsg("Removing thread: " + t.name,"info")
                else:
                    self.logMsg("--- Thread active: " + t.name,"info")
        else:
            self.logMsg("--- 0 thread running","info")
        #threadList = [t for t in threadList if not t.handled]

    def threadExists(self, threadList, name):
        for t in threadList:
            if t.name == name:
                return True
        return False

    def threadCount(self, threadList):
        counter = 0
        for t in threadList:
            if t.is_alive():
                counter += 1
        return counter
    
    def thread_run(self, function, zApi, hostID):
        threadName="check-host-"+hostID
        if self.threadExists(self.threads, threadName):
            self.threadRemove(self.threads)
            time.sleep(5)
        else:
            try:
                t = threading.Thread(name=threadName, target=function, args=(zApi, hostID))
                self.logMsg("START new thread: "+threadName,"info")
                self.threads.append(t)
                t.start()
                time.sleep(5)
            except:
                self.logMsg("unable to start thread "+threadName,"error")
    

def helpArgs():
    print ("Arguments:\n\t\t-u|--username <zabbix username>\n\t\t-p|--password <zabbix password>\n\t\t-l|--link <zabbix server link>")

def getHostList(zApi):
    return zApi.host.get(output="extend")

def setInventoryName(zApi, hostID):
    for h in zApi.host.get(output="extend",hostids=hostID, selectInventory=["name"]):
        if h['name'] == h['host']:
            if h['inventory']:
                if len(h['inventory']['name']) > 0:
                    print(h['inventory']['name'])
                    zApi.host.update(hostid=hostID,name=h['inventory']['name'])

 

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hu:p:l:n:t:a:",["help","username=","password=","link=","name="])
    except getopt.GetoptError:
        helpArgs()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            helpArgs()
            sys.exit()
        elif opt in ("-u","--username"):
            zbxUsername = arg
        elif opt in ("-p","--password"):
            zbxPassword = arg
        elif opt in ("-l","--link"):
            zbxLink = arg.lower()

    zapi = ZabbixAPI(zbxLink)
    zapi.login(zbxUsername,zbxPassword)
    t = threadManagement()
    #print("Connected to Zabbix API %s Version %s" % (zbxLink,zapi.api_version()))
    while True:
        for h in getHostList(zapi):
            t.thread_run(setInventoryName, zapi, h['hostid'])
            #time.sleep(timeout)
       #setInventoryName(zapi, h['hostid'])





if __name__ == "__main__":
    main(sys.argv[1:])
