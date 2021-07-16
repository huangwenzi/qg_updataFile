#!\\usr\\bin\\python3

import socket
import os
import json
import lib.file_lib as fileLibMd
import lib.svr_net_mgr as SvrNetMgr
import select
import time

# 监听目录
tar_path = "D:/game/mab"

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "192.168.31.239"
port = 12000
s.connect((host, port))
s.setblocking(False)

# 等待输入
def wait_recv(s):
    infds = []
    while True:
        infds,outfds,errfds = select.select([s,],[],[],5)
        if len(infds) >0:
            return infds
        else:
            continue
    
# 接受指定数量字节
def get_recv_len(s, recv_len):
    # 使用send(),最大可发送的数据也是int类型最大上限的值,32位的系统,int类型最高好象是65535,64KB左右.
    one_len = 2048
    get_len = 0
    msg = b''
    
    while True:
        wait_recv(s)
        if recv_len - get_len > one_len:
            get_len += one_len
            msg += s.recv(one_len)
        else:
            msg += s.recv(recv_len - get_len)
            get_len += (recv_len - get_len)
            return msg
       
# 接受指定数量字节到文件
def get_recv_len_to_file(s, recv_len, f_out):
    # 使用send(),最大可发送的数据也是int类型最大上限的值,32位的系统,int类型最高好象是65535,64KB左右.
    one_len = 20480
    get_len = 0
    msg = b''
    
    while True:
        wait_recv(s)
        if recv_len - get_len > one_len:
            msg = s.recv(one_len)
            # 上面不一定能获取one_len的长度
            get_len += len(msg)
            f_out.write(msg)
        else:
            recv_len_1 = recv_len - get_len
            msg = s.recv(recv_len_1)
            # 上面不一定能获取one_len的长度
            msg_len = len(msg)
            get_len += msg_len
            f_out.write(msg)
            if msg_len == recv_len_1:
                return msg
            else:
                pass
        
        
    

while True:
    recv_str = ""
    # 接受全部文件
    while True:
        msg = None
        try:
            # msg = s.recv(1024)
            # msg = msg.decode('utf-8')
            # if msg and len(msg) > 0:
            #     recv_str += msg
            # else :
            #     break
            
            infds = wait_recv(s)
            # 先接受包大小
            msg = s.recv(4)
            if len(msg)==0:
                continue
            
            send_byte = int.from_bytes(msg, byteorder='big')
            print("send_byte:" + str(send_byte))
            if send_byte == 1:
                # 接受文件信息大小
                wait_recv(s)
                send_str_len = s.recv(4)
                send_str_len = int.from_bytes(send_str_len, byteorder='big')
                # 接受文件信息
                wait_recv(s)
                msg = s.recv(send_str_len)
                msg = msg.decode('utf-8')
                print(recv_obj)
                recv_obj = json.loads(msg)
                # 接受文件数据
                wait_recv(s)
                
                # msg = s.recv(recv_obj["len"])
                # msg = get_recv_len(s, recv_obj["len"])
                file_path = recv_obj["file_path"]
                # path = os.path.join(tar_path, file_path)
                path = tar_path + file_path
                if recv_obj["type"] == SvrNetMgr.enum_remove_file:
                    os.remove(path)
                elif recv_obj["type"] == SvrNetMgr.enum_update_file:
                    # 检查目录
                    dir_name = os.path.dirname(path)
                    if not os.path.exists(dir_name):
                        os.makedirs(dir_name)
                    with open(path, "wb") as f_out:
                        # msg = msg.decode('utf-8')
                        # f_out.write(msg)
                        # 这效率也太高了，打开文件边读边写
                        get_recv_len_to_file(s, recv_obj["len"], f_out)
            else:
                print("丢弃脏包")
                # 丢弃脏包
                while True:
                    wait_recv(s)
                    msg = s.recv(1024)
                    if len(msg) == 0:
                        break
            # 发送文件名和类型还有大小
            
            # 发送文件内容
        except Exception as err:
            print(err)
            print("err")
            # # 丢弃脏包
            # s.recv()
            break
        
    # if len(recv_str) > 0:
    #     recv_obj = json.loads(recv_str)
    #     file_path = recv_obj["file_path"]
    #     path = os.path.join(tar_path, file_path)
    #     path = fileLibMd.change_path_of_sys(path)
    #     print("path:" + path)
    #     print("type:" + recv_obj["type"])
    #     if recv_obj["type"] == SvrNetMgr.enum_remove_file:
    #         os.remove(path)
    #     elif recv_obj["type"] == SvrNetMgr.enum_update_file:
    #         # 检查目录
    #         dir_name = os.path.dirname(path)
    #         if not os.path.exists(dir_name):
    #             os.makedirs(dir_name)
    #         with open(path, "w", encoding='UTF-8') as f_out:
    #             f_out.write(recv_obj["file_str"])

