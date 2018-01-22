# coding=utf-8

'''

b = flatbuffers.Builder(0)

        # make a child Monster within a vector of Monsters:
        MyGame.Example.Monster.MonsterStart(b)
        MyGame.Example.Monster.MonsterAddHp(b, 99)
        sub_monster = MyGame.Example.Monster.MonsterEnd(b)

        # build the vector:
        MyGame.Example.Monster.MonsterStartTestarrayoftablesVector(b, 1)
        b.PrependUOffsetTRelative(sub_monster)
        vec = b.EndVector(1)

        # make the parent monster and include the vector of Monster:
        MyGame.Example.Monster.MonsterStart(b)
        MyGame.Example.Monster.MonsterAddTestarrayoftables(b, vec)
        mon = MyGame.Example.Monster.MonsterEnd(b)
        b.Finish(mon)



b = flatbuffers.Builder(0)

accountStr = b.CreateString("accountcccddddcc4444333")
versionStr = b.CreateString("2017.10.17.ddddd1")

EnterGame.EnterGameStart(b)
EnterGame.EnterGameAddPlatform(b,1)
EnterGame.EnterGameAddAccount(b,accountStr)
EnterGame.EnterGameAddVersion(b,versionStr)

req = EnterGame.EnterGameEnd(b)
b.Finish(req)

data = b.Output()

print(len(data))


monsterAccount = EnterGame.EnterGame.GetRootAsEnterGame(data,0)

print(monsterAccount.Account())




from protos import EnterGameResp

b = flatbuffers.Builder(0)
EnterGameResp.EnterGameRespStart(b)
EnterGameResp.EnterGameRespAddRet(b, EnterGameErrorCode.EnterGameErrorCode.Succeed)
req = EnterGameResp.EnterGameRespEnd(b)
b.Finish(req)
print(len(b.Output()))

'''
from NetProto import Proto
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import time

#req = Proto.EnterGameReq()

resp = Proto.SEnterGameResp(Proto.SEnterGameRespErrorCode.Faild)

print(resp.errorCode)



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


PACKAGE_FLAG = 0xf638
PACKAGE_GUID = 11111


def PackData(protoId, bytedata):
    sendbytes = bytearray()
    sendbytes[0:] = UShortToBytes(PACKAGE_FLAG)
    sendbytes[2:] = ULongToBytes(PACKAGE_GUID)
    sendbytes[10:] = IntToBytes(protoId)
    sendbytes[14:] = UIntToBytes(len(bytedata))
    sendbytes[18:] = bytedata
    return sendbytes




def HandleHeartBeatReq(client, bytedata):
    clientReq = Proto.RHeartBeatReq(bytedata)
    timestamp = int(time.time())
    resp = Proto.SHeartBeatResp(timestamp)
    protoBytes = resp.GetBytes()
    sendBytes = PackData(Proto.ProtoID.ProtoID.HeartBeatResp,protoBytes)
    client.transport.write(sendBytes)
    print("heart beat response:",client.addr.host)


protoHandlerDict = {
    Proto.ProtoID.ProtoID.HeartBeatReq:HandleHeartBeatReq,
}


def GetHandler(protoId):
    if protoHandlerDict.__contains__(protoId):
        print("Find Handler")
        return protoHandlerDict[protoId]
    return None
