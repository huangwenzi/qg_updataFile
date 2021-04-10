import socket            
import copy

# 套接字类
class SvrSocket():
    t_socket = None
    t_ip = None
    t_port = None

    def __init__(self, t_socket, t_ip, t_port):
        self.t_socket = t_socket
        self.t_ip = t_ip
        self.t_port = t_port
        

# 热更socket管理
class NetMgr():
    # 连接进来的端
    socket_map = []
    # 连接失败的端
    fail_map = []

    # 初始化
    def __init__(self):
        pass
    
    ## 获取函数
    # 获取socket key
    def get_socket_key(self, ip, port):
        return ip + ":" + str(port)
    
    ## 检查函数
    
    
    ## 修改函数
    # 添加新端
    def add_socket(self, ip, port):
        try:
            socket_key = self.get_socket_key(ip, port)
            # 是否已存在
            if socket_key not in self.socket_map:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                s.connect((ip, port))
                s.setblocking(False)
                tmp_socket = SvrSocket(s, ip, port)
                self.socket_map[socket_key] = tmp_socket
                # 如果存在失败端，删除
                if socket_key in self.fail_map:
                    del self.fail_map[socket_key]
                return True
        except :
            self.fail_map[socket_key] = {"ip":ip, "port":port}
            return False
            
    # 删除端
    def remove_socket(self, socket_key):
        socket_obj = self.socket_map[socket_key]
        socket_obj.t_socket.close()
        del self.socket_map[socket_key]
        # 也删除失败连接的
        if socket_key in self.fail_map:
            del self.fail_map[socket_key]
        
    # 重连失败端
    def reconnect_fail_list(self):
        # 先拷贝一份fail_map， add_socket会修改自身fail_map
        new_fail_map = copy.deepcopy(self.fail_map)
        for socket_key in new_fail_map:
            fail_info = new_fail_map[socket_key]
            self.add_socket(self, fail_info["ip"], fail_info["port"])
        
    # 给单个端发送消息
    def send_by_socket_key(self, socket_key, send_str):
        try:
            if socket_key in self.socket_map:
                self.socket_map[socket_key].t_socket.send(send_str.encode("utf8", errors='ignore'))
            else:
                print("send_by_socket_key err 没有正确连接")
        except :
            print("send_by_socket_key err 发送错误")
                
    # 广播发送信息
    def send_all_socket(self, send_str):
        for socket_key in self.socket_map:
            self.send_by_socket_key(socket_key, send_str)
    