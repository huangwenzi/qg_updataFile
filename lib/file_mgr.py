import os
import time
import platform
import lib.file_lib as fileLibMd

# 文件处理
class FileMgr():
    # 源目录
    source_path = ""
    # 跳过检查的关键字
    pass_str = []
    # 操作系统类型
    sysstr = ""
    # 文件数据
    file_map = {}
    
    # 初始化
    def __init__(self, source_path, pass_str):
        self.source_path = source_path
        # 操作系统
        self.sysstr = platform.system()
        self.pass_str = pass_str
        self.update_file()
        
    ## 获取函数
    # 获取文件key
    def get_file_key(self, file_path):
        path_begin_idx = len(self.source_path)
        return file_path[path_begin_idx:]
    
    
    
    ## 检查函数
    # 文件是否需要过滤
    def check_file_pass(self, file_path):
        # 是否在过滤目录
        for tmp_str in self.pass_str:
            if tmp_str in file_path:
                return True
        return False
    
    
        
    ## 修改函数
    # 更新文件数据
    def update_file(self):
        new_file_map = {}       # 新文件对象map
        remove_list = []        # 删除的文件列表
        add_list = []           # 新加的文件列表
        update_list = []        # 更新的文件列表
        ## 遍历目录文件
        for root, dirs, files in os.walk(self.source_path, topdown=False):
            for file_name in files:
                tmp_file_path = os.path.join(root, file_name)
                # 是否需要过滤
                if not self.check_file_pass(tmp_file_path):
                    ## 添加到新文件对象map
                    file_key = self.get_file_key(tmp_file_path)
                    new_file_obj = fileLibMd.FileObj(file_name, file_key, tmp_file_path)
                    new_file_map[file_key] = new_file_obj
                    ## 是否新加的文件
                    if file_key not in self.file_map:
                        add_list.append(file_key)
                    else:
                        ## 是否有变化
                        old_file_obj = self.file_map[file_key]
                        if old_file_obj.mtime != new_file_obj.mtime:
                            update_list.append(file_key)
        ## 遍历旧目录文件对象
        for old_file_key in self.file_map:
            # 是否文件被删除
            if old_file_key not in new_file_map:
                remove_list.append(old_file_key)
        self.file_map = new_file_map
        return remove_list, add_list, update_list
    
    # 删除目标目录文件
    def remove_file_list(self, file_list, tmp_path):
        # 删除文件
        for tmp_remove_path in file_list:
            tmp_remove_path = tmp_path + tmp_remove_path
            os.remove(tmp_remove_path)
    # 添加目标目录文件
    def add_file_list(self, file_list, tmp_path):
        # 添加文件
        for tmp_add_path in file_list:
            file_obj = self.file_map[tmp_add_path]
            tmp_add_path = tmp_path + tmp_add_path
            fileLibMd.copy_file(file_obj, tmp_add_path)
    # 更新目标目录文件
    def update_file_list(self, file_list, tmp_path):
        # 更新文件
        for tmp_update_path in file_list:
            file_obj = self.file_map[tmp_update_path]
            tmp_update_path = tmp_path + tmp_update_path
            fileLibMd.copy_file(file_obj, tmp_update_path)
        
        
        
        
        
        
        
        
        

    