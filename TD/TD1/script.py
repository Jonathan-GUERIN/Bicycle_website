# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:08:25 2020

@author: artco
"""

import sqlite3
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd


regions = [("Rhône Alpes","blue"), ("Auvergne","green"), ("Auvergne-Rhône Alpes","cyan"), ('Bourgogne',"red"), ('Franche Comté','orange'), ('Bourgogne-Franche Comté','olive') ]


conn = sqlite3.connect('ter.db')
c = conn.cursor()


if False: 
    
    requete = c.execute('SELECT DISTINCT Région FROM train;')
    
    for x in requete:
        print(x)


if False: 
    
    requete = c.execute('SELECT DISTINCT ID FROM train;')
    
    for x in requete:
        print(x)


if False: 
    
    requete = c.execute('SELECT ID,Région FROM train GROUP BY Région ORDER BY SUBSTR(ID, 3, 2) ASC;')
    
    for x in requete:
        print(x)
        
if False: 
    
    requete = c.execute('SELECT SUM(Nombredetrainsenretardàlarrivée) FROM train;')
    
    for x in requete:
        print(str(x[0])+' trains en retard')
        
        
if False: 
    
    c.execute('SELECT Date,Tauxderégularité FROM train WHERE ID="TER_20" ORDER BY Date ASC;')
    
    requete = c.fetchall()
    
    x = [pltd.date2num(dt.date(int(a[0][:4]),int(a[0][5:]),1)) for a in requete if not a[1] == ''] 
    y = [float(a[1]) for a in requete if not a[1] == '']
    
    plt.plot_date(x,y,linestyle='dashed')
    plt.grid()
    plt.ylabel('Taux de régularité')
    plt.xlabel('Date')
    
    
if False: 
    
    plt.figure(figsize=(18,4))
    for region in regions:
        c.execute('SELECT Date,Tauxderégularité FROM train WHERE Région="'+str(region[0])+'" ORDER BY Date ASC;')
        
        requete = c.fetchall()
        
        x = [pltd.date2num(dt.date(int(a[0][:4]),int(a[0][5:]),1)) for a in requete if not a[1] == ''] 
        y = [float(a[1]) for a in requete if not a[1] == '']
        
        plt.plot_date(x,y,color=region[1],linestyle='dashed',label=region[0])
    
    plt.ylim(80,100)
    plt.grid()
    plt.legend()
    plt.ylabel('Taux de régularité')
    plt.xlabel('Date')
    plt.title('Taux de régularité TER')
    
    
    