import mysql.connector
import requests
import json
from icinga2api.client import Client
from icinga2 import Icinga2API

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #Suppression des warnings lié au fait que l'on est un certificat ssl non valide 

def connectobdd():

    db = mysql.connector.connect(host="127.0.0.1", user="felix", password="felix22", database="srtest2") #connexion a la base de donnée 
    req=db.cursor() #Creation d'une variable pour envoyer la requete a la BDD
    req.execute("SELECT *  FROM switches INNER JOIN configswitches ON switches.ConfigSwitchId = configswitches.ConfigSwitchId INNER JOIN modeles ON switches.ModeleId = modeles.ModeleId") # Requete envoyer a la BDD
    reponce= req.fetchall() #Recuperation de tous les information qu'il a pus trouver a la suite de la requete 

    for row in reponce:

        ip = row[8] #Recuperation de la colone 8 avec l'ip
        switch = row[11]+"_"+row[10] #Recuperation de la colone 11 et 10 contenant la marque et le nom du switch

        print("Information recuperer dans le base de donnée : ")
        print("Ip : "+ip)
        print("Switch : "+switch)
        verifier(switch, ip) #Verification si le switch existe deja sur l'hyperviseur !
        

    db.close()

def addHost(ip, switch):

    client = Client('https://172.20.20.73:5665', 'felix', 'felix22') #connexion a l'API REST
    client.objects.create('Host', switch, ['generic-host'], {'address': ip}) #Ajout d'un d'un switch avec les information recuperer dans la BDD






def verifier(switch, ip):

    api = Icinga2API(username="felix", password="felix22", url="https://172.20.20.73:5665") #Connexion a l'API REST
    
    if api.hosts.exists(switch) == True: #ON verifie sur le switch existe grace a l'api qui nous repondra True ou False
        print("[Iconga2] - Le Switch Existe Déja") 
        print("===============================================================")
        pass # Si c'est true on ne fait rien
    else:
        print("[Icinga2] - Le Switch N'existe Pas")
        print("===============================================================")
        addHost(ip, switch) #sinon on envoie les infos a la fonction ADDHOST !

    

if __name__ == "__main__":
    connectobdd()