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

try:    
    CONFIG = sys.argv [1]
    if len(sys.argv) != 2:
        sys.exit("Usage: python proxy_registrar.py config")
except IndexError:
        sys.exit("Usage: python3 proxy.registrar.py config")

class XMLHandler(ContentHandler):   

    def __init__(self):
        self.lista = []
        self.DicEtiquetas = {
                            'server': ['name','ip','puerto'],
                            'database': ['path','passwdpath'],
                            'log': ['path']}

    def startElement(self, name, attrs):
        if name in self.DicEtiquetas:
            dicc_clientes = {}
            for atributo in self.DicEtiquetas[name]:
                dicc_clientes[atributo] = attrs.get(atributo, "")
            diccname = {name: dicc_clientes}
            self.lista.append(diccname)

    def get_tags(self):
        return self.lista     
    
#Saca el contenido del fichero XML 
parser = make_parser()
cHandler = XMLHandler()
parser.setContentHandler(cHandler)
parser.parse(open(CONFIG))
PROXY = cHandler.get_tags()

#Mete los valores del XML en variables
SERVER_NAME = PROXY[0]['server']['name']
SERVER_IP = PROXY[0]['server']['ip']
SERVER_PUERTO = PROXY[0]['server']['puerto']
PATH_DATABASE = PROXY[1]['database']['path']
PASSWD_DATABASE = PROXY[1]['database']['passwdpath']
PATH_LOG = PROXY[2]['log']['path']

class SIPProxyRegisterHandler(socketserver.DatagramRequestHandler):

    dicc_clientes = {}

    #def password2json(self):
    #    archivo = open("password.json",'r')
    #   self.dicc_passw = json.upload(archivo)

    def register2json(self):
        """Archivo json de registro."""
        json_file = open("registered.json", "w")
        json.dump(self.dicc_clientes, json_file)
        json_file.close()

    def usuariosregistrados(dicc_clientes, Clientes):
        # Función para ver si un usuario está registrado, nos devuelve 0 si el
        # usuario no está registrado con ninguna de las claves, en caso cotrario se
        # devuelven los datos del cliente
        if Clientes not in dicc_clientes.keys():
            datos = '0'
        else:
            datos = dicc_clientes[Clientes]
        return datos

    def json2registered(self):
        """Comprobacion de json."""
        try:
            #("Estamos probando")
            with open("registered.json", "r") as file:
                self.dicc_clientes = json.load(file)
        except:
                pass


    def handle(self):
        #while 1:
            text = self.rfile.read()
            data_text = text.decode('utf-8')
            Data_lines = data_text.split()
            METHOD = Data_lines[0].upper()
            LINEA_SIP = Data_lines[1].split(':')
            USER = Data_lines[2].upper()
            PUERTO_USER = Data_lines[3].upper()
            print("La peticion es: ", METHOD)
            print("Listening...")

            if METHOD == 'REGISTER':
                
                EXPIRES = data_text.split(' ')[5].upper()
                expires = int(EXPIRES)
                Dir_IP = self.client_address[0]
                Puerto = self.client_address[1]

                #Sin autenticación
                LINEA = "REGISTER sip: " + ":" + " SIP/2.0\r\n" + "Expires: " + "\r\n"
                Hora_actual = time.time()
                Time_Exp = Hora_actual + int(EXPIRES)
                Dir_IP = self.client_address[0]

                self.dicc_clientes[USER] = {"address": Dir_IP, 
                                            "port": PUERTO_USER, 
                                            "tiempo_exp": Time_Exp}

                Lista_Expirados = []
                for user in self.dicc_clientes:
                    if Hora_actual >= self.dicc_clientes[user]["tiempo_exp"]:
                        Lista_Expirados.append(user)
                for user in Lista_Expirados:
                    del self.dicc_clientes[user]

                self.register2json
                self.wfile.write(b" SIP/2.0 200 OK\r\n\r\n")
                print(self.dicc_clientes)

            elif METHOD == 'INVITE':
                
                print (data_text)
                
                US_INVITADO = Data_lines[2]
                print("USUARIO INVITADO:", US_INVITADO)
                US_ORIGEN = Data_lines[7].split("=")[1]
                print("USUARIO ORIGEN:", US_ORIGEN)

                print("hasta aqui llega ok")
                
                with open("registered.json", "r") as fichero:
                    self.dicc_clientes = json.load(fichero)
                    
                    Cliente_reg = self.usuariosregistrados()
                    if usuariosregistrados == '0':
                        msg = "SIP/2.0 404 User Not Found\r\n" + "Via: SIP/2.0/UDP " + "branch=z9hG4bKnashds7\r\n\r\n"
                        self.wfile.write(bytes(msg,'utf-8'))
                    else:
                        IP_Registrada = Cliente_reg[0]
                        print (IP_Registrada)
                        Puerto_Registrado = Cliente_reg[1]
                        LINEA = "INVITE sip: " + " SIP/2.0\r\n" + "Content-Type: application/sdp\r\n\r\n" + "v=0\r\n" + "o = "
                        LINEA += " " + "\r\n" + "s=misesion\r\n" + "t=0\r\n" + "m = audio" + " RTP\r\n"
                        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        my_socket.connect((SERVER_IP, int(SERVER_PUERTO)))
                        my_socket.send(bytes(LINEA, 'utf-8') + b'\r\n')
                        data = my_socket.recv(1024)
                    self.json2registered







            elif METHOD == "BYE":
                LINEA = "BYE sip: " + " SIP/2.0\r\n"

            else:
                print("Mal")




if __name__ == "__main__":

    msgprox = 'server ' + SERVER_NAME + ' listening at port '
    msgprox += SERVER_PUERTO + '...' + '\r\n'
    print (msgprox)

    PORT = int(SERVER_PUERTO)
    IP = SERVER_IP
    serv = socketserver.UDPServer((IP,PORT),SIPProxyRegisterHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        sys.exit("Finish")