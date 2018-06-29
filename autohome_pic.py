# coding:utf8

import re
from selenium import webdriver
import time
import requests
from lxml import etree
import os

# 获取目标站点html代码
def get_the_code():
    url = 'https://www.autohome.com.cn/car/'
    browser = webdriver.Chrome()
    browser.get(url)
    # 等待页面载入
    time.sleep(5)
    # 页面为lazyloading，使用浏览器模拟翻页，间隔2秒
    for i in range(0,1):
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
    # 获取html代码
    result = browser.page_source
    browser.quit()
    return result

# 获取各字母对应的html代码
def get_the_letter(letter,content,regex):
    if letter == 'Z':
        result = re.findall(r"%s[\S\s]*?tab-content-item1" % regex, content)[0]
    else:
        try:
            result = re.findall(r"%s[\S\s]*?vos=\"gs\"" % regex, content)[0]
        except:
            return
    return result

# 获取汽车品牌名称和logo地址
def get_the_brand(result):
    html = etree.HTML(result)
    # 品牌数量
    no_of_brand = len(html.xpath('//dl'))
    # 品牌logo列表
    brand_pic = ['http:'+ i for i in html.xpath('//dt/a/img/@src')]
    # 品牌名称列表
    brand_name = html.xpath('//dt/div/a/text()')
    # 返回品牌数量、品牌名称、品牌logo地址
    return (no_of_brand,brand_name,brand_pic)

# 下载品牌logo
def save_the_brand(path,brand_name,brand_pic):
    # 请求品牌logo链接
    r = requests.get(brand_pic)
    # 设置保存的文件夹
    brand_path = path + '/' + brand_name
    # 无对应文件时创建
    if not os.path.exists(brand_path):
        os.mkdir(brand_path)
    # 设置保存的文件路径和文件名称
    this_path = brand_path + '/' + brand_name + 'logo'
    with open(this_path, 'wb') as f:
        f.write(r.content)
    # 返回品牌所在路径
    return brand_path

# 获取车系列表信息
def get_the_series(series,path):
    series_car = {}
    # 匹配车系列表
    series_car_list = re.findall(r"<ul[\S\s]*?/ul>",series)
    # 格式化html对象
    html = etree.HTML(series)
    # 获取车系名称
    series_name = html.xpath('//div[@class="h3-tit"]/a/text()')
    # 遍历各车系
    for i in range(0,len(series_name)):
        # 组装为车型列表字典（车系名称：车系网页代码）
        series_car[series_name[i]] = series_car_list[i]
        # 创建车系文件夹路径
        series_path = path + '/' + series_name[i]
        if not os.path.exists(series_path):
            os.mkdir(series_path)
    # 返回车系字典数据
    return series_car

# 下载汽车图片
def get_the_car(path,series_car):
    for i in series_car:
        # 将车系的网页代码解析为html标签
        html = etree.HTML(series_car[i])
        # 获取车系下的车型名称列表
        car_name = html.xpath('//li/h4/a/text()')
        # 获取车系下的车型链接地址列表
        car_link = html.xpath('//li/h4/a/@href')
        # 遍历车型
        for j in range(0,len(car_name)):
            # 初始化车型链接地址
            link = 'https:' + car_link[j].encode('utf8')
            # 获取车型页面的网页源码
            car_code = requests.get(link).text
            try:
                # 获取车型页面的车型图片链接
                car_pic_link = etree.HTML(car_code).xpath('//picture/source/img/@src')[0]
            except:
                # 获取失败时，采用另一种匹配方式
                car_pic_link = etree.HTML(car_code).xpath('//dl[@class="models_pics"]/dt/a/img/@src')[0]
            # 设置车型图片保存地址
            car_path = path + '/' + i + '/' + car_name[j]
            car_pic = requests.get(car_pic_link)
            # 保存车型图片
            with open(car_path, 'wb') as f:
                f.write(car_pic.content)
    return

if __name__ == '__main__':
    # 获取网页源码
    content = get_the_code()
    # 初始化程序的保存路径
    if not os.path.exists('/Users/jason/autohome'):
        os.mkdir('/Users/jason/autohome')
    # 遍历品牌首字母（A-Z）
    for i in range(65,66):
        letter = chr(i)
        # 初始化首字母对应品牌的保存路径
        path = '/Users/jason/autohome/%s' % letter
        if not os.path.exists(path):
            os.mkdir(path)
        # 品牌首字母的网页源码正则匹配
        regex = '<div class="uibox-con rank-list rank-list-pic" id="html' + letter
        # 获取首字母对应的所有品牌的网页源码
        result = get_the_letter(letter,content,regex)
        # 获取汽车品牌，返回品牌数量、名称、logo链接
        brand = get_the_brand(result)
        # 车系的网页源码正则匹配
        series = re.findall(r"<dd>[\S\s]*?</dd>",result)
        # 遍历各品牌
        for i in range(0,brand[0]):
            # 保存品牌logo图片，返回品牌所在路径
            brand_path = save_the_brand(path,brand[1][i],brand[2][i])
            # 获取品牌下的车系数据
            series_car = get_the_series(series[i],brand_path)
            # 保存车系下的车型图片
            get_the_car(brand_path,series_car)