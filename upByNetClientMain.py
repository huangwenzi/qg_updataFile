#!\\usr\\bin\\python3

import socket
import os
import json
import lib.file_lib as fileLibMd
import lib.svr_net_mgr as SvrNetMgr

# 监听目录
tar_path = "updateFile/new"


# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "127.0.0.1"
port = 12000
s.connect((host, port))
s.setblocking(False)

while True:
    recv_str = ""
    # 接受全部文件
    while True:
        msg = None
        try:
            msg = s.recv(1024)
            msg = msg.decode('utf-8')
            if msg and len(msg) > 0:
                recv_str += msg
            else :
                break
        except:
            break
        
    if len(recv_str) > 0:
        recv_obj = json.loads(recv_str)
        file_path = recv_obj["file_path"]
        path = os.path.join(tar_path, file_path)
        path = fileLibMd.change_path_of_sys(path)
        print("path:" + path)
        print("type:" + recv_obj["type"])
        if recv_obj["type"] == SvrNetMgr.enum_remove_file:
            os.remove(path)
        elif recv_obj["type"] == SvrNetMgr.enum_update_file:
            with open(path, "w", encoding='UTF-8') as f_out:
                f_out.write(recv_obj["file_str"])

