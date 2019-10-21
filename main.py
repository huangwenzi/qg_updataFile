
import os
import time


# 刷新文件
# 源目录
old_path = "updateFile/old"
# 刷新目录
new_path = "updateFile/new"
# 刷新间隔
time_interval = 1

# 文件类
class FileObj():
    file_name = ""
    dir_name = ""
    file_path = ""
    mtime = 0
    
    def __init__(self, file_name, dir_name, file_path):
        self.file_name = file_name
        self.dir_name = dir_name
        self.file_path = file_path
        self.mtime = os.stat(self.file_path).st_mtime

last_time = 0
while True:
    # 是否到时间刷新
    now = time.time()
    if now < last_time + time_interval:
        time.sleep(last_time + time_interval - now + 0.1)
    last_time = now

    # 获取源目录每个表更新的时间
    old_file_time = {}
    for root, dirs, files in os.walk(old_path, topdown=False):
        for name in files:
            tmp_file_path = os.path.join(root, name)
            old_file_time[tmp_file_path[len(old_path):]] = FileObj(name, root, tmp_file_path)

    # 获取刷新目录每个表更新的时间
    new_file_time = {}
    for root, dirs, files in os.walk(new_path, topdown=False):
        for name in files:
            tmp_file_path = os.path.join(root, name)
            new_file_time[tmp_file_path[len(new_path):]] = FileObj(name, root, tmp_file_path)

    for key in old_file_time:
        tmp_file = old_file_time[key]
        old_file_name = tmp_file.file_path
        new_file_name = old_file_name.replace(old_path, new_path)
        # 刷新目录文件是否存在
        # 文件不存在
        if key not in new_file_time:
            # 刷新目录文件，目录是否存在
            new_file_dir = new_file_name[:-len(tmp_file.file_name)]
            if not os.path.exists(new_file_dir):
                os.makedirs(new_file_dir)
            # 拷贝文件
            with open(new_file_name, 'w', encoding='utf-8', errors='ignore') as fin:
                pass
            os_str = ("copy %s %s" % (old_file_name, new_file_name))
            # 这里要装换，windows不能用'/', 要替换成'\\'
            os_str = os_str.replace('/', '\\')
            os.system(os_str)
            # 修改时间
            os.utime(new_file_name,(tmp_file.mtime, tmp_file.mtime))
        # 文件存在
        else:
            # 对比时间
            new_file = new_file_time[key]
            if tmp_file.mtime > new_file.mtime:
                os_str = ("copy %s %s" % (old_file_name, new_file_name))
                os_str = os_str.replace('/', '\\')
                os.system(os_str)
                # 修改时间
                os.utime(new_file_name,(tmp_file.mtime, tmp_file.mtime))

    
