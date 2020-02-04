import mysql.connector

db = mysql.connector.connect(host="localhost",
                            user="felix",password="felix22",
                            database="srtest2")

cursor =db.cursor()

cursor.execute("SELECT *  FROM switches INNER JOIN configswitches ON switches.ConfigSwitchId = configswitches.ConfigSwitchId INNER JOIN modeles ON switches.ModeleId = modeles.ModeleId")

result = cursor.fetchall()


#print(result)

for row in result:
    
    print("Ip : "+row[8])
    print("Nom : "+row[11])
    print("Marque : "+row[10])
    print("=================")
    
    




    

    



