# coding=utf8

import requests
from lxml import etree

class get_duanzi(object):

    def __init__(self, url='https://www.qiushibaike.com/text/page/'):
        self.url = url

    def get_code(self,page):
        content = requests.get(self.url+str(page)).text
        html = etree.HTML(content)
        div_jokes = html.xpath('//div[@id="content-left"]/div')
        return div_jokes

    def get_jokes(self,div_jokes):
        jokes = ''
        for div in div_jokes:
            username = '用户：' + div.xpath('.//h2/text()')[0].encode('utf-8').strip('\n') + '\n'
            try:
                gender_class = div.xpath('./div/div/@class')[0].split()[1]
                if gender_class == 'manIcon':
                    gender = '性别：男  '
                else:
                    gender = '性别：女  '
            except:
                gender = ' '
                age = ' \n'
            else:
                age = '年龄：' + div.xpath('./div/div/text()')[0] + '\n'
            content = '帖子：\n' + '\n'.join(div.xpath('.//div[@class="content"]/span/text()')).encode('utf-8').strip('\n') + '\n'
            up = '好笑：' + div.xpath('.//i[@class="number"]/text()')[0] + '\n'
            comments = '评论：' + div.xpath('.//i[@class="number"]/text()')[1]
            jokes += username+gender+age+content+up+comments+'\n\n============\n\n'
        return jokes

    def save_jokes(self,jokes):
        with open('jokes.txt','a') as f:
            f.write(jokes)

if __name__ == '__main__':
    duanzi = get_duanzi()
    startpage = input('startpage:')
    endpage = input('endpage:')
    for i in range(startpage,endpage+1):
        code = duanzi.get_code(i)
        jokes = duanzi.get_jokes(code)
        duanzi.save_jokes(jokes)
