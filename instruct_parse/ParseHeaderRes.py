import json

from instruct_parse.CIstruct.define_cim_struct import magnetic_file_name
from instruct_parse.InstructionsModel import *
from tool.api_parsechar import BinaryToChar, CharToBinary


def SetProtocolHeader(module, ins, length):

    ch = fcps_command_header_t(FCPS_PROTOCOL_CMD_MAGIC, module, ins, length)

    return ch.pack()


def CheckResp(buffer):
    ch = fcps_response_header_t(buffer)

    flag = ch.magic == FCPS_PROTOCOL_RESP_MAGIC

    return flag, ch.status, ch.respDataLen

if __name__ == "__main__":
    print(CharToBinary("12"))
    buff = magnetic_file_name("12").pack(True)

    buff = SetProtocolHeader(6, 0x37, len(buff)) + buff
    print(BinaryToChar(buff))
    print(struct.unpack("I", ""))