# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 01:01:31 2020

@author: LENOVO
"""

import matplotlib.pyplot as pt
import sqlite3 as sq
import datetime as dte
import matplotlib.dates as ptdte




# l'utilisateur détermine la date de debut et la date de fin de la courbe 
# ainsi que les stations concernées(par des cases à cocher par exemple) 
# et le pas ( 5 mins par défaut ) multiple de 5 mins
# station := une liste des id des stations

def tracer_courbes_disp_velos(date_deb,date_fin,stations,pas):
    con=sq.connect('donnees/bdd.bd')
    cur=con.cursor()
    d=date_deb.isoformat()
    f=date_fin.isoformat()
    
    for s in stations :
        cur.execute("SELECT time_ISO,bikes FROM historique WHERE velov_number='velov-'+{} and time_ISO>{} and time_ISO<{} ORDER BY time_ISO".format(str(s),d,f))
        l=cur.fetchall()

        L=[l[i][1]for i in range(0,pas/5,len(l))]   
        T=[l[i][0] for i in range(0,pas/5,len(l))]
        pt.plot(T,L,label=s)
        
    
    pt.grid()
    pt.legend()
    pt.xlabel('Date')
    pt.ylabel('Nombre de vélos disponibles par station')
    pt.title('Disponibilité des vélos dans les stations choisies')
    
    ch='_'.join([chr(s) for s in stations])
    ch=ch+'.jpg'
    pt.savefig(ch)
    
        
        
        
            
    
    