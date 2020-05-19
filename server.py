#-*- coding:utf8 -*-
import socket
from time import ctime
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Client(threading.Thread):
    client_dict = {}

    def __init__(self,sock,addr):
        threading.Thread.__init__(self)
        self.sock = sock
        self.addr = addr


    def online(self):
        client_on_str = ""
        for user in Client.client_dict:
            client_on_str = client_on_str + user + '\n'
        client_on_str = client_on_str + "--------------\n"
        return client_on_str


    def airing(self,data):
        print(data)
        for user in Client.client_dict:
            client_sock = Client.client_dict[user]
            client_sock.send((data).encode('utf-8'))


    def private_chat(self,data,aim_id,user_id):
        result = ""
        if aim_id == user_id:
            result = "不可以给自己发消息！"
        else:
            if aim_id in Client.client_dict:
                context = "%s跟你说：%s        %s"%(user_id,data,ctime())
                aim_sock = Client.client_dict[aim_id]
                aim_sock.send(context.encode('utf-8'))
                print("%s跟%s说：%s     %s"%(user_id,aim_id,data,ctime()))
                result = "发送成功！        %s"%ctime()
            else:
                result = "发送失败！该用户不在线！      %s"%ctime()
        return result


    def run(self):
        user_id = self.sock.recv(1024).decode('utf-8')
        Client.client_dict[user_id] = self.sock
        air_data = "%s 已连接！     %s"%(user_id,ctime())
        self.airing(air_data)
        try:
            while True:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'exit':
                    Client.client_dict.pop(user_id)
                    air_data = "%s 已下线！     %s"%(user_id,ctime())
                    print("%s 已下线！"%user_id)
                    self.airing(air_data)
                    self.sock.close()
                    break
                elif message == "pchat":
                    aim_id = self.sock.recv(1024).decode('utf-8')
                    while True:
                        data = self.sock.recv(1024).decode('utf-8')
                        if data != 'q':
                            result = self.private_chat(data,aim_id,user_id)
                            self.sock.send(result.encode('utf-8'))
                        else:
                            break

                elif message == "online":
                    client_online = self.online()
                    print(client_online)
                    self.sock.send(("当前在线人员:\n--------------  %s\n%s"%(ctime(),client_online)).encode('utf-8'))
                else:
                    self.sock.send("无该命令！".encode('utf-8'))
                    continue

        except Exception,e:
            print(e)
            if user_id in Client.client_dict:
                Client.client_dict.pop(user_id)
                air_data = "%s 已下线！     %s"%(user_id,ctime())
                self.airing(air_data)
                print("%s 已断开！      %s"%(user_id,ctime()))
                self.sock.close()
            

def func_make_server(ip_addr):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(ip_addr)
    s.listen(5)
    return s



def func_accept_client(s):
    while True:
        client_sock,client_addr = s.accept()
        Client_connect = Client(client_sock,client_addr)
        Client_connect.start()

if __name__ == '__main__':
    ip_addr = ("127.0.0.1",8000)
    s = func_make_server(ip_addr)
    func_accept_client(s)
