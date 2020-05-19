#-*- coding:utf-8 -*-
import socket
import threading
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Chat(object):
    def __init__(self,ip_addr):
        self.ip_addr = ip_addr
        self.func_connect_server()
        self.func_chat()
    def func_connect_server(self):
        try:
            self.c = socket.socket()
            self.c.connect(self.ip_addr)
        except  Exception,e:
            print e
            sys.exit(1)
    
    def func_accept_server(self):
        while True:
            data = self.c.recv(1024).decode('utf-8')
            print(data)
    

    def func_chat(self):
        user_id = raw_input("请输入你的用户名：")
        self.c.send(user_id.encode('utf-8'))
    
        print("******************************")
        print("*online     :显示当前在线的人*")
        print("*pchat      :私聊            *")
        print("*exit       :退出            *")
        print("******************************")
    
        s = threading.Thread(target=self.func_accept_server)
        s.setDaemon(True)
        s.start()
    
        while True:
            time.sleep(1)
            order = raw_input("请输入你的命令：")
            self.c.send(order.encode('utf-8'))
            if order == 'exit':
                print("聊天结束")
                break
            elif order == 'pchat':
                aim_id = raw_input("接收者ID：")
                self.c.send(aim_id.encode('utf-8'))
                print("如果你想退出当前聊天，请输入:q")
                while True:
                    time.sleep(1)
                    data = raw_input("输入：")
                    self.c.send(data.encode('utf-8'))
                    if data == 'q':
                        break
            else:
                continue
        
        print("退出中...")
        self.c.close()


if __name__ == '__main__':
    ip_addr = ('127.0.0.1',8000)
    user = Chat(ip_addr)

