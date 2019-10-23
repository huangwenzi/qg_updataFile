# 配置文件

# globalCfg = {
#     # 源目录
#     "source_path" : "E:/huangwen/code/server/l-src",
#     # 目标目录
#     "target_path" : [
#         "E:/huangwen/code/server_1/l-src",
#         "E:/huangwen/code/server_cp/l-src",
#     ],
#     # 跳过的文件
#     "pass_file" : [
#         "E:/huangwen/code/server/l-src/conf",
#     ],
#     # 检查间隔
#     "time_interval" : 5,
# }

globalCfg = {
    # 源目录
    "source_path" : "E:\\huangwen\\code\\server\\l-src",
    # 目标目录
    "target_path" : [
        "E:\\huangwen\\code\\server_1\\l-src",
        "E:\\huangwen\\code\\server_cp\\l-src",
    ],
    # 跳过的文件
    "pass_file" : [
        "E:\\huangwen\\code\\server\\l-src\\conf",
    ],
    # 跳过的目录
    "pass_dir" : [
        "E:\\huangwen\\code\\server\\l-src\\log",
    ],
    # 跳过的关键字
    "pass_str" : [
        ".svn",
    ],
    # 检查间隔
    "time_interval" : 5,
    # 需要热更的地址
    "hot_ip" : "127.0.0.1",
    "hot_port" : [5000, 5010, 7000],
}