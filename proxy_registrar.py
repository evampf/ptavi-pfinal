#!/usr/bin/python3

import socketserver
import sys
import time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


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
            for name in self.DicEtiquetas[name]:
                dicc[name] = attrs.get(name,"")
            diccname = {name : dicc}
            self.lista.append(diccname)

    def get_tags(self):
        return self.lista     


class SIPProxyRegisterHandler(socketserver.DatagramRequestHandler):

    dicc_clientes = {}
    nonce_dicc = {}


    def handle(self):
        while 1:
            line = self.rfile.read()
            data_text = text.decode('utf-8')
            Words_datas = data_text.split()
            REQUEST = Words_datas[0]
            Dir_IP = self.client_address[0]
            Puerto = self.client_address[1]
            print("La peticion es: ", REQUEST)
            print("Listening...")
            if not line:
                break

            if REQUEST == "register":
                Message = ("REGISTER sip:" + DIRECCTION + " SIP/2.0\r\n")
                Message += ("Expires: " + EXPIRES + "\r\n\r\n")
                user = data_text[1].split(':')[1]
                print("Enviando:", Message)

if __name__ == "__main__":
    
    CONFIG = sys.argv [1]
    if len(sys.argv) != 2:
        sys.exit("Usage: python proxy_registrar.py config")
    
    parser = make_parser()
    cHandler = XMLHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(CONFIG))
    config = cHandler.get_config()
    serv = socketserver.UDPServer(("",int(config[2])),SIPProxyRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
