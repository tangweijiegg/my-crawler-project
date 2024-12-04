
import movie
import music
import remark
from movie import main
from music import  main
from remark import  get_hot_topics

while True:
    name=str(input("请输入想要爬取的数据类型(输入“结束”则终止程序)："))
    if name=="音乐":
        music.main()
    elif name=="电影":
        movie.main()
    elif name=='评论':
        remark.get_hot_topics()
    elif name=="结束":
        break
    else:
        print("错误输入，请输入正确的爬取数据类型：")
        continue

