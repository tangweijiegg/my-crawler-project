import requests
import json
from datetime import datetime
import time
import random


class WeiboHotSearchCrawler:
    def __init__(self):
        # 微博热搜API地址
        self.url = "https://weibo.com/ajax/side/hotSearch"

        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': ''  # 需要填入有效的Cookie
        }

    def get_random_user_agent(self):
        """随机生成User-Agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        return random.choice(user_agents)

    def fetch_hot_search(self):
        """获取热搜数据"""
        try:
            # 随机更换User-Agent
            self.headers['User-Agent'] = self.get_random_user_agent()

            # 添加随机延时
            time.sleep(random.uniform(1, 3))

            response = requests.get(self.url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"请求失败，状态码：{response.status_code}")
                return None

        except Exception as e:
            print(f"获取热搜失败: {str(e)}")
            return None

    def parse_hot_search(self, data):
        """解析热搜数据"""
        try:
            hot_searches = []

            if 'data' in data and 'realtime' in data['data']:
                for item in data['data']['realtime']:
                    hot_item = {
                        'rank': item.get('rank', ''),
                        'topic': item.get('note', ''),
                        'hot_score': item.get('raw_hot', 0),
                        'category': item.get('category', ''),
                        'url': f"https://s.weibo.com/weibo?q=%23{item.get('note', '')}%23",
                        'is_hot': item.get('is_hot', False),
                        'is_boom': item.get('is_boom', False),
                        'is_new': item.get('is_new', False)
                    }
                    hot_searches.append(hot_item)

            return hot_searches

        except Exception as e:
            print(f"解析数据失败: {str(e)}")
            return []

    def save_to_json(self, hot_searches):
        """保存热搜数据到JSON文件"""
        try:
            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'weibo_hot_search_{timestamp}.json'

            # 添加元数据
            data = {
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'weibo.com',
                'total_count': len(hot_searches),
                'hot_searches': hot_searches
            }

            # 将数据写入JSON文件
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"数据已保存到 {filename}")
            return True

        except Exception as e:
            print(f"保存JSON文件失败: {str(e)}")
            return False

    def crawl(self):
        """执行爬虫主流程"""
        print("开始爬取微博热搜榜...")

        # 获取热搜数据
        raw_data = self.fetch_hot_search()
        if not raw_data:
            return False

        # 解析数据
        hot_searches = self.parse_hot_search(raw_data)
        if not hot_searches:
            print("未找到热搜数据")
            return False

        # 打印爬取结果
        print(f"\n成功爬取 {len(hot_searches)} 条热搜:")
        for item in hot_searches:
            print(f"\n{item['rank']}. {item['topic']}")
            print(f"热度: {item['hot_score']}")
            print(f"分类: {item['category']}")
            if item['is_hot']:
                print("🔥 热门")
            if item['is_boom']:
                print("💥 爆")
            if item['is_new']:
                print("🆕 新")

        # 保存到JSON文件
        return self.save_to_json(hot_searches)


def main():
    # 创建爬虫实例
    crawler = WeiboHotSearchCrawler()

    try:
        # 执行爬虫
        success = crawler.crawl()

        if success:
            print("\n爬取完成!")
        else:
            print("\n爬取失败!")

    except KeyboardInterrupt:
        print("\n用户中断爬取")
    except Exception as e:
        print(f"\n发生错误: {str(e)}")


if __name__ == "__main__":
    main()