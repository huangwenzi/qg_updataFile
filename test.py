


tmp_file = "C:\\Users\\hw\\1.txt"


begin_idx = tmp_file.rfind("\\") + 1
end_idx = tmp_file.rfind(".")
file_name = tmp_file[begin_idx:end_idx]
send_str = "hot %s"%(file_name)
print(send_str)