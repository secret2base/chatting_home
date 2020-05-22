#-*- coding:utf-8 -*-
import socket
import threading
import pymysql
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Screen(object):
    def print_tips(self,str_info):
        print('\033[1;34m%s\033[0m'%str_info)

    def print_info(self,str_info):
        print('\033[1;32m%s\033[0m'%str_info)

    def print_warn(self,str_info):
        print('\033[1;33m%s\033[0m'%str_info)

    def print_err(self,str_info):
        print('\033[1;31m%s\033[0m'%str_info)

    def print_beau(self,str_info):
        print('\033[1;35m%s\033[0m'%str_info)

    def raw_input_info(self,str_info):
        return raw_input('\033[1;32m%s\033[0m'%str_info)

    def mysend(self,data):
        data = data.encode("utf-8")
        self.c.send(data)

    def myrecv(self,data):
        data = data.decode("utf-8")
        return data



class Chat(Screen):
    def __init__(self,ip_addr,user_id):
        self.user_id = user_id
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
            data = self.myrecv(self.c.recv(1024))
            self.print_beau(data)
    

    def func_chat(self):
        self.mysend(self.user_id)
    
        self.print_tips("***********************")
        self.print_tips("* 1 : 显示当前在线的人*")
        self.print_tips("* 2 : 私聊            *")
        self.print_tips("* 3 : 退出            *")
        self.print_tips("***********************")
    
        s = threading.Thread(target=self.func_accept_server)
        #s.setDaemon(True)
        s.start()
    
        while True:
            time.sleep(1)
            order = self.raw_input_info("请输入你的命令:")
            self.mysend(order)
            if order == '3':
                self.print_err("聊天结束")
                break
            elif order == '2':
                aim_id = self.raw_input_info("接收者ID:")
                self.mysend(aim_id)
                self.print_err("如果你想退出当前聊天，请输入:quit")
                while True:
                    time.sleep(1)
                    data = self.raw_input_info("输入:")
                    self.mysend(data)
                    if data == 'quit':
                        break
            else:
                continue
        
        self.print_err("退出中...")
        self.c.close()

class User(Screen):
    def __init__(self,host,user,db_name,db_pwd):
        self.db = self.func_connect_mysql(host,user,db_name,db_pwd) #连接数据库
        self.func_main()  

#连接数据库函数
    def func_connect_mysql(self,host,user,db_name,db_pwd):
        message = {
              "host":host,
              "user":user,
              "password":db_pwd,
              "database":db_name,
              "autocommit":True,
              "use_unicode":True,
              "charset":'utf8'
              }
        db = pymysql.connect(**message)
        return db

#登录函数
    def func_login(self):
        flag = False
        self.print_beau("登录")
        user_name = self.raw_input_info("用户名:")
        user_pwd = self.raw_input_info("密码:")
        sql_all = "select * from users where username = '%s' and password = '%s'"%(user_name,user_pwd)
        result_all = self.cursor.execute(sql_all)
        if result_all:
            self.user_name = user_name
            self.user_pwd = user_pwd
            self.print_tips("%s登录成功"%user_name)
            sql_id = "select id from users where username = '%s'"%user_name
            row = self.cursor.execute(sql_id)
            if row:
                self.id = self.cursor.fetchone()[0]
            flag = True
        else:
            sql_name = "select * from users where username = '%s'"%user_name
            result_name = self.cursor.execute(sql_name)
            if result_name:
                self.print_err("密码错误！")
                flag = False
            else:
                self.print_err("账户不存在！")
                flag = False

        return flag
#修改用户名
    def func_change_username(self):
        flag = False
        self.print_beau("修改用户名")
        while True:
            new_username = self.raw_input_info("新用户名:")
            sql = "select * from users where username = '%s'"%new_username
            row = self.cursor.execute(sql)
            if row:
                self.print_err("用户已存在！")
                continue
            else:
                sql = "update users set username = '%s' where id = '%d'"%(new_username,self.id)
                result = self.cursor.execute(sql)
                if result:
                    flag = True
                    break
        return flag

#修改密码
    def func_change_password(self):
        flag = False
        self.print_beau("修改密码")
        while True:
            new_password = self.raw_input_info("新密码:")
            new_password_bak = self.raw_input_info("确认密码:")
            if new_password != new_password_bak:
                self.print_err("密码不一致，请重输")
                continue
            elif new_password == self.user_pwd:
                self.print_err("与旧密码一致，请重输")
            else:
                sql = "update users set password = '%s' where id = '%d'"%(new_password,self.id)
                result = self.cursor.execute(sql)
                if result:
                    flag = True
                    break
                    
        return flag
        
#修改手机号
    def func_change_phonenum(self):
        flag = False
        self.print_beau("修改手机号")
        while True:
            new_phone = self.raw_input_info("新手机号:")
            sql = "select * from users where phone = '%s'"%new_phone
            row = self.cursor.execute(sql)
            if row:
                self.print_err("该手机号已被注册，请重输")
                continue
            else:
                sql = "update users set phone = '%s' where id = '%d'"%(new_phone,self.id)
                result = self.cursor.execute(sql)
                if result:
                    flag = True
                    break

        return flag

    def func_registration(self):
        self.print_beau("注册")
        while True:
            user_name = self.raw_input_info("用户名：")
            sql1 = "select * from users where username = '%s'"%user_name
            result1 = self.cursor.execute(sql1)
            if result1:
                self.print_err("用户名已存在！")
                continue
            else:
                password = self.raw_input_info("密码：")
                password_bak = self.raw_input_info("确认密码：")
                if password != password_bak:
                    self.print_err("密码不一致")
                    continue
                else:
                    phone_number = self.raw_input_info("手机号：")
                    sql = "select * from users where phone = '%s'"%phone_number
                    row = self.cursor.execute(sql)
                    if row:
                        self.print_err("手机号已被注册")
                    else:
                        sql = "insert into users(username,password,phone) values ('%s','%s','%s');"%(user_name,password,phone_number)
                        result = self.cursor.execute(sql)
                        if result:
                            self.print_err("注册成功")
                            break
                        else:
                            self.print_err("注册失败，请重试")
    def func_find_pwd(self):
        self.print_beau("找回密码")
        while True:
            user_name = self.raw_input_info("用户名：")
            sql1 = "select * from users where username = '%s'"%user_name
            result1 = self.cursor.execute(sql1)
            if not result1:
                self.print_err("用户名不存在！")
                continue
            else:
                phone_number = self.raw_input_info("手机号：")
                sql = "select password from users where username = '%s' and phone = '%s'"%(user_name,phone_number)
                row = self.cursor.execute(sql)
                if not row:
                    self.print_err("手机号不正确")
                    continue
                else:
                    password = self.cursor.fetchone()
                    self.print_err("密码为:%s"%password)
                    break




#主函数
    def func_main(self):
        #创建数据库游标
        self.cursor = self.db.cursor()
        self.cursor.execute("create table if not exists users(id int primary key auto_increment,username char(10) unique,password char(20),phone char(11))")
        while True:
            try:
                flag_login = True
                flag_registration = ""
                password = ""
                self.print_tips("****************")
                self.print_tips("* 1 : 登录     *")
                self.print_tips("* 2 : 注册     *")
                self.print_tips("* 3 : 找回密码 *")
                self.print_tips("* 4 : 退出     *")
                self.print_tips("****************")
                num_login = self.raw_input_info("选择:")
                if num_login == '4':
                    self.print_err("退出中...")
                    time.sleep(2)
                    break
                elif num_login == '3':
                    self.func_find_pwd()
                elif num_login == '2':
                    self.func_registration()
                    continue
                elif num_login == '1':
                    flag_login = self.func_login()
                    if flag_login:
                        while True:
                            flag_alter = False
                            self.print_tips("****************")
                            self.print_tips("* 1 : 设置     *")
                            self.print_tips("* 2 : 聊天     *")
                            self.print_tips("* 3 : 退出登录 *")
                            self.print_tips("****************")
                            num_choose = self.raw_input_info("选择:")
                            if num_choose == '1':
                                while True:
                                    self.print_tips("******************")
                                    self.print_tips("* 1 : 修改用户名 *")
                                    self.print_tips("* 2 : 修改密码   *")
                                    self.print_tips("* 3 : 修改手机号 *")
                                    self.print_tips("* 4 : 退出设置   *")
                                    self.print_tips("******************")
                                    num_setting = self.raw_input_info("选择:")
                                    if num_setting == '1':
                                        flag_alter = self.func_change_username()
                                        if flag_alter:
                                            self.print_info("修改成功")
                                            break
                                        else:
                                            self.print_err("修改失败，请重试")
                                            continue
                                    elif num_setting == '2':
                                        flag_alter = self.func_change_password()
                                        if flag_alter:
                                            self.print_info("修改成功")
                                            break
                                        else:
                                            self.print_err("修改失败，请重试")
                                            continue
                                    elif num_setting == '3':
                                        flag_alter = self.func_change_phonenum()
                                        if flag_alter:
                                            self.print_info("修改成功")
                                            break
                                        else:
                                            self.print_err("修改失败，请重试")
                                            continue

                                    elif num_setting == '4':
                                        self.print_err("退出中...")
                                        time.sleep(2)
                                        break
                                    else:
                                        self.print_err("无该命令，重新选择")
                                        continue
                            elif num_choose == '2':
                                ip_addr = ('127.0.0.1',8000)
                                chat_user = Chat(ip_addr,self.user_name)
                            elif num_choose == '3':
                                self.print_err("退出中...")
                                time.sleep(2)
                                break
                            else:
                                self.print_err("无该命令，重新选择")
                                continue
                    else:
                        continue
                        
                else:
                    self.print_err("无该命令，重新选择")
                    continue
            except Exception,e:
                self.print_err(e)
                break

    

if __name__ == '__main__':
    #ip_addr = ('127.0.0.1',8000)
    #user = Chat(ip_addr)
    user = User("localhost","root","Student_base","123456")


