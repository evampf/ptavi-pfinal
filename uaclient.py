#!/usr/bin/python3

import socket
import sys
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


CONFIG = sys.argv[1]
METHOD = sys.argv [2].upper()
OPCION = sys.argv [3]

if len(sys.argv) != 4:
    sys.exit("Usage: python client.py config method option")



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
print ("Llego aqui")	        

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    if METHOD == "register":
        Message = ("REGISTER sip:" + DIRECCTION + " SIP/2.0\r\n")
        Message += ("Expires: " + EXPIRES + "\r\n\r\n")
        print("Enviando:", Message)
    print("Aqui tambien")

