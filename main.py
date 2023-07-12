import socket
import sys
import os
import time
from art import *
import random
import string
import hashlib
import threading
from _thread import *
from multiprocessing import Process

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QMainWindow, QScrollArea,QLabel
)
import time
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt

characters = string.ascii_letters + string.digits

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Anon local chat'
        self.left = 10
        self.top = 10
        self.width = 440
        self.height = 280
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(500, 500)


        self.widget = QWidget(self)
        self.vbox = QVBoxLayout(self) 



        self.input_msg = QLineEdit(self)
        self.input_msg.setGeometry(10, 450, 480, 40)
        self.input_msg.move(10, 415)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(10, 450, 480, 300)
        self.scroll_area.move(5, 20)

        button_send = QPushButton(self)
        button_send.setGeometry(450, 450, 55, 35)
        button_send.move(430, 460)
        button_send.setText("send")
        button_send.clicked.connect(self.send_text)
        button_send.clicked.connect(self.input_msg.clear)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget)
        
    def send_text(self):
        text = self.input_msg.text()
        object = QLabel(text)
        self.vbox.addWidget(object)
        print(self.input_msg.text())



class Server():
    
    def __init__(self, ip_adr, port, key, nickname):
        
        self.ip_adr = ip_adr
        self.port = port
        self.key = key
        self.nickname = nickname
        self.socket = None
        self.socketConnection = None
        self.connectionAddress = None
        self.clients = []
        self.nicknames = []


    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} has left the chat room!'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break


   

    def broadcast(self, message):
        for client in self.clients:
            print(message)
            client.send(message)

    def runServer(self):

        self.socket = socket.socket()
        self.socket.bind((self.ip_adr, self.port))
        self.socket.listen()
        print(f'Server is running and listening on port {self.port} by private key {self.key}...')
        while True:
            print(self.clients, self.nickname)
            self.socketConnection, self.connectionAddress = self.socket.accept()
            print(f'connection is established with {str(self.connectionAddress)}')

            receivedMsg = self.socketConnection.recv(128)

            receivedString = receivedMsg.decode('utf-8')

            nickname = receivedString[-16::]
            nickname.replace("\x00", "")

            if nickname not in self.nicknames:
                self.nicknames.append(nickname)
            
            if self.socketConnection not in self.clients:
                self.clients.append(self.socketConnection)

            nickname_for_send = nickname.replace("\x00", "")
            self.broadcast(f'\xaa{nickname_for_send} has connected to chat'.encode('utf-8'))
            thread = threading.Thread(target=self.handle_client, args=(self.socketConnection,))
            thread.start()

        

    def closeConnection(self):
        self.socketConnection.close()
        self.socket.close()
        self.connectionAddress = None



class Client():
    def __init__(self, ip_adr, port, key, nickname):
        self.ip_adr = ip_adr
        self.port = port 
        self.key = key
        self.nickname = nickname
        self.socket = None

    def run_Gui(self):
        app = QApplication(sys.argv)
        ex = App()
        ex.show()
        sys.exit(app.exec())

    def connect_to_server(self):
        self.socket = socket.socket()
        count_of_connection = 0
        while True:
            try:
                self.socket.connect((self.ip_adr, self.port))
                break
            except socket.error as error:
                print("Error while connecting to server")
                print(error)
                count_of_connection += 1
                if count_of_connection > 4:
                    print("You try it for 5+ times, we gonna close your connection")
                    self.socket.close()
                    return False
                time.sleep(1)
        list_for_join = []
        nickname_enc = self.nickname.encode('utf-8')
        need_bytes_of_zero = 16 - len(nickname_enc)

        list_for_join.append(b'\x00'*need_bytes_of_zero)
        list_for_join.append(nickname_enc)

        messageToSend = b''.join(list_for_join)

        try:
            self.socket.send(messageToSend)
        except socket.error as error:
            print("Sorry, we can't send your message")
            print(error)
        return True
    
    def sendMsg(self):
        while True:

            list_for_join = []

            keyboardInput = input()
            message_enc = keyboardInput.encode("utf-8")

            nickname_enc = self.nickname.encode('utf-8')
            need_bytes_of_zero = 16 - len(nickname_enc)

            list_for_join.append(message_enc)
            list_for_join.append(b'\x00'*need_bytes_of_zero)
            list_for_join.append(nickname_enc)

            messageToSend = b''.join(list_for_join)

            try:
                self.socket.send(messageToSend)
            except socket.error as error:
                print("Sorry, we can't send your message")
                print(error)

    def recieveMsg(self):

        while True:
            receivedMsg = self.socket.recv(128)
            
            if receivedMsg[0] == 194:
                receivedString = receivedMsg.decode("utf-8")
                print(receivedString[1::])
            else:
                receivedString = receivedMsg.decode("utf-8")

                nickname = receivedString[-16::]
                nickname.replace("\x00", "")


                if nickname.replace("\x00", "") != self.nickname.replace("\x00", ""):
                    message = receivedString[0:-16]
                    self.full_recieved_msg = f"{nickname}: {message}"
                    print(self.full_recieved_msg)
    
    def runClient(self):
        
        
        sendThread = threading.Thread(target=self.sendMsg)
        receiveThread = threading.Thread(target=self.recieveMsg)
        GuiProc = Process(target=self.run_Gui)
        
        GuiProc.start()
        sendThread.start()
        receiveThread.start()

        sendThread.join()
        receiveThread.join()

        
        

    def closeConnection(self):
        self.socket.close()



class Start():
    def main_start():


        #### read open ports ####
        list_of_ports = []

        for i in range(65536):
            s = socket.socket()
            s.settimeout(1)
            try:
                s.connect(('127.0.0.1', i))
            except socket.error:
                pass
            else:
                s.close
                list_of_ports.append(i)
        #########################

        os.system("clear")
        tprint("Anon    chat")




        command = str(input("Are you [S]erver or [C]lient?\n"))

        if command == "S":
            key_is_correct = False
            ip_adr = "localhost"
            nickname = None
            while not key_is_correct:
                os.system("clear")
                tprint("Anon    chat")
                private_key = "?" + ''.join(random.choice(characters) for i in range(6))
                print(f"checking key {private_key} for unic.")
                time.sleep(0.75)
                os.system("clear")
                tprint("Anon    chat")
                print(f"checking key {private_key} for unic..")
                time.sleep(0.75)
                os.system("clear")
                tprint("Anon    chat")
                print(f"checking key {private_key} for unic...")
                time.sleep(0.75)
                
                hash_object = hashlib.sha256(bytes(private_key.encode('utf-8')))
                hash_dig = hash_object.hexdigest()
                numbers = ''.join(i for i in hash_dig if not i.isalpha())
                port_for_key = int(sum(list(map(int, numbers)))**1.64)
                time.sleep(0.3)

                if port_for_key not in list_of_ports or port_for_key > 2000:
                    try:
                        
                        os.system("clear")
                        tprint("Anon    chat")
                        print(f"trying to create server by private key {private_key}")
                        server = Server(ip_adr, port_for_key, private_key, nickname)
                        server.runServer()
                        
                        
                        key_is_correct = True
                    except:

                        key_is_correct = False
            


        elif command == "C":

            ip_adr = "localhost"

            private_key_for_client = input("Enter the key: ")
            
            hash_object = hashlib.sha256(bytes(private_key_for_client.encode('utf-8')))
            hash_dig = hash_object.hexdigest()
            numbers = ''.join(i for i in hash_dig if not i.isalpha())
            port_for_key = int(sum(list(map(int, numbers)))**1.64)
            time.sleep(0.3)

            if port_for_key not in list_of_ports or port_for_key < 2000:
                key_is_correct = True
                os.system("clear")
                tprint("Anon    chat")
                print(f"done! {private_key_for_client} is correct")
            nickname = input("Enter your nickname for chat (max len 16): ")

            client = Client(ip_adr, port_for_key, private_key_for_client, nickname)

            isConnected = client.connect_to_server()

            if isConnected:
                

                client.runClient()
                

                
                
            else:
                print("Error while connecting to server")
                exit()

        else:
            print("wrong input, restarting software")
            Start.main_start()



if __name__ == "__main__":
    
    Start.main_start()
    
    #TODO: 1. проверка пользователя не только по нику а еще по ip
    #      2. нормальная генерация портов
    #      3. почитать что-то про безопасность и прослушку соединения по порту