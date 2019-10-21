import os
import time

from updateByNet.server.fileMgr import FileMgr
from updateByNet.server.netMgr import NetMgr

# 刷新文件
# 源目录
old_path = "E:/huangwen/code/server/l-src"
# 刷新间隔
time_interval = 5


fileMgr = FileMgr(old_path)
netMgr = NetMgr()
# 下次更新的时间
last_time = 0
# 每个文件更新的时间保存
file_update_time = fileMgr.get_file_update_time()

while True:
    # 是否到时间刷新
    now = time.time()
    if now < last_time + time_interval:
        time.sleep(last_time + time_interval - now + 0.1)
    last_time = time.time()

    # 记录耗时
    begin_time = time.time()

    # 修改过的文件列表
    revise_file_list = []
    # 删除的文件列表
    remove_file_list = []

    # 检查更新时间
    new_time = fileMgr.get_file_update_time()
    
    # 获取修改的文件时间，包含更新file_update_time
    revise_file_list = fileMgr.get_add_or_revise_file(file_update_time)
    remove_file_list = fileMgr.get_remove_file(file_update_time)

    # 记录耗时
    end_time = time.time()
    print("consume:%f"%(end_time - begin_time))
    # # 打印修改的文件
    # print("revise_file_list:")
    # print(revise_file_list)
    # print("remove_file_list:")
    # print(remove_file_list)

    # 发送修改
    if len(revise_file_list) > 0:
        print(1)
        for tmp_file in revise_file_list:
            netMgr.send_file_to_client(tmp_file, old_path)
    

    
        
