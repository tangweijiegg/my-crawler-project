import requests
import json
import os
from datetime import datetime


class NeteaseMusicCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.search_url = 'http://music.163.com/api/search/get'
        self.song_url = 'http://music.163.com/api/song/detail/'
        self.comments_url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}'

    def search_music(self, keyword):
        params = {
            's': keyword,
            'type': 1,  # 1: 单曲, 10: 专辑, 100: 歌手, 1000: 歌单
            'offset': 0,
            'limit': 5
        }
        try:
            response = requests.get(self.search_url, params=params, headers=self.headers)
            result = response.json()
            return result['result']['songs']
        except Exception as e:
            print(f"搜索出错: {str(e)}")
            return []

    def get_song_details(self, song_id):
        params = {
            'id': song_id,
            'ids': f'[{song_id}]'
        }
        try:
            response = requests.get(self.song_url, params=params, headers=self.headers)
            result = response.json()
            return result['songs'][0]
        except Exception as e:
            print(f"获取歌曲详情出错: {str(e)}")
            return None

    def get_comments(self, song_id, limit=20):
        url = self.comments_url.format(song_id)
        params = {
            'limit': limit,
            'offset': 0
        }
        try:
            response = requests.get(url, params=params, headers=self.headers)
            result = response.json()
            return result['hotComments']
        except Exception as e:
            print(f"获取评论出错: {str(e)}")
            return []

    def save_to_file(self, song_info, comments, output_dir='music_data'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename = f"{song_info['name']}_{song_info['artists'][0]['name']}.txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            # 写入歌曲基本信息
            f.write(f"歌曲名称：{song_info['name']}\n")
            f.write(f"演唱者：{song_info['artists'][0]['name']}\n")
            f.write(f"所属专辑：{song_info['album']['name']}\n\n")

            # 写入热门评论
            f.write("热门评论：\n")
            f.write("-" * 50 + "\n")
            for comment in comments:
                f.write(f"用户：{comment['user']['nickname']}\n")
                f.write(f"评论：{comment['content']}\n")
                f.write(f"时间：{datetime.fromtimestamp(comment['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"点赞数：{comment['likedCount']}\n")
                f.write("-" * 50 + "\n")


def main():
    crawler = NeteaseMusicCrawler()

    # 获取用户输入
    keyword = input("请输入要搜索的歌曲名或歌手名：")

    # 搜索音乐
    print("正在搜索...")
    songs = crawler.search_music(keyword)

    if not songs:
        print("未找到相关音乐")
        return

    # 显示搜索结果
    print("\n搜索结果：")
    for i, song in enumerate(songs):
        print(f"{i + 1}. {song['name']} - {song['artists'][0]['name']}")

    # 用户选择
    choice = int(input("\n请选择要下载的音乐序号（1-5）：")) - 1
    if choice < 0 or choice >= len(songs):
        print("无效的选择")
        return

    selected_song = songs[choice]

    # 获取详细信息和评论
    print("正在获取歌曲信息和评论...")
    song_details = crawler.get_song_details(selected_song['id'])
    comments = crawler.get_comments(selected_song['id'])

    # 保存信息
    if song_details and comments:
        crawler.save_to_file(song_details, comments)
        print(f"信息已保存到 music_data 文件夹中")
    else:
        print("获取信息失败")


if __name__ == "__main__":
    main()
