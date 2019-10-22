# 导入 socket、sys 模块
import socket
import sys
import os
import json


# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "127.0.0.1"
port = 5002
s.connect((host, port))
s.setblocking(False)

s.send(b"e w0 print(1)\r\n")