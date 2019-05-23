from socket import *
import sys

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
macAddress='881FA11D3E14'
ipAddress=' '


def listenForMsg():
    message=''
    while (message==''):
            message,serverAddress = clientSocket.recvfrom(2048)
            modifiedMessage = message.decode().upper()
            
    return modifiedMessage

def checkMac(message):
    if message==macAddress:
        #print(message)
        #print(macAddress)
        return True
    else:
        return False

def sendRequest(ipOffered):
    request="REQUEST|"+str(macAddress)+"|"+str(ipOffered)
    clientSocket.sendto(request.encode(),(serverName, serverPort))
    #print(request)
    
    
def sendDiscover():
    discover="DISCOVER|"+str(macAddress)
    clientSocket.sendto(discover.encode(),(serverName, serverPort))
    #print (modifiedMessage.decode())

def sendRelease():
    release="RELEASE|"+str(macAddress)+"|"+str(ipAddress)
    clientSocket.sendto(release.encode(),(serverName, serverPort))
    #print(ipAddress)

def sendRenew():
    print(ipAddress)
    renew="RENEW|"+str(macAddress)+"|"+str(ipAddress)
    clientSocket.sendto(renew.encode(),(serverName, serverPort))
    
def seperateMsg(message):
    msg=['','','']
    msgIndex=0
    for i in range(len(message)):
        if message[i]=="|":
            msgIndex=msgIndex+1
        else:
            msg[msgIndex]=msg[msgIndex]+message[i]
    #print(msg)
    return msg

def identifyMessage(message,ipAddress):
    msg=seperateMsg(message)
    print(msg)
    if (msg[0]=="OFFER"):
        checkFlag=False
        checkFlag=checkMac(msg[1])
        if checkFlag:
            sendRequest(msg[2])#sent with ip Offered
    if(msg[0]=="ACKNOWLEDGE"):
        checkFlag=False
        checkFlag=checkMac(msg[1])
        ipAddress=msg[2]
        #print()
        if checkFlag ==False:
            print("Error:Recieved Wrong MAC Address")
            sys.exit()
    return ipAddress
    #print(msg)
        
def displayMenu(ipAddress):
    while True:
        choice=''
        print("To Release <re>")
        print("To Renew <rn>")
        print("To Quit <q>")
        choice=input("Choice: ")
        if choice=="re":
            sendRelease()
        elif choice=="rn":
            sendRenew()
            message=listenForMsg()
            ipAddress=identifyMessage(message,ipAddress)
            message=listenForMsg()
            ipAddress=identifyMessage(message,ipAddress)

        elif choice=="q":
            sys.exit()
        print()
    return ipAddress

sendDiscover()
message=listenForMsg()
#print(message)
ipAddress=identifyMessage(message,ipAddress)
message=listenForMsg()
ipAddress=identifyMessage(message,ipAddress)
#print(message)
ipAddress=displayMenu(ipAddress)

    #message, clientAddress = serverSocket.recvfrom(2048)
    #print(message)
