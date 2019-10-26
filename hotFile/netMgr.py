import socket
import sys
import json
import select
import time            
import platform

# 套接字类
class SvrSocket():
    # socket
    t_socket = None
    t_ip = None
    t_port = None

    def __init__(self, t_socket, t_ip, t_port):
        self.t_socket = t_socket
        self.t_ip = t_ip
        self.t_port = t_port
        

# 热更socket管理
class NetMgr():
    
    # 连接进来的服务端
    socket_list = []
    # 连接失败的服务端
    fail_list = []
    # 系统类型
    sysstr = ""

    # 初始化
    # ip        :   监听的ip
    # port_list ：  监听的端口
    def __init__(self, ip, port_list):
        self.sysstr = platform.system()
        # 初始化监听的socket
        for tmp_port in port_list:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                s.connect((ip, tmp_port + 2))
                s.setblocking(False)
                tmp_svr = SvrSocket(s, ip, tmp_port)
                self.socket_list.append(tmp_svr)
            except :
                self.fail_list.append({
                    "ip":ip, "tmp_port":tmp_port
                })
            
        

    # 给客户端发送文件
    # file_list     :   文件列表
    def send_hot_file(self, file_list):
        # 尝试连接失败的服务器
        tmp_fail_list = []
        for tmp_fail in self.fail_list:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                s.connect((tmp_fail["ip"], tmp_fail["tmp_port"] + 2))
                s.setblocking(False)
                tmp_svr = SvrSocket(s, tmp_fail["ip"], tmp_fail["tmp_port"])
                self.socket_list.append(tmp_svr)
            except :
                tmp_fail_list.append({
                    "ip":tmp_fail["ip"], "tmp_port":tmp_fail["tmp_port"]
                })
        self.fail_list = tmp_fail_list

        # 循环文件列表
        for tmp_file in file_list:
            # 获取文件名
            file_name = self.get_file_name(tmp_file)
            send_str = "hot %s\r\n"%(file_name)
            # 循环服务端
            for tmp_s in self.socket_list:
                # 这里缺少断开的判断
                try:
                    tmp_s.t_socket.send(send_str.encode("utf8", errors='ignore'))
                except :
                    print("t_socket err")
                    print("t_socket ip:%s, port:%d"%(tmp_s.t_ip, tmp_s.t_port))
                    # 尝试重连
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                        s.connect((tmp_s.t_ip, tmp_s.t_port + 2))
                        s.setblocking(False)
                        tmp_s.t_socket = s
                        tmp_s.t_socket.send(send_str.encode("utf8", errors='ignore'))
                        print("t_socket Reconnect ok")
                    except :
                        self.fail_list.append({
                            "ip":tmp_s.t_ip, "tmp_port":tmp_s.t_port
                        })
                        print("t_socket Reconnect err")
                

    # 获取文件名
    def get_file_name(self, tmp_file):
        if self.sysstr == "Windows":
            begin_idx = tmp_file.rfind("\\") + 1
            end_idx = tmp_file.rfind(".")
            file_name = tmp_file[begin_idx:end_idx]
            return file_name
        else:
            begin_idx = tmp_file.rfind("/") + 1
            end_idx = tmp_file.rfind(".")
            file_name = tmp_file[begin_idx:end_idx]
            return file_name