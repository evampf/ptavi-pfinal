#!/usr/bin/python3

import socketserver
import sys
import time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

CONFIG = sys.argv [1]

if len(sys.argv) != 2:
    sys.exit("Usage: python proxy_registrar.py config")

class XMLHandler(ContentHandler):   

	def __init__(self):
	    self.lista = []
	    self.DicEtiquetas = {
	        'server':['name','ip','data'],
	        'database':['path','passwdpath'],
	        'log':['path']}

	def startElement(self, name, attrs):
	    if name in self.DicEtiquetas:
	        dicc = {}
	        for atributo in self.DicEtiquetas[name]:
	            dicc[atributo] = attrs.get(atributo, "")
	        diccname = {name: dicc}
	        self.lista.append(diccname)

def handle(self):
    while 1:
        line = self.rfile.read()
        LINE = text.decode('utf-8')
        Words_LINES = LINE.split()
        REQUEST = Words_LINES[0]
        print("La peticion es: ", REQUEST)
        print("Listening...")

        if METHOD == "register":
            Message = ("REGISTER sip:" + DIRECCTION + " SIP/2.0\r\n")
            Message += ("Expires: " + EXPIRES + "\r\n\r\n")
            print("Enviando:", Message)

if __name__ == "__main__":
    serv = socketserver.UDPServer((sys.argv[1], ContentHandler))
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")


