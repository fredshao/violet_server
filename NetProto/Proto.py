import flatbuffers
from protos import EnterGameReq
from protos import EnterGameResp
from protos import EnterGameErrorCode
from protos import HeartBeatReq
from protos import HeartBeatResp
from protos import ProtoID

class REnterGameReq(object):
    def __init__(self, bytedata):
        req = EnterGameReq.EnterGameReq.GetRootAsEnterGameReq(bytedata,0)
        self.account = req.Account()
        self.platform = req.Platform()
        self.version = req.Version()


class SEnterGameRespErrorCode(object):
    Succeed = 0
    Faild = 1


class SEnterGameResp(object):
    def __init__(self, errorCode):
        self.errorCode = errorCode

    def GetBytes(self):
        b = flatbuffers.Builder(0)
        EnterGameResp.EnterGameRespStart(b)
        EnterGameResp.EnterGameRespAddRet(b, self.errorCode)
        resp = EnterGameResp.EnterGameRespEnd(b)
        b.Finish(resp)
        return b.Output()

class RHeartBeatReq(object):
    def __init__(selfs,bytedata):
        req = HeartBeatReq.HeartBeatReq.GetRootAsHeartBeatReq(bytedata,0)


class SHeartBeatResp(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def GetBytes(self):
        b = flatbuffers.Builder(0)
        HeartBeatResp.HeartBeatRespStart(b)
        HeartBeatResp.HeartBeatRespAddTimestamp(b,self.timestamp)
        resp = HeartBeatResp.HeartBeatRespEnd(b)
        b.Finish(resp)
        return b.Output()