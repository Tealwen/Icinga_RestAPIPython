import mysql.connector
import requests
import json
from icinga2api.client import Client
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
        print("===============================================================")
        addHost(ip, switch)

def addHost(ip, switch):

    client = Client('https://172.20.20.73:5665', 'felix', 'felix22')
    client.objects.create(
        'Host',
        switch,
        ['generic-host'],
        {'address': ip})



if __name__ == "__main__":
    connectobdd()