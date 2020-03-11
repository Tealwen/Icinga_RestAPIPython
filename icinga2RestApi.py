import requests
import json
from datetime import datetime
from enum import Enum

def icingaAddDependency(db, addr, id, password):
    
    req = db.cursor()
    req.execute("SELECT s.NomSwitch, s0.NomSwitch FROM Cascades c JOIN Switches s on s.SwitchId = c.SwitchId JOIN Switches s0 on s0.SwitchId = c.SwitchIdLiaison")
    
    reponce = req.fetchall()
    
    for row in reponce:
        
        parent = row[0]
        enfant = row[1]
        
        requests_url = addr+"/v1/objects/dependencies/"+enfant+"!"+parent
        
        headers = {
            'Accept': 'application/json',
            'X-HTTP-Method-Override': 'PUT'
        }
        
        data = {
            "attrs": {"parent_host_name": parent,"child_host_name": enfant}
        }
        
        r = requests.post(requests_url,
                        headers=headers,
                        auth=(id, password),
                        data=json.dumps(data),
                        verify=False)
    
        responceRestAPI(r)
        
    
        
def icingaDelAllDependency(addr,id,password):
    requests_url = addr+"/v1/objects/dependencies/"
        
    headers = {
        'Accept': 'application/json',
        'X-HTTP-Method-Override': 'DELETE'
    }
        
    data = {}
        
    r = requests.post(requests_url,
                        headers=headers,
                        auth=(id, password),
                        data=json.dumps(data),
                        verify=False)
    
    responceRestAPI(r)


def responceRestAPI(r):
    
    print("Request URL: " + str(r.url))
    print("Status code: " + str(r.status_code))

    if (r.status_code == 200):
        print("["+str(datetime.now())+"] :"+" Result: " + json.dumps(r.json()))
        print("==============================================================")
    else:
        print(r.text)
        r.raise_for_status()
        
def AddSwitchIcinga(db, client,ip, switch, idSwitch):
    
    req = db.cursor()
    req.execute("UPDATE `Switches` SET `Tag` = 2 WHERE `Switches`.`SwitchId`="+str(idSwitch))
    db.commit()
    client.objects.create('Host', switch, ['generic-host'], {'address': ip}) #Ajout d'un d'un switch avec les information recuperer dans la BDD
    
     
def DelAllSwitch(db, addr, id, password):
    
    requests_url = addr+"/v1/objects/Hosts?cascade=1&pretty=1"
        
    headers = {
        'Accept': 'application/json',
        'X-HTTP-Method-Override': 'DELETE'
    }
        
    data = {}
        
    r = requests.post(requests_url,
                        headers=headers,
                        auth=(id, password),
                        data=json.dumps(data),
                        verify=False)
    
    responceRestAPI(r)
    
    req = db.cursor()
    req.execute("UPDATE `Switches` SET `Tag` = 0")
    db.commit()

    
