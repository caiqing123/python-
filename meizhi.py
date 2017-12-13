#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup
import re
import requests

class meizhi:
    def __init__(self):
        self.siteURL = 'http://www.58pic.com/piccate/10-0-0-default-0_2_0_0_id_0-0.html'
        self.save_pic_path = 'D://mmJPG/'
        # 创建文件夹
        self.create_dir_path()

    def getBeautifulSoup(self, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html)
        # print(soup.prettify())
        return soup

    def crawlData(self, page):
        url = self.siteURL
        if page != 1:
            url=url.replace('id_0-0.html','id_0-'+str(page)+'.html')
        # 开始爬取数据
        # print(url+'------------')
        soup = self.getBeautifulSoup(url)
        items = soup.find_all('div', class_='flow-box')[0]
        # print(items)
        for item in items:
            # print(item)
            title = item.find('a',class_='thumb-box').find('img').get('alt')
            imageUrl = item.find('div',class_='card-img').find('img').get('src')
            if imageUrl.find('http://')==-1:
                imageUrl = item.find('div', class_='card-img').find('img').get('data-original')
            self.download_pic(imageUrl, title + '.jpg')

    # 创建文件夹
    def create_dir_path(self):
        exists = os.path.exists(self.save_pic_path)
        if not exists:
            print('创建文件夹')
            os.makedirs(self.save_pic_path)
        else:
            print('文件夹已存在')

    # 保存图片到本地
    def download_pic(self, pic_url, pic_name):
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer': "http://www.mmjpg.com"
        }
        try:
            # 设置绝对路径，文件夹路径 + 图片路径
            path = self.save_pic_path + pic_name
            if os.path.isfile(path):
                print('该图片已存在  ' + pic_name)
                return
            print('文件路径：' + path + ' 图片地址：' + pic_url)
            try:
                img = requests.get(pic_url, headers=headers, timeout=10)
                with open(path, 'ab') as f:
                    f.write(img.content)
                    print(path)
            except Exception as e:
                print(e)

            print("保存图片完成")
        except Exception as e:
            print(e)
            print("保存图片失败: " + pic_url)

    # 获取总页码
    def get_page(self):
        soup = self.getBeautifulSoup(self.siteURL)
        string_page = soup.find_all('div', class_='qt-pagination')[0].find('a', rel='external nofollow').string.strip()
        int_page = int(re.findall('\d+', string_page)[0])
        return int_page


meizhi = meizhi()
max_page = meizhi.get_page() + 1
print(max_page)
for page in range(1, max_page):
    meizhi.crawlData(page)
print('------------->>>>>>>>>>>>>>爬取完成')
