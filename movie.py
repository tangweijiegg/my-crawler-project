import requests
from bs4 import BeautifulSoup
import time
import os
import random


class DoubanMovieCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 创建存储文件夹
        self.base_folder = 'movie_data'
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)

    def get_movie_list(self, movie_type):
        # 豆瓣电影分类URL
        url = f'https://movie.douban.com/j/search_subjects?type=movie&tag={movie_type}&sort=recommend&page_limit=20&page_start=0'

        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()['subjects']
            return []
        except Exception as e:
            print(f"获取电影列表时出错: {e}")
            return []

    def get_movie_detail(self, movie_url):
        try:
            response = requests.get(movie_url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 获取电影详细信息
                title = soup.find('h1').find('span', property='v:itemreviewed').text.strip()
                year = soup.find('span', class_='year').text.strip('()')
                director = soup.find('a', rel='v:directedBy').text if soup.find('a', rel='v:directedBy') else '未知'
                rating = soup.find('strong', property='v:average').text if soup.find('strong',
                                                                                     property='v:average') else '暂无评分'

                # 获取演员信息
                actors = soup.find_all('a', rel='v:starring')
                actors = [actor.text for actor in actors[:3]]  # 只取前三个演员

                # 获取剧情简介
                summary = soup.find('span', property='v:summary')
                if summary:
                    summary = summary.text.strip()
                else:
                    summary = '暂无简介'

                return {
                    'title': title,
                    'year': year,
                    'director': director,
                    'rating': rating,
                    'actors': ', '.join(actors),
                    'summary': summary
                }
            return None
        except Exception as e:
            print(f"获取电影详情时出错: {e}")
            return None

    def save_movie_info(self, movie_info, movie_type):
        if movie_info:
            # 创建类型文件夹
            type_folder = os.path.join(self.base_folder, movie_type)
            if not os.path.exists(type_folder):
                os.makedirs(type_folder)

            # 创建文件名（使用电影名称和年份）
            filename = f"{movie_info['title']}_{movie_info['year']}.txt"
            file_path = os.path.join(type_folder, filename)

            # 写入信息
            with open(file_path, 'w', encoding='utf-8') as f:
                width=20
                f.write(f"电影名称：{movie_info['title']}\n")
                f.write(f"上映年份：{movie_info['year']}\n")
                f.write(f"导演：{movie_info['director']}\n")
                f.write(f"豆瓣评分：{movie_info['rating']}\n")
                f.write(f"主要演员：{movie_info['actors']}\n")
                f.write(f"\n剧情简介：\n{movie_info['summary']}\n")

    def crawl_movies(self, movie_type):
        print(f"开始爬取{movie_type}类型的电影...")
        movies = self.get_movie_list(movie_type)

        for movie in movies:
            print(f"正在爬取电影：{movie['title']}")
            movie_detail = self.get_movie_detail(movie['url'])
            if movie_detail:
                self.save_movie_info(movie_detail, movie_type)
                # 添加随机延时，避免被封IP
                time.sleep(random.uniform(1, 3))

        print(f"爬取完成！电影信息已保存到 {self.base_folder}/{movie_type} 文件夹中")


def main():
    crawler = DoubanMovieCrawler()
    movie_type = input("请输入要爬取的电影类型（如：剧情、喜剧、动作等）：")
    crawler.crawl_movies(movie_type)


if __name__ == "__main__":
    main()