#!/usr/bin/python3

import socketserver
import sys
import os
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import time

CONFIG = sys.argv [1]

if len(sys.argv) != 2:
    sys.exit("Usage: python uaserver.py config")

def FICH_LOG(Evento):
		
	fichero = open('LogUaClient.txt', 'a+')
	HoraActual = time.gmtime(time.time())
	HoraActual = time.strftime('%Y%m%d%H%M%S', HoraActual)
	fichero.write(str(HoraActual) + ' ' + Evento + '\r\n')


class XMLHandler(ContentHandler):   


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

parser = make_parser()
cHandler = XMLHandler()
parser.setContentHandler(cHandler)
parser.parse(open(sys.argv[1]))
UASERVER = cHandler.get_tags()
print(UASERVER)

'DATOS'
#Saco datos del diccionario creado

ACCOUNT = UASERVER[0]['account']['username']
UASERVER_PORT = UASERVER[1]['uaserver']['puerto']
UAS_IP = UASERVER[1]['uaserver']['ip']
RTP_PORT = UASERVER[2]['rtpaudio']['puerto']
PROXY_PORT = UASERVER[3]['regproxy']['puerto']
PROXY_IP = UASERVER[3]['regproxy']['ip']
LOG_PATH = UASERVER[4]['log']['path']
AUDIO_PATH = UASERVER[5]['audio']['path']



class EchoHandler(socketserver.DatagramRequestHandler):
    	
	lista = []

	def handle(self):
		"""Escribe dirección y puerto del cliente."""
	#while 1:
		text = self.rfile.read()
		datos = text.decode('utf-8').split()
		print("datos:", datos)
		print("El cliente nos manda:", text.decode('utf-8'))
		REQUESTS = ['INVITE', 'ACK', 'BYE']

		if datos[0] == 'INVITE':
			RTP_PORT_RECIBIDO = datos[12]
			self.lista.append(RTP_PORT_RECIBIDO)
			#Hemos añadido el puerto a un diccionario
			print("Puerto RTP nos envia el cliente en INVITE: ")
			print(RTP_PORT_RECIBIDO)

		if not datos[0] in REQUESTS:
			LINE_405 = 'SIP/2.0 405 Method Not Allowed\r\n\r\n'
			self.wfile.write(LINE_405)

		if datos[0] == 'INVITE':

			metodo = datos[0]
			print("este es metodo:", metodo)
			self.lista.append(RTP_PORT_RECIBIDO)

			mensaje = b'SIP/2.0 100 Trying \r\n\r\n'
			mensaje += b'SIP/2.0 180 Ring \r\n\r\n'
			mensaje += b'SIP/2.0 200 OK \r\n\r\n'
			mensaje += b"Content-Type: application/sdp\r\n\r\n"
			mensaje += b"v=0\r\n" + b"o="
			mensaje += ACCOUNT[2].encode('utf-8') + b" "
			mensaje += UAS_IP.encode('utf-8') + b" \r\n" + b"s=misesion\r\n"
			mensaje += b"t=0\r\n" + b"m=audio " + PROXY_PORT.encode('utf-8')
			mensaje += b" RTP\r\n\r\n"
			self.wfile.write(mensaje)
			print("llega aqui ")
			Evento = 'Received from ' + PROXY_IP
			Evento += ':' + PROXY_PORT + ': ' + mensaje.decode('utf-8')
			FICH_LOG(Evento)

		elif datos[0] == 'ACK':
    		
			mi_puerto = self.lista[1]
			aEjecutar = './mp32rtp -i 127.0.0.1 -p ' + mi_puerto + ' < '
			aEjecutar += AUDIO_PATH
			print('Ejecutando...', aEjecutar)
			os.system(aEjecutar)
			print('Fin de la cancion')
			Evento = 'Sent to ' + PROXY_IP
			Evento += ':' + mi_puerto + ': ' + 'cancion.mp3'
			FICH_LOG(Evento)
		
		elif datos[0] == 'BYE':
			self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
			Evento = 'Received from ' + regproxy_ip
			Evento += ':' + PROXY_PORT + ': ' + mensaje.decode('utf-8')
			FICH_LOG(Evento)



if __name__ == "__main__":
    	
    serv = socketserver.UDPServer((UAS_IP, int(UASERVER_PORT)), EchoHandler)
    print("Listening...")


    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
