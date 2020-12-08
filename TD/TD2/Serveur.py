# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 10:36:34 2020

@author: artco
"""

import http.server
import socketserver
import sqlite3
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd
conn = sqlite3.connect('ter.db')
c = conn.cursor()



class HTTPRequest(http.server.SimpleHTTPRequestHandler):
        
    def do_GET(self):
        
        if self.path == '/time':
            self.send_time()
            
        elif self.path == '/regions':
            self.send_regions()
            
        elif self.path == '/ponctualite':
            self.send_graph()
        
        else:
            print(self.path)
            self.path = '/client' + self.path
            http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def send(self,body,headers=[]):
    
        # on encode la chaine de caractères à envoyer
        encoded = bytes(body, 'UTF-8')
    
        # on envoie la ligne de statut
        self.send_response(200)
    
        # on envoie les lignes d'entête et la ligne vide
        [self.send_header(*t) for t in headers]
        self.send_header('Content-Length',int(len(encoded)))
        self.end_headers()
    
        # on envoie le corps de la réponse
        self.wfile.write(encoded)
        
    def send_time(self):
        
        time = self.date_time_string()
        
        body = "<!doctype html><meta charset='utf-8'><title>Heure</title><h2>Heure du serveur</h2><p>"+time+"</p>"
        headers = [('Content-Type','text/html;charset=utf-8')]
        
        self.send(body,headers)
        
    def send_regions(self):
        
        body = "<!doctype html><meta charset='utf-8'><title>Régions</title><h2>Liste des régions désservis : </h2>"
        requete = c.execute('SELECT DISTINCT Région FROM train;')
        for x in requete:
            body = body + '<p>' + str(x[0]) + '</p>'
        headers = [('Content-Type','text/html;charset=utf-8')]
        
        self.send(body,headers)
    
    def send_graph(self):
        
        body = "<!doctype html><meta charset='utf-8'><title>Graph</title>"
        body = body + '<img src=/images/TD2-courbe1.png></img>'
        headers = [('Content-Type','text/html;charset=utf-8')]
        
        self.send(body,headers)

PORT = 8081

Handler = HTTPRequest

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
    