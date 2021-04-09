
import os
import time
import lib.file_lib as fileLibMd
import lib.file_mgr as fileMgrMd


# 刷新文件
# 源目录
src_path = "updateFile/old"
# 刷新目录
update_path = ["updateFile/new"]
# 跳过检查的关键字
pass_str = []
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

            
while True:
    remove_list, add_list, update_list = file_mgr.update_file()
    for tmp_path in update_path:
        # 删除文件
        file_mgr.remove_file_list(remove_list, tmp_path)
        # 添加文件
        file_mgr.add_file_list(add_list, tmp_path)
        # 更新文件
        file_mgr.update_file_list(update_list, tmp_path)
        
    ## 间隔
    time.sleep(time_interval)
