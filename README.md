
    已经将本开源项目包打包上传至PYPI，目前版本0.0.8.4版本，用户可以直接通过命令pip进行下载，pip install crawltwj，即可安装本包进行使用爬取，同时正在增加qt图形界面程序，可视化爬取操作，已更新到0.0.2版本，但目前bug还很多，建议用户继续使用终端操作方法。
    
音乐爬取程序输入：

                from crawl import music
                
                food.get_music_data()

电影爬取程序输入：

                from crawl import movie
                
                movie.get_movie_data()
食品爬取程序输入：

                from crawl import food
                
                food.get_food_data()

评论爬取程序输入：
                
                from crawl import remark
                
                remark.music.get_hot_topics()

热搜爬取程序输入：

                from crawl import news
                
                news.main()

购物爬取程序输入：

                from crawl import shop
                
                shop.main()


1、
music代码，可以实现从网易云音乐根据用户输入的歌曲名称或者歌手名字爬取相关音乐的详细信息，包括歌名，歌手名，专辑，评论等，存储到music_data文件夹中，并且以文本文件的形式提供给用户进行使用或者处理。

![music](https://github.com/user-attachments/assets/12319d68-1c6b-4cce-97c6-cce87232c44f)

![image](https://github.com/user-attachments/assets/51f1832b-5086-4bb4-afb3-93561c7fe9d8)

2、
movie代码，可以实现从豆瓣电影根据用户输入的电影分类类型爬取该网站此电影分类的前20部电影的详细信息，包括电影的名称，上映时间，导演，豆瓣评分，演员，简介等，存储到movie_data文件夹中，以文本形式提供给用户进行使用或处理。

![image](https://github.com/user-attachments/assets/69a1f6fc-febb-432b-b3c9-73391e67e04c)

![image](https://github.com/user-attachments/assets/37c66b3a-1b7d-42fb-bfed-f41dec62021c)

3、food代码，实现按照用户需求从指定城市爬取肯德基餐厅的详细信息，包括位置，营业方式等，并以json文件方式存储，便于用户进行进一步处理。

![image](https://github.com/user-attachments/assets/fa7e5431-5b53-4f27-90f8-2a9a7e7b2e17)

![image](https://github.com/user-attachments/assets/4261c721-cfd3-4364-97b6-22e6db56b067)

4、评论爬取正在编写

5、爬取新浪网热搜的爬取程序。

![{189D8CCE-259F-4D3C-8A6B-D15660D37B48}](https://github.com/user-attachments/assets/682687a7-7f9d-48e1-81d1-702543ace4da)

6、新增购物商场爬取程序

![image](https://github.com/user-attachments/assets/def3eac4-3ab4-4a69-9bab-fd18858f5ed6)

![image](https://github.com/user-attachments/assets/49437d25-6d72-429c-951e-50ac01efdc33)

![image](https://github.com/user-attachments/assets/cee13bfc-7c5a-4298-a586-4a5c410ff6ff)

![image](https://github.com/user-attachments/assets/cfff9482-d029-4bd0-b4ad-2482058177eb)





