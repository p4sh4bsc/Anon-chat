import socket
import sys
import os
import time
from art import *





class Server():
    def main_server():
        pass


class Client():
    def main_client():
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
        command = str(input("Are you [C]lient or [S]erver?\n"))

        if command == "C":
            print(list_of_ports)
        elif command == "S":
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