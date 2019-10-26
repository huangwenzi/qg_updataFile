import os
import time
import platform


# 文件处理
class FileMgr():
    # 源目录
    source_path = ""
    # 跳过检查的文件
    pass_file = []
    # 跳过检查的目录
    pass_dir = []
    # 跳过检查的关键字
    pass_str = []
    # 操作系统类型
    sysstr = ""
    
    # 初始化
    def __init__(self, source_path, pass_file, pass_dir, pass_str):
        self.source_path = source_path
        # 操作系统
        self.sysstr = platform.system()
        print("sysstr:" + self.sysstr)
        # 跳过的文件
        tmp_pass_file = []
        for tmp_file in pass_file:
            tmp_pass_file.append(self.unite_path(tmp_file))
        self.pass_file = tmp_pass_file
        # 跳过的目录
        tmp_pass_dir = []
        for tmp_dir in pass_dir:
            tmp_pass_dir.append(self.unite_path(tmp_dir))
        self.pass_dir = tmp_pass_dir
        self.pass_str = pass_str
        
    
    # 统一路径格式
    def unite_path(self, tmp_path):
        if self.sysstr == "Windows" :
            return tmp_path.replace('/', '\\')
        return tmp_path

    # 获取文件更新时间
    def get_file_update_time(self):
        file_time = {}
        for root, dirs, files in os.walk(self.source_path, topdown=False):
            for name in files:
                tmp_file_path = os.path.join(root, name)
                tmp_file_path = self.unite_path(tmp_file_path)
                # 是否需要跳过
                if tmp_file_path in self.pass_file:
                    continue
                # 跳过目录
                ispass = False
                for tmp_dir in self.pass_dir:
                    if tmp_dir in tmp_file_path:
                        ispass = True
                        break
                if ispass:
                    continue
                # 跳过关键字
                for tmp_str in self.pass_str:
                    if tmp_str in tmp_file_path:
                        ispass = True
                        break
                if ispass:
                    continue

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
    # file_time_list : 文件时间对比字典
    def get_remove_file(self, file_time_list):
        remove_file_list = []
        new_file_time = self.get_file_update_time()
        for tmp_file_path in file_time_list:
            if tmp_file_path not in new_file_time:
                remove_file_list.append(tmp_file_path)
        # 不能在迭代的字典里修改它
        for tmp_file_path in remove_file_list:
            del file_time_list[tmp_file_path]
        return remove_file_list

    # 同步文件到目录
    # source_path   ：  源文件目录
    # target_path   ：  目标文件目录
    # file_list     :   同步的文件列表
    def synchronize_file(self, source_path, target_path, file_list):
        # 第一步都是转文件格式
        source_path = self.unite_path(source_path)
        target_path = self.unite_path(target_path)
        
        # 循环修改文件
        for tmp_file in file_list:
            # 替换地址
            rep_file = tmp_file.replace(source_path, target_path)
            # 检查文件是否存在
            if not os.path.exists(tmp_file):
                print("file notExists, :%s"%(tmp_file))
                continue
            # 修改文件
            # with open(tmp_file, 'r', encoding='UTF-8') as f_in:             # 日记居然是gbk编码，坑爹，跳过就好了，日志不同步
            with open(tmp_file, 'rb') as f_in:             # 日记居然是gbk编码，坑爹，跳过就好了，日志不同步
                file_str = f_in.read()
                # 先判断目录是否存在，不存在就创建
                idx = rep_file.rfind("\\")
                tmp_str = rep_file[:idx]
                if not os.path.exists(tmp_str):
                    os.makedirs(tmp_str)
                # with open(rep_file, 'w+', encoding='UTF-8') as f_out:
                with open(rep_file, 'wb+') as f_out:
                    f_out.write(file_str)

    # 同步删除文件
    # source_path   ：  源文件目录
    # target_path   ：  目标文件目录
    # file_list     :   删除的文件列表
    def synchronize_remove_file(self, source_path, target_path, file_list):
        # 第一步都是转文件格式
        source_path = self.unite_path(source_path)
        target_path = self.unite_path(target_path)
        # 循环删除文件
        for tmp_file in file_list:
            # 替换地址
            rep_file = tmp_file.replace(source_path, target_path)
            # 先判断目录是否存在，存在就删除
            if os.path.exists(rep_file):
                os.remove(rep_file)