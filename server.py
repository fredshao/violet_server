from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import struct
import asyncio
import threading
import time
import ProtoHandle

PACKAGE_FLAG = 0xf638
PACKAGE_GUID = 11111



PACKAGE_HEAD_FLAG_LEN = 2
PACKAGE_HEAD_GUID_LEN = 8
PACKAGE_HEAD_PROTO_ID = 4
PACKAGE_HEAD_DATA_LEN = 4
PACKAGE_HEAD_LEN = 18


def UShortToBytes(usNum):
    return usNum.to_bytes(2, byteorder='little')

def BytesToUShort(bytes):
    return int.from_bytes(bytes, byteorder='little')

def UIntToBytes(uiNum):
    return uiNum.to_bytes(4, byteorder='little')

def BytesToUInt(bytes):
    return int.from_bytes(bytes, byteorder='little')

def ULongToBytes(ulNum):
    return ulNum.to_bytes(8, byteorder='little')

def BytesToULong(bytes):
    return int.from_bytes(bytes, byteorder='little')

def ShortToBytes(sNum):
    return sNum.to_bytes(2, byteorder='little', signed=True)

def BytesToShort(bytes):
    return int.from_bytes(bytes, byteorder='little', signed=True)

def IntToBytes(iNum):
    return iNum.to_bytes(4, byteorder='little', signed=True)

def BytesToInt(bytes):
    return int.from_bytes(bytes, byteorder='little', signed=True)

def LongToBytes(lNum):
    return lNum.to_bytes(8, byteorder='little', signed=True)

def BytesToLong(bytes):
    return int.from_bytes(bytes, byteorder='little', signed=True)


def PackData(protoId, bytedata):
    sendbytes = bytearray()
    sendbytes[0:] = UShortToBytes(PACKAGE_FLAG)
    sendbytes[2:] = ULongToBytes(PACKAGE_GUID)
    sendbytes[10:] = IntToBytes(protoId)
    sendbytes[14:] = UIntToBytes(len(bytedata))
    sendbytes[18:] = bytedata
    return sendbytes


class AppDataSet(object):
    def __init__(self):
        pass


class UserProtocol(Protocol):
    def __init__(self, factory, addr):
        self.factory = factory
        self.addr = addr
        self.buffer = bytearray()
        self.currBufferLen = 0

    def connectionMade(self):
        print("Client connected: ", self.addr.host,self.addr.port)
        #self.transport.write("Welcome meetthere!\n".encode('utf-8'))
        self.factory.OnClientConnected(self)

    def connectionLost(self, reason):
        print("Client lost: ", self.addr.host)
        self.factory.OnClientClosed(self)


    def UnPackData(self):
        if(self.currBufferLen <= PACKAGE_HEAD_LEN):
            return

        flagBytes = self.buffer[0:PACKAGE_HEAD_FLAG_LEN]
        print("flagBytes len:",len(flagBytes))
        guidBytes = self.buffer[2:PACKAGE_HEAD_GUID_LEN + 2]
        print("guidBytes len:",len(guidBytes))
        protoIdBytes = self.buffer[10:PACKAGE_HEAD_PROTO_ID + 10]
        print("protoIdBytes len:", len(protoIdBytes))
        dataLenBytes = self.buffer[14:PACKAGE_HEAD_DATA_LEN + 14]
        print("dataLenBytes len:",len(dataLenBytes))

        flag = BytesToUShort(flagBytes)
        guid = BytesToULong(guidBytes)
        protoId = BytesToInt(protoIdBytes)
        dataLen = BytesToUInt(dataLenBytes)

        totalPackageLen = PACKAGE_HEAD_LEN + dataLen

        #print(flag, guid, protoId, dataLen, totalPackageLen,self.currBufferLen)

        # the package not complete
        if(self.currBufferLen - PACKAGE_HEAD_LEN < dataLen):
            return

        # package complete , unpack the package
        dataBytes = self.buffer[PACKAGE_HEAD_LEN:totalPackageLen]
        self.buffer[0:totalPackageLen] = b''
        self.currBufferLen -= totalPackageLen

        # deserialize object from flatbuffer
        handler = ProtoHandle.GetHandler(protoId)
        if (handler is None):
            print("Un handled proto:",protoId)
        else:
            print("Handle Proto:",protoId)
            handler(self,dataBytes)

    def dataReceived(self, data):

        received_len = len(data)

        print("Received Data Len:",received_len)

        if(received_len == 0):
            return

        self.buffer[self.currBufferLen:] = data
        self.currBufferLen += received_len

        self.UnPackData()

        #if(self.currBufferLen > PACKAGE_HEAD_LEN):
            #UnPackData()

    def HeartBeatTick(self,timestamp):
        pass




class UserFactory(Factory):
    def __init__(self):
        self.appData = AppDataSet()
        self.clients = []
        #threading.Thread(target=self.Broadcast,args=()).start()

    def buildProtocol(self, addr):
        return UserProtocol(self,addr)

    def OnClientConnected(self,client):
        self.clients.append(client)

    def OnClientClosed(self,client):
        self.clients.remove(client)

    def Broadcast(self):
        while True:
            timestamp = int(time.time())
            print("tick: ",timestamp)
            time.sleep(1)


reactor.listenTCP(8000, UserFactory())
reactor.run()