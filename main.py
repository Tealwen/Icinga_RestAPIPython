import mysql.connector
import json
from icinga2api.client import Client
from icinga2 import Icinga2API
from enum import Enum 

class Tag(Enum):
    New = 1
    Modify = 2
    NothingToDo = 3
    Delete = 4

db = mysql.connector.connect(host="172.20.20.74", user="alexylap", password="felix22", database="srtest2") #connexion a la base de donnée 
client = Client('https://172.20.20.73:5665', 'felix', 'felix22') #connexion a l'API REST

def infoBdd():
    
    req=db.cursor()
    req.execute("SELECT * FROM Switches INNER JOIN ConfigSwitches ON Switches.ConfigSwitchId = ConfigSwitches.ConfigSwitchId INNER JOIN Modeles ON Switches.ModeleId = Modeles.ModeleId") # Requete envoyer a la BDD
    reponce= req.fetchall() #Recuperation de tous les information qu'il a pus trouver a la suite de la requete 
    
    for row in reponce:

        idSwitch= row[0]
        nomSwitch = row[8]
        ipNotSplit = row[10] #Recuperation de la colone 9 avec l'ip en CIDR
        ipSplit = ipNotSplit.split('/') #On coupe la variable pour lui dire que nous voulont separé , l'ip et le CIDR
        tag=row[5] #Recuperation de l'information tag ( qui nous dit si le switch a deja été pris en compte null = nouveau , 0 = rien a faire, 1 = doit etre modifier)
        
        print("Information recuperer dans la base de donnée : ")
        print("ID Du Switch : "+ str(idSwitch))
        print("Nom Du Switch :"+ nomSwitch)
        print("Ip : "+ipSplit[0])
        print("Tag : "+str(tag))
        
        relationSwitch(idSwitch, nomSwitch)
        #verifier(nomSwitch, ipSplit[0], tag, idSwitch) #Verification si le switch existe deja sur l'hyperviseur !

def addHost(ip, switch, idSwitch):
    
    req=db.cursor()
    req.execute("UPDATE `Switches` SET `Tag` = 0 WHERE `Switches`.`SwitchId`="+str(idSwitch))
    db.commit()
    client.objects.create('Host', switch, ['generic-host'], {'address': ip}) #Ajout d'un d'un switch avec les information recuperer dans la BDD
    client.actions.restart_process() #Redemarage du service icinga2 pour mettre la map du reseau a jour 

def verifier(switch, ip, tag, idSwitch):
    
    if tag == Tag.New: #Si l'information dans la base de donner vaut 1 cela veut dire qu'il est nouveau et qu'il faut donc le crée
        addHost(ip, switch, idSwitch)
    elif tag == Tag.Modify: # Si Tag est a 2 le switch est a modifier sur icinga2 
        print("Le Switch a été modifier")
        print("=================================")
        delete(idSwitch, switch)
        addHost(ip, switch, idSwitch)
    elif tag == Tag.NothingToDo: #Si tag est  a 3 il n'a pas ete modifier rien a faire
        print("Le Switch n'a pas été modifier")
        print("=================================")
        pass
    elif tag == Tag.Delete:
        delete(idSwitch,switch)
        print("Le Switch"+switch+"a ete surpprimer")
        print("================================")
  
def relationSwitch(idSwitch, switch):
    
    req=db.cursor()
    req.execute("SELECT * FROM Cascades")
    
    client.objects.create('Dependency', switch, ['generic-host'], {'address': ip}) #Ajout d'un d'un switch avec les information recuperer dans la BDD
    
    
    

def delete(idSwitch, switch):
    client.objects.delete('Host', switch) #on supprime le switch a modifier
    
    
    


if __name__ == "__main__":
    infoBdd()
