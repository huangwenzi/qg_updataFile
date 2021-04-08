
import os
import time
import lib.file_lib as fileMd


# 刷新文件
# 源目录
src_path = "updateFile/old"
# 刷新目录
update_path = ["updateFile/new"]
# 刷新间隔
time_interval = 5

# 同一路径斜杆
src_path = fileMd.change_path_of_sys(src_path)
update_path_1 = []
for tmp in update_path:
    update_path_1.append(fileMd.change_path_of_sys(tmp))
update_path = update_path_1




## 初始化源目录数据
path_begin_idx = len(src_path)
src_file_map = {}
for root, dirs, files in os.walk(src_path, topdown=False):
    for file_name in files:
        tmp_file_path = os.path.join(root, file_name)
        ## 获取key
        file_key = tmp_file_path[path_begin_idx:]
        src_file_map[file_key] = fileMd.FileObj(file_name, file_key, tmp_file_path)
            
while True:
    ## 更新和添加新的文件
    for root, dirs, files in os.walk(src_path, topdown=False):
        for file_name in files:
            tmp_file_path = os.path.join(root, file_name)
            ## 获取key
            file_key = tmp_file_path[path_begin_idx:]
            src_file_map[file_key] = fileMd.FileObj(file_name, file_key, tmp_file_path)
            
    # 需要删除的源文件对象
    need_remove_file = []
    # 遍历更新目录
    for son_file_path in update_path:
        # 遍历文件
        for file_key in src_file_map:
            file_obj = src_file_map[file_key]
            # 更新文件的地址
            update_file_path = file_obj.file_path.replace(src_path, son_file_path)
            # 源文件是否还存在
            if os.path.exists(file_obj.file_path) == False:
                need_remove_file.append(file_key)
                # 删除不应存在的文件
                if os.path.exists(update_file_path):
                    os.remove(update_file_path)
                continue
                
            # 更新文件是否存在
            if os.path.exists(update_file_path) == False:
                fileMd.copy_file(file_obj, update_file_path)
            else:
                # 对比时间
                update_file_time = os.stat(update_file_path).st_mtime
                if file_obj.mtime != update_file_time:
                    # 拷贝文件过去，并修改时间
                    fileMd.copy_file(file_obj, update_file_path)
        
    # 删除已经不存在的文件
    for file_key in need_remove_file:
        del src_file_map[file_key]
        
    ## 间隔
    time.sleep(time_interval)
