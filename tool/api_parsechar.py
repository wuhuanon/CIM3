import binascii
import struct

def BinaryToChar(b):
    if b:
        return binascii.b2a_hex(b).upper().decode('utf-8')
    else:
        return ''

def CharToBinary(b):
    if b:
        return binascii.a2b_hex(b)
    else:
        return ''

if __name__ == "__main__":
    # print(struct.pack("10s", "asf"))
    print(BinaryToChar(b"123456AB01"))