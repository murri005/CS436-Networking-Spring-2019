from socket import *
from array import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))


#clientName='localhost'
#clientPort=12000
#clientSocket = socket(AF_INET, SOCK_DGRAM)


print ('The server is ready to receive')
assignedIPCount=0;
nextIPAddressToAssign=[192,168,1,1]
assignedIPAddresses=[]
assignedIPAddressesIndex=0
macAddresses=[[]]#contains slot index for assigned ip
macAddressesCount=0

w=3
h=255
macAddresses = [['' for x in range(w)] for y in range(h)]



systemMode=0 #0 none 1 Discover
#def initalizeVar():
 #   systemMode=0

#initalizeVar()

def decodeMacAddress(data):
    decodedMacAddress=[]
    for i in range(len(data)):
        if data[i]!=":":
            decodedMacAddress.append((data[i]))
    return decodedMacAddress#list type


def checkMacAddressForAssignedIP(data):
    for i in range(len(macAddresses)):    
        if macAddresses[i][0]==data:
            print(macAddresses[i][0])
            print(data)
            print(macAddresses[i][1])
            return True, macAddresses[i][1];
        else:
            return False, 0;

def updateMacAddresses(ipIndexLocation,macAddress,macAddressesCount,ipAddress):
    macAddresses[macAddressesCount][0]=macAddress
    macAddresses[macAddressesCount][1]=ipAddress
    macAddresses[macAddressesCount][2]=ipIndexLocation
    macAddressesCount=macAddressesCount+1
    
    


def whatToSend(found,ipAddressFound,msg,clientAddress):
    if found==True:
        offer="OFFER|"+str(msg[1])+"|"+str(ipAddressFound)
        serverSocket.sendto(offer.encode(),clientAddress)
        print(offer)
    elif assignedIPCount<256:
        convertIP=''.join(str(e) for e in nextIPAddressToAssign)
        offer="OFFER|"+str(msg[1])+"|"+str(convertIP)
        serverSocket.sendto(offer.encode(),clientAddress)
    else:
        serverSocket.sendto('DECLINE|'.encode(),clientAddress)
    #print(offer)

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

def processRequest(msg,recievedIP,clientAddress,assignedIPAddressesIndex,macAddressesCount):
    assignedFlag=False
    for i in range(len(assignedIPAddresses)):
        if(assignedIPAddresses[i]==recievedIP):
            assignedFlag=True
            break
    if assignedFlag:
        convertIP=''.join(str(e) for e in nextIPAddressToAssign)
        offer="OFFER|"+str(msg[1])+"|"+str(convertIP)
        serverSocket.sendto(offer.encode(),clientAddress)
        #print(offer)
        return
    else:
        offer="ACKNOWLEDGE|"+str(msg[1])+"|"+str(recievedIP)
        serverSocket.sendto(offer.encode(),clientAddress)
        nextIPAddressToAssign[3]=nextIPAddressToAssign[3]++1
        updateMacAddresses(assignedIPAddressesIndex,msg[1],macAddressesCount,msg[2])
        assignedIPAddresses.append(msg[2])

def releaseClient(message):
    #print(macAddresses)
    #print(assignedIPAddresses)

    #for i in range(len(macAddresses)):
     #   if message[1]==macAddresses[i][0]:
      #      macAddresses[i][0]=""
       #     macAddresses[i][1]=""
        #    break
        #print(message[2])
    assignedIPAddresses.remove(message[2])
    #for i in range(len(assignedIPAddresses)):
     #   if assignedIPAddresses[i]==message[2]:
      #      assignedIPAddresses=""
            #break
    #print(macAddresses)
    #print(assignedIPAddresses)
    
def renew(msg,clientAddress):
    #print('InREnew')
    ip=""
    for i in range(len(macAddresses)):
        if msg[1]==macAddresses[i][0]:
            ip=macAddresses[i][1]
            break
    if len(ip)>0:
        flag=False
        for i in range(len(assignedIPAddresses)):
            if msg[1]==assignedIPAddresses[i]:
                flag==True
        if flag==True:#assign ip
            convertIP=''.join(str(e) for e in nextIPAddressToAssign)
            offer="OFFER|"+str(msg[1])+"|"+str(convertIP)
            serverSocket.sendto(offer.encode(),clientAddress)
        else:
            offer="OFFER|"+str(msg[1])+"|"+str(ip)
            serverSocket.sendto(offer.encode(),clientAddress)
            #print(offer)
    else:
        offer="OFFER|"+str(msg[1])+"|"+str(ip)
        serverSocket.sendto(offer.encode(),clientAddress)
        #print(offer)
        
    
def identifyMessage(message,clientAddress,assignedIPAddressesIndex,macAddressesCount):
        msg=seperateMsg(message)
        print(msg)
        if msg[0] == "DISCOVER":
            checkFlag=False
            ipAddressFound=0;
            checkFlag,ipAddressFound = checkMacAddressForAssignedIP(msg[1])
            whatToSend(checkFlag,ipAddressFound,msg,clientAddress)
          #print(systemMode)
        elif msg[0]== "REQUEST":
            processRequest(msg,msg[2],clientAddress,assignedIPAddressesIndex,macAddressesCount)
        elif msg[0]== "RELEASE":
            releaseClient(msg,)
        elif msg[0]== "RENEW":
            renew(msg,clientAddress)
        

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    #print(message.decode())
    modifiedMessage = message.decode().upper()
    identifyMessage(modifiedMessage,clientAddress,assignedIPAddressesIndex,macAddressesCount)
    #serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    #print(modifiedMessage)
