# coding:utf8

import requests
import csv


def crawl(csdn_url):
    req = requests.get(csdn_url, headers=headers)
    data = req.json()
    offset.append(data['shown_offset'])
    articles = data['articles']
    info = []
    for i in articles:
        lst = []
        try:
            lst.append(i['title'].encode('utf8'))
            lst.append(i['views'])
            lst.append(i['user_name'].encode('utf8'))
            info.append(lst)
        except Exception as e:
            print e
            continue
    return info


def save(result):
    with open('csvfile.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['标题', '阅读量', '作者'])
        for i in result:
            writer.writerow(i)


csdn_url = 'https://www.csdn.net/api/articles?type=new&category=newarticles&first_view=true'
headers = {
'Cookie':'uuid_tt_dd=-5386611972168856380_20170822; csdn_tt_dd=v10_50b07916fc87f0297cca8540f70d1855effe5e1c1c9d8c4deb108d6bd36194d7; dc_session_id=10_1512383470100.987526; UM_distinctid=1614aeff1087d4-0d5ec028224d03-163c6657-13c680-1614aeff109ca7; TY_SESSION_ID=b8bd03db-5e20-4a6f-9518-3ec5dea1a8e1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1532664202,1532669317,1532676862,1532679567; ADHOC_MEMBERSHIP_CLIENT_ID1.0=becb4c29-b110-8614-036b-c832cc2cfacb; dc_tos=pcin4i; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1532679571',
'Host':'www.csdn.net',
'Referer':'https://www.csdn.net/nav/newarticles',
'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'
}


def main():
    global csdn_url
    result_list = []
    info = crawl(csdn_url)
    result_list.extend(info)
    for i in range(2):
        shown_offset = offset.pop()
        csdn_url = 'https://www.csdn.net/api/articles?type=more&category=newarticles&shown_offset=%s&first_view=false' % shown_offset
        info = crawl(csdn_url)
        result_list.extend(info)
    save(result_list)


if __name__ == '__main__':
    offset = []
    main()
