import mysql.connector
import json
import requests
from icinga2api.client import Client
from icinga2 import Icinga2API
from enum import Enum 

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Tag(Enum):
    New = 0
    Modify = 1
    NothingToDo = 2
    Delete = 3

db = mysql.connector.connect(host="172.20.20.74", user="alexylap", password="felix22", database="srtest2") #connexion a la base de donnée 
req=db.cursor(buffered=True)
client = Client('https://172.20.20.73:5665', 'felix', 'felix22') #connexion a l'API REST

def infoBdd():

    req.execute("SELECT * FROM Switches INNER JOIN ConfigSwitches ON Switches.ConfigSwitchId = ConfigSwitches.ConfigSwitchId INNER JOIN Modeles ON Switches.ModeleId = Modeles.ModeleId") # Requete envoyer a la BDD
    
    reponce= req.fetchall() #Recuperation de tous les information qu'il a pus trouver a la suite de la requete 
    
    for row in reponce:

        idSwitch= row[0]
        nomSwitch = row[1]
        ipNotSplit = row[10] #Recuperation de la colone 9 avec l'ip en CIDR
        ipSplit = ipNotSplit.split('/') #On coupe la variable pour lui dire que nous voulont separé , l'ip et le CIDR
        tag=row[6] #Recuperation de l'information tag ( qui nous dit si le switch a deja été pris en compte null = nouveau , 0 = rien a faire, 1 = doit etre modifier)
        
        print("Information recuperer dans la base de donnée : ")
        print("ID Du Switch : "+ str(idSwitch))
        print("Nom Du Switch :"+ nomSwitch)
        print("Ip : "+ipSplit[0])
        print("Tag : "+str(tag))
        
        verifier(nomSwitch, ipSplit[0], tag, idSwitch) #Verification si le switch existe deja sur l'hyperviseur !
    
    relationSwitch(idSwitch, nomSwitch) #Verifier et ajouter les cascade entre les switch

def addHost(ip, switch, idSwitch):
    
    req.execute("UPDATE `Switches` SET `Tag` = 2 WHERE `Switches`.`SwitchId`="+str(idSwitch))
    db.commit()
    client.objects.create('Host', switch, ['generic-host'], {'address': ip}) #Ajout d'un d'un switch avec les information recuperer dans la BDD
    client.actions.restart_process() #Redemarage du service icinga2 pour mettre la map du reseau a jour 

def verifier(switch, ip, tag, idSwitch):
    
    if tag == Tag.New.value: #Si l'information dans la base de donner vaut 1 cela veut dire qu'il est nouveau et qu'il faut donc le crée
        addHost(ip, switch, idSwitch)
    elif tag == Tag.Modify.value: # Si Tag est a 2 le switch est a modifier sur icinga2 
        print("Le Switch a été modifier")
        print("=================================")
        delete(idSwitch, switch)
        addHost(ip, switch, idSwitch)
    elif tag == Tag.NothingToDo.value: #Si tag est  a 3 il n'a pas ete modifier rien a faire
        print("Le Switch n'a pas été modifier")
        print("=================================")
        pass
    elif tag == Tag.Delete.value:
        delete(idSwitch,switch)
        print("Le Switch "+switch+" a ete surpprimer")
        print("================================")
  
def relationSwitch(idSwitch, switch):
    
    req.execute("SELECT s.NomSwitch, s0.NomSwitch FROM Cascades c JOIN Switches s on s.SwitchId = c.SwitchId JOIN Switches s0 on s0.SwitchId = c.SwitchIdLiaison")
    
    reponce = req.fetchall()
    print(reponce)
    
    requests_url_for_delete = "https://172.20.20.73:5665/v1/objects/dependencies/"
        
    headers_for_delete = {
        'Accept': 'application/json',
        'X-HTTP-Method-Override': 'DELETE'
    }
        
    data_for_delete = {}
        
    r = requests.post(requests_url_for_delete,
                        headers=headers_for_delete,
                        auth=('felix', 'felix22'),
                        data=json.dumps(data_for_delete),
                        verify=False)
    print("Request URL: " + str(r.url))
    print("Status code: " + str(r.status_code))

    if (r.status_code == 200):
        print("Result: " + json.dumps(r.json()))
    else:
        print(r.text)
        r.raise_for_status()
    
    for row in reponce:
        
        parent = row[0]
        enfant = row[1]
        
        #client.objects.create('Dependency', parent+"!"+enfant, {'parent_host_name': parent, 'child_host_name': enfant}) #Ajout d'un d'un switch avec les information recuperer dans la BDD
        
        requests_url = "https://172.20.20.73:5665/v1/objects/dependencies/"+enfant+"!"+parent
        
        headers = {
            'Accept': 'application/json',
            'X-HTTP-Method-Override': 'PUT'
        }
        
        data = {
            "attrs": {"parent_host_name": parent,"child_host_name": enfant}
        }
        
        r = requests.post(requests_url,
                          headers=headers,
                          auth=('felix', 'felix22'),
                          data=json.dumps(data),
                          verify=False)
        print("Request URL: " + str(r.url))
        print("Status code: " + str(r.status_code))

        if (r.status_code == 200):
            print("Result: " + json.dumps(r.json()))
        else:
            print(r.text)
            r.raise_for_status()
        
    client.actions.restart_process() #Redemarage du service icinga2 pour mettre la map du reseau a jour 

def delete(idSwitch, switch):
    
    client.objects.delete('Host')
    req.execute("UPDATE `Switches` SET `Tag` = 0")
    db.commit()
    infoBdd
    
    
if __name__ == "__main__":
    infoBdd()