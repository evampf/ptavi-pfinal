#!/usr/bin/python3

from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import socketserver
import socket
import sys
import time
import json
import hashlib
import random

class XMLHandler(ContentHandler):   

    def __init__(self):
        self.lista = []
        self.DicEtiquetas = {
                            'server': ['name','ip','data'],
                            'database': ['path','passwdpath'],
                            'log': ['path']}

    def startElement(self, name, attrs):
        if name in self.DicEtiquetas:
            dicc = {}
            for atributo in self.DicEtiquetas[name]:
                dicc[atributo] = attrs.get(atributo, "")
            diccname = {name: dicc}
            self.lista.append(diccname)

    def get_tags(self):
        return self.lista     


class SIPProxyRegisterHandler(socketserver.DatagramRequestHandler):

    dicc_clientes = {}
    nonce_dicc = {}


    def handle(self):
        while 1:
            line = self.rfile.read()
            data_text = text.decode('utf-8')
            Words_datas = data_text.split()
            REQUEST = Words_datas[0]
            Dir_IP = self.client_address[0]
            Puerto = self.client_address[1]
            print("La peticion es: ", REQUEST)
            print("Listening...")
            if not line:
                break

            if REQUEST == "register":
                Message = ("REGISTER sip:" + DIRECCTION + " SIP/2.0\r\n")
                Message += ("Expires: " + EXPIRES + "\r\n\r\n")
                user = data_text[1].split(':')[1]
                print("Enviando:", Message)
def PORTValid(port):
    try:
        Puerto = int(port)
    except ValueError:
        sys.exit("El puerto debe ser integer")
    return Puerto

if __name__ == "__main__":

    try:    
        CONFIG = sys.argv [1]
        if len(sys.argv) != 2:
            sys.exit("Usage: python proxy_registrar.py config")
    except IndexError:
        sys.exit("Usage: python3 proxy.registrar.py config")

    #Saca el contenido del fichero XML 
    parser = make_parser()
    cHandler = XMLHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(CONFIG))
    PROXY = cHandler.get_tags()

    #Mete los valores del XML en variables
    #SERVER_NAME = PROXY['server_name']
    #SERVER_IP = config['server_ip']
    #SERVER_PUERTO = config['server_puerto']
    #PATH_DATABASE = config[1]['database']['path']
    #PASSWD_DATABASE = config[1]['database']['passwdpath']
    #PATH_LOG = config[2]['log']['path']

    #fichero = open(PATH_DATABASE, "a")
    #fichero.close()


    
    #msgprox = 'server' + SERVER_NAME + 'listening at port'
    #msgprox = SERVER_PUERTO + '...' + '\r\n'
    #print ('msgprox')

    PORT = PORTValid(PROXY['server_puerto'])
    IP = '127.0.0.1'
    serv = socketserver.UDPServer((IP,PORT),SIPProxyRegisterHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        sys.exit("Finish")