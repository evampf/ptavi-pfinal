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

class UACLIENT():
    	
	try:
		CONFIG = sys.argv[1]
		METHOD = sys.argv[2].upper()
		OPCION = sys.argv[3]
	except Exception:
		sys.exit('Usage: python client.py config method option')

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
CONFIG = sys.argv[1]
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
AUDIO_IP = UACLIENT[2]['rtpaudio']['ip']
PROXY_IP = UACLIENT[3]['regproxy']['ip']
PROXY_PUERTO = UACLIENT[3]['regproxy']['puerto']
LOG_PATH = UACLIENT[4]['log']['path']
AUDIO_PATH = UACLIENT[5]['audio']['path']


if __name__ == "__main__":

	if METHOD == REGISTER:
    #Sin autenticación
		LINEA = "REGISTER sip: " + ACCOUNT_USERNAME + ":" + PUERTO_SERVER + " SIP/2.0\r\n" + "Expires: " + OPCION + "\r\n"
		print(LINEA)


	my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	my_socket.connect((PROXY_IP, int(PROXY_PUERTO)))
	#my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
	PROXY = UACLIENT(PROXY_IP) + ':' + UA(PROXY_PUERTO)


