"""
搭建数据报套接字
"""
from socket import *
import os, sys, time

# 消息结构：　Ｃ　发送者名称　内容
recv_chat_msg = {}
# 服务器地址
ADDR = ("176.122.17.105", 9998)
name = ""
msg_type = ["L", "C", "Q"]


def request_login(s):
    for i in range(5):
        global name
        name = ""
        name = input("请输入你的昵称：")
        result = send_login(s)
        if result:
            return True
    name = ""
    return False


def recv_msg(s):
    msg, addr = s.recvfrom(2048)
    list_msg = msg.decode().split(" ")
    str_msg = " ".join(list_msg[2:])

    if list_msg[0] not in msg_type:
        print("收到的信息类型错误", str_msg[0])
        return

    if list_msg[0] == msg_type[0]:
        if str_msg == "ok":
            print("你已经进入聊天室")
            return True
        else:
            print(str_msg)
            return False

    if list_msg[0] == msg_type[1]:
        print(list_msg[1] + " 说：" + str_msg)
    time.sleep(1)

    if list_msg[0] == msg_type[2]:
        print("退出聊天室")
        sys.exit()




def send_login(s):
    msg = msg_type[0] + " " + name
    s.sendto(msg.encode(), ADDR)
    return recv_msg(s)

def send_msg(s):
    try:
        msg = input("请输入你的消息：")
    except KeyboardInterrupt:
        msg = "quit"

    if msg == "quit":
        msg = msg_type[2] + " " + name
        s.sendto(msg.encode(), ADDR)

    if msg != "":
        msg = msg_type[1] + " %s %s" % (name, msg)
        s.sendto(msg.encode(), ADDR)


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    i = 0
    loginstatus = request_login(s)
    if loginstatus:  # login success
        pid = os.fork()
        if pid < 0:
            sys.exit("Error")
        elif pid == 0:
            while True:
                time.sleep(0.3)
                recv_msg(s)
        else:
            while True:
                try:
                    pid, status = os.waitpid(-1, os.WNOHANG)
                # 非等待,当该次运行到此处时，子进程没有退出的情况下返回为０，本次不处理
                except ChildProcessError as e:
                    print("接收消息的子进程异常，退出")
                    return

                time.sleep(0.2)
                send_msg(s)


    else:
        print("5次登录均不成功，退出")
        return


if __name__ == "__main__":
    main()
