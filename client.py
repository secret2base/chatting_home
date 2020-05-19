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
    print("*pchat      :私聊            *")
    print("*exit       :退出            *")
    print("******************************")

    s = threading.Thread(target=func_accept_server, args=(c,))
    s.setDaemon(True)
    s.start()

    while True:
        time.sleep(1)
        order = raw_input("请输入你的命令：")
        c.send(order.encode('utf-8'))
        if order == 'exit':
            print("聊天结束")
            break
        elif order == 'pchat':
            aim_id = raw_input("接收者ID：")
            c.send(aim_id.encode('utf-8'))
            print("如果你想退出当前聊天，请输入:q")
            while True:
                time.sleep(1)
                data = raw_input("输入：")
                c.send(data.encode('utf-8'))
                if data == 'q':
                    break
        else:
            continue
    
    print("退出中...")
    c.close()





if __name__ == '__main__':
    ip_addr = ('127.0.0.1',8000)
    c = func_connect_server(ip_addr)
    func_chat(c)
