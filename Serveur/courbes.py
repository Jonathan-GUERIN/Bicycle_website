# -*- coding: utf-8 -*-

import sqlite3
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd


conn = sqlite3.connect('donnees/bdd.db')
c = conn.cursor()

def creationcourbe(stations):
    
    plt.figure(figsize=(18,4))
    for station in stations:
        c.execute('SELECT Date,Tauxderégularité FROM train WHERE Région="'+str(station)+'" ORDER BY Date ASC;')
        
        requete = c.fetchall()
        
        x = [pltd.date2num(dt.date(int(a[0][:4]),int(a[0][5:]),1)) for a in requete if not a[1] == ''] 
        y = [float(a[1]) for a in requete if not a[1] == '']
        
        plt.plot_date(x,y,linestyle='dashed',label=station)
    
    plt.ylim(80,100)
    plt.grid()
    plt.legend()
    plt.ylabel('Taux de régularité')
    plt.xlabel('Date')
    plt.title('Taux de régularité TER')
    string= 'images/'
    for station in stations:
        string = string + station
    string = string +'.jpg'
    plt.savefig('client/'+string)
    return string


