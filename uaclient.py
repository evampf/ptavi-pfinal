#!/usr/bin/python3

import socket
import sys
import os
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from uaserver import XMLHandler


if __name__ == "__main__":  
	try:
		CONFIG = sys.argv[1]
		METHOD = sys.argv[2].upper()
		OPCION = sys.argv[3]
	except Exception:
		sys.exit('Usage: python client.py config method option')

	if len(sys.argv) != 4:
		sys.exit("Usage: python client.py config method option")
	

	parser = make_parser()
	cHandler = XMLHandler()
	parser.setContentHandler(cHandler)
	parser.parse(open(CONFIG))
	listaUA = cHandler.get_tags()

	my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	my_socket.connect((IP_PROXY, int(PORT_PROXY)))
	my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')


