import requests
import pandas as pd
import json
import time
from datetime import datetime
import os


class MallScraper:
    def __init__(self):
        # 高德地图API密钥
        self.api_key = "00e78d0e751e7e9074fbe362701a3553"
        self.base_url = "https://restapi.amap.com/v3/place/text"

    def search_malls(self, city, page=1, page_size=20):
        """
        搜索指定城市的商场信息
        """
        params = {
            'key': self.api_key,
            'keywords': '购物中心|商场',
            'city': city,
            'citylimit': 'true',
            'offset': page_size,
            'page': page,
            'extensions': 'all'
        }

        try:
            response = requests.get(self.base_url, params=params)
            return response.json()
        except Exception as e:
            print(f"请求出错: {str(e)}")
            return None

    def get_all_malls(self, city):
        """
        获取城市所有商场信息
        """
        all_malls = []
        page = 1
        total_pages = 1

        print(f"开始获取{city}的商场信息...")

        while page <= total_pages:
            result = self.search_malls(city, page)

            if not result or result.get('status') != '1':
                print(f"获取第{page}页数据失败")
                break

            if page == 1:
                total_count = int(result.get('count', 0))
                total_pages = (total_count + 19) // 20
                print(f"共找到 {total_count} 个商场，约 {total_pages} 页")

            pois = result.get('pois', [])
            for poi in pois:
                mall_info = {
                    '名称': poi.get('name', ''),
                    '地址': poi.get('address', ''),
                    '电话': poi.get('tel', ''),
                    '类型': poi.get('type', ''),
                    '评分': poi.get('biz_ext', {}).get('rating', ''),
                    '营业时间': poi.get('business_area', ''),
                    '经度': poi.get('location', '').split(',')[0] if poi.get('location') else '',
                    '纬度': poi.get('location', '').split(',')[1] if poi.get('location') else '',
                    '所属区域': poi.get('adname', ''),
                    '商场面积': poi.get('indoor_data', {}).get('floor_area', ''),
                    '停车场': poi.get('parking_type', ''),
                    '采集时间': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                all_malls.append(mall_info)

            print(f"已完成第 {page}/{total_pages} 页")
            page += 1
            time.sleep(1)  # 添加延迟，避免请求过快

        return all_malls

    def save_data(self, malls, city):
        """
        保存商场信息到CSV和JSON文件
        """
        if not malls:
            print("没有数据需要保存")
            return

        # 创建输出目录
        output_dir = "mall_data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 保存为CSV
        csv_filename = os.path.join(output_dir, f"{city}_商场信息_{timestamp}.csv")
        df = pd.DataFrame(malls)
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')

        # 保存为JSON
        json_filename = os.path.join(output_dir, f"{city}_商场信息_{timestamp}.json")
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(malls, f, ensure_ascii=False, indent=2)

        print(f"\n数据已保存到:")
        print(f"CSV文件: {csv_filename}")
        print(f"JSON文件: {json_filename}")

        # 输出统计信息
        print(f"\n统计信息:")
        print(f"共采集到 {len(malls)} 个商场")
        print(f"按区域分布:")
        print(df['所属区域'].value_counts())


def main():
    print("城市商场信息采集程序")
    print("-" * 50)

    # 获取用户输入
    city = input("请输入要查询的城市名称(如: 北京): ").strip()

    if not city:
        print("城市名称不能为空！")
        return

    scraper = MallScraper()

    try:
        # 获取商场信息
        malls = scraper.get_all_malls(city)

        if malls:
            # 保存数据
            scraper.save_data(malls, city)
        else:
            print(f"\n未能获取到{city}的商场信息")

    except Exception as e:
        print(f"\n程序运行出错: {str(e)}")

    print("\n程序已结束")


if __name__ == "__main__":
    main()
