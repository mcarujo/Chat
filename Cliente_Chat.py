#author: Marco Antonio Moreira Carujo
#where: Natal,RN,Brazil
#when: 15-05-2017


import threading
import time
import socket
import os


serverName = 'localhost' # ip do servidor
serverPort = 12001
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

contador=0
chave=True
def cont():
    global contador
    global chave
    while chave:
        contador=0
        time.sleep(2)
def enviar():
    global contador
    global chave
    nick = input('\nInforme seu nick:')
    clientSocket.send(nick.encode())
    while chave:
        sentence = input('\nVocê diz:')
        if sentence=='sair()':
            clientSocket.send(sentence.encode())
            chave = False
        else:
            if contador<5:
                clientSocket.send(sentence.encode())
                contador+=1
            else:#bugado
                print('\nVocê enviou muitas mensagens,aguarde um tempo, vai aguardar 10 segundos para enviar novamente!')
                time.sleep(10)
                contador = 0
                print('\nVocê agora pode enviar mensagens novamente!')
def receber():
    global chave
    chave1=True
    while chave1:
        modifiedSentence = clientSocket.recv(1024)
        modifiedSentence=modifiedSentence.decode()
        if modifiedSentence=='sair()':
            clientSocket.close()
            chave=False
            chave1=False
            os._exit(1)
        elif modifiedSentence=='sair()2':
            print('\nServidor está finalizando o chat!')
            clientSocket.send('sair()'.encode())
        else:
            print('\n')
            print(modifiedSentence)

thread1=threading.Thread(name='enviar',target=enviar)
thread2=threading.Thread(name='receber',target=receber)
thread3=threading.Thread(name='cont',target=cont)
thread1.start()
thread2.start()
thread3.start()
