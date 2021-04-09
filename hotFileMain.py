import os
import time
import platform
import lib.file_mgr as fileMgrMd
import lib.file_lib as fileLibMd
import lib.net_mgr as netMgrMd

# 刷新文件
# 源目录
src_path = "updateFile/old"
# 刷新目录
update_path = ["updateFile/new"]
# 跳过检查的关键字
pass_str = ["/log"]
# 接收端地址
hot_addr = [["127.0.0.1", 5000]]
# 刷新间隔
time_interval = 5

# 同一路径斜杆
src_path = fileLibMd.change_path_of_sys(src_path)
update_path_1 = []
for tmp in update_path:
    update_path_1.append(fileLibMd.change_path_of_sys(tmp))
update_path = update_path_1

# 初始化文件管理器
file_mgr = fileMgrMd.FileMgr(src_path, pass_str)
# 初始化网络管理器
net_mgr = netMgrMd.NetMgr(src_path, pass_str)
# 添加目标地址
for tmp_addr in hot_addr:
    net_mgr.add_socket(tmp_addr[0], tmp_addr[1])
    

# 刷新文件并热更文件
while True:
    remove_list, add_list, update_list = file_mgr.update_file()
    # 热更只针对更新的文件
    for tmp_update_file in update_list:
        tmp_update_file_name = fileLibMd.get_file_name(tmp_update_file)
        net_mgr.send_all_socket("hot " + tmp_update_file_name)


