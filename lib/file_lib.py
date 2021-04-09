import os
import platform
sysstr = platform.system()

# 文件操作

# 文件类
class FileObj():
    file_name = ""  # 文件名
    file_key = ""   # 文件key 去掉前面目录
    file_path = ""  # 文件地址
    mtime = 0       # 文件更新时间
    
    def __init__(self, file_name, file_key, file_path):
        self.file_name = file_name
        self.file_key = file_key
        self.file_path = change_path_of_sys(file_path)
        self.mtime = os.stat(self.file_path).st_mtime
        
## 检查函数
# 文件是否相同  检查修改时间和文件大小
def check_file_identical(file_path_1, file_path_2):
    # 修改时间
    if os.stat(file_path_1).st_mtime != os.stat(file_path_2).st_mtime:
        return False
    # 文件大小
    if os.path.getsize(file_path_1) != os.path.getsize(file_path_2):
        return False
    return True
        
## 修改函数  
# 根据系统转换斜杆
def change_path_of_sys(path):
    if sysstr == "Windows":
        return path.replace('/', '\\')
    else:
        return path.replace('\\', '/')

# 拷贝文件
def copy_file(file_obj, update_file_path):
    # 不存在目录就创建
    update_file_dir = update_file_path[:-len(file_obj.file_name)]
    if not os.path.exists(update_file_dir):
        os.makedirs(update_file_dir)
    os_str = ("copy %s %s" % (file_obj.file_path, update_file_path))
    os.system(os_str)
    # 修改时间
    os.utime(update_file_path,(file_obj.mtime, file_obj.mtime))
    
