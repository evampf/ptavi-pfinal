#!/usr/bin/python3
# -*- coding: utf-8 -*-


from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import socketserver
import socket
import sys
import time
import json
import hashlib
import random
import os


CONFIG = sys.argv[1]
METHOD = sys.argv[2].upper()
OPCION = sys.argv[3]
print(CONFIG)

def FICH_LOG(Evento):
    
    fichero = open('LogUaClient.txt', 'a+')
    HoraActual = time.gmtime(time.time())
    HoraActual = time.strftime('%Y%m%d%H%M%S', HoraActual)
    fichero.write(str(HoraActual) + ' ' + Evento + '\r\n')

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

		LINEA = "REGISTER sip: " + ACCOUNT_USERNAME + ": " + PUERTO_SERVER + " SIP/2.0\r\n" + "Expires: " + OPCION + "\r\n"
		print(LINEA)
		my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		my_socket.connect((PROXY_IP, int(PROXY_PUERTO)))
		my_socket.send(bytes(LINEA, 'utf-8') + b'\r\n')
		data = my_socket.recv(1024)
		print(data.decode('utf-8'))
		Evento = 'Sent to ' + PROXY_IP + ':' + PROXY_PUERTO + ': ' + LINEA
		FICH_LOG(Evento)

	
	if METHOD == "INVITE":
		LINEA = "INVITE sip: " + OPCION + " SIP/2.0\r\n" + "Content-Type: application/sdp\r\n\r\n" + "v=0\r\n" + "o="
		LINEA += ACCOUNT_USERNAME + " " + IP_SERVER + "\r\n" + "s=misesion\r\n" + "t=0\r\n" + "m=audio "
		LINEA += AUDIO_PUERTO + " RTP\r\n"
		print(LINEA);
		my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		my_socket.connect((PROXY_IP, int(PROXY_PUERTO)))
		my_socket.send(bytes(LINEA, 'utf-8') + b'\r\n')
		data = my_socket.recv(1024)
		print(data.decode('utf-8'))
		Evento = 'Sent to ' + str(PROXY_IP) + ':'
		Evento += str(PROXY_PUERTO) + ': ' + LINEA
		FICH_LOG(Evento)

	elif METHOD == "BYE":
		LINEA = "BYE sip: " + OPCION + " SIP/2.0\r\n"
		print (LINEA)
		Evento = 'Sent to ' + PROXY_IP + ':' + PROXY_PUERTO + ': ' + LINEA
		FICH_LOG(Evento)
		
	else:
		Evento = 'Sent to ' + PROXY_IP + ':' + PROXY_PUERTO + ': ' + LINEA
		FICH_LOG(Evento)
		print('Usage: python uaclient.py config method option')


my_socket.send(bytes(LINEA, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)
datos_recibido = data.decode('utf-8').split()
imprime = data.decode('utf-8')

print('Recibiendo:', imprime)

recibo = data.decode('utf-8').split(' ')
#print("EVA ESTO ES RECIBO:", recibo2)
print("Data:", recibo)

if (recibo[2] == 'Trying' and recibo[5] == 'Ring' and recibo[8] == 'OK'):
	
    linea = 'ACK sip:' + OPCION + ":" + PUERTO_SERVER + ' SIP/2.0'
    my_socket.send(bytes(linea, 'utf-8') + b'\r\n\r\n')
    Evento = 'Receieved from ' + PROXY_IP
    Evento += ':' + PUERTO_SERVER + ': ' + LINEA
    FICH_LOG(Evento)
    Evento = 'Sent to: ' + AUDIO_PUERTO + ': ' + 'cancion.mp3'
    FICH_LOG(Evento)
    aEjecutar = './mp32rtp -i 127.0.0.1 -p '
    aEjecutar += AUDIO_PUERTO + ' < ' + AUDIO_PATH
    print('Vamos a ejecutar', aEjecutar)
    os.system(aEjecutar)
    print('Ha acabado la cancion')





