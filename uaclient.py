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


CONFIG = sys.argv[1]
METHOD = sys.argv[2].upper()
OPCION = sys.argv[3]
print(CONFIG)

class UACLIENT(ContentHandler):
    	
	if len(sys.argv) != 4:
		sys.exit("Usage: python client.py config method option")

    
	def __init__(self):
		self.lista = []
		self.DicEtiquetas = {
			'account': ['username', 'passwd'],
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

	def get_tags(self):
		return self.lista 

#Saca el contenido del fichero XML 
parser = make_parser()
cHandler = UACLIENT()
parser.setContentHandler(cHandler)
parser.parse(open(CONFIG))
UACLIENT = cHandler.get_tags()

#Mete los valores del XML en variables
ACCOUNT_USERNAME = UACLIENT[0]['account']['username']
ACCOUNT_PASSWD = UACLIENT[0]['account']['passwd']
IP_SERVER = UACLIENT[1]['uaserver']['ip']
PUERTO_SERVER = UACLIENT[1]['uaserver']['puerto']
AUDIO_PUERTO = UACLIENT[2]['rtpaudio']['puerto']
PROXY_IP = UACLIENT[3]['regproxy']['ip']
PROXY_PUERTO = UACLIENT[3]['regproxy']['puerto']
LOG_PATH = UACLIENT[4]['log']['path']
AUDIO_PATH = UACLIENT[5]['audio']['path']


if __name__ == "__main__":

	
	if METHOD == "REGISTER":
    #Sin autenticación
		LINEA = "REGISTER sip: " + ACCOUNT_USERNAME + ": " + PUERTO_SERVER + " SIP/2.0\r\n" + "Expires: " + OPCION + "\r\n"
		print(LINEA)
		my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		my_socket.connect((PROXY_IP, int(PROXY_PUERTO)))
		my_socket.send(bytes(LINEA, 'utf-8') + b'\r\n')
		data = my_socket.recv(1024)
		print(data.decode('utf-8'))

	if METHOD == "INVITE":
		LINEA = "INVITE sip: " + OPCION + " SIP/2.0\r\n" + "Content-Type: application/sdp\r\n\r\n" + "v=0\r\n" + "o = "
		LINEA += ACCOUNT_USERNAME + " " + IP_SERVER + "\r\n" + "s=misesion\r\n" + "t=0\r\n" + "m = audio" 
		LINEA += AUDIO_PUERTO + " RTP\r\n"
		print(LINEA)
	if METHOD == "BYE":
		LINEA = "BYE sip: " + OPCION + " SIP/2.0\r\n"
