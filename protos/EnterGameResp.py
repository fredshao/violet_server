# automatically generated by the FlatBuffers compiler, do not modify

# namespace: 

import flatbuffers

class EnterGameResp(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsEnterGameResp(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = EnterGameResp()
        x.Init(buf, n + offset)
        return x

    # EnterGameResp
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # EnterGameResp
    def Ret(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 1

def EnterGameRespStart(builder): builder.StartObject(1)
def EnterGameRespAddRet(builder, ret): builder.PrependInt8Slot(0, ret, 1)
def EnterGameRespEnd(builder): return builder.EndObject()