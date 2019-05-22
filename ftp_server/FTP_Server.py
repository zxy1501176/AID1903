"""
ftp　文件服务器
并发网络功能训练
"""

from socket import *
from threading import Thread
import os
from time import sleep

# 　全局变量
HOST = '0.0.0.0'
PORT = 8080
ADDR = (HOST, PORT)
FTP = "/home/tarena/project/pythonNet/net/day07/ftp_lib/"  # 文件库路径


# 将客户端请求功能封装为类
class FtpServer:
    def __init__(self, connfd, FTP_PATH):
        self.connfd = connfd
        self.path = FTP_PATH
        self.file_list = []
        self.send_file_list = []
        self.allfile_bak = []

    def get_all_file(self):
        self.file_list.clear()
        self.send_file_list.clear()
        self.allfile_bak.clear()
        for i in os.walk(self.path):  # 遍历指定目录下的所有的文件
            self.file_list.append(i)
        print(self.file_list)
        for i in range(len(self.file_list)):
            print("i = ", i)
            for item in self.file_list[i][-1]:
                print(item)
                if os.path.isfile(os.path.join(self.file_list[i][0], item)) and item[0] != ".":
                    self.allfile_bak.append(os.path.join(self.file_list[i][0], item))
                    self.send_file_list.append(item)
        print(self.send_file_list)
        print(self.allfile_bak)

    #
    # ['Linux.html', 'exercise.txt', '4_3态.png', '6_ctype.png', '4_5态.png']
    # ['/home/tarena/month02/pythonNet/day07/ftp_lib/data/Linux.html',
    #  '/home/tarena/month02/pythonNet/day07/ftp_lib/data/exercise.txt',
    #  '/home/tarena/month02/pythonNet/day07/ftp_lib/image/4_3态.png',
    #  '/home/tarena/month02/pythonNet/day07/ftp_lib/image/6_ctype.png',
    #  '/home/tarena/month02/pythonNet/day07/ftp_lib/image/4_5态.png']

    def send_ok(self):
        sleep(0.1)
        self.connfd.send(b"OK")
        sleep(0.1)

    def send_end(self):
        sleep(0.1)
        self.connfd.send(b"##")
        sleep(0.1)

    def do_list(self):
        # 　获取文件列表
        print("enter do_list")
        self.get_all_file()
        if len(self.send_file_list) == 0:
            self.connfd.send("没有文件".encode())
        else:
            self.send_ok()
            all_files = " ".join(self.send_file_list)
            self.connfd.send(all_files.encode())

    def do_get(self, filename):
        print("enter do_get", filename)

        self.get_all_file()
        if filename not in self.send_file_list:
            print("客户端输入文件名不存在")
            print(filename)
            self.connfd.send("客户端输入文件名不存在".encode())
            return
        else:
            self.send_ok()
            print(filename)

        for item in self.allfile_bak:
            if filename == item.split("/")[-1]:
                fd = open(item, 'rb')
                while True:
                    data = fd.read(1024)
                    if not data:
                        self.send_end()
                        fd.close()
                        return
                    self.connfd.send(data)

    def do_up(self, filename):
        filepath = self.path + "upload/" + filename
        print(filepath)
        if os.path.exists(filepath):
            os.remove(filepath)
        self.send_ok()
        print(filepath)
        fd = open(filepath, "wb")
        while True:
            data = self.connfd.recv(1024)
            if data == b"##":
                print("传送完毕")
                fd.flush()
                fd.close()
                break
            elif data.decode() == "":
                print("传送文件为空")
                fd.close()
            else:
                fd.write(data)


# 客户端请求处理函数
def handle(connfd):
    # 　选择文件夹
    ftp = FtpServer(connfd, FTP)
    print(ftp)
    while True:
        # 接受客户端请求
        data = connfd.recv(1024).decode()
        # 　如果客户端断开返回ｄａｔａ为空
        if not data or data[0] == 'Q':
            return
        elif data[0] == 'L':
            ftp.do_list()
        elif data[0] == "G":
            filename = data.split(" ")[-1]
            ftp.do_get(filename)
        elif data[0] == "P":
            filename = data.split(" ")[-1]
            ftp.do_up(filename)
        else:
            print("接收指令错误", data)


# 网络搭建
def main():
    # 　创建套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print("Listen the port 8080...")
    while True:
        try:
            connfd, addr = sockfd.accept()
        except KeyboardInterrupt:
            print("退出服务程序")
            return
        except Exception as e:
            print(e)
            continue
        print("链接的客户端：", addr)
        # 　创建线程处理请求
        client = Thread(target=handle, args=(connfd,))
        client.setDaemon(True)
        client.start()


if __name__ == "__main__":
    main()
