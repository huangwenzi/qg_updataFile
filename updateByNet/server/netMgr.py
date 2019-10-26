import socket
import sys
import json
import threading
import select
import time

# 文件类型
revise_file = 1
remove_file = 2

# 监听socket
def listen_client(client_list, ser_socket):
    inputs = [ser_socket,]
    outputs = []
    while True:
        time.sleep(1)
        rlist,wlist,eList = select.select(inputs,outputs,[],0.5)
        #print("inputs:",inputs) #查看inputs列表变化
        print("rlist:",rlist) #查看rlist列表变化
        print("wlist:",wlist) #查看rlist列表变化
        print("eList:",eList) #查看rlist列表变化
        for r in rlist:
            if r == ser_socket: #如果r是服务端
                conn,address = r.accept()#
                inputs.append(conn) #把连接的句柄加入inputs列表监听
                client_list.append(conn)
                print (address)
            else:
                client_data = None
                try:
                    client_data = r.recv(1024)
                except :
                    inputs.remove(r)    #否则移除
                    idx = 0
                    for item in client_list:
                        if item == r:
                            del client_list[idx]
                            break
                        idx += 1
                    

class NetMgr():
    # 服务器socket
    ser_socket = None
    # 连接进来的客户端
    client_list = []

    # 初始化
    def __init__(self):
        # 初始化监听的socket
        self.serversocket = socket.socket() 
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(("192.168.88.180", 12000))
        self.serversocket.listen(5)

        # 分线程去监听接入的客户端
        t1 = threading.Thread(target=listen_client, args=(self.client_list, self.serversocket))
        t1.start()

    # 给客户端发送文件
    # file_path : 文件地址
    # old_path ： 检查的地址
    def send_file_to_client(self, file_path, old_path):
        # 先把文件读取到内存
        file_str = ""
        with open(file_path, 'r', encoding='UTF-8', errors='ignore') as f_in:
            file_str = f_in.read()
        file_path = file_path[len(old_path):]
        send_obj = {"file_path":file_path, "file_str":file_str, "type": revise_file}
        send_str = json.dumps(send_obj)
        print("send_str" + send_str)

        # 发送文件
        num = 0
        for tmp_client in list(self.client_list):
            print("num:%d"% (num))
            num += 1
            try:
                tmp_client.send(send_str.encode('utf-8', errors='ignore'))
            except :
                idx = 0
                for item in self.client_list:
                    if item == tmp_client:
                        del self.client_list[idx]
                        break
                    idx += 1
            
