import json

import  requests
if __name__ == '__main__':
    # 指定url地址
    url='https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
    # UA伪装
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    # 参数处理
    city=input('enter a city:')
    pageIndex=1
    total_data=[]
    while True:
        params={
            'cname':'',
            'pid':'',
            'keyword':city,
            'pageIndex': pageIndex,
            'pageSize': '10',
        }
        # 获取相应数据
        response=requests.post(url=url,params=params,headers=headers)
        page_text=response.text
        dic_obj=json.loads(page_text)
        shopNum=len(dic_obj['Table1'])
        if shopNum>0:
            total_data.extend(dic_obj['Table1'])
            print('抓取第'+str(pageIndex)+'页成功！')
            pageIndex+=1
        if shopNum<10:
            print('抓取结束！')
            break
    fileName=city+'肯德基地址.json'
    with open(fileName,'w',encoding='utf-8') as fp:
        json.dump(total_data,fp=fp,ensure_ascii=False,indent=1)
    print('over!')