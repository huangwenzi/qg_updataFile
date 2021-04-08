# qg_updataFile
实时同步指定目录下的文件到另一个目录

## 为什么做这个
做游戏，调跨服功能，每个服都是独立的代码。  
每次更新都要把其他服也更新，代码又没提交。
与其手动复制，不如让机器替我自动同步，解放双手。

## 使用
对本地指定目录做同步
main.py 

通知服务器热更文件
hotFileMain.py

异步目录同步    
upByNetClientMain.py        需要同步的客户端
upByNetSerMain.py           作为源文件的服务端