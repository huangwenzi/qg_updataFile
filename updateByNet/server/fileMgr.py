import os
import time

# # 文件类
# class FileObj():
#     file_name = ""
#     dir_name = ""
#     file_path = ""
#     mtime = 0
    
#     def __init__(self, file_name, dir_name, file_path):
#         self.file_name = file_name
#         self.dir_name = dir_name
#         self.file_path = file_path
#         self.mtime = os.stat(self.file_path).st_mtime

# 文件处理
class FileMgr():
    # 源目录
    target_path = ""
    # 刷新间隔
    time_interval = 0
    
    # 初始化
    def __init__(self, target_path, interval = 5):
        self.target_path = target_path
        self.time_interval = interval
    
    # 统一路径格式
    def unite_path(self, tmp_path):
        return tmp_path.replace('/', '\\')

    # 获取文件更新时间
    def get_file_update_time(self):
        file_time = {}
        for root, dirs, files in os.walk(self.target_path, topdown=False):
            for name in files:
                tmp_file_path = os.path.join(root, name)
                tmp_file_path = self.unite_path(tmp_file_path)
                if os.path.exists(tmp_file_path):
                    file_time[tmp_file_path] = os.stat(tmp_file_path).st_mtime
        return file_time

    # 查找新加或修改的文件
    # file_time_list : 文件时间对比字典
    def get_add_or_revise_file(self, file_time_list):
        revise_file_list = []
        new_file_time = self.get_file_update_time()
        for tmp_file_path in new_file_time:
            # 是否是新添加的文件
            if tmp_file_path not in file_time_list:
                revise_file_list.append(tmp_file_path)
                file_time_list[tmp_file_path] = new_file_time[tmp_file_path]
            # 是否有更新
            elif file_time_list[tmp_file_path] != new_file_time[tmp_file_path]:
                revise_file_list.append(tmp_file_path)
                file_time_list[tmp_file_path] = new_file_time[tmp_file_path]
        return revise_file_list

    # 查找删除的文件
    def get_remove_file(self, file_time_list):
        remove_file_list = []
        change_file = []
        new_file_time = self.get_file_update_time()
        for tmp_file_path in file_time_list:
            if tmp_file_path not in new_file_time:
                remove_file_list.append(tmp_file_path)
                change_file.append(tmp_file_path)
        # 不能在迭代的字典里修改它
        for tmp_file_path in change_file:
            del file_time_list[tmp_file_path]
        return remove_file_list


    
        
