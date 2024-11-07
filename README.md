# my-crawler-project
按照用户需求进行数据爬取，便于用户进行决策和选择
music.py 
NetEaseMusic 类是主要的功能类，
包含了：
初始化方法设置了请求头和 API URL
搜索歌曲的方法 search_song()
下载歌曲的方法 download_song()
主要功能：
搜索功能 (search_song):
通过网易云音乐的 API 搜索歌曲
默认返回歌曲的搜索结果
使用 requests 库发送 GET 请求到搜索 API
下载功能 (download_song):
根据歌曲 ID 构建下载链接
创建下载目录（默认为 'music-downloads'）
下载并保存 MP3 文件
主程序流程 (main 函数):
错误处理：
包含了异常处理机制
在搜索和下载过程中如果出现错误会打印相应提示
使用方式：
运行程序后，输入要搜索的歌曲名称
从显示的搜索结果中选择一首歌曲下载
歌曲将被下载到 'music-downloads' 目录中
这个程序使用了网易云音乐的公开 API，可能受到 API 限制或变更的影响。下载音乐时请注意版权问题。
![image](https://github.com/user-attachments/assets/bad7b8a5-6900-4a86-bb73-bcdeaa48911f) ![image](https://github.com/user-attachments/assets/62221a55-b9f1-4477-9365-16df5f4e9f42)

