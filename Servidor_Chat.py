#author: Marco Antonio Moreira Carujo
#where: Natal,RN,Brazil
#when: 15-05-2017

from threading import Thread
import time
import socket
import os

#INICIALIZANDO SERVIDOR:
serverName = ''  # ip do servidor (em branco)
serverPort = 12001  # porta a se conectar
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # criacao do socket TCP
serverSocket.bind((serverName, serverPort))  # bind do ip do servidor com a porta
serverSocket.listen(0)       # socket pronto para "ouvir" conexoes
connectionSocket=[]          #Vetor de conexões, Clientes conectados ao Servidor
numero_de_clientes=0         #Numero de conexões atual no servidor
addrs=[]
nomes=[]                     #Nick dos usuarios no chat
bool=[]
chaveacc=True
#Declaração da Thread que está aguardando e recebendo as mensagens do cliente

def recebe(idsocket):
        global connectionSocket                     #Vetor de conexões com o cliente
        global nomes                                #vetor com os nicks dos clientes
        global numero_de_clientes                   #Numero de clientes
        auxnomes=connectionSocket[idsocket].recv(1024)
        auxnomes=auxnomes.decode()
        nomes.append(auxnomes)
        aux4=str(nomes[idsocket])+' entrou no chat!'
        print('\n',aux4)
        Thread(group=None, target=enviar, name=enviar, args=(idsocket, aux4,0,), kwargs={}).start()
        chave=True
        while chave:
            sentence= connectionSocket[idsocket].recv(1024)     # Aguarda e recebe a mensagem do cliente
            sentence=sentence.decode()
            aux=sentence.split('(')
            #tratamento, se realmente é uma mensagem ou se é um comando
            if sentence=="sair()":                                  #Aqui eu tenho que desconectar o cliente
                aux5=str(nomes[idsocket]) + ' saiu do chat! ' + str(addrs[idsocket])
                print(aux5)
                connectionSocket[idsocket].send(sentence.encode())
                connectionSocket[idsocket].close()
                Thread(group=None, target=enviar, name=enviar, args=(idsocket, aux5, 0,), kwargs={}).start()
                chave=False
                bool[idsocket]=False
            elif aux[0]=="nome":                                 #Aqui eu terei que alterar o nome do cliente
                aux2=aux[1].split(')')
                aux6=str(nomes[idsocket]) + " Alterou o nome para " + str(aux2[0])
                nomes[idsocket] = aux2[0]
                print(aux6)
                Thread(group=None, target=enviar, name=enviar, args=(idsocket, aux6, 0,), kwargs={}).start()
            elif sentence=="lista()":
                aux3=gerarlista()
                connectionSocket[idsocket].send(aux3.encode())
            else:               #Aqui crio uma nova thread para enviar a mensagem para todos os outros conetados no chat
                print(nomes[idsocket]," >>> ",sentence)
                Thread(group=None, target=enviar, name=enviar, args=(idsocket,sentence,1,), kwargs={}).start()

def enviar(idsocket,mensagem,key):
        global connectionSocket#vetor de conexões
        global nomes#vetor com nick das conexões
        global numero_de_clientes#numero de clientes
        if key==1:
            auxmensagem = nomes[idsocket] + " >>> " + mensagem#Montando a mensagem no padrão exigido pelo chat
        else:
            auxmensagem=mensagem
        for i in range(numero_de_clientes):#começando a enviar para todos os cliente
           if idsocket != i and bool[i]:#encvia para todos os clientes, menos quem me enviou a mensagem
                connectionSocket[i].send(auxmensagem.encode())#envio da mensagem propriamente dito'''


def aceitar_novas_conexoes():                                                    #Essa é a thread principal
        global connectionSocket                                                  #ela nao tem self ou class porque nao precisa de parametros
        global addrs
        global numero_de_clientes  #Numeros de cliente
        global chaveacc

        while chaveacc:
            connectionSocketaux,addraux=serverSocket.accept()                    #Aguardando a conexão de um novo cliente]
            connectionSocket.append(connectionSocketaux)
            addrs.append(addraux)
            bool.append(True)
            Thread(group=None, target=recebe, name=recebe, args=(numero_de_clientes,), kwargs={}).start()   #Cria a threade que vai receber com o nick e o id do novo cliente
            numero_de_clientes+=1 # inclementa o numero de clientes

def gerarlista():
    aux3 = ''
    for i in range(numero_de_clientes):  # começando a enviar para todos os cliente
        if bool[i]:  # encvia para todos os clientes, menos quem me enviou a mensagem
            aux3 += str(nomes[i]) + ":" + str(addrs[i]) + ";"
    if aux3=='':
        aux3='Não há clientes conectados!'
    return aux3

Thread(target=aceitar_novas_conexoes).start()
chaveserv=True
while chaveserv:
    entrada=input('Terminal:')
    if entrada=='lista()':
        aux3 = gerarlista()
        print(aux3)
    elif entrada=='sair()':
        print('Finalizando o servidor')
        for i in range(numero_de_clientes):#começando a enviar para todos os cliente
           if bool[i]:#encvia para todos os clientes, menos quem me enviou a mensagem
                connectionSocket[i].send('sair()2'.encode())#envio da mensagem propriamente dito'''
        time.sleep(1)
        serverSocket.close()
        chaveserv=False
        chaveacc=False
        os._exit(1)
    else:
        print('\nCOMANDO INVALIDO\n')
