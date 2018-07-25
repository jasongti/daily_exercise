# coding:utf-8

import requests

url1 = 'https://www.zhihu.com/api/v4/members/'
url2 = '/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
headers = {'cookie':'_zap=3d606cba-68a1-477b-9885-b7b09edc01d4; d_c0="AECCtPUyVAyPTu0NvqZYYwM9I-wXR9t2dy0=|1504588933"; q_c1=2df33300e5f84d40bea2c48f03c29032|1508467270000|1502963257000; aliyungf_tc=AQAAABUYIz9xAQ0AaqMtJCO4L6peHzxJ; _xsrf=54e89b03-1f8d-4f63-9b0c-13b4b873c0ef; __DAYU_PP=a2vIyyyYnZjQze7NAZEAffffffffd3aa8089b818; l_n_c=1; n_c=1; q_c1=2df33300e5f84d40bea2c48f03c29032|1529918758000|1502963257000; l_cap_id="NGE0ODA1ZTRlYmM4NGQ2ZWE3YTIwMzYzYzc5NDFlOWU=|1532501068|6807509ebb071fd0540df412b0329085e502f3ea"; r_cap_id="NmRmNTdjODE3MGViNGZiYWI1ZmU1YzY4MjU5NGQ1MzE=|1532501068|cc3dfdb370a2d8b38e2ace74c760af3219c198e5"; cap_id="YzQyYTQxODFhM2IwNGVhNjgyYzczMzM3NjIxNTBiNGU=|1532501068|17595bf8c964b2704d047b9cde13666b540287cd"; capsion_ticket="2|1:0|10:1532501112|14:capsion_ticket|44:MWYwZjc5YjQ5YjJmNDc0NTliYWUwMzI4M2I0MTQ2NmQ=|80f3cf6fb0aa8da1bc4a731f6fe85e125a74a95a940634b4d8835875bafb9303"; z_c0="2|1:0|10:1532501166|4:z_c0|92:Mi4xaDdsQUN3QUFBQUFBUUlLMDlUSlVEQ1lBQUFCZ0FsVk5ybXBGWEFEdG5xdmxUT1pHUHZIRG5aVGF0aGpSR1BiWm5B|2865317cf392b1cde5504f4213774f5932b71619284e5a7f1f3460e4f9130f09"; __utma=155987696.1460996648.1532507464.1532507464.1532507464.1; __utmc=155987696; __utmz=155987696.1532507464.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); tgw_l7_route=ec452307db92a7f0fdb158e41da8e5d8; anc_cap_id=3cf8733c7e694eb7baca1f998bfd06b5',
           'referer':'https: // www.zhihu.com / people / crossin / following?page = 6',
           'user-agent':'Mozilla/5.0(Linux; Android 6.0;Nexus 5 Build / MRA58N) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 67.0.3396.99MobileSafari / 537.36'}


def get_kol(user):
    print 'crawling:', user
    url = url1 + user + url2
    global to_crawl, crawled
    while True:
        req = requests.get(url, headers=headers)
        data = req.json()
        for i in data['data']:
            if i['follower_count'] > 500000:
                if i['url_token'] not in to_crawl and i['url_token'] not in crawled:
                    print i['name']
                    to_crawl.append(i['url_token'])
        if data['paging']['is_end']:
            print '==========\n'
            break
        url = data['paging']['next'].replace('http:', 'https:')

to_crawl = ['crossin']
crawled = []

while len(to_crawl) > 0:
    kol = to_crawl.pop()
    crawled.append(kol)
    get_kol(kol)
print crawled
