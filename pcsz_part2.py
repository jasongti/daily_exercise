# coding:utf-8

from bs4 import BeautifulSoup
import requests
from threading import Thread


def get_pic_link():
    retries = 0
    img_list = []
    link_list = []
    while retries < 3:
        try:
            res = requests.get('https://pixabay.com/', timeout=15)
        except:
            retries += 1
            print 'connect the link timeout %d times' % retries
        else:
            html = res.text
            soup = BeautifulSoup(html, 'lxml')
            img_list += soup.find_all('img', attrs={'srcset': True}) + soup.find_all('img', attrs={'data-lazy': True})
            for img in img_list:
                try:
                    link_list.append(img['data-lazy'])
                except:
                    link_list.append(img['src'])
            break
    return link_list


def save_pic(link):
    reties = 0
    pic_name = link.split('/')[-1]
    while reties < 3:
        try:
            pic = requests.get(link, timeout=10)
        except:
            reties += 1
            print 'download the pic:%s failed %d times' % (pic_name, reties)
        else:
            with open('pic/%s' % pic_name, 'wb') as f:
                f.write(pic.content)
            print 'download the pic:%s success' % pic_name
            break
    return


if __name__ == '__main__':
    pic_link = get_pic_link()
    for i in pic_link:
        action = Thread(target=save_pic, args=(i,))
        action.start()
