import socket
import json
import threading
import select
import time

# 文件修改类型枚举
enum_update_file = 1    # 更新文件
enum_remove_file = 2    # 删除文件

# 发送指定数量字节
def send_data_len(c, send_len, data):
    # 使用send(),最大可发送的数据也是int类型最大上限的值,32位的系统,int类型最高好象是65535,64KB左右.
    one_len = 2048
    sen_idx = 0
    c.send(data)
    # while True:
    #     if send_len - sen_idx > one_len:
    #         c.send(data[sen_idx : sen_idx+one_len])
    #         sen_idx += one_len
    #     else:
    #         c.send(data[sen_idx : ])
    #         sen_idx += len(data[sen_idx : ])
    #         print("send_len:" + str(sen_idx))
    #         break
        

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
        # with open(src_path + file_path, 'r', encoding='UTF-8', errors='ignore') as f_in:
        #     file_str = f_in.read()
        # send_obj = {"file_path":file_path, "file_str":file_str, "type": enum_update_file}
        # send_str = json.dumps(send_obj)
        # 二进制的格式打开文件
        with open(src_path + file_path, 'rb') as f_in:
            file_str = f_in.read()
            # file_str = file_str.encode('utf-8', errors='ignore')
        file_str_len = len(file_str)
        send_obj = {"file_path":file_path, "type": enum_update_file, "len": file_str_len}
        send_str = json.dumps(send_obj)

        # 发送文件
        for tmp_client in list(self.client_list):
            try:
                # 接收数据提示
                begin_int = 1
                send_byte = begin_int.to_bytes(4,byteorder='big', signed=False)
                tmp_client.send(send_byte)
                # 发送文件名和类型还有大小
                # 下面这句不能少，不指定编码会失败
                send_str = send_str.encode('utf-8', errors='ignore')
                send_str_len = len(send_str)
                send_byte = send_str_len.to_bytes(4,byteorder='big', signed=False)
                tmp_client.send(send_byte)
                tmp_client.send(send_str)
                # 发送文件内容
                # print(file_str)
                print(send_obj)
                send_data_len(tmp_client, file_str_len, file_str)
                # tmp_client.send(file_str)
                # time.sleep(0.1)
                
                
                # tmp_client.send(send_str.encode('utf-8', errors='ignore'))
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
            
