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


def creationcourbe(date_deb,date_fin,stations,pas):
    
    plt.figure(figsize=(18,4))
    d=date_deb +'+00:00'
    f=date_fin +'+00:00'
    pas = int(pas) // 5
    idstation = []
    for station in stations:
        
        c.execute("SELECT DISTINCT idstation,nbbornette FROM stations WHERE nom = '"+str(station)+"';")
        requete = c.fetchall()
        idstation.append((requete[0][0],station,requete[0][1]))

    for i in range(len(idstation)):
        c.execute("SELECT time_ISO,bikes FROM historique WHERE velov_number='velov-"+str(idstation[i][0])+"' AND time_ISO > '"+d+"' and time_ISO<'"+f+"' ORDER BY time_ISO;")
        requete = c.fetchall()

        x = [pltd.date2num(dt.datetime(int(a[0][:4]),int(a[0][5:7]),int(a[0][8:10]),int(a[0][11:13]),int(a[0][14:16]),1)) for a in requete if not a[1] == ''] 
        y = [float(a[1]/idstation[i][2])*100 for a in requete if not a[1] == '']
        
        x_pas=[x[pas*i] for i in range(int(len(x)//pas))]
        
        y_pas=[y[pas*i] for i in range(int(len(y)//pas))]
        plt.plot_date(x_pas,y_pas,linestyle='dashed',label=idstation[i][1])


    alt = '_'.join([str(s) for s in stations])

    #nettoyage chane pour eviter bug d'enregistrement
    string = alt.split(' ')
    stations = ''.join([str(s) for s in string])

    string = stations.split('/')
    stations = ''.join([str(s) for s in string])

    plt.grid()
    plt.legend()
    
    plt.ylabel("Taux de disponibilité")
    plt.xlabel("Date")
    plt.title("Taux de disponibilité des vélo'v")
    
    string= date_deb[:13]+date_fin[:13]+str(pas)
    string=string + stations
    string = string +'.jpg'
    plt.savefig('client/images/graphes/'+string)
    
    return string,alt

#creationcourbe('2020-11-15T04:00:00','2020-11-16T05:00:00',['CROUS','Gailleton'],'5 minutes')



