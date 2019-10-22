import os
import time

from hotFile.fileMgr import FileMgr
from hotFile.netMgr import NetMgr
from hotFile.config import globalCfg as G_cfg


# 刷新文件并热更文件

# 文件管理器
fileMgr = FileMgr(G_cfg["source_path"], G_cfg["pass_file"], G_cfg["pass_dir"])
# 网络管理器
netMgr = NetMgr(G_cfg["hot_ip"], G_cfg["hot_port"])
# 每个文件更新的时间保存
file_update_time = fileMgr.get_file_update_time()
# 上次更新的时间
last_time = 0
# 更新间隔
time_interval = G_cfg["time_interval"]


while True:
    # 是否到时间刷新
    now = time.time()
    if now < last_time + time_interval:
        time.sleep(last_time + time_interval - now + 0.1)
        continue
    last_time = time.time()

    # 记录耗时
    begin_time = time.time()
    # 修改过的文件列表
    revise_file_list = []
    # 删除的文件列表
    remove_file_list = []

    # # 获取更新时间
    # new_time = fileMgr.get_file_update_time()
    
    # 获取修改的文件时间，包含更新file_update_time
    revise_file_list = fileMgr.get_add_or_revise_file(file_update_time)
    remove_file_list = fileMgr.get_remove_file(file_update_time)

    # end_time = time.time()
    # print("get_add_or_revise_file consume:%f"%(end_time - begin_time))
    # # 打印修改的文件
    print("revise_file_list:")
    print(revise_file_list)
    print("remove_file_list:")
    print(remove_file_list)

    
    # 记录耗时
    # begin_time = time.time()
    for tmp_path in G_cfg["target_path"]:
        # 进行替换
        fileMgr.synchronize_file(G_cfg["source_path"], tmp_path, revise_file_list)
        # 进行删除
        fileMgr.synchronize_remove_file(G_cfg["source_path"], tmp_path, remove_file_list)
    # end_time = time.time()
    # print("synchronize_file consume:%f"%(end_time - begin_time))

    # 发送热更
    netMgr.send_hot_file(revise_file_list)
    end_time = time.time()
    print("consume:%f"%(end_time - begin_time))
