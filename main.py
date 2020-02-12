import mysql.connector
import json
from icinga2api.client import Client
from icinga2 import Icinga2API


db = mysql.connector.connect(host="172.20.20.74", user="alexylap", password="felix22", database="srtest2") #connexion a la base de donnée 
client = Client('https://172.20.20.73:5665', 'felix', 'felix22') #connexion a l'API REST

def infoBdd():
    
    req=db.cursor()
    req.execute("SELECT * FROM Switches INNER JOIN ConfigSwitches ON Switches.ConfigSwitchId = ConfigSwitches.ConfigSwitchId INNER JOIN Modeles ON Switches.ModeleId = Modeles.ModeleId") # Requete envoyer a la BDD
    reponce= req.fetchall() #Recuperation de tous les information qu'il a pus trouver a la suite de la requete 

    for row in reponce:

        idSwitch= row[0]
        ipNotSplit = row[9] #Recuperation de la colone 9 avec l'ip en CIDR
        ipSplit = ipNotSplit.split('/') #On coupe la variable pour lui dire que nous voulont separé , l'ip et le CIDR
        switch = row[13]+"_"+row[12] #Recuperation de la colone 11 et 10 contenant la marque et le nom du switch
        tag=row[7] #Recuperation de l'information tag ( qui nous dit si le switch a deja été pris en compte null = nouveau , 0 = rien a faire, 1 = doit etre modifier)
        
        print("Information recuperer dans la base de donnée : ")
        print("ID Du Switch : "+ str(idSwitch))
        print("Ip : "+ipSplit[0])
        print("Switch : "+switch)
        print("Tag : "+str(tag))
        
        verifier(switch, ipSplit[0], tag, idSwitch) #Verification si le switch existe deja sur l'hyperviseur !

def addHost(ip, switch, idSwitch):
    
    
    req=db.cursor()
    req.execute("UPDATE `Switches` SET `Tag` = 0 WHERE `Switches`.`SwitchId`="+str(idSwitch))
    db.commit()
    client.objects.create('Host', switch, ['generic-host'], {'address': ip}) #Ajout d'un d'un switch avec les information recuperer dans la BDD
    client.actions.restart_process() #Redemarage du service icinga2 pour mettre la map du reseau a jour 


def verifier(switch, ip, tag, idSwitch):
    
    if tag == None: #Si tag est a null cela veut dire qu'il est nouveau et qu'il faut donc le crée
        addHost(ip, switch, idSwitch)
    elif tag == 0: #Si tag est  a 0 il n'a pas ete modifier rien a faire
        print("Le Switch n'a pas été modifier")
        print("=================================")
        pass
    elif tag == 1: # Si Tag est a 1 le switch est a modifier sur icinga2 
        print("Le Switch a été modifier")
        print("=================================")
        client.objects.delete('Host', switch)
        addHost(ip, switch, idSwitch)
        
"""def relationSwitch():
    
    req.execute("SELECT")"""


if __name__ == "__main__":
    infoBdd()