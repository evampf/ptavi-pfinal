#!/usr/bin/python3

import socketserver
import sys
import os
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

CONFIG = sys.argv [1]

if len(sys.argv) != 2:
    sys.exit("Usage: python uaserver.py config")

class XMLHandler(ContentHandler):   

	def __init__(self):
	    self.lista = []
	    self.DicEtiquetas = {
	        'account': ['userame', 'passwd'],
	        'uaserver':['ip','puerto'],
	        'rtpaudio':['puerto'],
	        'regproxy':['ip','puerto'],
	        'log':['path'],
	        'audio':['path']}

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
			print("El cliente nos manda " + text.decode('utf-8'))
			LINE = text.decode('utf-8')
			Words_LINES = LINE.split()
			REQUEST = Words_LINES[0]
			print("La peticion es: ", REQUEST)
			print("Listening...")

if __name__ == "__main__":
	serv = socketserver.UDPServer(('', 6001), XMLHandler)
	print("Lanzando servidor UDP de eco...")
	try:
		serv.serve_forever()
	except KeyboardInterrupt:
		print("Finalizado servidor")
