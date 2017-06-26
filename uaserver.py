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
		print("El cliente nos manda:", text.decode('utf-8'))
		datos = text.decode('utf-8').split()
		print("datos:", datos)

		if datos[0] == 'INVITE':

			metodo = datos[0]
			print("este es metodo:", metodo)
			mensaje = b'SIP/2.0 100 Trying \r\n\r\n'
			mensaje += b'SIP/2.0 180 Ring \r\n\r\n'
			mensaje += b'SIP/2.0 200 OK \r\n\r\n'
			mensaje += b"Content-Type: application/sdp\r\n\r\n"
			mensaje += b"v=0\r\n" + b"o=" 
			mensaje += ACCOUNT[2].encode('utf-8') + b" "
			mensaje += UAS_IP.encode('utf-8') + b" \r\n" + b"s=misesion\r\n"
			mensaje += b"t=0\r\n" + b"m=audio " + RTP_PORT[2].encode('utf-8')
			mensaje += b" RTP\r\n\r\n"
			self.wfile.write(mensaje)
			print("llega aqui ")

		elif datos[0] == 'ACK':
			
			metodo = datos[0]
			print("metodo 2:", metodo)
			puerto = self.RTP_PORT[0]
			print ("puerto:", puerto)
			print("Entra en el ACK")
			self.wfile.write(b'ACK')
			aEjecutar = './mp32rtp -i 127.0.0.1 -p ' + puerto + ' < '
			aEjecutar += AUDIO_PATH
			print('Ejecutando...', aEjecutar)
			os.system(aEjecutar)
			print('Fin de la cancion')
		
		elif datos[0] == 'BYE':
			self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")


if __name__ == "__main__":
    serv = socketserver.UDPServer((UAS_IP, int(UASERVER_PORT)), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
