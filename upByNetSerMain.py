import time
import lib.svr_net_mgr as SvrNetMgr
import lib.file_mgr as fileMgrMd
import lib.file_lib as fileLibMd

# 刷新文件
# 源目录
src_path = "updateFile/old"
# 跳过检查的关键字
pass_str = ["/log"]
# 接收端地址
hot_addr = [["127.0.0.1", 12000]]
# 刷新间隔
time_interval = 5

# 同一路径斜杆
src_path = fileLibMd.change_path_of_sys(src_path)
pass_str = fileLibMd.change_path_of_sys(pass_str)

# 初始化文件管理器
file_mgr = fileMgrMd.FileMgr(src_path, pass_str)
# 初始化网络管理器
svr_net_mgr = SvrNetMgr.SvrNetMgr(hot_addr[0], hot_addr[1])


# 刷新文件并热更文件
while True:
    remove_list, add_list, update_list = file_mgr.update_file()
    # 删除文件
    for tmp_update_file in remove_list:
        svr_net_mgr.remove_file_to_client(tmp_update_file)
    # 添加文件
    for tmp_add_file in add_list:
        svr_net_mgr.send_file_to_client(tmp_add_file, src_path)
    # 修改文件
    for tmp_update_file in update_list:
        svr_net_mgr.send_file_to_client(tmp_update_file, src_path)
    time.sleep(time_interval)
    
    

    
        
