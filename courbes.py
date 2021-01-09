# -*- coding: utf-8 -*-

import sqlite3
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd

conn = sqlite3.connect("donnees/bdd.db")
c = conn.cursor()


# l'utilisateur détermine la date de debut et la date de fin de la courbe 
# ainsi que les stations concernées
# et le pas ( 5 mins par défaut ) multiple de 5 mins
# station := une liste des noms des stations


def creationcourbe(date_deb,date_fin,stats,pas):
    
    plt.figure(figsize=(18,4))
    d=date_deb +'+00:00'
    f=date_fin +'+00:00'
    pas = int(pas) // 5
    strstation =''
    
    c.execute("SELECT commune FROM stations GROUP BY commune HAVING COUNT(*) > 15 ORDER BY commune ASC;")
    r=c.fetchall()
    arrs=[a[0].strip() for a in r]
    S=[]
    for s in stats:
        if s in arrs:
            c.execute("SELECT nom FROM stations WHERE commune='"+str(s)+"'")
            R=c.fetchall()
            L=[elt[0] for elt in R ]
            S=S+L
        else:
            S.append(s)
            
    stations=list(set(S))     #supprimer des éventuels doublons  
    
    
    idstation = []
    for station in stations:
        
        c.execute("SELECT DISTINCT idstation,nbbornette FROM stations WHERE nom = '"+str(station)+"';")
        requete = c.fetchall()
        idstation.append((requete[0][0],station,requete[0][1]))
        strstation = strstation + str(station)

    for i in range(len(idstation)):
        c.execute("SELECT time_ISO,bikes FROM historique WHERE velov_number='velov-"+str(idstation[i][0])+"' AND time_ISO > '"+d+"' and time_ISO<'"+f+"' ORDER BY time_ISO;")
        requete = c.fetchall()

        x = [pltd.date2num(dt.datetime(int(a[0][:4]),int(a[0][5:7]),int(a[0][8:10]),int(a[0][11:13]),int(a[0][14:16]),1)) for a in requete if not a[1] == ''] 
        y = [float(a[1]/idstation[i][2])*100 for a in requete if not a[1] == '']
 

        x_pas=[x[pas*i] for i in range(int(len(x)//pas))] 
        y_pas=[y[pas*i] for i in range(int(len(y)//pas))]
        plt.plot_date(x_pas,y_pas,linestyle='dashed',label=idstation[i][1])

    
    c.execute("SELECT id from cache ORDER BY id DESC LIMIT 1")
    req = c.fetchall()
    print(req)
    if req == []:
        id = 1
    else:
        id = req[0][0]+1
    
    alt = '_'.join([str(s) for s in stations])

    plt.grid()
    plt.legend()
    
    plt.ylabel("Taux de disponibilité")
    plt.xlabel("Date")
    plt.title("Taux de disponibilité des vélo'v")
    
    #enregistrement du graphique
    link=str(id)+'.jpg'
    plt.savefig('client/images/graphes/'+link)


    return link,alt



