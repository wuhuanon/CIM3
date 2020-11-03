# coding: utf-8
import socket
import json
import struct
import threading


# server_config = [("10.100.102.66", 20201), ("10.100.102.66", 20202), ("10.100.101.220", 20203), ("10.100.101.78", 9888), ("10.100.101.78", 9666)]
# server_config = [("10.100.101.220", 20201), ("10.100.101.220", 20202), ("10.100.101.220", 20203), ("10.100.101.78", 9888), ("10.100.103.182", 9666)]
# server_config = ("1270.0.1", 9999)
# print(server_config)
# size = config.get("IpAddress", 'address', 2048)

# @singleton
from pubsub import pub


class ClientSocket(object):
    def __init__(self):
        self.__client = socket.socket()
        self.isConnect = False
        self.timeout = 120
        self.__client.settimeout(3)

    def connect(self, address):
        # Create aTCP/IP socket
        connect_time = 0
        while connect_time < 3:
            try:
                connect_time += 1
                self.__client.connect(address)
                # print(server_address[connect])
                self.isConnect = True
                self.__client.settimeout(self.timeout)
                return
            except OSError:
                self.__client = socket.socket()
                self.__client.settimeout(3)
                # self.__client.connect(server_config[connect])
                # self.isConnect = True
        # pub.sendMessage("serverError")

    def send(self, data):
        flag = False
        try:
            if self.__client:
                # with self.lock:
                self.__client.sendall(data)
                flag = True

        except socket.error as e:
            import traceback
            traceback.print_exc(e)
            self.isConnect=False
            pub.sendMessage("serverError")
        except ConnectionResetError:
            pub.sendMessage("serverError")
            raise ConnectionResetError
        except Exception as e:
            import traceback
            traceback.print_exc(e)
            self.isConnect=False
            pub.sendMessage("serverError")
        finally:
            # self.__client.close()
            return flag

    def recive(self, bufsize=1024):
        data = ""
        try:

            data = self.__client.recv(bufsize)

            return data

        except socket.timeout as t:
            print(t, "1")
            self.isConnect=False

        except socket.error as e:
            print(e, "2")
            self.isConnect=False
        except Exception as e:

            import traceback
            traceback.print_exc()
        finally:
            return data

    def settimeout(self, timeout):
        if self.__client:
            self.timeout = timeout
            self.__client.settimeout(self.timeout)

    def close(self):
        if self.__client:
            self.__client.close()

    def getFile(self):
        return self.__client.fileno()


if __name__ == '__main__':
    server_address = ('10.100.101.210', 20202)
    client = ClientSocket()
    client.connect(1)
    client.recive()
    print("连接成功", client)
    # send_data = {"magic": 1, "function_id": 1, "data": {"name": "wu1", "pin": "12345678"}}
    # client.send(send_data)
    # data = client.recive()
    #
    # client.close()
    # print("连接关闭")