#-*- coding:utf-8 -*-
import socket
import threading
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def func_connect_server(ip_addr):
    try:
        c = socket.socket()
        c.connect(ip_addr)
        return c
    except  Exception,e:
        print e
        sys.exit(1)

def func_accept_server(c):
    while True:
        data = c.recv(1024).decode('utf-8')
        print(data)


def func_chat(c):
    user_id = raw_input("请输入你的用户名：")
    c.send(user_id.encode('utf-8'))
    print("******************************")
    print("*online     :显示当前在线的人*")
    print("*privatechat:私聊            *")
    print("*exit       :退出            *")
    print("******************************")
    s = threading.Thread(target=func_accept_server, args=(c,))
    s.setDaemon(True)
    s.start()

    global is_exit

    while True:
        order = raw_input("请输入你的命令：")
        c.send(order.encode('utf-8'))
        if order == 'exit':
            print("聊天结束")
            break
        elif order == 'privatechat':
            aim_id = raw_input("接收者ID：")
            c.send(aim_id.encode('utf-8'))
            data = raw_input("发送内容：")
            c.send(data.encode('utf-8'))
        else:
            continue
    
    print("退出中...")
    c.close()





if __name__ == '__main__':
    ip_addr = ('127.0.0.1',8000)
    c = func_connect_server(ip_addr)
    func_chat(c)
