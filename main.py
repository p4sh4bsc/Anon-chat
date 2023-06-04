import socket
import sys
import os
import time
from art import *
import random
import string
import hashlib
import threading


characters = string.ascii_letters + string.digits

class Server():
    def __init__(self, ip_adr, port, key):

        self.ip_adr = ip_adr
        self.port = port
        self.key = key
        self.socket = None
        self.socketConnection = None
        self.connectionAddress = None

    def create_chat(self):

        self.socket = socket.socket()
        self.socket.bind((self.ip_adr, self.port))
        self.socket.listen(1)
        print(f"Creating chat by key {self.key}...")
        time.sleep(1)
        
        try:
            self.socketConnection, self.connectionAddress = self.socket.accept()
            print("Chat created!")
        except socket.error as error:
            print("Something goes wrong")
            print(error)
            self.socket.close()
    def sendMsg(self):
        while True:
            keyboardInput = input()
            messageToSend = keyboardInput.encode('utf-8')

            try:
                self.socketConnection.send(messageToSend)
                print(f"Message sent: {messageToSend}")
            except socket.error as error:
                print("I cant send this message, sorry")
                print(error)

    def receiveMsg(self):
        while True:
            receivedMsg = self.socketConnection.recv(128)
            receivedString = receivedMsg.decode('utf-8')
            print(f"Received Message: {receivedMsg}")

    def runServer(self):
        sendThread = threading.Thread(target=self.sendMsg)
        receiveThread = threading.Thread(target=self.receiveMsg)

        sendThread.start()
        receiveThread.start()

        sendThread.join()
        receiveThread.join()

    def closeConnection(self):
        self.socketConnection.close()
        self.socket.close()
        self.connectionAddress = None






class Client():
    pass



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
            ip_adr = "127.0.0.1"

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

                if port_for_key not in list_of_ports or port_for_key < 2000:
                    key_is_correct = True
                    os.system("clear")
                    tprint("Anon    chat")
                    print(f"done! {private_key} is correct")
                    print(f"!!! for debug port is {port_for_key} !!!")
            

        elif command == "C":
            print(list_of_ports)
        else:
            
            Start.main_start()


if __name__ == "__main__":
    Start.main_start()




















"""
mas = [20, 21, 22, 23, 25, 42, 43, 53, 67, 69, 80, 110, 115, 123, 137, 138, 139, 143, 161, 179, 443, 445, 514, 515, 993, 995, 1080, 1194, 1433, 1702, 1723, 3128, 3268, 3306, 3389, 5432, 5060, 5900, 5938, 8080, 10000, 20000]
print ('«Простейший сканер портов на питоне»')
print ('» «')
host = input('Введите имя сайта или IP адрес: ')
print ('«———————————«')
print ('«Ожидайте идёт сканирование портов!»')
print ('«———————————«')
for i in range(65536):
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect((host, i))
    except socket.error:
        pass
    else:
        s.close
        print (host + ': ' + str(i) + ' порт активен')
print ('«———————————«')
print ('«Процесс завершен»')
"""