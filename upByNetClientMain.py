#!\\usr\\bin\\python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import sys
import os
import json

# 监听目录
tar_path = "/usr/file/server/l-src"


# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "192.168.88.180"
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
        print(recv_str)
        recv_obj = json.loads(recv_str)

        # send_obj = {"file_path":file_path, "file_str":file_str, "type": revise_file}
        file_path = recv_obj["file_path"]
        if file_path[0:1] == "\\":
            file_path = file_path[1:]
        path = os.path.join(tar_path, file_path)
        path = path.replace('\\', '/')
        file_str = recv_obj["file_str"]
        print("path:" + path)
        with open(path, "w", encoding='UTF-8') as f_out:
            f_out.write(file_str)

    

s.close()
