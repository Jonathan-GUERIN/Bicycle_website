# -*- coding: utf-8 -*-

import sqlite3
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd

conn = sqlite3.connect("donnees/bdd.db")
c = conn.cursor()


# l'utilisateur détermine la date de debut et la date de fin de la courbe 
# ainsi que les stations concernées(par des cases à cocher par exemple) 
# et le pas ( 5 mins par défaut ) multiple de 5 mins
# station := une liste des id des stations


def creationcourbe(date_deb,date_fin,stations,pas):
    
    plt.figure(figsize=(18,4))
    d=date_deb.isoformat()
    f=date_fin.isoformat()
    
    for station in stations:
        c.execute("SELECT time_ISO,bikes FROM historique WHERE velov_number='velov-'+{} and time_ISO>{} and time_ISO<{} ORDER BY time_ISO".format(str(station),d,f))
        
        requete = c.fetchall()
        
        x = [pltd.date2num(dt.date(int(a[0][:4]),int(a[0][5:]),1)) for a in requete if not a[1] == ''] 
        y = [float(a[1]) for a in requete if not a[1] == '']
        
        plt.plot_date(x,y,linestyle='dashed',label=station)

    plt.ylim(80,100)
    plt.grid()
    plt.legend()
    plt.ylabel("Taux de disponibilité")
    plt.xlabel("Date")
    plt.title("Taux de disponibilité des vélo'v")
    string= 'images/'+date_deb+date_fin+pas
    ch='_'.join([chr(s) for s in stations])
    string = string +'.jpg'
    plt.savefig('client/'+string)
    return string


