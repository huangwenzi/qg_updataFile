import socket
import sys
import json
import select
import time            


# 热更socket管理
class NetMgr():
    
    # 连接进来的服务端
    socket_list = []

    # 初始化
    # ip        :   监听的ip
    # port_list ：  监听的端口
    def __init__(self, ip, port_list):
        # 初始化监听的socket
        for tmp_port in port_list:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            s.connect((ip, tmp_port + 2))
            s.setblocking(False)
            self.socket_list.append(s)

    # 给客户端发送文件
    # file_list     :   文件列表
    def send_hot_file(self, file_list):
        # 循环文件列表
        for tmp_file in file_list:
            # 获取文件名
            begin_idx = tmp_file.rfind("\\") + 1
            end_idx = tmp_file.rfind(".")
            file_name = tmp_file[begin_idx:end_idx]
            send_str = "hot %s\r\n"%(file_name)
            # 循环服务端
            for tmp_s in self.socket_list:
                tmp_s.send(send_str.encode("utf8"))
