"""

"""

from socket import *
import os, sys

# 服务器地址
ADDR = ("0.0.0.0", 9998)
# 存储用户信息
user = {}
msg_type = ["L", "C", "Q"]

# 消息结构：　Ｃ　发送者名称　内容
recv_chat_msg = {}


def do_login(s, name, addr):
    if name in user or "管理员" in name:
        msg = "该用户名已经存在"
        do_chat(s,msg_type[0],name,msg)
        return

    do_chat(s, msg_type[0], name, b"ok")

    #
    msg = "欢迎　%s 进入聊天室" % name
    for i in user:
        s.sendto(msg.encode(), user[i])

    # 将用户加入
    user[name] = addr
    print(user)


def do_chat(s, type,name, str_msg):
    if type not in msg_type:
        return
    msg = type+" %s %s" % (name, str_msg)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])
    else:
        return


def do_quit(s, name):
    """
    用户自己退出，循环发送给其他用户
    :param s:
    :param name:
    :return:
    """
    msg = "%s 退出了聊天室" % name
    print(msg)
    if name in user:
        for i in user:
            if i != name:
                do_chat(s,msg_type[1],"管理员消息", msg)
                # s.sendto(msg.encode(), user[i])
            else:
                do_chat(s, msg_type[2], user[i], b"EXIT")#给退出用户发送ｅｘｉｔ指令

        del user[name]  # 删除用户


def do_request(s):
    """
    循环接收各种请求
    :param s:　
    :return:
    """
    while True:
        data, addr = s.recvfrom(1024)  # L zhag
        print(data.decode())
        msg = data.decode().split(" ")
        if msg[0] not in msg_type:
            return

        if msg[0] == msg_type[0]:
            do_login(s, msg[1], addr)

        elif msg[0] == msg_type[1]:
            str_msg = " ".join(msg[2:])
            do_chat(s,msg_type[1], msg[1], str_msg)

        elif msg[0] == msg_type[2]:
            do_quit(s, msg[1])


# 创建网络链接
def main():
    # socket
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
    # 发送管理员消息
    elif pid == 0:
        while True:
            if len(user)!=0:
                msg = input("管理员消息：")
                if msg != "":
                    do_chat(s, msg_type[1],"管理员消息", msg)
    else:
        while True:
            do_request(s)  # 请求客户端处理


if __name__ == "__main__":
    main()
