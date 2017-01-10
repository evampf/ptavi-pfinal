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
		#while 1:
		line = self.rfile.read()
		print("El cliente nos manda " + text.decode('utf-8'))
		LINE = text.decode('utf-8')
		Words_LINES = LINE.split()
		REQUEST = Words_LINES[0]
		print("La peticion es: ", REQUEST)
		print("Listening...")

		if METHOD == "REGISTER":
			#Sin autenticación
			LINEA = "REGISTER sip: " + ACCOUNT_USERNAME + ":" + PUERTO_SERVER + " SIP/2.0\r\n" + "Expires: " + OPCION + "\r\n"
			print(LINEA)
		if METHOD == "INVITE":
			LINEA = "INVITE sip: " + OPCION + " SIP/2.0\r\n" + "Content-Type: application/sdp\r\n\r\n" + "v=0\r\n" + "o = "
			LINEA += ACCOUNT_USERNAME + " " + IP_SERVER + "\r\n" + "s=misesion\r\n" + "t=0\r\n" + "m = audio" 
			LINEA += AUDIO_PUERTO + " RTP\r\n"
			print(LINEA)
		if METHOD == "BYE":
			LINEA = "BYE sip: " + OPCION + " SIP/2.0\r\n"

		my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		my_socket.connect((PROXY_IP, int(PROXY_PUERTO)))

if __name__ == "__main__":
	serv = socketserver.UDPServer(('', 6001), XMLHandler)
	print("Lanzando servidor UDP de eco...")
	try:
		serv.serve_forever()
	except KeyboardInterrupt:
		print("Finalizado servidor")
