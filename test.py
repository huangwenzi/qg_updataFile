
import os
# tmp_str = 'copy updateFile\\old\\1.txt updateFile/new\\1.txt /Y'
tmp_str = 'type nul> newtest.txt'
a = os.system(tmp_str)
tmp_str = 'copy newtest.txt updateFile\\1.txt'
a = os.system(tmp_str)
# os_str = "copy  './1.txt'  '2.txt' "
# os.system(os_str)