import mysql.connector
import json
from icinga2api.client import Client
from icinga2 import Icinga2API


db = mysql.connector.connect(host="127.0.0.1", user="felix", password="felix22", database="srtest2") #connexion a la base de donnée 
client = Client('https://172.20.20.73:5665', 'felix', 'felix22') #connexion a l'API REST

def infoBdd():
    
    req=db.cursor()
    req.execute("SELECT * FROM switches INNER JOIN configswitches ON switches.ConfigSwitchId = configswitches.ConfigSwitchId INNER JOIN modeles ON switches.ModeleId = modeles.ModeleId") # Requete envoyer a la BDD
    reponce= req.fetchall() #Recuperation de tous les information qu'il a pus trouver a la suite de la requete 

    for row in reponce:

        idSwitch= row[0]
        ip = row[10] #Recuperation de la colone 8 avec l'ip
        switch = row[13]+"_"+row[12] #Recuperation de la colone 11 et 10 contenant la marque et le nom du switch
        tag=row[7] #Recuperation de l'information tag
        print("Information recuperer dans le base de donnée : ")
        print("ID Du Switch : "+ str(idSwitch))
        print("Ip : "+ip)
        print("Switch : "+switch)
        print("Tag : "+str(tag))
        verifier(switch, ip, tag, idSwitch) #Verification si le switch existe deja sur l'hyperviseur !
        

    

def addHost(ip, switch, idSwitch):
    
    
    req=db.cursor()
    req.execute("UPDATE `switches` SET `Tag` = 0 WHERE `switches`.`SwitchId`="+str(idSwitch))
    db.commit()
    client.objects.create('Host', switch, ['generic-host'], {'address': ip}) #Ajout d'un d'un switch avec les information recuperer dans la BDD


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
        update(switch,ip,tag)
        
def update(switch,ip,tag):
    
    client.objects.update(
        'Host',
        switch,
        {'address': ip}
    )



"""def relationSwitch():
    
    req.execute("SELECT")"""


    

    


if __name__ == "__main__":
    infoBdd()