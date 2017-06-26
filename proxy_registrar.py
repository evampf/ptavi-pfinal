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
PROXY_NAME = PROXY[0]['server']['name']
PROXY_IP = PROXY[0]['server']['ip']
PROXY_PUERTO = PROXY[0]['server']['puerto']
PATH_DATABASE = PROXY[1]['database']['path']
PASSWD_DATABASE = PROXY[1]['database']['passwdpath']
PATH_LOG = PROXY[2]['log']['path']

class SIPProxyRegisterHandler(socketserver.DatagramRequestHandler):

    dicc_clientes = {}

    #def password2json(self):
    #    archivo = open("password.json",'r')
    #   self.dicc_passw = json.upload(archivo)


    def register2json(self):
    
        json_file = open("miregistro.json", "w")
        json.dump(self.dicc_clientes, json_file)
        json_file.close()

    def json2registered(self):
    
        try:
            with open("miregistro.json", "r") as JsonFile:
                self.dicc_clientes = json.load(JsonFile)
        except:
            print('Creando fichero json..')
            pass

    def usuariosregistrados(dicc_clientes, Clientes):
        # Función para ver si un usuario está registrado, nos devuelve 0 si el
        # usuario no está registrado con ninguna de las claves, en caso cotrario se
        # devuelven los datos del cliente
        encontrado = False
        lineas = dicc_clientes.readlines()
        for line in lineas:
            if user == line.split(":")[0]:
                encontrado = True
        return encontrado



    def handle(self):
        #while 1:
            text = self.rfile.read()
            data_text = text.decode('utf-8')
            Data_lines = data_text.split()
            METHOD = Data_lines[0].upper()
            print("ESTO ES DATA_LINES", Data_lines)
            LINEA_SIP = Data_lines[2].split(" ")[0]
            print ("ESTO ES LINEA_SIP:", LINEA_SIP)
            USER = Data_lines[2]
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
                PUERTO_USER = Data_lines[3].upper()
                print (PUERTO_USER)

                self.json2registered()

                self.dicc_clientes[USER] = {"address": Dir_IP, 
                                            "port": PUERTO_USER, 
                                            "tiempo_exp": Time_Exp}

                Lista_Expirados = []
                for user in self.dicc_clientes:
                    if Hora_actual >= self.dicc_clientes[user]["tiempo_exp"]:
                        Lista_Expirados.append(user)
                self.register2json()

                for user in Lista_Expirados:
                    del self.dicc_clientes[user]

                self.register2json()

                self.wfile.write(b" SIP/2.0 200 OK\r\n\r\n")
                print(self.dicc_clientes)

            elif METHOD == 'INVITE':

                USER_SIP = LINEA_SIP.upper()
                print("USER_SIP:", USER_SIP)
                USER_INVITADO = Data_lines[2].upper()
                print("USUARIO INVITADO:", USER_INVITADO)
                USER_ORIGEN = Data_lines[7].split("=")[1]
                print("USUARIO ORIGEN:", USER_ORIGEN)

                with open("miregistro.json") as JsonFile:
                    datos_clientes = json.load(JsonFile)
                    cliente = datos_clientes
                    print ("cliente:", cliente)

                    encontrado = False
                    for usuario in cliente:
                        print("MIRA AQUI:", usuario)
                        usuario2 = usuario.split(":")[0].split(':')[0].upper()
                        print ("usuario2:", usuario2)
                        if usuario2 == USER_INVITADO:
                            encontrado = True
                
                            print("Encontrado:", encontrado)
                

                    if encontrado:  
                    
                        if USER_INVITADO == "RONWHISLEY@HARRY.COM":
                            datospuerto = "5690"
                        if USER_INVITADO == "HERMIONE@HARRY.COM": 
                            datospuerto = "5689"
                        
                        puerto = datospuerto

                        LINEA = "INVITE sip: " + " SIP/2.0\r\n" + "Content-Type: application/sdp\r\n\r\n" + "v=0\r\n" + "o = "
                        LINEA += " " + "\r\n" + "s=misesion\r\n" + "t=0\r\n" + "m = audio" + " RTP\r\n"
                        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        my_socket.connect(('127.0.0.1', int(puerto)))
                        my_socket.send(bytes(LINEA, 'utf-8') + b'\r\n')
                        data = my_socket.recv(1024)
                        imprimir = data.decode('utf-8')
                        print(imprimir)
                        self.wfile.write(data)

                    else:
                        msg = "SIP/2.0 404 User Not Found\r\n" + "Via: SIP/2.0/UDP " + "branch=z9hG4bKnashds7\r\n\r\n"
                        self.wfile.write(bytes(msg,'utf-8'))

            elif METHOD == "ACK":
                
                LINEA_ACK = text.decode('utf-8')
                print("esta es la linea_ack:", LINEA_ACK)
                USER_SIP = LINEA_SIP.upper()
                USER_INVITADO = Data_lines[2].upper()

    
                with open("miregistro.json") as JsonFile:
                    datos_clientes = json.load(JsonFile)
                    cliente = datos_clientes
                    print ("cliente:", cliente)
                    encontrado = False

                    for usuario in cliente:
                        usuario2 = usuario.split(":")[0].split(':')[0].upper()
                        if usuario2 == USER_INVITADO:
                            encontrado = True
                    
                    if encontrado:  
                    
                        if USER_INVITADO == "RONWHISLEY@HARRY.COM":
                            datospuerto = "5690"
                        if USER_INVITADO == "HERMIONE@HARRY.COM": 
                            datospuerto = "5689"
                        
                        puerto = datospuerto      

                        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        my_socket.connect(('127.0.0.1', int(puerto)))
                        my_socket.send(bytes(LINEA_ACK, 'utf-8') + b'\r\n')
                        imprimir = data.decode('utf-8')

                    print("he entrado en el ack")

            elif METHOD == "BYE":
                
                LINEA = "BYE sip: " + " SIP/2.0\r\n"
                USER_BORRADO = Data_lines[2].upper()

                with open("miregistro.json") as JsonFile:
                    datos_clientes = json.load(JsonFile)
                    cliente = datos_clientes
                    for usuario in cliente:
                        usuarioborrado = usuario.split(":")[0].split(':')[0].upper()

                        if USER_BORRADO == "RONWHISLEY@HARRY.COM":
                                datospuerto = "5690"
                        if USER_BORRADO == "HERMIONE@HARRY.COM": 
                                datospuerto = "5689"
                        
                        puerto = datospuerto   

                        if usuarioborrado == USER_BORRADO:
                            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                            my_socket.connect(('127.0.0.1', int(puerto)))
                            my_socket.send(bytes(LINEA_ACK, 'utf-8') + b'\r\n')






            else:
                print("Mal")


if __name__ == "__main__":

    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((PROXY_IP, int(PROXY_PUERTO)), SIPProxyRegisterHandler)
    print("Server " + PROXY_NAME + " listening at port " + PROXY_PUERTO + " ...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizando...")
