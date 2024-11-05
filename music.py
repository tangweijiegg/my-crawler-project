import requests
import json
import os
from urllib.parse import quote


class NetEaseMusic:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.search_url = 'http://music.163.com/api/search/get/web'
        self.song_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'

    def search_song(self, keyword, limit=5):
        """搜索歌曲"""
        params = {
            's': keyword,
            'type': 1,  # 1: 单曲, 10: 专辑, 100: 歌手, 1000: 歌单
            'offset': 0,
            'limit': limit
        }

        try:
            response = requests.get(self.search_url, params=params, headers=self.headers)
            result = response.json()
            if result['code'] == 200:
                return result['result']['songs']
            return None
        except Exception as e:
            print(f"搜索出错: {e}")
            return None

    def download_song(self, song_id, song_name, save_path='music-downloads'):
        """下载歌曲"""
        # 创建下载目录
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 构建下载链接
        download_url = self.song_url.format(song_id)

        try:
            # 下载音乐文件
            response = requests.get(download_url, headers=self.headers)

            # 检查是否成功获取到音乐文件
            if response.status_code == 200 and len(response.content) > 0:
                # 构建保存路径
                file_path = os.path.join(save_path, f"{song_name}.mp3")

                # 保存文件
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"下载成功: {song_name}")
                return True
            else:
                print(f"下载失败: {song_name}")
                return False
        except Exception as e:
            print(f"下载出错: {e}")
            return False


def main():
    # 创建网易云音乐下载器实例
    netease = NetEaseMusic()

    # 获取用户输入
    keyword = input("请输入要搜索的歌曲名称: ")

    # 搜索歌曲
    songs = netease.search_song(keyword)

    if songs:
        print("\n搜索结果:")
        for i, song in enumerate(songs):
            print(f"{i + 1}. {song['name']} - {song['artists'][0]['name']}")

        # 获取用户选择
        choice = int(input("\n请选择要下载的歌曲序号(1-5): ")) - 1

        if 0 <= choice < len(songs):
            selected_song = songs[choice]
            # 下载选中的歌曲
            netease.download_song(
                selected_song['id'],
                f"{selected_song['name']} - {selected_song['artists'][0]['name']}"
            )
        else:
            print("无效的选择!")
    else:
        print("未找到相关歌曲!")


if __name__ == "__main__":
    main()
