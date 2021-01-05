import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import json
import sqlite3
import courbes

conn = sqlite3.connect('donnees/bdd.db')
c = conn.cursor()
port = 8080

# définition du handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):

  # sous-répertoire racine des documents statiques
  static_dir = '/client'


  # on surcharge la méthode qui traite les requêtes GET
  def do_GET(self):
    self.init_params()

    # renvoie toute les stations
    if self.path_info[0] == 'stations':
        self.send_stations()
    
    # liste des stations dans le chemin d'accès
    elif self.path_info[0] == "courbe":
      self.send_courbe(self.params['stations'][0],self.params['pas'][0],self.params['datedebut'][0],self.params['datefin'][0])

    # requête générique
    elif self.path_info[0] == "service":
      self.send_html('<p>Path info : <code>{}</p><p>Chaîne de requête : <code>{}</code></p>' \
          .format('/'.join(self.path_info),self.query_string));

    else:
      self.send_static()


  # méthode pour traiter les requêtes HEAD
  def do_HEAD(self):
      self.send_static()


  # méthode pour traiter les requêtes POST
  def do_POST(self):
    self.init_params()
      
    # requête générique
    if self.path_info[0] == "service":
      self.send_html(('<p>Path info : <code>{}</code></p><p>Chaîne de requête : <code>{}</code></p>' \
          + '<p>Corps :</p><pre>{}</pre>').format('/'.join(self.path_info),self.query_string,self.body));

    else:
      self.send_error(405)

   
    # renvoie la courbe des stations 
  def send_courbe(self,stations,pas,datdeb,datfin):
      
    liststations = stations.split(',')
    liststations.sort()
    liststations = [stat for stat in liststations if not stat == '']
  
#    c.execute("SELECT lien,alt FROM cache WHERE stations =\'"+strstation+"\' AND pas = '"+pas+"' AND datedebut = '"+datdeb[:13]+"' AND datefin = '"+datfin[:13]+"';")
#    r = c.fetchall()
#    print(r)
#    if len(r) !=0:
#        link,alt = r[0]
#    else:
#        print(datdeb,datfin,liststations,pas)
#        link,alt = courbes.creationcourbe(datdeb,datfin,liststations,pas)

    link,alt = courbes.creationcourbe(datdeb,datfin,liststations,pas)
    body = json.dumps({"linkimg": link,"alt":alt})
    headers = [('Content-Type','application/json')]
    self.send(body,headers)
    
    # renvoie toute les stations

  def send_stations(self):
    
    c.execute("SELECT nom, Y, X FROM stations WHERE ouverte = 'Oui';")
    r = c.fetchall()
    
    headers = [('Content-Type','application/json')];
    body = json.dumps([{'nom':n, 'lat':lat, 'lon': lon} for (n,lat,lon) in r])
    self.send(body,headers)

  # on envoie le document statique demandé
  def send_static(self):

    # on modifie le chemin d'accès en insérant le répertoire préfixe
    self.path = self.static_dir + self.path

    # on appelle la méthode parent (do_GET ou do_HEAD)
    # à partir du verbe HTTP (GET ou HEAD)
    if (self.command=='HEAD'):
        http.server.SimpleHTTPRequestHandler.do_HEAD(self)
    else:
        http.server.SimpleHTTPRequestHandler.do_GET(self)


  # on envoie un document html dynamique
  def send_html(self,content):
      headers = [('Content-Type','text/html;charset=utf-8')]
      html = '<!DOCTYPE html><title>{}</title><meta charset="utf-8">{}' \
          .format(self.path_info[0],content)
      self.send(html,headers)


  # on envoie la réponse
  def send(self,body,headers=[]):
     encoded = bytes(body, 'UTF-8')

     self.send_response(200)

     [self.send_header(*t) for t in headers]
     self.send_header('Content-Length',int(len(encoded)))
     self.end_headers()

     self.wfile.write(encoded)



  #     
  # on analyse la requête pour initialiser nos paramètres
  #
  def init_params(self):
    # analyse de l'adresse
    info = urlparse(self.path)
    self.path_info = [unquote(v) for v in info.path.split('/')[1:]]  # info.path.split('/')[1:]
    self.query_string = info.query
    self.params = parse_qs(info.query)

    # récupération du corps
    length = self.headers.get('Content-Length')
    ctype = self.headers.get('Content-Type')
    if length:
      self.body = str(self.rfile.read(int(length)),'utf-8')
      if ctype == 'application/x-www-form-urlencoded' : 
        self.params = parse_qs(self.body)
    else:
      self.body = ''
   
    # traces
    print('info_path =',self.path_info)
    print('body =',length,ctype,self.body)
    print('params =', self.params)


# instanciation et lancement du serveur
print('Le serveur est lancé sur le port : ' + str(port))
httpd = socketserver.TCPServer(("", port), RequestHandler)
httpd.serve_forever()