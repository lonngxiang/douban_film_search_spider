# -*- coding:utf-8 -*-
#@Time : 2021/1/5 15:44
#@Author: lonng
#@File : 豆瓣日期评分检测.py


import requests
from tqdm import tqdm
import csv
from lxml import etree
from collections import Counter
import pandas as pd
import re

def douban(url):
    headers2 = {
      
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36"
    }
    html2 = requests.get(url, headers=headers2).text
    return etree.HTML(html2)


if __name__ == '__main__':
    all_datas = []
    datas = pd.read_csv(r'C:\Users\lonng\Desktop\媒资数据处理\ablum_mango_all1.csv')
    datas = datas[(datas['type'] == 1) & (datas['status'] == 1) & (datas['channel'] == "电影")]  # 获取type为1的数据
    for i in tqdm(range(20)):
        keyword = datas.iloc[i, :]['video_name']
        print(keyword)
        contents = douban(f"https://m.douban.com/search/?query={keyword}")
        try:
            score = contents.xpath('//ul[@class="search-results"]//li[1]//ul/li[1]/a//p/span[2]//text()')[0]
        except:
            score = 0
        try:
            url3 = 'https://m.douban.com' + contents.xpath('//ul[@class="search-results"]//li[1]//ul/li[1]/a/@href')[0]
            contents_detail = douban(url3)
            data = re.findall('.*?\（(.*?)\）', contents_detail.xpath('//div[@class="sub-original-title"]//text()')[0])[0]
        except:
            data = datas.iloc[i, :]['publishyear']
        data = int(data)
        print(data, score)
        # print(type(data),type(int(datas.iloc[i, :]['publishyear'])))
        if int(datas.iloc[i, :]['publishyear']) == data:
            pass
        else:
            new_data = datas.iloc[i, :].to_list()
            new_publishyear = data
            issue_publishyear = "日期不一致"

            new_data.append(new_publishyear)
            new_data.append(issue_publishyear)
            all_datas.append(new_data)
        if datas.iloc[i, :]['score'] == 0 or datas.iloc[i, :]['score'] == "" :
            new_data = datas.iloc[i, :].to_list()
            new_score = score
            issue_score = "没有得分"

            new_data.append(new_score)
            new_data.append(issue_score)
            all_datas.append(new_data)
        else:
            pass

    headers = ['vendor', 'ch*************************8888'heat', 'new_publishyear', 'issue_publishyear', 'new_score', 'issue_score']
    # 可以将字典型列表转化为表格模式
    with open(r"ablum_douban_mgtv_film_change1.csv", 'w', encoding='utf-8-sig', newline="") as f:
        f_csv = csv.writer(f, dialect="excel")

        f_csv.writerow(headers)
        for list in all_datas:
            f_csv.writerow(list)
    print("##############")



