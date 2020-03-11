#==============================
#Crée par: Le Lay Quentin
#Classe: BTS SN2
#Projet: Supervision reseau
#But: Creation, Modification et Suppresion des hosts et des cascades de switch sur l'hyperviseur Icinga2 grace a son API REST
#===============================

import updateHyperviseur
import icinga2RestApi
import mysql.connector
from icinga2api.client import Client
from enum import Enum

class Tag(Enum):
    New = 0
    Modify = 1
    NothingToDo = 2
    Delete = 3
     
if __name__ == "__main__":
    
    config = updateHyperviseur.LoadConfigFile('config.cfg')
    
    #Information Icinga
    addrIcinga     = config.get("addrIcinga")
    idIcinga       = config.get("idIcinga")
    passwordIcinga = config.get("passwordIcinga")    
    
    #Information BDD
    hostBDD     = config.get("hostBDD")
    userBDD     = config.get("userBDD")
    passwordBDD = config.get("passwordBDD")
    database    = config.get("database")
    
    db     = mysql.connector.connect(host=hostBDD, user=userBDD, password=passwordBDD, database=database) #connexion a la base de donnée 
    client = Client(addrIcinga, idIcinga, passwordIcinga) #connexion a l'API REST

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
        print("Tag : "+str(tag))
        
        if tag == Tag.New.value: #Si l'information dans la base de donner vaut 1 cela veut dire qu'il est nouveau et qu'il faut donc le crée
            
            icinga2RestApi.AddSwitchIcinga(db,client,ipSplit[0],switchName,idSwitch)
            
        elif tag == Tag.Modify.value: # Si Tag est a 1 le switch est a modifier sur icinga2 
            
            icinga2RestApi.icingaDelAllDependency(addrIcinga, idIcinga, passwordIcinga)
            icinga2RestApi.DelAllSwitch(db, addrIcinga, idIcinga, passwordIcinga)
            
            print("Le Switch "+switchName+" a été modifier")
            print("=================================")
            
        elif tag == Tag.NothingToDo.value: #Si tag est  a 3 il n'a pas ete modifier rien a faire
            print("Le Switch n'a pas été modifier")
            print("=================================")
            pass
        elif tag == Tag.Delete.value:
            
            print("Le Switch "+switchName+" a ete surpprimer")
            print("================================")
    
    icinga2RestApi.icingaDelAllDependency(addrIcinga, idIcinga, passwordIcinga)
    icinga2RestApi.icingaAddDependency(db, addrIcinga, idIcinga, passwordIcinga)
    
    client.actions.restart_process() #Redemarage du service icinga2 pour mettre la map du reseau a jour