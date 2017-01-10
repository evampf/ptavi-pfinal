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

try:    
    CONFIG = sys.argv [1]
    if len(sys.argv) != 2:
        sys.exit("Usage: python proxy_registrar.py config")
except IndexError:
        sys.exit("Usage: python3 proxy.registrar.py config")

class XMLHandler(ContentHandler):   

    def __init__(self):
        self.lista = []
        self.DicEtiquetas = {
                            'server': ['name','ip','puerto'],
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
    
#Saca el contenido del fichero XML 
parser = make_parser()
cHandler = XMLHandler()
parser.setContentHandler(cHandler)
parser.parse(open(CONFIG))
PROXY = cHandler.get_tags()

#Mete los valores del XML en variables
SERVER_NAME = PROXY[0]['server']['name']
SERVER_IP = PROXY[0]['server']['ip']
SERVER_PUERTO = PROXY[0]['server']['puerto']
PATH_DATABASE = PROXY[1]['database']['path']
PASSWD_DATABASE = PROXY[1]['database']['passwdpath']
PATH_LOG = PROXY[2]['log']['path']

class SIPProxyRegisterHandler(socketserver.DatagramRequestHandler):

    dicc_clientes = {}

    def register2json(self):
    
        json_file = open("registered.json", "w")
        json.dump(self.dicc_clientes, json_file, separators=(',', ': '), indent=4)
        json_file.close()
        print(dicc_clientes)

    def handle(self):
        #while 1:
            text = self.rfile.read()
            data_text = text.decode('utf-8')
            METHOD = data_text.split(' ')[0].upper()
            Dir_IP = self.client_address[0]
            Puerto = self.client_address[1]
            Expires = int(data_text[data_text.find("Expires: ") + 9: data_text.find("\r\n\r\n")])
            print("La peticion es: ", METHOD)
            print("Listening...")

            if METHOD == "REGISTER":
                #Sin autenticación
                LINEA = "REGISTER sip: " + ":" + " SIP/2.0\r\n" + "Expires: " + "\r\n"
                Time_Exp = Expires + int(time.time())
                Dir_IP = self.client_address[0]
                str_ex = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(Time_Exp))
                if Expires == 0:
                    del self.dicc_clientes[Dir_IP]
                    self.register2json()
                elif Expires > 0:
                    self.dicc_clientes[data_text] = {'address': Dir_IP, 'Expires': str_ex}
                    self.register2json()
                
                self.wfile.write(b" SIP/2.0 200 OK\r\n\r\n")
                

            elif METHOD == "INVITE":
                LINEA = "INVITE sip: " + " SIP/2.0\r\n" + "Content-Type: application/sdp\r\n\r\n" + "v=0\r\n" + "o = "
                LINEA += " " + "\r\n" + "s=misesion\r\n" + "t=0\r\n" + "m = audio" + " RTP\r\n"

            elif METHOD == "BYE":
                LINEA = "BYE sip: " + " SIP/2.0\r\n"

            else:
                print("Mal")




if __name__ == "__main__":

    msgprox = 'server ' + SERVER_NAME + ' listening at port '
    msgprox += SERVER_PUERTO + '...' + '\r\n'
    print (msgprox)

    PORT = int(SERVER_PUERTO)
    IP = SERVER_IP
    serv = socketserver.UDPServer((IP,PORT),SIPProxyRegisterHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        sys.exit("Finish")