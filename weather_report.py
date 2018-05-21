# coding:utf-8

import requests
import json
import re
import time
# from StringIO import StringIO
# import gzip

def get_the_weather(city):
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + city
    content = requests.get(url)
    # urllib模块无gzip解压，需单独处理，requests则不需要，需考虑有压缩和无压缩两种情况
    # try:
    #     buf = StringIO(content.text)
    #     f = gzip.GzipFile(fileobj=buf)
    #     result = json.loads(f.read())
    # except:
    # 使用json模块进行解析，将字符串解析为字典
    result = json.loads(content.text)
    if result.get('data'):
        print '数据加载中，请稍候'
        time.sleep(1)
        # 获取当前温度和aqi
        temp = result["data"]["wendu"].encode('utf8')
        cold = result["data"]["ganmao"].encode('utf8')
        # 获取当天天气
        weather = result["data"]["forecast"][0]
        for i in weather:
            weather[i] = weather[i].encode('utf8')
        weather["fengli"] = re.findall(r'\[.*\[(.*)\].*\]',weather["fengli"])[0]
        print '%s当前温度：%s摄氏度' %(city,temp)
        print '%s,天气：%s'%(weather["date"],weather["type"])
        print '%s,%s'%(weather["high"],weather["low"])
        print '风向：%s,风力：%s'%(weather["fengxiang"],weather["fengli"])
        print '天气指数：%s' %cold
    # 异常处理
    else:
        print '未能获取到天气数据'
    return

if __name__ == "__main__":
    while True:
        city = raw_input("请输入要查询的城市：")
        get_the_weather(city)
        # 允许多次查询
        times = raw_input('是否继续？（q:退出，其他任意按键继续查询）')
        if times == 'q':
            break