from socket import *
import sys
from time import sleep


# 具体功能
class FtpClient:
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def send_ok(self):
        sleep(0.01)
        self.sockfd.send(b"OK")
        sleep(0.01)

    def send_end(self):
        sleep(0.01)
        self.sockfd.send(b"##")
        sleep(0.01)

    def do_list(self):
        self.sockfd.send(b'L')  # 发送请求
        # 等待回复
        data = self.sockfd.recv(128).decode()
        # 　ｏｋ表示请求成功
        if data == 'OK':
            # 　接收文件列表
            data = self.sockfd.recv(4096)
            print(data.decode())
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit("谢谢使用")

    def do_get(self, filename):
        self.sockfd.send(("G " + filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            print("接收中．．．")
            fd = open(filename, "wb")
            while True:
                data = self.sockfd.recv(1024)
                print(data)
                if data == b"##":
                    print("接收完毕")
                    # self.send_end()
                    fd.close()
                    return
                fd.write(data)
        else:
            print(data)

    def do_put(self, filename):
        try:
            f = open(filename, "rb")
        except Exception as e:
            print("没有该文件")
            return

        newfile = filename.strip(" ").split("/")[-1]
        print(newfile)
        self.sockfd.send(("P " + newfile).encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            while True:
                data = f.read(1024)
                if not data:
                    print("传送完毕")
                    self.send_end()
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)


# 发起请求
def request(sockfd):
    ftp = FtpClient(sockfd)

    while True:
        print("\n==========命令选项===========")
        print("*********** list ************")
        print("********* get file  *********")
        print("********* put file  *********")
        print("*********** quit ************")
        print("==============================")

        cmd = input("输入命令:")
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd.strip() == 'quit':
            ftp.do_quit()
        elif cmd[:3] == 'get':
            filename = cmd.strip(" ").split(" ")[-1]
            ftp.do_get(filename)
        elif cmd[:3] == "put":
            filename = cmd.strip(" ").split(" ")[-1]
            ftp.do_put(filename)


# 网络链接
def main():
    # 　服务器地址
    ADDR = ('127.0.0.1', 8888)
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print("链接服务器失败")
        return
    else:
        request(sockfd)  # 发送具体请求


if __name__ == "__main__":
    main()
