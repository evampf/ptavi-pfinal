#!/usr/bin/python3

import socketserver
import sys
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


if METHOD == "register":
    Message = ("REGISTER sip:" + DIRECCTION + " SIP/2.0\r\n")
    Message += ("Expires: " + EXPIRES + "\r\n\r\n")
    print("Enviando:", Message)

if __name__ == "__main__":
    serv = socketserver.UDPServer((sys.argv[1], int(sys.argv[2])), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")


