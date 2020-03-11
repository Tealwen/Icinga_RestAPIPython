import configparser
import mysql.connector
import icinga2RestApi

from datetime import datetime
from icinga2api.client import Client
from enum import Enum

class Tag(Enum):
    New = 0
    Modify = 1
    NothingToDo = 2
    Delete = 3

def LoadConfigFile(file):
    
    cfg = configparser.ConfigParser()
    cfg.read(file)
    
    config = {}
    
    #Recuperation Information Icinga2 Dans Le Fichier De Config
    config["addrIcinga"]      = cfg.get('Icinga2', 'address')
    config["idIcinga"]        = cfg.get('Icinga2', 'id')
    config["passwordIcinga"]  = cfg.get('Icinga2', 'password')
    
    #Recuperation Information BDD Dans Le Fichier De Config
    config["hostBDD"]         = cfg.get('BDD', 'host')
    config["userBDD"]         = cfg.get('BDD', 'user')
    config["passwordBDD"]     = cfg.get('BDD', 'password')
    config["database"]        = cfg.get('BDD', 'database')
    
    return config
    
"""def GetSwitchInfoInBDD(db):

    req = db.cursor()
    req.execute("SELECT SwitchId,NomSwitch,Tag,AdIpCidr FROM Switches INNER JOIN ConfigSwitches ON Switches.ConfigSwitchId = ConfigSwitches.ConfigSwitchId INNER JOIN Modeles ON Switches.ModeleId = Modeles.ModeleId") # Requete envoyer a la BDD
    
    reponce = req.fetchall()                    #Recuperation de tous les information qu'il a pus trouver a la suite de la requete 
    
    for row in reponce:
        
        idSwitch    = row[0]                    #Recuperation de l'id du switch
        switchName  = row[1]                    #Recuperation du nom du switch
        tag         = row[2]                    #Recuperation de l'information tag ( qui nous dit si le switch a deja été pris en compte null = nouveau , 0 = rien a faire, 1 = doit etre modifier)
        ipNotSplit  = row[3]                    #Recuperation de la colone 9 avec l'ip en CIDR
        ipSplit     = ipNotSplit.split('/')     #On coupe la variable pour lui dire que nous voulont separé , l'ip et le CIDR
        
        #Affichage des informations dans le terminal avec la date, str() pour afficher les valeur comme chaine de caractere
        print("Information recuperer dans la base de donnée : ") 
        print("ID Du Switch : "+ str(idSwitch))
        print("Nom Du Switch :"+ switchName)
        print("Ip : "+ipSplit[0])
        print("Tag : "+str(tag))"""
        
        
        
   
        