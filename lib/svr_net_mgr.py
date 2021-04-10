import socket
import json
import threading
import select
import time

# 文件修改类型枚举
enum_update_file = 1    # 更新文件
enum_remove_file = 2    # 删除文件

# 监听socket
def listen_client(client_list, ser_socket):
    inputs = [ser_socket,]
    outputs = []
    while True:
        time.sleep(1)
        rlist,wlist,eList = select.select(inputs,outputs,[],0.5)
        # print("inputs:",inputs) # 查看inputs列表变化
        # print("rlist:",rlist) # 查看rlist列表变化
        # print("wlist:",wlist) # 查看rlist列表变化
        # print("eList:",eList) # 查看rlist列表变化
        for r in rlist:
            if r == ser_socket: # 如果r是服务端
                conn,address = r.accept()
                inputs.append(conn) # 把连接的句柄加入inputs列表监听
                client_list.append(conn)
                print (address)
            else:
                # 尝试读取数据
                client_data = None
                try:
                    client_data = r.recv(1024)
                    # 下面可以添加处理
                    
                except :
                    inputs.remove(r)
                    client_list.remove(r)
                    

class SvrNetMgr():
    # 服务器socket
    ser_socket = None
    # 连接进来的客户端
    client_list = []

    # 初始化
    def __init__(self, ip, port):
        # 初始化监听的socket
        self.serversocket = socket.socket() 
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((ip, port))
        self.serversocket.listen(5)

        # 分线程去监听接入的客户端
        t1 = threading.Thread(target=listen_client, args=(self.client_list, self.serversocket))
        t1.start()

    # 给客户端发送文件
    def send_file_to_client(self, file_path, src_path):
        # 先把文件读取到内存
        file_str = ""
        with open(src_path + file_path, 'r', encoding='UTF-8', errors='ignore') as f_in:
            file_str = f_in.read()
        send_obj = {"file_path":file_path, "file_str":file_str, "type": enum_update_file}
        send_str = json.dumps(send_obj)

        # 发送文件
        for tmp_client in list(self.client_list):
            try:
                tmp_client.send(send_str.encode('utf-8', errors='ignore'))
            except :
                self.client_list.remove(tmp_client)
                
    # 客户端删除文件
    def remove_file_to_client(self, file_path):
        send_obj = {"file_path":file_path, "file_str":"", "type": enum_remove_file}
        send_str = json.dumps(send_obj)

        # 发送文件
        for tmp_client in list(self.client_list):
            try:
                tmp_client.send(send_str.encode('utf-8', errors='ignore'))
            except :
                self.client_list.remove(tmp_client)
            
